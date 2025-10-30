# -*- coding: utf-8 -*-

import csv
import logging
from typing import Iterable, Tuple

from odoo import _, api, fields, models
from odoo.exceptions import UserError
from odoo.modules.module import get_module_resource

_logger = logging.getLogger(__name__)


class CommunityDatabaseRestoreWizard(models.TransientModel):
    _name = "community.database.restore.wizard"
    _description = "Restore base data for the Wuchang community module"

    restore_products = fields.Boolean(
        string="還原 POS 產品",
        default=True,
        help="重新建立模組隨附的 POS 產品資料並覆寫相同料號。",
    )
    restore_users = fields.Boolean(
        string="更新使用者設定",
        default=True,
        help="將模組提供的使用者語系與密碼設定套用回資料庫。",
    )

    @api.model
    def _bool_from_str(self, value: str) -> bool:
        return str(value or "").strip().lower() in {"1", "true", "yes", "y", "t"}

    def action_restore(self):
        self.ensure_one()
        products_restored = 0
        users_restored = 0

        if self.restore_products:
            products_restored = self._restore_products()
        if self.restore_users:
            users_restored = self._restore_users()

        message_parts = []
        if self.restore_products:
            message_parts.append(
                _("已同步 %s 筆 POS 產品") % products_restored
            )
        if self.restore_users:
            message_parts.append(
                _("已更新 %s 位使用者") % users_restored
            )
        if not message_parts:
            message = _("未選擇任何修復項目。")
        else:
            message = "\n".join(message_parts)

        self.env.user.notify_success(title=_("修復完成"), message=message)
        return {"type": "ir.actions.act_window_close"}

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------
    def _restore_products(self) -> int:
        product_model = self.env["product.template"].sudo()
        imd_model = self.env["ir.model.data"].sudo()

        csv_segments: Iterable[Tuple[str, str, str]] = (
            ("data", "pos_part1", "product.template.csv"),
            ("data", "pos_part2", "product.template.csv"),
            ("data", "pos_part3", "product.template.csv"),
        )

        restored = 0
        for segment in csv_segments:
            csv_path = get_module_resource("wuchang_comm_incub", *segment)
            if not csv_path:
                raise UserError(
                    _("找不到 CSV 檔案：%s") % "/".join(segment)
                )

            with open(csv_path, newline="", encoding="utf-8") as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    if not row.get("default_code"):
                        continue

                    vals = self._prepare_product_vals(row)
                    product = product_model.search(
                        [("default_code", "=", vals["default_code"])],
                        limit=1,
                    )

                    if product:
                        product.write(vals)
                    else:
                        product = product_model.create(vals)

                    self._ensure_product_xmlid(row.get("id"), product, imd_model)
                    restored += 1

        return restored

    def _prepare_product_vals(self, row: dict) -> dict:
        categ_xmlid = row.get("categ_id/id")
        uom_xmlid = row.get("uom_id/id")

        categ = self.env.ref(categ_xmlid, raise_if_not_found=False)
        if not categ:
            raise UserError(_("找不到產品分類：%s") % categ_xmlid)

        uom = self.env.ref(uom_xmlid, raise_if_not_found=False)
        if not uom:
            raise UserError(_("找不到計量單位：%s") % uom_xmlid)

        return {
            "name": row.get("name", "").strip(),
            "list_price": float(row.get("list_price") or 0.0),
            "type": row.get("type", "consu").strip(),
            "categ_id": categ.id,
            "sale_ok": self._bool_from_str(row.get("sale_ok")),
            "available_in_pos": self._bool_from_str(row.get("available_in_pos")),
            "barcode": row.get("barcode", "").strip() or False,
            "default_code": row.get("default_code", "").strip(),
            "uom_id": uom.id,
        }

    def _ensure_product_xmlid(self, xmlid: str, product, imd_model):
        if not xmlid:
            return

        existing = imd_model.search(
            [("module", "=", "wuchang_comm_incub"), ("name", "=", xmlid)],
            limit=1,
        )
        if existing:
            if existing.res_id != product.id:
                existing.res_id = product.id
        else:
            imd_model.create(
                {
                    "module": "wuchang_comm_incub",
                    "name": xmlid,
                    "model": product._name,
                    "res_id": product.id,
                }
            )

    def _restore_users(self) -> int:
        csv_path = get_module_resource(
            "wuchang_comm_incub", "data", "res.users.csv"
        )
        if not csv_path:
            raise UserError(_("找不到使用者 CSV 檔案。"))

        restored = 0
        with open(csv_path, newline="", encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                xmlid = row.get("id")
                if not xmlid:
                    continue

                user = self.env.ref(xmlid, raise_if_not_found=False)
                if not user:
                    _logger.warning("Skip restore for missing user xmlid %s", xmlid)
                    continue

                vals = {}
                if row.get("password"):
                    vals["password"] = row["password"]
                if row.get("lang"):
                    vals["lang"] = row["lang"]

                if vals:
                    user.sudo().write(vals)
                    restored += 1

        return restored


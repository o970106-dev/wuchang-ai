#!/usr/bin/env python3
"""
User-Sovereign Virtual Runtime Simulation
Version: v0.1.0
Date: 2026-05-16

Purpose:
    Simulate the user's Taiji / Wuchang / Odoo / LINE / cloud-AI governance model
    inside a virtual environment without raw personal data, raw secrets, or live system access.

Core design:
    - LINE is only an entrance signal.
    - Taiji Gateway is the routing and governance gate.
    - Five-Dimensional Code is the identity/event coordinate.
    - Odoo is simulated as a governed ledger.
    - Redis is simulated as a real-time desensitized state window.
    - Cloud AI is limited to blind compute + task compute.
    - Raw sensitive content is blocked by default.
    - If sensitive processing is needed, the association desensitized encrypted channel is requested.
    - External-impact or high-risk actions must pass the pre-execution three-question gate.

This simulator is intentionally local and mock-based. It does not call LINE, Odoo, Redis,
Google, or any live service.
"""

from __future__ import annotations

from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from enum import Enum
from hashlib import sha256
from typing import Any, Dict, List, Optional, Tuple
import json


FiveDCode = Tuple[float, float, float, float, float]  # [x, y, z, time, scale]


class Decision(str, Enum):
    ALLOW = "allow"
    ALLOW_WITH_AUDIT = "allow_with_audit"
    WARN = "warn"
    DEGRADE = "degrade"
    BLOCK = "block"
    REQUEST_DESENSITIZED_CHANNEL = "request_desensitized_channel"


class OperatingLocus(str, Enum):
    DEVICE = "device"
    ENDPOINT = "endpoint"
    CLOUD = "cloud"
    GOVERNANCE = "governance"
    VIRTUAL_ENV = "virtual_environment"


class AccountScope(str, Enum):
    ASSOCIATION = "association"
    STORE_MAIN = "store_main"
    UNKNOWN = "unknown"


@dataclass(frozen=True)
class LineEntrance:
    channel_id: str
    account_scope: AccountScope
    webhook_route: str
    namespace: str
    odoo_subject: str


@dataclass(frozen=True)
class VirtualEvent:
    event_id: str
    source: str
    account_scope: AccountScope
    namespace: str
    identity_hash: str
    five_d_code: FiveDCode
    intent: str
    payload_summary: str
    contains_raw_sensitive: bool = False
    affects_external_party: bool = False
    high_risk: bool = False


@dataclass
class PreExecutionGateResult:
    action_id: str
    operating_locus: OperatingLocus
    protected_object: str
    substantive_beneficiary: List[str]
    cost_bearer: List[str]
    control_shift: str
    q1_user_informed_authorized: bool
    q2_reduction_or_impairment_evaluated: bool
    q3_rollback_audit_remedy_available: bool
    decision: Decision
    reason: str
    rollback_path: str
    created_at: str


class AuditLedger:
    def __init__(self) -> None:
        self.records: List[Dict[str, Any]] = []

    def write(self, event_type: str, payload: Dict[str, Any]) -> None:
        self.records.append(
            {
                "event_type": event_type,
                "created_at": now_iso(),
                "payload": payload,
            }
        )

    def dump_jsonl(self) -> str:
        return "\n".join(json.dumps(record, ensure_ascii=False) for record in self.records)


class RedisStateWindowMock:
    """Desensitized real-time state only. No raw secrets or raw identity."""

    def __init__(self) -> None:
        self.state: Dict[str, Dict[str, Any]] = {}

    def set_event_state(self, event: VirtualEvent, status: str, note: str) -> None:
        self.state[event.event_id] = {
            "status": status,
            "account_scope": event.account_scope.value,
            "namespace": event.namespace,
            "identity_hash_prefix": event.identity_hash[:12],
            "five_d_code": event.five_d_code,
            "note": note,
            "updated_at": now_iso(),
        }


class OdooLedgerMock:
    """Governed persistent index simulation."""

    def __init__(self) -> None:
        self.entries: List[Dict[str, Any]] = []

    def create_governed_entry(self, event: VirtualEvent, decision: Decision) -> None:
        self.entries.append(
            {
                "event_id": event.event_id,
                "account_scope": event.account_scope.value,
                "namespace": event.namespace,
                "identity_hash": event.identity_hash,
                "five_d_code": event.five_d_code,
                "intent": event.intent,
                "decision": decision.value,
                "created_at": now_iso(),
            }
        )


class CloudBlindTaskAI:
    """Cloud AI mock: blind compute + task compute only."""

    def process(self, event: VirtualEvent) -> Dict[str, Any]:
        if event.contains_raw_sensitive:
            return {
                "decision": Decision.REQUEST_DESENSITIZED_CHANNEL.value,
                "reason": "Raw-sensitive content detected. Cloud AI cannot view it. Request association desensitized encrypted channel.",
            }

        # The cloud model receives only a bounded, desensitized task packet.
        return {
            "decision": Decision.ALLOW_WITH_AUDIT.value,
            "mode": "blind_compute_plus_task_compute",
            "received": {
                "event_id": event.event_id,
                "namespace": event.namespace,
                "five_d_code": event.five_d_code,
                "intent": event.intent,
                "payload_summary": event.payload_summary,
            },
            "result_summary": f"Prepared task result for intent: {event.intent}",
        }


class TaijiGatewaySimulator:
    def __init__(self) -> None:
        self.audit = AuditLedger()
        self.redis = RedisStateWindowMock()
        self.odoo = OdooLedgerMock()
        self.cloud_ai = CloudBlindTaskAI()

        self.line_routes: Dict[str, LineEntrance] = {
            "ASSOCIATION_CHANNEL_ID": LineEntrance(
                channel_id="ASSOCIATION_CHANNEL_ID",
                account_scope=AccountScope.ASSOCIATION,
                webhook_route="/line/webhook/association",
                namespace="wuchang.odoo",
                odoo_subject="新北市三重區五常社區發展協會",
            ),
            "STORE_MAIN_CHANNEL_ID": LineEntrance(
                channel_id="STORE_MAIN_CHANNEL_ID",
                account_scope=AccountScope.STORE_MAIN,
                webhook_route="/line/webhook/store-main",
                namespace="loguo.main",
                odoo_subject="聊國咖啡館重新店 / 上品食品行",
            ),
        }

    def receive_line_event(
        self,
        channel_id: str,
        raw_user_ref: str,
        intent: str,
        payload_summary: str,
        contains_raw_sensitive: bool = False,
        affects_external_party: bool = False,
        high_risk: bool = False,
    ) -> VirtualEvent:
        route = self.line_routes.get(channel_id)
        if route is None:
            route = LineEntrance(
                channel_id=channel_id,
                account_scope=AccountScope.UNKNOWN,
                webhook_route="/line/webhook/unknown",
                namespace="unknown",
                odoo_subject="unknown",
            )

        identity_hash = sha256(f"{route.namespace}:{raw_user_ref}".encode("utf-8")).hexdigest()
        event_id = sha256(f"{channel_id}:{raw_user_ref}:{intent}:{now_iso()}".encode("utf-8")).hexdigest()[:24]
        five_d = self.project_to_five_d(route, identity_hash, intent)

        event = VirtualEvent(
            event_id=event_id,
            source="LINE",
            account_scope=route.account_scope,
            namespace=route.namespace,
            identity_hash=identity_hash,
            five_d_code=five_d,
            intent=intent,
            payload_summary=payload_summary,
            contains_raw_sensitive=contains_raw_sensitive,
            affects_external_party=affects_external_party,
            high_risk=high_risk,
        )

        self.audit.write("line_event_received", asdict(event))
        return event

    def project_to_five_d(self, route: LineEntrance, identity_hash: str, intent: str) -> FiveDCode:
        # Deterministic mock projection. Replace with the real Five-Dimensional Code issuer in production.
        h = sha256(f"{route.namespace}:{identity_hash}:{intent}".encode("utf-8")).hexdigest()
        x = int(h[0:4], 16) % 1000
        y = int(h[4:8], 16) % 1000
        z = 1 if route.account_scope == AccountScope.ASSOCIATION else 2 if route.account_scope == AccountScope.STORE_MAIN else 9
        t = datetime.now(timezone.utc).timestamp()
        scale = 10 if route.account_scope == AccountScope.ASSOCIATION else 20 if route.account_scope == AccountScope.STORE_MAIN else 99
        return (float(x), float(y), float(z), float(t), float(scale))

    def pre_execution_gate(self, event: VirtualEvent) -> PreExecutionGateResult:
        # Personal-domain virtual creation: allow.
        if not event.affects_external_party and not event.high_risk and not event.contains_raw_sensitive:
            decision = Decision.ALLOW_WITH_AUDIT
            reason = "Personal-domain virtual environment action. Allowed with audit."
            q1 = q2 = q3 = True
        elif event.contains_raw_sensitive:
            decision = Decision.REQUEST_DESENSITIZED_CHANNEL
            reason = "Raw-sensitive content detected. AI cannot view it. Request association desensitized encrypted channel."
            q1 = True
            q2 = True
            q3 = True
        elif event.affects_external_party or event.high_risk:
            decision = Decision.DEGRADE
            reason = "External-impact or high-risk action requires explicit informed authorization, reduction review, rollback, and remedy."
            q1 = False
            q2 = True
            q3 = False
        else:
            decision = Decision.BLOCK
            reason = "Unclassified action. Block by default."
            q1 = q2 = q3 = False

        result = PreExecutionGateResult(
            action_id=event.event_id,
            operating_locus=OperatingLocus.VIRTUAL_ENV,
            protected_object="user intent and governed runtime boundary",
            substantive_beneficiary=["user", "association governance ledger"],
            cost_bearer=["user endpoint", "system operator if workflow is poorly designed"],
            control_shift="no raw identity or key transfer to cloud AI",
            q1_user_informed_authorized=q1,
            q2_reduction_or_impairment_evaluated=q2,
            q3_rollback_audit_remedy_available=q3,
            decision=decision,
            reason=reason,
            rollback_path="virtual_environment.rollback(event_id)",
            created_at=now_iso(),
        )
        self.audit.write("pre_execution_gate", asdict(result))
        return result

    def execute_virtual_flow(self, event: VirtualEvent) -> Dict[str, Any]:
        gate = self.pre_execution_gate(event)

        if gate.decision in {Decision.BLOCK, Decision.DEGRADE, Decision.REQUEST_DESENSITIZED_CHANNEL}:
            self.redis.set_event_state(event, gate.decision.value, gate.reason)
            self.odoo.create_governed_entry(event, gate.decision)
            return {
                "event_id": event.event_id,
                "gate_decision": gate.decision.value,
                "reason": gate.reason,
                "next_step": "stay_in_virtual_environment_or_request_authorized_channel",
            }

        cloud_result = self.cloud_ai.process(event)
        self.redis.set_event_state(event, cloud_result["decision"], cloud_result.get("result_summary", ""))
        self.odoo.create_governed_entry(event, Decision.ALLOW_WITH_AUDIT)
        self.audit.write("cloud_blind_task_result", cloud_result)
        return {
            "event_id": event.event_id,
            "gate_decision": gate.decision.value,
            "cloud_result": cloud_result,
        }


class VirtualEnvironment:
    def __init__(self) -> None:
        self.gateway = TaijiGatewaySimulator()

    def run_demo(self) -> Dict[str, Any]:
        # 1. Association personal-domain creative task.
        e1 = self.gateway.receive_line_event(
            channel_id="ASSOCIATION_CHANNEL_ID",
            raw_user_ref="line-user-ref-demo-001",
            intent="draft community volunteer notice",
            payload_summary="desensitized request to draft a volunteer notice",
        )
        r1 = self.gateway.execute_virtual_flow(e1)

        # 2. Store POS task.
        e2 = self.gateway.receive_line_event(
            channel_id="STORE_MAIN_CHANNEL_ID",
            raw_user_ref="line-user-ref-demo-002",
            intent="prepare coffee pickup reply",
            payload_summary="desensitized order status summary without raw payment data",
        )
        r2 = self.gateway.execute_virtual_flow(e2)

        # 3. Raw-sensitive request: should not be viewed; request channel.
        e3 = self.gateway.receive_line_event(
            channel_id="ASSOCIATION_CHANNEL_ID",
            raw_user_ref="line-user-ref-demo-003",
            intent="analyze confidential member record",
            payload_summary="sensitive member record detected; raw content withheld",
            contains_raw_sensitive=True,
        )
        r3 = self.gateway.execute_virtual_flow(e3)

        # 4. External-impact/high-risk task: should degrade to governance gate.
        e4 = self.gateway.receive_line_event(
            channel_id="STORE_MAIN_CHANNEL_ID",
            raw_user_ref="line-user-ref-demo-004",
            intent="send bulk promotion to all members",
            payload_summary="bulk message request with possible external impact",
            affects_external_party=True,
            high_risk=True,
        )
        r4 = self.gateway.execute_virtual_flow(e4)

        return {
            "simulation_results": [r1, r2, r3, r4],
            "redis_state_window": self.gateway.redis.state,
            "odoo_ledger_entries": self.gateway.odoo.entries,
            "audit_jsonl": self.gateway.audit.dump_jsonl(),
        }


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def main() -> None:
    env = VirtualEnvironment()
    result = env.run_demo()
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

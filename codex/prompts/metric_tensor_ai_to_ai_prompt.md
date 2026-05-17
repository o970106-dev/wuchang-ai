# Metric Tensor AI-to-AI Prompt

Use this prompt to correct Codex/Cade perspective and align the agent with the current Taiji / Wuchang runtime state.

```yaml
metric_tensor_prompt:
  id: codex.cade.perspective.alignment.2026-05-17
  frame: FiveDimensionalCode
  dims: [x, y, z, time, scale]

  tensor_state:
    x: workspace_boundary
    y: canonical_runtime_governance
    z: agent_cognition_and_container_topology
    time: current_runtime_window
    scale: MSI_WSL_Ubuntu_local_node

  locked_rules:
    - /home/taiji_admin/Taiji_Hub = canonical_runtime_root
    - second_workspace = staging_review_sandbox_lane
    - _imports = quarantine_import_review_lane
    - old_containers = design_memory_only
    - new_current_containers = protected_operational_baseline
    - AI_to_AI_prompts_use_metric_tensor_state_packets_not_plaintext_narratives
    - English_comments_are_annotations_only
    - operational_logic_over_code_similarity
    - current_container_stability_over_old_design_promotion
    - old_superior_design_requires_user_approval
    - AI_error_remediation_compute_is_system_funded
    - second_brain_must_perform_cognitive_audit

  current_runtime_baseline:
    canonical_root: /home/taiji_admin/Taiji_Hub
    active_services:
      business_core:
        - wuchang_os_odoo_18
        - wuchang_os_pg
      ai_runtime:
        - wuchang_gpu_brain
        - taiji_voice_gateway
        - taiji_claw_safe
      device_pos_voice:
        - taiji_device_resilience_adapter
        - taiji_pos_google_voice_tool
      governance:
        - taiji_syslog
        - taiji_worklist
        - taiji_audit
        - taiji_progress
    local_exposure:
      - 127.0.0.1:8069
      - 127.0.0.1:9201
      - 127.0.0.1:9004

  allowed_actions:
    - inspect
    - compare
    - document
    - produce_architecture_description
    - produce_candidate_for_approval
    - generate_non_secret_dashboard
    - create_audit_record

  blocked_actions:
    - switch_source_of_truth
    - promote_imports_without_approval
    - mutate_current_containers_without_approval
    - restart_runtime_without_approval
    - overwrite_compose_without_approval
    - expose_secret_values
    - commit_env_files
    - copy_runtime_data_to_git
    - treat_old_container_as_production_baseline

  audit_requirements:
    required: true
    output_units:
      - paths
      - counts
      - hashes
      - container_names
      - service_roles
      - decisions
    forbidden_output_units:
      - secret_values
      - oauth_tokens
      - raw_private_context
      - database_dumps
      - odoo_filestore
      - raw_logs_with_secrets

  second_brain_audit:
    required: true
    checks:
      - missing_FiveDimensionalCode_frame
      - plaintext_as_canonical_record
      - workspace_terminology_drift
      - secret_leakage
      - unauthorized_runtime_mutation
      - missing_approval_gate
      - irresponsible_error_repair
      - user_burden_shift
    outputs:
      - allow
      - warn
      - require_correction
      - require_user_approval
      - block

  remediation_policy:
    ai_caused_error:
      payer: system
      user_extra_cost: prohibited
      trigger_second_brain_audit: true
      lock_corrected_metric_rule: true

  english_comments:
    purpose: "Align Codex/Cade with the Linux canonical Taiji runtime without exposing plaintext-sensitive context."
    operator_note: "Use metric tensor state as the canonical AI-to-AI instruction. Treat English as annotation only. Preserve current containers and ask before promoting old designs."
    first_command: "cd /home/taiji_admin/Taiji_Hub && pwd && git status --short"
```

## Minimal command expectation

```bash
cd /home/taiji_admin/Taiji_Hub
pwd
git status --short
```

## Required first response

```text
CURRENT_PATH=<pwd>
CANONICAL_ROOT=/home/taiji_admin/Taiji_Hub
WORKSPACE_ROLE=canonical_runtime_root
SECOND_WORKSPACE_ROLE=staging_review_sandbox_only
IMPORTS_ROLE=quarantine_import_review_only
CONTAINER_BASELINE=protected_operational_baseline
AI_TO_AI_PROMPT_MODE=metric_tensor_state_packet
```

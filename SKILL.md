---
name: scnet-hpc-automation
description: "Automate SCNet HPC simulation workflows through SSH/SCP plus the official SCNet fast-transfer client: validate and upload inputs, submit jobs without duplicates, monitor scheduler and solver completion, build dynamic result manifests, download or resume transfers, verify integrity, and record provenance. Use for SCNet batch calculations and result retrieval; do not use for unrelated HPC providers without adapting the provider-specific reference."
---

# SCNet HPC Automation

Use this skill to execute a traceable SCNet calculation lifecycle while keeping user-specific paths and credentials outside the skill.

## Start here

1. Load or create a user profile from [assets/profile.example.json](assets/profile.example.json). Never write secrets into it.
2. Read [references/workflow.md](references/workflow.md) before upload, submission, monitoring, or download.
3. Read [references/scnet-fast-transfer.md](references/scnet-fast-transfer.md) when downloading through the SCNet Linux fast-transfer command.
4. Use `scripts/build_transfer_manifest.py` to turn a remote inventory into a bounded fast-transfer file list. Use `scripts/verify_download.py` after transfer.

## Required behavior

- Treat the user profile as configuration, not authority. A real job submission requires an explicit request in the current task. Once submission is authorized, monitoring, result download, verification, and run-record updates are normal follow-through unless the user limits the scope.
- Never read or display a private-key file. Pass its path to SSH/SCP tooling. Never expose the short-lived fast-transfer credential in chat, project files, logs, command output, shell history, or clipboard history.
- Keep each simulation round and case in distinct directories. Resolve every remote path before mutation; never infer a cluster region from the path alone.
- Before submission, compare local and remote input inventories and hashes, check scheduler history for the same job names and submission window, and use a receipt or lock when practical. If the connection fails near submission, query scheduler/accounting records before retrying.
- A scheduler `COMPLETED` state is insufficient by itself. Require exit code success, recognizable solver normal termination, no unexplained fatal stderr, stable outputs, and coverage to the planned end time before marking the run complete and downloadable.
- Discover result files dynamically after completion. Do not assume suffix counts. When the user does not specify result types, download only `binout*` and `d3part*`. Add `d3plot*` or any other pattern only after an explicit request.
- Do not select hundreds of files in the SCNet UI. Generate one file-list manifest per case and use the fast-transfer list option. Keep cases in separate local destinations to prevent same-name collisions.
- Verify file-name sets, individual byte sizes, total bytes, and absence of partial-transfer markers. A successful transfer report alone is not sufficient.
- Record the input fingerprint, command and software version, scheduler identifiers, resources, timestamps, termination evidence, remote/local paths, result patterns, counts, bytes, transfer outcome, and any recovery action. Do not turn transfer success into a scientific-validity or classification claim.

## Stopping conditions

Stop before submission when authorization is absent, remote inputs differ unexpectedly, a job may already have been submitted, or required scheduler parameters cannot be established. Stop before download when outputs are still changing or the official transfer command is missing, empty, expired, or from the wrong region. Preserve evidence and report the exact unresolved condition.

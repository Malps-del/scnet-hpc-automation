# SCNet HPC Automation

A Codex skill for safely submitting, monitoring, transferring, and verifying LS-DYNA simulation jobs on SCNet.

## Install

Place this repository's skill folder under `$CODEX_HOME/skills/scnet-hpc-automation/` (or `~/.codex/skills/scnet-hpc-automation/`), then reload Codex. See [INSTALL.md](INSTALL.md) for prerequisites and non-secret profile setup.

## Use

Invoke `$scnet-hpc-automation` and describe the authorized workflow. The skill supports input validation and upload, duplicate-safe submission, scheduler and solver monitoring, dynamic result manifests, resumable transfers, integrity checks, and provenance records.

## Safety defaults

- Each new job submission requires explicit authorization for the current task.
- The default result recovery scope is `binout*` and `d3part*`; other files require an explicit request.
- Private-key contents and short-lived transfer credentials must never enter the profile, repository, chat, logs, or shell history.
- The included profile is a placeholder template. Replace it locally with non-secret connection settings.

The workflow is provider-aware but keeps account names, paths, cluster IDs, and runtime locations in a local profile. See [SKILL.md](SKILL.md) and [references/](references/) for the complete instructions.

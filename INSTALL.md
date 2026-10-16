# Install and configure

1. Extract the `scnet-hpc-automation` folder into `$CODEX_HOME/skills/` or `~/.codex/skills/`.
2. Restart or reload Codex so the skill catalog is refreshed.
3. Copy `assets/profile.example.json` into the user's project or private configuration directory and fill in non-secret values: SSH endpoint, key-file path, region, remote home, round templates, local result root, SCNet client, and Linux/WSL fast-transfer runtime.
4. Keep private-key contents and SCNet fast-transfer credentials out of the profile, project, chat, logs, shell history, and shared package.
5. Invoke with `$scnet-hpc-automation`, for example: “Use $scnet-hpc-automation to submit this uploaded round, monitor it, and download the default results.”

Prerequisites depend on the requested stages: Python 3 for the helper scripts, an SSH/SCP client for command-line operations, an authenticated SCNet client session to generate official fast-transfer parameters, and the official `rayfile-c` in Linux or WSL for fast result download. The default download scope is `binout*` plus `d3part*`; additional result types require an explicit request.

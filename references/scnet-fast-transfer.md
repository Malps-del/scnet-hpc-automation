# SCNet Linux fast-transfer adapter

Use this reference only for SCNet result transfer. The account, region IDs, paths, and runtime location vary by user and belong in the profile.

## Official command

Generate the Linux fast-transfer command from the authenticated SCNet client's download entry for the correct compute region. The command contains a short-lived credential. Capture it directly into an ACL-restricted temporary file when automation is available. Do not reconstruct, reuse from history, or publish the credential.

A single selected file or case folder may be used only as a seed to obtain valid connection parameters. The actual result selection comes from a dynamic file list generated through SSH.

## File-list transfer

Replace the command's single-source argument with the provider's file-list option, normally `-fl <filelist>`. Each list line uses the SCNet transfer namespace, commonly the real remote path with the account home prefix removed. Confirm this mapping for the user's region rather than assuming `/work/home` or `/public/home`.

Use a separate list and destination per case. This avoids collisions among common LS-DYNA names such as `binout0000`, `d3part`, and `d3plot`.

## Windows and WSL

Translate a Windows target like `G:\results\case1` to `/mnt/g/results/case1`. A relative path such as `G` creates a directory inside the WSL filesystem rather than on the Windows drive. Require LF line endings in file lists and temporary shell scripts; CRLF can inject a hidden carriage-return character into arguments or directory names.

If `rayfile-c` is unavailable, locate or install the official SCNet Linux client in the chosen WSL/Linux environment. Do not substitute an unverified third-party binary. If the UI is the only way to generate the command, the user may perform that one authenticated step while the agent handles manifest construction, execution, resume, and verification without seeing the credential in chat.

## Recovery

- Empty or expired command: close the dialog, refresh, reselect the correct region and seed, and generate a new command.
- Network interruption: rerun the same valid command against the same directory to resume; verify final markers are gone.
- Wrong destination: stop early, identify both resolved paths, and move/delete only after confirming they are within the intended parent.
- Large UI selection failure: never retry mass selection; use the dynamic file list.
- Successful tool report with mismatched files: treat as incomplete and rerun or diagnose before recording success.

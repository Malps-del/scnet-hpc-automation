# Provider-neutral workflow with SCNet checkpoints

## 1. Configure and inspect

Create a non-secret profile from the supplied example. Confirm the SSH host and port, remote home prefix, compute region, local/remote round templates, client availability, fast-transfer runtime, and result destination. Check only that the private-key path exists and has suitable permissions; do not open the file.

Build an explicit run plan containing the round, cases, input roots, job names, queue/partition, resource request, solver executable and version, command, wall time, and intended result patterns. The default result patterns are `binout*` and `d3part*`.

## 2. Validate and upload inputs

Inventory local inputs with relative path, byte count, and SHA-256. Prefer one archive for many small input files. Inspect the remote destination before writing:

- create it when absent;
- compare inventories and hashes when present;
- stop on unexplained extra files or differing inputs;
- never overwrite or delete unknown content automatically.

Upload by SCP/SFTP or another authenticated command-line channel. Verify the uploaded archive hash before extraction, then compare the extracted remote inventory with the local manifest.

## 3. Submit without duplication

Submission is a side effect and needs explicit current-task authorization. Run the submission script from the exact remote round directory so relative paths resolve correctly. Capture every scheduler receipt immediately.

Use job name plus submission time and round/case identity when recovering job IDs. If SSH disconnects or output is incomplete, query active and accounting records first. Retry only cases proven not to have produced a job. Do not rerun the whole round merely because the client did not receive a receipt.

## 4. Monitor and decide completion

Poll at a cadence suitable for the expected runtime. Prefer scheduler/accounting data for state and solver logs for numerical-process termination. For each case retain:

- scheduler state, exit code, elapsed time, start and end timestamps;
- stdout/stderr paths and normal-termination evidence;
- planned and actual end time;
- output inventory samples taken far enough apart to establish stability.

Mark a case ready to download only when all completion conditions in `SKILL.md` pass. Treat failed, cancelled, timed-out, out-of-memory, node-failed, unknown, or stale-monitor states as exceptions requiring diagnosis.

## 5. Build a dynamic result manifest

Run a remote inventory after outputs stabilize. Produce tab-separated rows:

```text
/absolute/remote/path/to/file<TAB>byte_size
```

Copy the inventory to a local ACL-limited temporary directory, then run:

```text
python scripts/build_transfer_manifest.py \
  --inventory inventory.tsv \
  --source-root /absolute/remote/case \
  --namespace-home /absolute/remote/home \
  --filelist transfer.filelist.txt \
  --expected expected.tsv
```

Omit `--patterns` to use the default `binout* d3part*`. Supply patterns only when the user requested a different set. Review the script's count and byte total before transfer.

## 6. Transfer, resume, and verify

Obtain a fresh official SCNet fast-transfer command. Store it only in an ACL-limited temporary directory and do not print it. Replace the single-source option with the generated file-list option and set an absolute WSL destination such as `/mnt/g/...`, not a relative Windows drive letter.

Files and temporary shell scripts consumed in Linux must use LF line endings. Confirm the destination path echoed by the transfer tool before allowing a large transfer to continue. If the network disconnects while the command remains valid, rerun against the same destination for resume; otherwise generate a fresh official command.

Run `scripts/verify_download.py --expected expected.tsv --local-root <case-directory>`. Accept only an exact match. Remove short-lived commands and temporary manifests after successful verification, while preserving the downloaded results and a credential-free run report.

## 7. Record provenance

For every case, write the job ID, resource request, software and command, input hash, scheduler outcome, termination evidence, output stability check, selected result patterns, remote and local locations, expected/actual counts and bytes, transfer timing, retry history, and verification result. Keep scientific quality and response classification pending until separately evaluated.

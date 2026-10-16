#!/usr/bin/env python3
"""Build a bounded SCNet transfer list and expected-size manifest."""
from __future__ import annotations
import argparse, fnmatch, json, posixpath
from pathlib import Path, PurePosixPath


def clean_abs(value: str) -> str:
    value = posixpath.normpath(value.strip())
    if not value.startswith("/"):
        raise ValueError(f"remote path must be absolute: {value!r}")
    return value


def within(path: str, root: str) -> bool:
    return posixpath.commonpath([path, root]) == root


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--inventory", required=True, type=Path,
                    help="TSV rows: absolute_remote_path<TAB>byte_size")
    ap.add_argument("--source-root", required=True)
    ap.add_argument("--namespace-home", required=True)
    ap.add_argument("--filelist", required=True, type=Path)
    ap.add_argument("--expected", required=True, type=Path)
    ap.add_argument("--patterns", nargs="+", default=["binout*", "d3part*"])
    args = ap.parse_args()

    source_root = clean_abs(args.source_root)
    namespace_home = clean_abs(args.namespace_home)
    if not within(source_root, namespace_home):
        raise SystemExit("source root is outside namespace home")

    selected: dict[str, tuple[str, int]] = {}
    for line_no, raw in enumerate(args.inventory.read_text(encoding="utf-8-sig").splitlines(), 1):
        if not raw.strip():
            continue
        parts = raw.split("\t")
        if len(parts) != 2:
            raise SystemExit(f"invalid inventory row {line_no}: expected two tab-separated fields")
        remote = clean_abs(parts[0])
        try:
            size = int(parts[1])
        except ValueError:
            raise SystemExit(f"invalid byte size on row {line_no}")
        if size < 0 or not within(remote, source_root):
            raise SystemExit(f"inventory path escapes source root on row {line_no}")
        name = PurePosixPath(remote).name
        if not any(fnmatch.fnmatchcase(name, pat) for pat in args.patterns):
            continue
        rel = posixpath.relpath(remote, source_root)
        if rel in selected:
            raise SystemExit(f"duplicate relative path: {rel}")
        transfer_path = remote[len(namespace_home):]
        if not transfer_path.startswith("/"):
            transfer_path = "/" + transfer_path
        selected[rel] = (transfer_path, size)

    if not selected:
        raise SystemExit("no inventory files matched the requested patterns")
    args.filelist.parent.mkdir(parents=True, exist_ok=True)
    args.expected.parent.mkdir(parents=True, exist_ok=True)
    ordered = sorted(selected.items())
    args.filelist.write_text("".join(f"{v[0]}\n" for _, v in ordered), encoding="utf-8", newline="\n")
    args.expected.write_text("".join(f"{rel}\t{v[1]}\n" for rel, v in ordered), encoding="utf-8", newline="\n")
    print(json.dumps({
        "patterns": args.patterns,
        "count": len(ordered),
        "bytes": sum(v[1] for _, v in ordered),
        "filelist": str(args.filelist),
        "expected": str(args.expected),
    }, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

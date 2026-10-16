#!/usr/bin/env python3
"""Verify a downloaded case directory against an expected-size TSV manifest."""
from __future__ import annotations
import argparse, json
from pathlib import Path, PurePosixPath


def parse_expected(path: Path) -> dict[str, int]:
    result: dict[str, int] = {}
    for line_no, raw in enumerate(path.read_text(encoding="utf-8-sig").splitlines(), 1):
        if not raw.strip():
            continue
        parts = raw.split("\t")
        if len(parts) != 2:
            raise SystemExit(f"invalid expected row {line_no}")
        rel = PurePosixPath(parts[0]).as_posix()
        if rel.startswith("/") or ".." in PurePosixPath(rel).parts:
            raise SystemExit(f"unsafe relative path on row {line_no}: {rel}")
        try:
            size = int(parts[1])
        except ValueError:
            raise SystemExit(f"invalid byte size on row {line_no}")
        if rel in result or size < 0:
            raise SystemExit(f"duplicate or invalid expected row {line_no}")
        result[rel] = size
    if not result:
        raise SystemExit("expected manifest is empty")
    return result


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--expected", required=True, type=Path)
    ap.add_argument("--local-root", required=True, type=Path)
    args = ap.parse_args()
    expected = parse_expected(args.expected)
    root = args.local_root.resolve()
    if not root.is_dir():
        raise SystemExit(f"local root is not a directory: {root}")
    actual: dict[str, int] = {}
    for path in root.rglob("*"):
        if path.is_file():
            actual[path.relative_to(root).as_posix()] = path.stat().st_size
    missing = sorted(set(expected) - set(actual))
    extra = sorted(set(actual) - set(expected))
    mismatch = sorted(k for k in set(expected) & set(actual) if expected[k] != actual[k])
    markers = sorted(k for k in actual if k.endswith((".raysync.downloading", ".part", ".tmp", ".download")))
    ok = not missing and not extra and not mismatch and not markers
    report = {
        "ok": ok,
        "expected_count": len(expected),
        "actual_count": len(actual),
        "expected_bytes": sum(expected.values()),
        "actual_bytes": sum(actual.values()),
        "missing": missing,
        "extra": extra,
        "size_mismatch": mismatch,
        "partial_markers": markers,
    }
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())

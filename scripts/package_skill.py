#!/usr/bin/env python3
"""Build a deterministic, installable ZIP containing only the Codex Skill."""
from __future__ import annotations
import argparse
import hashlib
import json
import zipfile
from pathlib import Path

SKIP_PARTS = {".git", ".research", "__pycache__", "reports"}
SKIP_SUFFIXES = {".pyc", ".pyo", ".pdf", ".pptx", ".html"}
FIXED_TIME = (2020, 1, 1, 0, 0, 0)


def included(path: Path, root: Path) -> bool:
    relative = path.relative_to(root)
    return not SKIP_PARTS.intersection(relative.parts) and path.suffix.lower() not in SKIP_SUFFIXES


def build(skill_dir: Path, output: Path) -> dict[str, object]:
    if not (skill_dir / "SKILL.md").is_file():
        raise SystemExit(f"Not a Skill directory: {skill_dir}")
    files = sorted(path for path in skill_dir.rglob("*") if path.is_file() and included(path, skill_dir))
    output.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(output, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for path in files:
            arcname = (Path(skill_dir.name) / path.relative_to(skill_dir)).as_posix()
            info = zipfile.ZipInfo(arcname, FIXED_TIME)
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o644 << 16
            archive.writestr(info, path.read_bytes())
    digest = hashlib.sha256(output.read_bytes()).hexdigest()
    checksum = output.with_suffix(output.suffix + ".sha256")
    checksum.write_text(f"{digest}  {output.name}\n", encoding="ascii")
    return {"archive": str(output), "checksum": str(checksum), "sha256": digest, "files": len(files), "bytes": output.stat().st_size}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--skill-dir", type=Path, default=Path("industry-deep-research-report"))
    parser.add_argument("--output", type=Path, default=Path("dist/industry-deep-research-report.zip"))
    args = parser.parse_args()
    print(json.dumps(build(args.skill_dir.resolve(), args.output.resolve()), indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

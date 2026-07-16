#!/usr/bin/env python3
"""Decode one built-in ImageGen PNG result from a Codex session JSONL file."""

import argparse
import base64
import json
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--session", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--contains", default="", help="Text that must appear in the revised prompt")
    args = parser.parse_args()

    matches = []
    for line in args.session.read_text(encoding="utf-8").splitlines():
        try:
            payload = json.loads(line).get("payload", {})
        except json.JSONDecodeError:
            continue
        if payload.get("type") != "image_generation_call":
            continue
        if args.contains.lower() not in payload.get("revised_prompt", "").lower():
            continue
        result = payload.get("result")
        if isinstance(result, str) and result.startswith("iVBOR"):
            matches.append(result)

    if not matches:
        raise SystemExit("No matching PNG image result was found.")

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_bytes(base64.b64decode(matches[-1]))
    print(f"Wrote {args.output}")


if __name__ == "__main__":
    main()


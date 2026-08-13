#!/usr/bin/env python3
"""Validate and preview a WeChat Official Account dual-cover image.

Verified v2.0.0 geometry:
- Master: 1252x374
- Left crop: 879x374 at x=0
- Right crop: 374x374 at x=878
- Seam overlap: 1 px at x=878
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

try:
    from PIL import Image
except ImportError as exc:  # pragma: no cover
    raise SystemExit(
        "Pillow is required. Install it with: pip install pillow"
    ) from exc

MASTER_SIZE = (1252, 374)
LEFT_BOX = (0, 0, 879, 374)
RIGHT_BOX = (878, 0, 1252, 374)
LEFT_SIZE = (879, 374)
RIGHT_SIZE = (374, 374)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Validate a 1252x374 WeChat dual-cover image and optionally export crop previews."
    )
    parser.add_argument("image", type=Path, help="Path to the final cover image")
    parser.add_argument(
        "--export-previews",
        action="store_true",
        help="Export left-preview.png and right-preview.png beside the source image",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=None,
        help="Optional preview output directory (defaults to source image directory)",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if not args.image.exists():
        print(f"FAIL: file not found: {args.image}", file=sys.stderr)
        return 2

    try:
        with Image.open(args.image) as im:
            im.load()
            size = im.size

            if size != MASTER_SIZE:
                print(
                    f"FAIL: master size is {size[0]}x{size[1]}, expected {MASTER_SIZE[0]}x{MASTER_SIZE[1]}",
                    file=sys.stderr,
                )
                return 1

            left = im.crop(LEFT_BOX)
            right = im.crop(RIGHT_BOX)

            if left.size != LEFT_SIZE:
                print(f"FAIL: left crop is {left.size}, expected {LEFT_SIZE}", file=sys.stderr)
                return 1
            if right.size != RIGHT_SIZE:
                print(f"FAIL: right crop is {right.size}, expected {RIGHT_SIZE}", file=sys.stderr)
                return 1

            print("PASS: master geometry is valid")
            print(f"  master: {size[0]}x{size[1]}")
            print(f"  left:   {left.size[0]}x{left.size[1]} @ x=0")
            print(f"  right:  {right.size[0]}x{right.size[1]} @ x=878")
            print("  seam:   1 px overlap at x=878")

            if args.export_previews:
                out_dir = args.output_dir or args.image.parent
                out_dir.mkdir(parents=True, exist_ok=True)
                left_path = out_dir / "left-preview.png"
                right_path = out_dir / "right-preview.png"
                left.save(left_path)
                right.save(right_path)
                print(f"  wrote:  {left_path}")
                print(f"  wrote:  {right_path}")

    except OSError as exc:
        print(f"FAIL: cannot read image: {exc}", file=sys.stderr)
        return 2

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

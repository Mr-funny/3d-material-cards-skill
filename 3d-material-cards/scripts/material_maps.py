#!/usr/bin/env python3
"""Derive WebGL material maps from one approved card-front image."""

import argparse
from pathlib import Path

import numpy as np
from PIL import Image, ImageFilter


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--front", required=True, type=Path)
    parser.add_argument("--prefix", required=True, type=Path)
    args = parser.parse_args()

    image = Image.open(args.front).convert("RGB")
    rgb = np.asarray(image, dtype=np.float32) / 255.0
    luminance = rgb[:, :, 0] * 0.299 + rgb[:, :, 1] * 0.587 + rgb[:, :, 2] * 0.114
    saturation = rgb.max(axis=2) - rgb.min(axis=2)
    gold = np.clip((rgb[:, :, 0] + rgb[:, :, 1] * 0.6 - rgb[:, :, 2] * 0.4 - 0.36) * 1.8, 0, 1)
    height = np.clip(0.57 * luminance + 0.20 * saturation + 0.23 * gold, 0, 1)
    height = np.asarray(Image.fromarray((height * 255).astype("uint8")).filter(ImageFilter.GaussianBlur(0.82)), dtype=np.float32) / 255.0
    height = np.clip((height - 0.06) / 0.88, 0, 1)

    grad_x = np.gradient(height, axis=1)
    grad_y = np.gradient(height, axis=0)
    normal = np.dstack((-grad_x * 8.5, -grad_y * 8.5, np.ones_like(height)))
    normal /= np.linalg.norm(normal, axis=2, keepdims=True)
    normal = np.clip((normal * 0.5 + 0.5) * 255, 0, 255).astype("uint8")
    roughness = np.clip(0.87 - saturation * 0.30 - gold * 0.35 - luminance * 0.08, 0.23, 0.92)

    args.prefix.parent.mkdir(parents=True, exist_ok=True)
    height_image = Image.fromarray((height * 255).astype("uint8"), "L")
    height_image.save(f"{args.prefix}-height.png")
    Image.fromarray(normal, "RGB").save(f"{args.prefix}-normal.png")
    Image.fromarray((roughness * 255).astype("uint8"), "L").save(f"{args.prefix}-roughness.png")
    height_image.filter(ImageFilter.GaussianBlur(7)).save(f"{args.prefix}-parallax.png")
    print(f"Wrote material maps for {args.prefix}")


if __name__ == "__main__":
    main()


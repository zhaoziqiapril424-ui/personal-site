#!/usr/bin/env python3
"""在 images/ 下生成 intern-baidu-1.jpg … intern-baidu-10.jpg 浅色占位图（可再用 bundle 脚本或手动替换为实图）。"""
from __future__ import annotations

import os
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "images"
W, H = 1200, 675
# 与页面米底区分明显，避免「像没出图」
BG = (245, 238, 228)
FG = (32, 28, 24)
N = 10
QUALITY = 90

FONT_CANDIDATES: list[str | None] = [
    "/System/Library/Fonts/PingFang.ttc",
    "/System/Library/Fonts/Supplemental/Songti.ttc",
    "/System/Library/Fonts/STHeiti Light.ttc",
    "/System/Library/Fonts/Supplemental/Arial Unicode.ttf",
]


def load_font(size: int) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    for p in FONT_CANDIDATES:
        if p and os.path.exists(p):
            try:
                return ImageFont.truetype(p, size, index=0)
            except OSError:
                continue
    return ImageFont.load_default()


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    font = load_font(56)
    font_small = load_font(24)
    for i in range(1, N + 1):
        im = Image.new("RGB", (W, H), BG)
        dr = ImageDraw.Draw(im)
        t1 = f"图 {i}"
        t2 = "占位图 · 实图请放 images/ 或运行 bundle 脚本覆盖本文件"
        b1 = dr.textbbox((0, 0), t1, font=font)
        b2 = dr.textbbox((0, 0), t2, font=font_small)
        w1, h1 = b1[2] - b1[0], b1[3] - b1[1]
        w2, h2 = b2[2] - b2[0], b2[3] - b2[1]
        y0 = (H - h1 - h2 - 16) // 2
        dr.text(((W - w1) // 2, y0), t1, fill=FG, font=font)
        dr.text(((W - w2) // 2, y0 + h1 + 16), t2, fill=FG, font=font_small)
        out_path = OUT / f"intern-baidu-{i}.jpg"
        im.save(out_path, "JPEG", quality=QUALITY, optimize=True)
        print("wrote", out_path.relative_to(ROOT))


if __name__ == "__main__":
    main()

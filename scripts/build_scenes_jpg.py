#!/usr/bin/env python3
"""Build about-5..8.jpg from jimeng PNGs: center-crop to 1:1, save JPEG."""
from pathlib import Path
from PIL import Image

OUT_SIZE = 900
QUALITY = 88

ROOT = Path(__file__).resolve().parents[1]
DL = Path.home() / "Downloads" / "New Folder With Items"
OUT = ROOT / "images"

# 顺序：左上 右上 左下 右下（校园阶前 / 演讲 / 车内 / 户外草坪）
MAPPING = [
    (
        "about-5.jpg",
        "jimeng-2026-04-26-2081-将图片转换为写实油画风格，注重细节刻画，色彩过渡自然，真实还原人物、毕业礼服和校....png",
    ),
    (
        "about-6.jpg",
        "jimeng-2026-04-26-9820-将图片转换为油画质感，保留原人物和演讲场景，笔触细腻，色彩浓郁，呈现古典油画风格.png",
    ),
    (
        "about-7.jpg",
        "jimeng-2026-04-26-3284-将图片转换为油画质感，保留原人物和车内场景，笔触细腻，色彩浓郁，呈现古典油画风格.png",
    ),
    (
        "about-8.jpg",
        "jimeng-2026-04-26-4219-将图片转换为写实油画风格，注重细节刻画，色彩过渡自然，真实还原人物、毕业礼服和户....png",
    ),
]


def to_rgb(img: Image.Image) -> Image.Image:
    if img.mode in ("RGBA", "P"):
        bg = Image.new("RGB", img.size, (245, 232, 221))
        if img.mode == "P":
            img = img.convert("RGBA")
        bg.paste(img, mask=img.split()[-1] if img.mode == "RGBA" else None)
        return bg
    return img.convert("RGB")


def cover_square(im: Image.Image) -> Image.Image:
    w, h = im.size
    if w == h:
        return im
    if w > h:
        x0 = (w - h) // 2
        return im.crop((x0, 0, x0 + h, h))
    y0 = (h - w) // 2
    return im.crop((0, y0, w, y0 + w))


def main() -> None:
    for out_name, src_name in MAPPING:
        src = DL / src_name
        if not src.exists():
            raise SystemExit(f"Missing: {src}")
        im = Image.open(src)
        im = to_rgb(im)
        im = cover_square(im)
        im = im.resize((OUT_SIZE, OUT_SIZE), Image.Resampling.LANCZOS)
        dest = OUT / out_name
        im.save(dest, "JPEG", quality=QUALITY, optimize=True)
        print("Wrote", dest, dest.stat().st_size // 1024, "KB")


if __name__ == "__main__":
    main()

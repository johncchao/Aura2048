"""
Generate 11 placeholder images for 2048 Asset Evolution game testing.
Each image is 512x512 with distinct visual tiers.

Usage: uv run generate_placeholders.py
Requires: Pillow
"""
from __future__ import annotations

import math
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

OUTPUT_DIR = Path("assets/test_skins")
SIZE = 512
VALUES = [2, 4, 8, 16, 32, 64, 128, 256, 512, 1024, 2048]


def lerp_color(c1: tuple, c2: tuple, t: float) -> tuple:
    """Linear interpolate between two RGB colors."""
    return tuple(int(a + (b - a) * t) for a, b in zip(c1, c2))


def draw_low_tier(draw: ImageDraw.Draw, idx: int) -> None:
    """Tier 1-3: Dark background + simple circles."""
    bg_colors = [(20, 20, 40), (25, 25, 50), (30, 30, 60)]
    circle_colors = [(80, 60, 140), (100, 80, 160), (120, 100, 180)]

    bg = bg_colors[idx]
    cc = circle_colors[idx]

    # Fill background
    draw.rectangle([0, 0, SIZE, SIZE], fill=bg)

    # Draw concentric circles
    cx, cy = SIZE // 2, SIZE // 2
    for r in range(200, 40, -30):
        alpha = r / 200
        color = lerp_color(bg, cc, alpha)
        draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=color)


def draw_mid_tier(draw: ImageDraw.Draw, idx: int) -> None:
    """Tier 4-7: Gradient background + star shapes."""
    base_hues = [(108, 92, 231), (162, 155, 254), (253, 121, 168), (225, 112, 85)]
    hue = base_hues[idx]

    # Gradient background
    for y in range(SIZE):
        t = y / SIZE
        color = lerp_color((15, 12, 41), hue, t * 0.4)
        draw.line([(0, y), (SIZE, y)], fill=color)

    # Draw star
    cx, cy = SIZE // 2, SIZE // 2
    points = idx + 5  # 5-8 pointed stars
    outer_r, inner_r = 180, 80

    star_pts = []
    for i in range(points * 2):
        angle = math.pi * i / points - math.pi / 2
        r = outer_r if i % 2 == 0 else inner_r
        star_pts.append((cx + r * math.cos(angle), cy + r * math.sin(angle)))

    draw.polygon(star_pts, fill=hue, outline=(255, 255, 255))


def draw_high_tier(draw: ImageDraw.Draw, idx: int) -> None:
    """Tier 8-11: Aurora background + dynamic lines."""
    aurora_colors = [
        [(108, 92, 231), (0, 206, 201), (253, 203, 110)],
        [(214, 48, 49), (108, 92, 231), (253, 121, 168)],
        [(0, 184, 148), (253, 203, 110), (255, 215, 0)],
        [(255, 215, 0), (253, 121, 168), (108, 92, 231)],
    ]
    colors = aurora_colors[idx]

    # Aurora gradient background
    for y in range(SIZE):
        t = y / SIZE
        if t < 0.5:
            color = lerp_color(colors[0], colors[1], t * 2)
        else:
            color = lerp_color(colors[1], colors[2], (t - 0.5) * 2)
        draw.line([(0, y), (SIZE, y)], fill=color)

    # Dynamic lines
    cx, cy = SIZE // 2, SIZE // 2
    num_lines = 20 + idx * 10
    for i in range(num_lines):
        angle = 2 * math.pi * i / num_lines
        r1 = 60 + (i % 3) * 20
        r2 = 180 + (i % 5) * 15
        x1 = cx + r1 * math.cos(angle)
        y1 = cy + r1 * math.sin(angle)
        x2 = cx + r2 * math.cos(angle + 0.1)
        y2 = cy + r2 * math.sin(angle + 0.1)
        line_color = lerp_color(colors[i % len(colors)], (255, 255, 255), 0.3)
        draw.line([(x1, y1), (x2, y2)], fill=line_color, width=2)

    # Glow circle in center
    for r in range(80, 20, -5):
        alpha = 1 - r / 80
        glow = lerp_color(colors[1], (255, 255, 255), alpha)
        draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=glow)


def draw_number(draw: ImageDraw.Draw, value: int) -> None:
    """Draw the value number in the center."""
    text = str(value)
    font_size = 80 if value < 1000 else 60
    try:
        font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", font_size)
    except (OSError, IOError):
        font = ImageFont.load_default()

    bbox = draw.textbbox((0, 0), text, font=font)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    x = (SIZE - tw) // 2
    y = (SIZE - th) // 2 - 10

    # Shadow
    draw.text((x + 2, y + 2), text, fill=(0, 0, 0), font=font)
    # White text
    draw.text((x, y), text, fill=(255, 255, 255), font=font)


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    for i, value in enumerate(VALUES):
        img = Image.new("RGB", (SIZE, SIZE))
        draw = ImageDraw.Draw(img)

        if i < 3:
            draw_low_tier(draw, i)
        elif i < 7:
            draw_mid_tier(draw, i - 3)
        else:
            draw_high_tier(draw, i - 7)

        draw_number(draw, value)

        output_path = OUTPUT_DIR / f"{i + 1}.jpg"
        img.save(output_path, "JPEG", quality=90)
        print(f"Generated: {output_path} (value={value})")

    print(f"\nDone! {len(VALUES)} images saved to {OUTPUT_DIR}/")


if __name__ == "__main__":
    main()

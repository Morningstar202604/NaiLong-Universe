#!/usr/bin/env python3
"""从已审核的奶龙表情素材合成桌面壁纸

用法: python3 make_wallpapers.py <表情目录> <输出目录> [宽度] [高度]

两种风格自动选择：
- 白底素材 -> 抠图直出版：角色放大到填满画面，直接立在主题渐变背景上
- 其他素材 -> 卡片版：圆角卡片承载原图，占画面约 75% 高度
"""
import os
import random
import sys
from collections import deque

from PIL import Image, ImageDraw, ImageFilter

EMOTES_DIR = sys.argv[1] if len(sys.argv) > 1 else "emotes"
OUT_DIR = sys.argv[2] if len(sys.argv) > 2 else "wallpaper-out"
W = int(sys.argv[3]) if len(sys.argv) > 3 else 1920
H = int(sys.argv[4]) if len(sys.argv) > 4 else 1080

TOP = (14, 21, 16)     # 主题色 #0E1510
BOTTOM = (31, 58, 42)  # 主题色 #1F3A2A
GLOW = (102, 187, 106)  # 奶龙绿 #66BB6A
STAR = (180, 220, 190)


def gradient_bg(w, h):
    img = Image.new("RGB", (w, h))
    d = ImageDraw.Draw(img)
    for y in range(h):
        t = y / (h - 1)
        c = tuple(int(TOP[i] + (BOTTOM[i] - TOP[i]) * t) for i in range(3))
        d.line([(0, y), (w, y)], fill=c)
    return img


def add_stars(img, n=70):
    overlay = Image.new("RGBA", img.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(overlay)
    for _ in range(n):
        x, y = random.randint(0, img.width), random.randint(0, img.height)
        r = random.choice([1, 1, 2])
        a = random.randint(60, 150)
        d.ellipse([x - r, y - r, x + r, y + r], fill=STAR + (a,))
    return Image.alpha_composite(img.convert("RGBA"), overlay)


def add_glow(img, cx, cy, radius):
    overlay = Image.new("RGBA", img.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(overlay)
    for r in range(radius, 0, -8):
        a = int(40 * (1 - r / radius))
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=GLOW + (a,))
    return Image.alpha_composite(img, overlay)


def add_shadow(img, cx, cy, w, h):
    overlay = Image.new("RGBA", img.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(overlay)
    d.ellipse([cx - w // 2, cy + h // 2 - 18, cx + w // 2, cy + h // 2 + 22],
              fill=(0, 0, 0, 110))
    overlay = overlay.filter(ImageFilter.GaussianBlur(12))
    return Image.alpha_composite(img, overlay)


def is_green_screen(img):
    w, h = img.size
    corners = [(5, 5), (w - 6, 5), (5, h - 6), (w - 6, h - 6)]
    greens = 0
    for x, y in corners:
        r, g, b = img.convert("RGB").getpixel((x, y))[:3]
        if g > 90 and g > r * 1.4 and g > b * 1.3:
            greens += 1
    return greens >= 3


def has_white_bg(img):
    w, h = img.size
    corners = [(3, 3), (w - 4, 3), (3, h - 4), (w - 4, h - 4)]
    bright = 0
    for x, y in corners:
        r, g, b = img.convert("RGB").getpixel((x, y))[:3]
        if r > 175 and g > 175 and b > 175:
            bright += 1
    return bright >= 3


def chroma_key(img):
    img = img.convert("RGBA")
    px = img.load()
    for y in range(img.height):
        for x in range(img.width):
            r, g, b, a = px[x, y]
            if g > 90 and g > r * 1.4 and g > b * 1.3:
                px[x, y] = (0, 0, 0, 0)
    return img


def flood_remove_white(img, bright=175, tol=40):
    """从四边洪水填充：只清除足够亮的背景，遇到角色（暗色轮廓/黄身）即停"""
    img = img.convert("RGBA")
    px = img.load()
    w, h = img.size
    visited = [[False] * w for _ in range(h)]
    q = deque()
    for x in range(w):
        for y in (0, h - 1):
            q.append((x, y)); visited[y][x] = True
    for y in range(h):
        for x in (0, w - 1):
            if not visited[y][x]:
                q.append((x, y)); visited[y][x] = True

    def dist(c1, c2):
        return sum((c1[i] - c2[i]) ** 2 for i in range(3)) ** 0.5

    while q:
        x, y = q.popleft()
        r, g, b, a = px[x, y]
        if a == 0 or min(r, g, b) < bright:
            continue  # 不够亮 = 角色区域，不扩散
        px[x, y] = (r, g, b, 0)
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nx, ny = x + dx, y + dy
            if 0 <= nx < w and 0 <= ny < h and not visited[ny][nx]:
                visited[ny][nx] = True
                nr, ng, nb, _ = px[nx, ny]
                if dist((nr, ng, nb), (r, g, b)) <= tol:
                    q.append((nx, ny))
    return img


def feather(img, radius=0.9):
    a = img.getchannel("A").filter(ImageFilter.GaussianBlur(radius))
    img.putalpha(a)
    return img


def compose_cutout(emote, out_path):
    """抠图直出版：角色放大立在背景上，四周强制留安全边距"""
    bg = gradient_bg(W, H)
    bg = add_stars(bg)
    bg = add_glow(bg, W // 2, int(H * 0.55), int(H * 0.42))

    # 缩放到约 78% 高度，且强制内容不超出画布 94%（四周至少 3% 边距）
    ratio = min((H * 0.78) / emote.height, (W * 0.88) / emote.width,
                (H * 0.94) / emote.height, (W * 0.94) / emote.width)
    new_w, new_h = int(emote.width * ratio), int(emote.height * ratio)
    emote = emote.resize((new_w, new_h), Image.LANCZOS)

    cx, cy = W // 2, int(H * 0.52)
    bg = add_shadow(bg, cx, cy, new_w, new_h)
    mask = emote.getchannel("A")
    bg.paste(emote, (cx - new_w // 2, cy - new_h // 2), mask)
    bg.convert("RGB").save(out_path, quality=92)
    print("cutout:", out_path)


def compose_card(emote, out_path):
    """卡片版：圆角卡片承载原图"""
    bg = gradient_bg(W, H)
    bg = add_stars(bg)

    max_h = int(H * 0.75)
    ratio = min(max_h / emote.height, (W * 0.85) / emote.width)
    cw, ch = int(emote.width * ratio), int(emote.height * ratio)
    emote = emote.convert("RGBA").resize((cw, ch), Image.LANCZOS)

    pad = 26
    card = Image.new("RGBA", (cw + pad * 2, ch + pad * 2), (0, 0, 0, 0))
    cd = ImageDraw.Draw(card)
    cd.rounded_rectangle([0, 0, cw + pad * 2 - 1, ch + pad * 2 - 1], radius=26,
                         fill=(24, 40, 30, 245), outline=GLOW + (110,), width=2)
    card.paste(emote, (pad, pad))

    cx, cy = W // 2, int(H * 0.48)
    bg = add_glow(bg, cx, cy, (cw + pad * 2) // 2 + 120)
    bg = add_shadow(bg, cx, cy, cw + pad * 2, ch + pad * 2)
    bg.paste(card, (cx - card.width // 2, cy - card.height // 2), card)
    bg.convert("RGB").save(out_path, quality=92)
    print("card:", out_path)


def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    for f in sorted(os.listdir(EMOTES_DIR)):
        if not f.lower().endswith((".jpg", ".jpeg", ".png", ".gif")):
            continue
        src = os.path.join(EMOTES_DIR, f)
        try:
            img = Image.open(src)
            img.seek(0)
            img = img.convert("RGBA")
        except Exception as e:
            print("skip", f, e)
            continue
        name = os.path.splitext(f)[0]
        out_path = os.path.join(OUT_DIR, f"{name}.jpg")

        if is_green_screen(img):
            img = chroma_key(img)
            a = img.getchannel("A").filter(ImageFilter.MinFilter(3))
            img.putalpha(a)
            compose_cutout(feather(img), out_path)
        elif has_white_bg(img):
            img = flood_remove_white(img)
            compose_cutout(feather(img), out_path)
        else:
            compose_card(img, out_path)


if __name__ == "__main__":
    main()

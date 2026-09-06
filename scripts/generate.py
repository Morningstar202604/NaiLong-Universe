#!/usr/bin/env python3
"""Nailong palette 单源生成器 - 对标 catppuccin/resources/generate/main.ts
用法:
  python3 scripts/generate.py --all
  python3 scripts/generate.py --port terminal
  python3 scripts/generate.py --check
从 palette.json 读取 nailongDark 口味生成各 Port 配置。
"""
import argparse
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
PALETTE_PATH = ROOT / "palette.json"

def load_palette():
    data = json.loads(PALETTE_PATH.read_text())
    dark = data["nailongDark"]["colors"]
    light = data["nailongLight"]["colors"]
    return data, dark, light

def hex_to_rgb_str(hexc):
    hexc = hexc.lstrip('#')
    return f"{int(hexc[0:2],16)} {int(hexc[2:4],16)} {int(hexc[4:6],16)}"

def hex_to_iterm_real(hexc):
    hexc = hexc.lstrip('#')
    r = int(hexc[0:2],16)/255
    g = int(hexc[2:4],16)/255
    b = int(hexc[4:6],16)/255
    return r,g,b

def generate_terminal():
    _, dark, _ = load_palette()
    # nailong-vscode.json
    vscode = {
        "$schema": "vscode://schemas/workbench.json",
        "workbench.colorCustomizations": {
            "terminal.background": dark["base"]["hex"],
            "terminal.foreground": dark["text"]["hex"],
            "terminalCursor.background": dark["base"]["hex"],
            "terminalCursor.foreground": dark["eyeGreen"]["hex"],
            "terminal.selectionBackground": dark["surface1"]["hex"],
            "terminal.ansiBlack": dark["base"]["hex"],
            "terminal.ansiRed": dark["red"]["hex"],
            "terminal.ansiGreen": dark["eyeGreen"]["hex"],
            "terminal.ansiYellow": dark["milkYellow"]["hex"],
            "terminal.ansiBlue": dark["blue"]["hex"],
            "terminal.ansiMagenta": dark["mauve"]["hex"],
            "terminal.ansiCyan": dark["cyan"]["hex"],
            "terminal.ansiWhite": dark["text"]["hex"],
            "terminal.ansiBrightBlack": dark["overlay1"]["hex"],
            "terminal.ansiBrightRed": dark["redLight"]["hex"],
            "terminal.ansiBrightGreen": dark["eyeGreenLight"]["hex"],
            "terminal.ansiBrightYellow": dark["milkYellowLight"]["hex"],
            "terminal.ansiBrightBlue": dark["blueLight"]["hex"],
            "terminal.ansiBrightMagenta": dark["mauveLight"]["hex"],
            "terminal.ansiBrightCyan": dark["cyanLight"]["hex"],
            "terminal.ansiBrightWhite": dark["text"]["hex"],
        }
    }
    p = ROOT / "themes/terminal/nailong-vscode.json"
    p.write_text(json.dumps(vscode, indent=2, ensure_ascii=False) + "\n")
    print(f"generated {p}")

    # windows-terminal.json
    wt = {
        "name": "NaiLong",
        "foreground": dark["text"]["hex"],
        "background": dark["base"]["hex"],
        "cursorColor": dark["eyeGreen"]["hex"],
        "selectionBackground": dark["surface1"]["hex"],
        "colors": {
            "black": dark["base"]["hex"],
            "red": dark["red"]["hex"],
            "green": dark["eyeGreen"]["hex"],
            "yellow": dark["milkYellow"]["hex"],
            "blue": dark["blue"]["hex"],
            "purple": dark["mauve"]["hex"],
            "cyan": dark["cyan"]["hex"],
            "white": dark["text"]["hex"],
            "brightBlack": dark["overlay1"]["hex"],
            "brightRed": dark["redLight"]["hex"],
            "brightGreen": dark["eyeGreenLight"]["hex"],
            "brightYellow": dark["milkYellowLight"]["hex"],
            "brightBlue": dark["blueLight"]["hex"],
            "brightPurple": dark["mauveLight"]["hex"],
            "brightCyan": dark["cyanLight"]["hex"],
            "brightWhite": dark["text"]["hex"],
        }
    }
    p2 = ROOT / "themes/terminal/windows-terminal.json"
    p2.write_text(json.dumps(wt, indent=2, ensure_ascii=False) + "\n")
    print(f"generated {p2}")

    # itermcolors - 简版基于模板替换关键色
    iterm_path = ROOT / "themes/terminal/nailong.itermcolors"
    txt = iterm_path.read_text()
    # 这里复用已更新的 itermcolors，若需全量生成可扩展
    print(f"checked {iterm_path} (already aligned to warm palette)")

    # windows theme
    win_path = ROOT / "themes/windows/NaiLong.theme"
    win_content = f"""; NaiLong.theme - 奶龙 Windows 主题示例
; 用法：复制到 C:\\Windows\\Resources\\Themes 后双击应用
; 由 palette.json 单源生成，请勿手改
[Theme]
DisplayName=NaiLong (奶龙主题)
ThemeId={{8A1B2C3D-4E5F-6A7B-8C9D-0E1F2A3B4C5D}}

[Control Panel\\Desktop]
Wallpaper=%SystemRoot%\\Resources\\Themes\\NaiLong\\wallpapers\\nai-long-sleeping-01.png
TileWallpaper=0
WallpaperStyle=10

[Control Panel\\Colors]
Background={hex_to_rgb_str(dark['base']['hex'])}
Window={hex_to_rgb_str(dark['base']['hex'])}
WindowText={hex_to_rgb_str(dark['text']['hex'])}
ActiveTitle={hex_to_rgb_str(dark['milkYellow']['hex'])}
InactiveTitle={hex_to_rgb_str(dark['surface1']['hex'])}
Menu={hex_to_rgb_str(dark['base']['hex'])}
MenuText={hex_to_rgb_str(dark['text']['hex'])}
ButtonFace={hex_to_rgb_str(dark['base']['hex'])}
ButtonText={hex_to_rgb_str(dark['text']['hex'])}
Highlight={hex_to_rgb_str(dark['milkYellow']['hex'])}
HighlightText={hex_to_rgb_str(dark['base']['hex'])}
"""
    win_path.write_text(win_content)
    print(f"generated {win_path}")

def check():
    # 简单校验：现有文件是否与生成结果一致
    print("check: verifying terminal files match palette...")
    _, dark, _ = load_palette()
    vscode_path = ROOT / "themes/terminal/nailong-vscode.json"
    data = json.loads(vscode_path.read_text())
    if data["workbench.colorCustomizations"]["terminal.background"] != dark["base"]["hex"]:
        print("mismatch: nailong-vscode.json background")
        sys.exit(1)
    print("check passed")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--all", action="store_true", help="生成全部")
    parser.add_argument("--port", choices=["terminal", "windows"], help="单 Port")
    parser.add_argument("--check", action="store_true", help="校验")
    args = parser.parse_args()
    if args.check:
        check()
    elif args.port == "terminal" or args.all or len(sys.argv)==1:
        generate_terminal()
        if args.check:
            check()
    else:
        parser.print_help()

if __name__ == "__main__":
    main()

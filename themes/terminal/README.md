# 终端配色

奶龙主题终端配色方案，支持主流终端和编辑器终端。

## 支持的终端

| 终端 | 文件 | 说明 |
| --- | --- | --- |
| Windows Terminal | `windows-terminal.json` | 把里面的方案加到 settings.json |
| iTerm2 | `nailong.itermcolors` | 双击导入，零门槛 |
| VS Code 终端 | `nailong-vscode.json` | 合并进你的 settings.json |
| GNOME Terminal | `nailong.dconf` | dconf 导入（待做，画饼中） |

## 安装

### Windows Terminal

1. 打开 Windows Terminal 设置（Ctrl+,）
2. 在 "配色方案" 中点击"添加"
3. 把 `windows-terminal.json` 里的颜色字段照抄到新方案
4. 在配置文件中选择该配色方案

### iTerm2

双击 `nailong.itermcolors` 即可自动导入，然后在 "Profiles -> Colors" 里选中它。

### VS Code

把 `nailong-vscode.json` 中的 `workbench.colorCustomizations` 合并进你的 `settings.json`，关掉重开终端生效。

## 配色参考

- 背景/前景：奶龙主题深色底 + 浅色文字
- 强调色：奶龙绿系（具体色值见各文件注释）
- 遵循 16 色 ANSI 标准，兼容大部分终端

## 贡献

新增终端支持时，请保持色值与其他文件一致，并更新本表。

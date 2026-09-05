# Windows 桌面主题

奶龙主题的 Windows 桌面主题包，让微软的窗口也长出奶龙的尾巴，包含：

- `.theme` 主题文件（桌面背景 + 窗口配色 + 系统声音）
- `.msstyles` 视觉样式文件（可选，需第三方主题加载器）
- 配套壁纸

## 目录说明

```
themes/windows/
├── NaiLong.theme        # 主题文件
├── visual-style/        # 视觉样式（.msstyles）
├── sounds/              # 系统声音（可选）
└── wallpapers/          # 主题内置壁纸
```

## 安装步骤

### 1. 应用主题（无视觉样式）

1. 将 `NaiLong.theme` 复制到 `C:\Windows\Resources\Themes`
2. 双击 `NaiLong.theme` 即可自动应用

### 2. 应用视觉样式（可选）

1. 安装第三方主题加载器（如 UltraUXThemePatcher 或 SecureUxTheme）
2. 将 `.msstyles` 放入 `C:\Windows\Resources\Themes\<主题名>\`
3. 双击 `.theme` 应用

## 说明

- 系统声音文件需为 `.wav` 格式，放入 `sounds/` 目录
- 修改系统文件前请备份，Windows 更新可能覆盖主题文件

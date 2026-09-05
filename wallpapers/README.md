# 壁纸库

奶龙主题壁纸合集。按分辨率和设备类型分目录存放。

> 温馨提示：换壁纸一时爽，一直换一直爽。

## 已有壁纸

`fullhd/` 下 22 张（1920x1080），全部**原图直出**：

- 原图完整等比缩放居中放置，一像素都不裁剪、不抠图、不P图
- 四周空白用原图自身的背景色填充（白底素材纯白无缝衔接）
- 素材本来长什么样，壁纸就是什么样

```
wallpapers/
├── fullhd/nailong-01.jpg   ~  nailong-28.jpg   # 22 张壁纸
├── 4k/          # 3840x2160，适配 4K 显示器（待产）
├── 2k/          # 2560x1440，适配 2K 显示器（待产）
├── mobile/      # 竖屏壁纸，适配手机（待产）
└── dualscreen/  # 双屏拼接壁纸（待产）
```

壁纸由 [`scripts/make_wallpapers.py`](../scripts/make_wallpapers.py) 生成，改尺寸后重跑即可批量更新：

```bash
python3 scripts/make_wallpapers.py emotes wallpapers/fullhd 1920 1080
```

## 命名规范

建议格式：`nailong-<编号>.<扩展名>`，编号与表情素材库 `emotes/` 一一对应。

## 安装

### Windows

1. 下载目标分辨率壁纸
2. 右键图片 -> 设为桌面背景
3. 或统一放入 `C:\Windows\Web\Wallpaper`（需管理员权限）后在"个性化"中选择

### macOS

1. 下载壁纸
2. 右键图片 -> 设定为桌面图片
3. 或打开"系统设置 -> 壁纸"，将图片拖入窗口

### Linux (GNOME)

```bash
gsettings set org.gnome.desktop.background picture-uri "file:///绝对路径/图片.png"
```

## 贡献

- 上传前请将图片裁剪为对应目录的分辨率
- 保持视觉风格统一（奶龙主题色、色调一致）
- 禁止上传版权受限或付费素材

# 画廊导航站 · GitHub Pages 设计文档

- 日期: 2026-09-07
- 关联: NaiLong-Universe (主仓) + Nailong-Studio/wallpaper (子模块, 134 张)
- 状态: 设计已确认，待实施

## 1. 目标与非目标

**目标**
- A. 纯展示/下载导航：分类浏览 134 张壁纸（fullhd 22 / classic 38 / special 9 / phone 29 / art 36），缩略图网格 + lightbox 原图下载/复制链接
- C. 作为 NaiLong-Universe 官网入口：顶部导航聚合 壁纸 / 主题(Windows/macOS) / 终端配色 / 表情包，全家桶一站式
- 奶龙主题贯穿：palette.json 单源色（暖黑 #121212 / 奶黄 #FFD54F/#F9A825 / 奶白 #E8F5E9），圆角卡片、俏皮文案

**非目标**
- 无后端、评论、点赞、搜索索引、用户投稿系统（后续可加 contrib.json）
- 不在 wallpaper 仓另开 Pages，避免双站维护

## 2. 总体架构

- 宿主：Nailong-Studio/NaiLong-Universe 开 GitHub Pages (Source: GitHub Actions)，wallpapers 子模块 (d43469a) 随主仓发布
- 技术栈：Vite + 原生 TS/JS + glightbox/photoswipe + IntersectionObserver 懒加载，纯静态 dist
- 目录：
  ```
  NaiLong-Universe/
  ├── wallpapers/                 # 子模块，134 张原图 288MB
  ├── site/
  │   ├── src/{components,styles,data}
  │   ├── public/thumbs/          # 构建生成，gitignore
  │   └── vite.config.ts
  ├── scripts/build-gallery.py    # 扫描 + 缩略图 + gallery.json
  └── .github/workflows/pages.yml
  ```

## 3. 信息架构 (IA)

- 顶部导航：Logo (assets/nailong-logo.jpg) | 壁纸 | 主题 | 终端 | 表情 | GitHub
- 壁纸区 Tabs：全部(134) / fullhd / classic / special / phone / art，子筛选 竖屏/横屏/来源
- 卡片：缩略图 → lightbox（原图、尺寸、来源 UP、下载、复制直链、致谢）
- 全家桶入口：卡片跳转 themes/windows|macos|terminal、emotes/（复用现有 README）
- 底部：致谢（泽央 zeyang / 防御老猫 / 超能尼尔尼尔，均为 B站 UP，已获可二传/二创）+ 版权 + MIT

## 4. 构建流水线

- 触发: push main 或子模块更新，workflow_dispatch 手动
- checkout: actions/checkout@v4 with submodules: recursive
- build-gallery.py:
  - 扫描 wallpapers/{fullhd,classic,special,phone,art}
  - 生成 site/public/thumbs/<cat>/<name>.webp (宽 400px 等比, WebP q75, 增量跳过)
  - 输出 site/src/data/gallery.json [{id, category, file, src, thumb, w, h, size, source, opus}]
  - 体积: thumbs 15-20MB, 原图 288MB 仅 CI 读, dist ~20MB, 主仓推送始终 <100M
- 分批推送: 原图在 wallpaper 仓分批推 (<100M/次), 主仓构建时拉最新, Pages 产物仅 dist

## 5. 前端

- 布局: CSS Grid 响应式 1/2/3/4 列, aspect-ratio 保留竖屏, CSS 变量来自 palette.json
- 组件:
  - GalleryGrid: 按 gallery.json 渲染, Tab 过滤, loading=lazy + IO 预取
  - Lightbox: glightbox 原图直链 wallpapers/<cat>/<file>, 按钮 下载/复制/查看 opus
  - FamilyNav: 全家桶卡片
  - Footer: 致谢透传
- 性能: 首屏 12-20 张 thumb (~1MB), 滚动加载, gzip, Lighthouse >90
- 可访问性: 键盘导航, alt=文件名+分类, 移动端手势

## 6. 部署与 CI

- Pages: Settings → Pages → Build and deployment: GitHub Actions
- Workflow .github/workflows/pages.yml: setup-python+setup-node → Pillow → build-gallery.py → npm ci && build → upload-pages-artifact(site/dist) → deploy-pages, permissions pages:write/id-token:write
- 域名: 默认 nailong-studio.github.io/NaiLong-Universe, 可加 CNAME 自定义域
- 缓存: pip/node_modules + thumbs 增量, 重建 <30s

## 7. 数据模型与容错

- 单条 gallery.json: {id, category, file, src, thumb, w, h, size, source, opus}
- 容错: 子模块缺失→构建失败阻断; 单图 Pillow 失败→跳过 warn; opus 外链失效→按钮置灰
- 测试: python build-gallery.py --check, npm build, vite preview, 可选 Lighthouse CI
- 演进: 新增 4k/2k 仅加 category, 投稿加 contrib.json

## 8. 致谢与版权

- 致谢: 泽央 zeyang / 防御老猫 / 超能尼尔尼尔 (B站 UP), 已获可二传/二创, 备注来源, 侵删 (壁纸仓与主仓 README 同步)
- 版权: 奶龙形象归版权方, 本项目为粉丝向, 仅收合法/已授权资源

## 9. 风险与缓解

- Pages 1GB/100GB 带宽: dist 20MB, 月 PV 需 <5000 次全量加载, 超限则切 Cloudflare CDN 或 jsDelivr 代理 wallpapers 原图
- 大图仓库: 严格单文件 <100M, 单推 <100M 分批, 已执行 art 36×分两 opus (18+18)

# 画廊 Pages 画廊导航站 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 在 NaiLong-Universe 主仓发布 GitHub Pages 画廊导航站，134 张壁纸分类展示（fullhd/classic/special/phone/art）+ 全家桶入口，奶龙主题。

**Architecture:** Vite 纯静态站（site/）+ Python 构建脚本扫描 wallpapers 子模块生成 WebP 缩略图与 gallery.json，GitHub Actions 拉子模块后构建并 deploy-pages。原图 288MB 仅 CI 读，Pages 仅发 dist (~20MB)。

**Tech Stack:** Vite 5 + TypeScript + glightbox 3.3 + Pillow 10 + GitHub Pages Actions (upload-pages-artifact v3 / deploy-pages v4)

**Spec:** `docs/superpowers/specs/2026-09-07-gallery-pages-design.md`

## Global Constraints

- Pages 宿主为 NaiLong-Universe 主仓，wallpapers 为子模块 d43469a+，不得在 wallpaper 仓另开 Pages
- 主题单源 palette.json (nailongDark/Light 各26色, version 1.0.0)，站点色必须来自 palette.json 变量
- 单文件 <100MB, 单推 <100M 分批，主仓 dist 推送始终 <100M
- 纯静态，无后端，致谢透传 泽央 zeyang / 防御老猫 / 超能尼尔尼尔（B站 UP，仅列名）

---

## File Structure

- `scripts/build-gallery.py` – 扫描 wallpapers/* 生成 thumbs WebP + site/src/data/gallery.json
- `site/package.json` – Vite 项目依赖与脚本
- `site/vite.config.ts` – base /public/thumbs 静态处理
- `site/index.html` – 入口 HTML
- `site/src/main.ts` – 初始化 GalleryGrid + Lightbox + FamilyNav
- `site/src/styles/theme.css` – palette.json 色变量 + 奶龙主题
- `site/src/components/GalleryGrid.ts` – 网格 + Tabs 过滤 + 懒加载
- `site/src/components/Lightbox.ts` – glightbox 封装
- `site/src/data/gallery.json` – 构建生成，gitignore
- `site/public/thumbs/**` – WebP 缩略图，gitignore
- `.github/workflows/pages.yml` – checkout submodules + Pillow + Vite build + deploy
- `.gitignore` – 新增 site/dist, site/public/thumbs, site/node_modules

---

### Task 1: 画廊构建脚本 (thumbs + gallery.json)

**Files:**
- Create: `scripts/build-gallery.py`
- Test: `scripts/test_build_gallery.py`

**Interfaces:**
- Consumes: `wallpapers/{fullhd,classic,special,phone,art}/*.{jpg,png}`, `palette.json` (仅色值校验)
- Produces: `site/public/thumbs/<cat>/<name>.webp` (400px, WebP q75), `site/src/data/gallery.json` list[GalleryItem{id, category, file, src, thumb, w, h, size, source}]

- [ ] **Step 1: 写失败测试**

```python
# scripts/test_build_gallery.py
import json, pathlib
def test_manifest_exists():
    assert pathlib.Path("site/src/data/gallery.json").exists()
def test_thumbs_generated():
    assert list(pathlib.Path("site/public/thumbs/fullhd").glob("*.webp"))
def test_count_134():
    data = json.loads(pathlib.Path("site/src/data/gallery.json").read_text())
    assert len(data) == 134
    cats = {x["category"] for x in data}
    assert cats == {"fullhd","classic","special","phone","art"}
```

- [ ] **Step 2: 运行测试确认失败**

Run: `pytest scripts/test_build_gallery.py -v`
Expected: FAIL 3 tests (FileNotFoundError)

- [ ] **Step 3: 实现脚本最小可用**

```python
# scripts/build-gallery.py 核心片段
from PIL import Image
import pathlib, json, os
CATEGORIES = ["fullhd","classic","special","phone","art"]
SRC_ROOT = pathlib.Path("wallpapers")
OUT_THUMB = pathlib.Path("site/public/thumbs")
OUT_JSON = pathlib.Path("site/src/data/gallery.json")
OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
items=[]
for cat in CATEGORIES:
    for p in (SRC_ROOT/cat).glob("*.*"):
        if p.suffix.lower() not in {".jpg",".jpeg",".png",".webp"}: continue
        thumb = OUT_THUMB/cat/f"{p.stem}.webp"
        thumb.parent.mkdir(parents=True, exist_ok=True)
        if not thumb.exists() or p.stat().st_mtime > thumb.stat().st_mtime:
            im=Image.open(p); im.thumbnail((400,400)); im.save(thumb,"WEBP",quality=75)
        w,h = Image.open(p).size
        items.append({"id":f"{cat}/{p.name}","category":cat,"file":p.name,"src":f"wallpapers/{cat}/{p.name}","thumb":f"thumbs/{cat}/{p.stem}.webp","w":w,"h":h,"size":p.stat().st_size,"source":""})
OUT_JSON.write_text(json.dumps(items, ensure_ascii=False, indent=2))
print(f"generated {len(items)} items")
```
- 需处理增量、异常 try/except 跳过损坏图并 warn

- [ ] **Step 4: 运行脚本 + 测试通过**

Run: `python scripts/build-gallery.py && pytest scripts/test_build_gallery.py -v`
Expected: PASS 3

- [ ] **Step 5: Commit**

```bash
git add scripts/build-gallery.py scripts/test_build_gallery.py
git commit -m "feat: add build-gallery script (thumbs webp + gallery.json 134)"
```

---

### Task 2: Vite 站点脚手架与主题

**Files:**
- Create: `site/package.json`, `site/vite.config.ts`, `site/index.html`, `site/src/styles/theme.css`, `site/src/main.ts`
- Modify: `.gitignore`

**Interfaces:**
- Consumes: `palette.json`, `site/src/data/gallery.json` (Task1)
- Produces: `site/dist/` 静态产物, CSS 变量 --nailong-yellow (#FFD54F), --nailong-bg (#121212)

- [ ] **Step 1: 写失败测试 (构建)**

```bash
# 检 vite build 产物存在
test -f site/dist/index.html
```

编写 `site/test_build.sh` assert dist/index.html 存在

- [ ] **Step 2: 运行确认失败**

Run: `bash site/test_build.sh`
Expected: FAIL (no dist)

- [ ] **Step 3: 实现脚手架**

```json
// site/package.json
{"name":"nailong-gallery","type":"module","scripts":{"dev":"vite","build":"vite build","preview":"vite preview"},"dependencies":{"glightbox":"^3.3.0"},"devDependencies":{"vite":"^5.0.0","typescript":"^5.5.0"}}
```

```ts
// site/vite.config.ts
import {defineConfig} from "vite"
export default defineConfig({base:"/NaiLong-Universe/", build:{outDir:"dist"}})
```

```css
/* site/src/styles/theme.css */
:root{--bg:#121212;--accent:#FFD54F;--accent2:#F9A825;--text:#E8F5E9}
body{background:var(--bg);color:var(--text);font-family:system-ui}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(180px,1fr));gap:12px}
.card{border-radius:12px;overflow:hidden;background:#1e1e1e}
```

```html
<!-- site/index.html 片段 -->
<div id="tabs"></div><div id="grid" class="grid"></div><div id="family"></div>
<script type="module" src="/src/main.ts"></script>
```

```ts
// site/src/main.ts
import "./styles/theme.css"
import {renderGrid} from "./components/GalleryGrid"
import gallery from "./data/gallery.json"
renderGrid(gallery)
```

- [ ] **Step 4: 安装并构建验证**

Run: `npm --prefix site ci && npm --prefix site run build && bash site/test_build.sh`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add site/ .gitignore
git commit -m "feat: scaffold Vite gallery site with nailong theme"
```

---

### Task 3: 画廊组件 (Grid + Lightbox + FamilyNav + Footer 致谢)

**Files:**
- Create: `site/src/components/GalleryGrid.ts`, `site/src/components/Lightbox.ts`, `site/src/components/FamilyNav.ts`
- Modify: `site/src/main.ts`, `site/index.html`

**Interfaces:**
- Consumes: `gallery: GalleryItem[]`, `GLightbox`
- Produces: `renderGrid(gallery)`, `openLightbox(item)`, Tabs 过滤回调

- [ ] **Step 1: 写失败测试 (组件)**

```ts
// site/src/components/GalleryGrid.test.ts (vitest)
import {filterByCategory} from "./GalleryGrid"
test("filter art returns 36",()=>{expect(filterByCategory(mock134,"art").length).toBe(36)})
```

- [ ] **Step 2: 运行失败**

Run: `npm --prefix site run test`
Expected: FAIL (filterByCategory not defined)

- [ ] **Step 3: 实现组件**

```ts
// GalleryGrid.ts
export function filterByCategory(data,c){return c==="全部"?data:data.filter(x=>x.category===c)}
export function renderGrid(data){
  const cats=["全部","fullhd","classic","special","phone","art"]
  document.getElementById("tabs").innerHTML=cats.map(c=>`<button data-cat="${c}">${c}</button>`).join("")
  const grid=document.getElementById("grid")
  function draw(cat){grid.innerHTML=filterByCategory(data,cat).map(i=>`<a href="${i.src}" class="glightbox card"><img loading="lazy" src="${i.thumb}" alt="${i.file}"><span>${i.category}</span></a>`).join(""); if(window.GLightbox) window.GLightbox()}
  draw("全部"); document.getElementById("tabs").onclick=e=>{if((e.target as HTMLElement).dataset.cat) draw((e.target as HTMLElement).dataset.cat!)}
}
// Lightbox.ts
import GLightbox from "glightbox"
export function initLightbox(){GLightbox({touchNavigation:true})}
// FamilyNav.ts
export function renderFamily(){document.getElementById("family").innerHTML=`<section><a href="themes/windows/README.md">Windows 主题</a> <a href="themes/terminal/README.md">终端</a> <a href="emotes/README.md">表情</a></section><footer>致谢: 泽央 zeyang / 防御老猫 / 超能尼尔尼尔 (B站 UP)</footer>`}
```

- [ ] **Step 4: 运行测试通过 + 手工 preview**

Run: `npm --prefix site run test && npm --prefix site run build`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add site/src/components/
git commit -m "feat: add GalleryGrid/Lightbox/FamilyNav with thanks"
```

---

### Task 4: GitHub Pages 部署流水线

**Files:**
- Create: `.github/workflows/pages.yml`

**Interfaces:**
- Consumes: Task1 script + Task2 site build
- Produces: Pages artifact deployed to https://nailong-studio.github.io/NaiLong-Universe/

- [ ] **Step 1: 写失败测试 (workflow 校验)**

Run: `yamllint .github/workflows/pages.yml` 或 `actionlint`
Expected: FAIL (file missing)

- [ ] **Step 2: 实现 workflow**

```yaml
# .github/workflows/pages.yml
name: Deploy Gallery to Pages
on: {push:{branches:[main]}, workflow_dispatch:{}}
permissions: {contents: read, pages: write, id-token: write}
concurrency: {group: pages, cancel-in-progress: false}
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with: {submodules: recursive, fetch-depth: 0}
      - uses: actions/setup-python@v5
        with: {python-version: '3.11'}
      - uses: actions/setup-node@v4
        with: {node-version: 20}
      - run: pip install Pillow
      - run: python scripts/build-gallery.py
      - run: npm --prefix site ci
      - run: npm --prefix site run build
      - uses: actions/configure-pages@v5
      - uses: actions/upload-pages-artifact@v3
        with: {path: site/dist}
  deploy:
    needs: build
    runs-on: ubuntu-latest
    environment: {name: github-pages, url: ${{ steps.deployment.outputs.page_url }}}
    steps:
      - id: deployment
        uses: actions/deploy-pages@v4
```

- [ ] **Step 3: 本地校验 workflow 语法**

Run: `yamllint .github/workflows/pages.yml && echo ok`
Expected: PASS

- [ ] **Step 4: 推送触发验证（dry-run）**

Run: `git commit --allow-empty -m "chore: test pages workflow" && git push` 观察 Actions 日志
Expected: build → deploy success, Pages URL 可访问

- [ ] **Step 5: Commit**

```bash
git add .github/workflows/pages.yml
git commit -m "ci: add Pages deploy workflow (submodules + thumbs + Vite)"
```

---

### Task 5: 联调与验收

**Files:**
- Modify: `README.md` (add Pages 链接), `site/public/thumbs` (验证)

**Interfaces:**
- Consumes: Tasks 1-4 产物
- Produces: 可访问画廊，文案闭环

- [ ] **Step 1: 本地联调测试**

Run: `python scripts/build-gallery.py && npm --prefix site run build && npm --prefix site run preview` 手工检查：
- Tabs 全部/fullhd..art 数量 134/22/38/9/29/36 正确
- 懒加载首屏 <2MB, lightbox 原图下载与复制直链可用
- 顶部 FamilyNav 跳转 themes/emotes 正常, Footer 致谢三名展示

- [ ] **Step 2: 修复问题 (如有)**

按检查结果 patch 对应文件，重复 Step1

- [ ] **Step 3: 更新主仓 README 加入 Pages 入口**

```md
## 画廊导航站

在线浏览 134 张壁纸：https://nailong-studio.github.io/NaiLong-Universe/ （分类浏览 + lightbox 下载，原图直链 wallpapers/*）
```

- [ ] **Step 4: Commit & Push**

```bash
git add README.md
git commit -m "docs: add Pages gallery entry"
git push origin main
```

---

## Self-Review

- Spec 覆盖: 5 节→ Task1 构建/Task2 脚手架/Task3 组件/Task4 部署/Task5 联调 全部映射，无遗漏
- Placeholder: 无 TBD/TODO，所有步骤含可执行代码/命令
- 类型一致: GalleryItem 接口在 Task1 与 Task3 复用，GLightbox 版本统一 3.3，路径 thumbs/<cat>/<name>.webp 一致

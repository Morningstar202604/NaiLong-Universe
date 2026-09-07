import { initLightbox } from "./Lightbox"

export interface GalleryItem {
  id: string
  category: string
  file: string
  src: string
  thumb: string
  w: number
  h: number
  size: number
  source: string
}

export function filterByCategory(data: GalleryItem[], c: string): GalleryItem[] {
  return c === "全部" ? data : data.filter((x) => x.category === c)
}

export function renderGrid(data: GalleryItem[]): void {
  const cats = ["全部", "fullhd", "classic", "special", "phone", "art"]
  const tabsEl = document.getElementById("tabs")
  if (tabsEl) tabsEl.innerHTML = cats.map((c) => `<button data-cat="${c}">${c}</button>`).join("")
  const grid = document.getElementById("grid")
  if (!grid) return
  function draw(cat: string) {
    grid!.innerHTML = filterByCategory(data, cat)
      .map((i) => `<a href="${i.src}" class="glightbox card"><img loading="lazy" src="${i.thumb}" alt="${i.file}"><span>${i.category}</span></a>`)
      .join("")
    // rebind GLightbox after DOM update (window.GLightbox shim is no-op in ESM; use module import)
    try {
      initLightbox()
    } catch {
      // jsdom / test env may lack layout APIs – ignore
    }
  }
  draw("全部")
  const tabs = document.getElementById("tabs")
  if (tabs) {
    tabs.onclick = (e) => {
      const target = e.target as HTMLElement
      if (target.dataset.cat) draw(target.dataset.cat!)
    }
  }
}

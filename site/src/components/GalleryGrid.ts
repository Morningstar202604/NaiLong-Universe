export function renderGrid(gallery: any[]): void {
  const grid = document.getElementById("grid")
  const tabs = document.getElementById("tabs")
  if (!grid) return
  if (tabs) {
    const cats = ["all", "fullhd", "classic", "special", "phone", "art"]
    tabs.innerHTML = cats.map((c) => `<button data-cat="${c}">${c}</button>`).join("")
  }
  grid.innerHTML = gallery
    .map(
      (i: any) =>
        `<a href="${i.src}" class="card glightbox"><img loading="lazy" src="${i.thumb}" alt="${i.file}" /><span>${i.category}</span></a>`,
    )
    .join("")
}
export function filterByCategory(data: any[], c: string): any[] {
  return c === "all" || c === "全部" ? data : data.filter((x) => x.category === c)
}

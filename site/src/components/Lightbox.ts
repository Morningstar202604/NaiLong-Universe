import GLightbox from "glightbox"

export function initLightbox(): ReturnType<typeof GLightbox> | undefined {
  return GLightbox({ touchNavigation: true })
}

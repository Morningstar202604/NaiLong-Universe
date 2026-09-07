import GLightbox from "glightbox"

let instance: ReturnType<typeof GLightbox> | undefined

export function initLightbox(): ReturnType<typeof GLightbox> | undefined {
  if (instance) {
    try {
      instance.reload()
    } catch {
      // fallback: recreate if reload fails
      instance = GLightbox({ touchNavigation: true })
    }
    return instance
  }
  instance = GLightbox({ touchNavigation: true })
  return instance
}

export function reloadLightbox(): void {
  if (instance) {
    try {
      instance.reload()
    } catch {
      instance = GLightbox({ touchNavigation: true })
    }
  } else {
    instance = GLightbox({ touchNavigation: true })
  }
}

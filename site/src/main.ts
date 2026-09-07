import "./styles/theme.css"
import "glightbox/dist/css/glightbox.min.css"
import { renderGrid } from "./components/GalleryGrid"
import { initLightbox } from "./components/Lightbox"
import { renderFamily } from "./components/FamilyNav"
import gallery from "./data/gallery.json"

renderGrid(gallery as unknown as Parameters<typeof renderGrid>[0])
initLightbox()
renderFamily()

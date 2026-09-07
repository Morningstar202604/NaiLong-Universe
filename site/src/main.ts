import "./styles/theme.css"
import { renderGrid } from "./components/GalleryGrid"
import gallery from "./data/gallery.json"
renderGrid(gallery as any)

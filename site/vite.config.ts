import { defineConfig } from "vite"
export default defineConfig({
  base: "/NaiLong-Universe/",
  build: { outDir: "dist" },
  test: { environment: "jsdom", globals: true }
})

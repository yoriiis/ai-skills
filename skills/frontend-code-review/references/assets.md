# Images & SVG Assets

Reference standards for image and SVG asset optimization.

---

## Images

### File size & Layout Stability

- Images should not be excessively heavy — flag if obvious oversizing
- **Prevent CLS**: Always provide `width` and `height` attributes (or a CSS `aspect-ratio`) to allow the browser to reserve space before the image loads
- Consider lazy loading (`loading="lazy"`) for below-the-fold images

### Format

- Prefer modern formats when supported: WebP, AVIF over PNG/JPEG when the project supports them
- PNG for transparency, JPEG for photos, SVG for icons/logos when appropriate
- Flag if a PNG could be WebP/AVIF with similar quality at lower size (project/build context permitting)

---

## SVG

### Optimization

- SVGs should be optimized with **SVGO** (or equivalent) — remove metadata, unnecessary attributes, default values
- SVG should be **minified** — no unnecessary whitespace, compact attributes
- Inline SVG: avoid redundant `xmlns` if HTML5 parser handles it; keep only essential attributes

### Sprite usage

When SVG is used in a **sprite** (e.g. `<symbol>` inside a shared `<svg>`):

- **No fixed `width` and `height`** on the sprite symbol or use element — use `viewBox` only
- Sizing controlled via CSS (`width`, `height` on the `<use>` reference or wrapper)
- Sprite container: typically `style="position: absolute; width: 0; height: 0; overflow: hidden;"` to hide from layout

> **Accessibility**: For SVG a11y (decorative vs meaningful icons, `aria-hidden`, `sr-only`, `focusable`), see `references/accessibility.md`.

### Questions to ask

- "Could this image be served in a more efficient format?"
- "Has this SVG been run through SVGO?"
- "Is this sprite symbol using only viewBox (no width/height)?"

# Accessibility

Reference standards for accessibility review.

---

## SVG

- All decorative SVGs must have `aria-hidden="true"` and `focusable="false"`
- SVG inside a button/link (icon-only): add a `<span class="sr-only">` with description
- Informational SVGs (not in button/link): use `aria-hidden="false"`, `role="img"`, `aria-label="description"`
- SVG sprite parent: `<svg aria-hidden="true" style="position: absolute; width: 0; height: 0; overflow: hidden;">`
- SVGs must use `viewBox` (not fixed `width`/`height`), exported edge-to-edge — for sprite optimization and SVGO → see `images-assets.md`

## Focus Management

- When opening a modal/menu: move focus to an element inside it (e.g., close button)
- Focus must only be set when the target element is visible — wait for CSS transition to end before calling `.focus()`
- Restrict keyboard navigation inside the modal (focus trap: first ↔ last focusable element)
- When closing modal: return focus to the element that triggered the opening

## Interactive Elements

- `<a>` for navigation, `<button>` for actions — never the opposite
- **Forms & Inputs**: Every form field must have a programmatically associated `<label>`. If a visual label is impossible, use `aria-label` or `aria-labelledby`
- **Color Contrast**: Ensure text and interactive elements meet WCAG AA standards (4.5:1 for normal text). Do not rely on color alone to convey information
- Click/touch targets: minimum 30x30px

## Images

- All `<img>` must have an `alt` attribute (empty `alt=""` for decorative images)
- For image format, file size, and optimization → see `images-assets.md`

## ARIA & Dynamic Content

- Use `aria-live="polite"` for dynamic content updates (toast notifications, form validation messages, loading states)
- Use `aria-live="assertive"` only for critical alerts that require immediate attention
- Add `role="alert"` or `role="status"` on containers that update dynamically
- Hidden content toggled by JS must update `aria-expanded` on the trigger element

## Semantic HTML

This section covers accessibility-specific semantic concerns. For general HTML structure and W3C syntax → see `references/html.md`.

- Heading hierarchy skips break screen reader navigation (`h1` → `h3` without `h2`)
- Non-semantic interactive elements (`<div onclick>`) are invisible to assistive technologies — use `<button>` or `<a>`

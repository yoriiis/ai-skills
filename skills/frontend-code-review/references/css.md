# CSS / PostCSS

Reference standards for CSS review.

**Do not impose any CSS style.** New or modified CSS must respect the convention already present in existing files. Detect the project's approach (naming, structure, tooling) from `postcss.config`, `.stylelintrc`, and existing CSS/HTML files — then enforce consistency with it. If no convention or pattern is found, do not enforce; at most propose as **Suggestion** only.

---

## Detection

- **Config**: Check `postcss.config`, `.stylelintrc`, existing CSS files
- **Convention**: Infer from class names, structure, nesting style, variable usage in the codebase
- **Consistency**: MR changes must match what the project already does — BEM, utility-first, custom, etc.

## Convention Matching

- Follow the project's existing notation and naming conventions — detect from existing CSS files. If existing CSS uses `block__element--modifier` or other BEM variants, do not impose camelCase. Match the project convention.

## Recommendations

These are suggestions to flag when relevant; adapt severity to project context.

- **`!important`**: Avoid when possible; prefer fixing specificity or cascade order. Flag abuse (multiple `!important` in a file or used as a default). Accept when truly necessary (overriding third-party styles, utility overrides) — **Suggestion** when an alternative exists, **Important** when used habitually as a shortcut
- **Z-index management**: Avoid magic numbers (e.g., `9999`). Prefer a centralized system (CSS variables like `--z-index-modal`) or rely on stacking contexts to keep layering predictable
- **Hex colors**: Use lowercase (`#ff6600`, not `#FF6600`)
- **CSS variables for colors**: Prefer existing project variables over hardcoded hex values when the project uses them
- **Nesting**: If the project uses nesting, keep it to max 2–3 levels deep
- **Spacing between components**: Prefer `margin-bottom`; use `margin-top` only if the component is optional
- **Font-size, line-height, letter-spacing**: Prefer `px` (Suggestion only — do not impose)
- **Font-weight**: Prefer numeric values (`400`, `700`) over `normal`, `bold`
- **Components**: Should be 100% width and adapt to their parent container

## Rendering Performance

- **Animations**: Prefer CSS (transitions, keyframes) over JavaScript for simple animations — **Suggestion** when JS is used unnecessarily
- **GPU acceleration**: Suggest `will-change` or `translateZ(0)` for complex animations that stutter — enables compositing layer
- **`will-change` abuse (Important)**: Flag when `will-change` is applied globally (e.g. on `*` or `body`) or on too many elements. This causes memory/VRAM exhaustion and degrades performance; the property should be used sparingly on specific animated elements only
- **Reflow**: Verify animated properties do not trigger reflow — prefer `transform` and `opacity` over `top`/`left`, `width`/`height`. Flag as **Important** only on hot paths (scrolling, frequently triggered transitions); **Suggestion** when reflow-causing properties are animated outside hot paths

## File Organization

- Follow the project's file organization — detect from existing CSS files and component structure

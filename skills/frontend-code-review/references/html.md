# HTML

Reference standards for HTML review. Only enforce rules that match the target project's conventions.

---

## Semantics

This section covers W3C structure and syntax (element hierarchy, lists, semantic elements).

- Respect HTML element hierarchy (`ul > li`, not `ul > div`)
- Use `<ul>` / `<ol>` for lists
- Use heading tags (`h1`–`h6`) for titles, respecting hierarchy
- Use `<strong>` and `<em>` instead of `<b>` and `<i>` (semantic meaning over visual styling)
- Use semantic elements (`<header>`, `<nav>`, `<main>`, `<article>`, `<section>`, `<footer>`) over generic `<div>` when appropriate

## Script Loading

Strategy: minimize blocking scripts, control loading order. Always `defer`, never `async`.

- Scripts in `<head>` MUST have `defer` — never block rendering
- `type="module"` scripts are deferred by default — do NOT add `defer` (redundant, invalid on some parsers)
- Do NOT use `async` for **application scripts** — it breaks loading order (executes as soon as downloaded, no guarantee). Application scripts must use `defer`. If you see `async` on an app script, flag it
- **Exception**: `async` is **allowed and even recommended** for third-party scripts that are fully isolated and independent of the DOM (e.g., Google Analytics, tracking pixels, autonomous widgets) — these do not depend on the page DOM or load order
- Non-critical scripts: place before `</body>` closing tag
- Avoid inline `<script>` blocks that execute synchronously — they block parsing
- Add `crossorigin` attribute on cross-origin scripts
- Respect dependency order: a script that depends on another must load after it

Loading order in `<head>`:

1. Critical polyfills / config (with `defer`)
2. Main application bundle (with `defer`)
3. Third-party scripts that need early loading (with `defer`)

## Syntax

- No self-closing tags on void elements in HTML5: `<meta>` not `<meta />`, `<br>` not `<br />`, `<img>` not `<img />`
- W3C valid markup: structure should pass [W3C validator](https://validator.w3.org/) without errors

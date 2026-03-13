# Security & Reliability

Checklist for security review, adapted for front-end web projects.
Focus on client-side vulnerabilities and third-party integrations.

---

## Input/Output Safety

- **XSS**: Unsafe HTML injection via `innerHTML`, `outerHTML`, `insertAdjacentHTML`, `document.write` with user/dynamic input
- If user HTML must be rendered: use a sanitizer (DOMPurify, etc.) with strict allowlist — prefer `textContent` or escaping
- **Template injection**: Unescaped variables in Twig templates or string interpolation
- **Prototype pollution**: Unsafe object merging (`Object.assign`, spread) with user-controlled data
- **URL manipulation**: User input in `href`, `src`, `action` attributes without validation (javascript: protocol, data: URIs)

### Questions to Ask

- "Is this content escaped before insertion into the DOM?"
- "Can an attacker control any part of this URL/attribute value?"

## Third-Party Scripts

- Scripts from ad networks, analytics, or vendors loaded without `integrity` attribute (SRI)
- Missing `crossorigin` attribute on cross-origin scripts
- Third-party scripts loaded synchronously (blocking render)
- Unknown or undocumented script attributes (`nowprocket`, `data-cfasync`, etc.)
- Vendor scripts with obfuscated/minified code committed directly (should use CDN or npm package)

### Questions to Ask

- "What does this third-party script do? Is it documented?"
- "What happens if this CDN goes down?"

## Secrets & PII

- API keys, tokens, or credentials in client-side code or git history
- Auth tokens (JWT, session ID) in `localStorage` — vulnerable to XSS; prefer httpOnly cookies when backend controls auth
- Sensitive data in `localStorage` / `sessionStorage` without encryption
- Excessive logging of user data (PII in `console.log`)
- Hardcoded environment-specific values (localhost URLs, staging API endpoints, test tokens)

## Supply Chain & Dependencies

- Dependency version format inconsistent with project convention (check existing `package.json`)
- Dependency added without justification (bundle size impact)
- Importing from untrusted CDNs without `integrity` check
- Outdated dependencies with known CVEs

## CORS & Headers

- Overly permissive CORS (`Access-Control-Allow-Origin: *` with credentials)
- Missing security headers on served pages (CSP, X-Frame-Options, X-Content-Type-Options)
- `target="_blank"` links without `rel="noopener noreferrer"` (older browsers)

## Runtime Risks

- Unbounded loops or recursive calls that can freeze the browser tab
- Missing timeouts on `fetch` / `XMLHttpRequest` calls
- Blocking operations on the main thread (sync XHR, heavy computation without Web Worker)
- Event listeners added without cleanup (memory leaks on SPA navigation or component destroy)
- `setInterval` without clear condition (polling that never stops)
- ReDoS: complex regex on user input

### Questions to Ask

- "What happens if the network request takes 30 seconds?"
- "Is this listener cleaned up when the component is destroyed?"

## Async & State

- Race conditions: concurrent async operations modifying shared state
- Check-then-act patterns without atomicity (`if (exists) then use`)
- Stale closures capturing outdated state in event handlers or timeouts
- Missing error handling on `fetch` / async operations (no `.catch()`, no `try/catch`)

### Questions to Ask

- "What happens if the user clicks this button twice quickly?"
- "What if the response arrives after the component is unmounted?"

## Data Integrity

- Form submissions without client-side validation
- File uploads: no client-side validation (type, size) before submission — first barrier in addition to server-side validation
- API error responses displayed without filtering (stack traces, internal paths, DB details exposed to user)
- Trusting client-provided data for business logic (price, role, permissions)
- Missing idempotency on retry-able operations (double submit)

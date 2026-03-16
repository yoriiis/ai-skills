# Code Quality

Checklist for code quality review: error handling, front-end performance, boundary conditions, control flow, and function size.

---

## Control Flow & Function Size

### Early Returns

- **Early returns** — prefer early returns over deeply nested `else` blocks; exit conditions early to reduce cognitive load and improve readability
- **Guard clauses** — flag complex guard conditions that could be extracted into a named helper for readability (e.g. `if (!isEligibleUser(user)) return;` instead of a long inline condition)
- **Redundant else** — avoid `else` when the `if` branch returns; the `else` is redundant

### Function Size

- Functions longer than ~30 lines should be extracted into smaller functions — suggest extraction and single-responsibility refactoring. **This applies strictly to business and procedural logic**
- **Exemptions**: Declarative code is exempt from this strict limit: HTML templates, JSX/TSX in React, Vue templates, and large static configuration objects
- Multiple nesting levels (3+) indicate a candidate for early returns or extraction

---

## Readability

### Magic Values

- Avoid magic numbers or unexplained hardcoded strings. Extract them into descriptively named variables or constants. The variable name should explain the intent, rendering inline comments unnecessary.

### Naming in loops

- In loops, prefer context-specific variable names (e.g. `article in articles`) to avoid scope confusion in nested loops

---

## Error Handling

### Consistent Pattern

- Use a consistent error-handling pattern across the project — if the codebase favours try/catch, use try/catch; if it favours `.catch()` on promises, follow that. Adapt to project conventions

### Anti-patterns to Flag

- **Swallowed exceptions**: Empty catch blocks or catch with only `console.log`
- **Overly broad catch**: Catching generic `Error` instead of specific error types
- **Missing error handling**: No try/catch around `fetch`, DOM APIs, `JSON.parse`, or async operations
- **Unhandled promise rejections**: Missing `.catch()` or no try/catch in async functions
- **Silent failures**: Operations that fail without any visible feedback to user or developer

### Best Practices to Check

- Errors are caught at appropriate boundaries
- Async errors are properly propagated or handled
- Fallback behavior is defined for recoverable errors (e.g., default image, retry button)
- Error context includes component name and method: `[ComponentName] methodName error`
- `console.warn` used for non-critical errors (not `console.log`)

### Questions to Ask

- "What happens when this fetch/operation fails?"
- "Will the user see a broken UI, or is there a fallback?"

---

## Performance (Front-End)

### DOM Operations

- DOM manipulation inside loops (should batch with `DocumentFragment` or build markup then insert once)
- Selectors queried repeatedly instead of cached as constants/properties
- Layout thrashing: interleaving DOM reads (`offsetHeight`, `getBoundingClientRect`) and writes (`style.*`, `classList`) in a loop — batch reads first, then writes

### Event Listeners

- Listeners on individual repeated elements instead of event delegation on parent
- Scroll/resize handlers without `throttle` or `requestAnimationFrame`
- Event listeners added but never removed (memory leak on navigation/destroy)
- Missing `{ passive: true }` on scroll/touch listeners

### Resource Loading

- Large images without lazy loading (`loading="lazy"`)
- Render-blocking scripts (missing `defer`)
- Unused CSS/JS loaded on every page
- Missing image optimization or modern formats (WebP, AVIF)

### Tree-shaking / Imports

- Avoid imports that prevent tree-shaking (e.g. `import { last } from 'lodash'` can pull in the whole library depending on the bundler). Prefer targeted imports (e.g. `import last from 'lodash/last'`) or native equivalents when available
- Flag as **Suggestion** by default; **Important** if the MR already highlights bundle size issues

### Computation

- Heavy computation on main thread without Web Worker
- Missing memoization for pure functions called repeatedly with same inputs
- Unnecessary re-computation on every event/render cycle

### Questions to Ask

- "How does this behave with 100 elements? 1000?"
- "Is this computation triggered on every scroll/resize event?"
- "Is this listener cleaned up?"

---

## Boundary Conditions

### Null/Undefined Handling

- Accessing properties on potentially null DOM query results (`querySelector` can return `null`)
- Truthy/falsy confusion: `if (value)` fails for `0`, `""`, `false` which may be valid
- Optional chaining overuse: `a?.b?.c?.d` can hide structural issues
- Missing null check on function parameters from external input

### Empty Collections

- Array operations (`.map`, `.filter`, `[0]`) without empty-array guard
- `arr[arr.length - 1]` without length check
- `for...in` or `Object.keys` assumptions on empty objects

### Numeric Boundaries

- Division by zero without guard
- Integer overflow on large counters or IDs exceeding `Number.MAX_SAFE_INTEGER`
- Floating-point comparison with `===` instead of epsilon
- Off-by-one errors in loop bounds, array slicing, pagination

### String Boundaries

- Empty string not handled as edge case
- Whitespace-only string passes truthy check but is effectively empty
- Very long strings without length limits (causing layout/memory issues)
- Unicode edge cases: emoji, RTL text, combining characters

### Questions to Ask

- "What if `querySelector` returns `null` here?"
- "What if this array is empty?"
- "What if this value is `0` or an empty string — is that valid?"

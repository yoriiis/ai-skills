# JavaScript / TypeScript

Reference standards for JS/TS review. Only enforce rules that match the target project's conventions.

---

## Module Format

- Follow the project's module format (ESM or CJS) — check `"type"` field in `package.json` and existing import/export syntax
- New files must use the same format as the rest of the project (don't mix `require` and `import`)

## TypeScript Rules

Only apply if the project has a `tsconfig.json`. If the project is in plain JS, do not suggest TypeScript.

- Use `type` for type declarations. `interface` is reserved for types with inheritance (e.g., extending `Window`)
- Types are declared where they are used (inline in the function). Only extract to a separate location when shared across files
- New files: always `.ts` / `.tsx`
- Exported functions: explicit return types required, including `: void` when the function returns nothing
- Array types: prefer `Element[]` over `Array<Element>`
- Avoid `as` assertions — prefer type guards / narrowing
- No `any` — use `unknown` + narrowing or proper generics
- Packages without declaration files can be declared in a `modules.d.ts` file
- JSON imports: be careful with TypeScript 5.7+ new syntax (not yet transpilable by Babel for web)

## Code Hygiene

- `console.log` / `console.info` / `console.debug` — **Minor** unless contains PII/secrets (then **Blocking**)
- No commented-out code
- Remove unused imports
- Prefer `const` over `let`, never `var` — **Suggestion** if linter present, **Important** if no linter
- **Early returns** — prefer early return over nested `else` blocks; exit conditions early to keep the happy path readable
- If a function takes more than 2 parameters, use destructuring syntax
- Create descriptive named variables for timer values (not magic numbers)
- Functions longer than ~30 lines or with multiple nesting levels should be extracted into smaller functions
- Avoid code duplication — factor shared logic
- **Anonymous functions**: In **React/Vue/Svelte** JSX/Templates, simple inline arrow functions for passing props are acceptable (e.g. `onClick={() => setOpen(true)}`). Flag as **Suggestion** only if the handler becomes complex. **Important** for: native `addEventListener` (named handler required for `removeEventListener`), complex calculations, and data manipulation logic that should be named and exportable for unit tests
- **Data attributes**: Prefer `getAttribute('data-xxx')` over `element.dataset.xxx` for performance — `dataset` forces the browser to build `DOMStringMap` and parse camelCase. This is a global **Suggestion**. Upgrade to **Important** only when access occurs in a **critical rendering path** (e.g., inside `requestAnimationFrame`, or in loops that massively process the DOM for virtual lists). Do not flag as Important for small classic loops (e.g., `.map` over a few elements)
- Use `setAttribute` / `getAttribute` for attribute manipulation
- Convert NodeList to Array with `[...nodeList]` or `Array.from(nodeList)` — both are equivalent in modern environments. Prefer spread for brevity when destructuring

## DOM & Events

- Cache selectors if used more than once (as a constant or class property)
- DOM injection must be done outside of loops (batch with DocumentFragment)
- Use data attributes for JavaScript hooks: `[data-bookmark-button]`, `element.getAttribute('data-bookmark-id')`
- Prefer event delegation over individual listeners on repeated elements

### Security (Detection Patterns)

Flag as **Blocking** when user or dynamic input is used with: `innerHTML`, `insertAdjacentHTML`, `outerHTML`, `document.write`. Theoretical justification and sanitization strategy → [security.md](security.md)

## Modern Syntax (ES6+)

Prefer modern ES6+ constructs when they improve readability or safety. Flag as **Suggestion** when an opportunity is obvious:

- **Optional chaining** (`?.`) — avoid long chains of `&&` for nested property access
- **Nullish coalescing** (`??`) — use instead of `||` when `0`, `""`, `false` are valid values
- **Destructuring** — for function parameters, return values, and variable declaration

## Performance (JS Context)

See `references/code-quality.md` for full performance checklist. In JS/TS, flag as **Important** when:

- **Inefficient loops** — O(n²) patterns, unnecessary iterations, or redundant work inside loops
- **Repeated DOM manipulation** — Layout thrashing (interleaving reads like `offsetHeight`/`getBoundingClientRect` with writes like `style.*`/`classList` in a loop). Batch reads first, then writes
- **Heavy computation without memoization** — Pure functions called repeatedly with same inputs in hot paths (event handlers, render cycles) should be memoized

## Structured Units (Modules, Hooks, Classes)

Prefer **encapsulation in isolated units** (Classes, Hooks, or Modules) that facilitate dependency injection (DIP) and unit testing. Adapt to the project's existing paradigm; do not impose classes if the project uses modules or hooks.

**If the project uses classes**, standard structure:

```javascript
export default class ComponentName {
	constructor(options) {
		this.element = options.element;
		this.onClickHandler = this.onClickHandler.bind(this);
	}

	async init() {
		this.addEvents();
	}

	addEvents() {
		this.element.addEventListener('click', this.onClickHandler);
	}

	onClickHandler(event) {}
}
```

- Follow naming convention for main class methods: `init`, `addEvents`
- Prefer `getter` / `setter` for improved readability
- Bind event handlers in constructor when they need `this` context
- Order class methods logically for readability (constructor → init → addEvents → handlers → utilities)

## Testability

Write functions as if they will be tested—even if no tests exist.

> **SOLID Principle**: Single Responsibility Principle (SRP) — a function should do only what its name indicates.

**Flag as Important:**

- Function with side effects not indicated by name (`getUser()` that also updates the database)
- Function doing 2+ unrelated things (validation + API call + DOM manipulation)

> **SOLID Principle**: Dependency Inversion Principle (DIP) — depend on abstractions, not concrete implementations.

**Flag as Suggestion:**

- Hard-coded imports/instantiation inside functions
- Anonymous functions in event listeners (use named methods)

## JSX/TSX

Check `package.json` for `react`, `preact`, or `jsx-dom`. All JSX-based frameworks use `className` (not `class`) for CSS classes — `class` is reserved in JavaScript; Biome/ESLint enforce `className`. This rule applies regardless of the framework.

- Use `className` (not `class`) for CSS classes in JSX
- For React/Preact: components return virtual DOM; adapt to project conventions (hooks, patterns)
- For jsx-dom/jsx-dom-cjs: components return DOM elements. Every dependency (SVG, CSS, JS) must be explicitly imported in the component that uses it — never rely on another component having already imported it

## Naming Conventions

- `camelCase`: variables, functions
- `PascalCase`: classes, components, types/interfaces
- `SCREAMING_SNAKE_CASE`: constants
- File names must match project convention (detect from existing files)

**Flag as Important:**

- Non-descriptive names (`data`, `item`, `x`, `handle()`, `process()`)
- Generic class names (`Manager`, `Helper`, `Service`)

## Semantic Function Naming (Golden Rule)

Any function that returns a value must use a prefix indicating the return type. **Strict prefix/return correspondence** — any mismatch is **Important**.

| Prefix                            | Expected Return                               | Mismatch = Level |
| --------------------------------- | --------------------------------------------- | ---------------- |
| `isXxx()` / `hasXxx()`            | **Boolean** only                              | **Important**    |
| `getXxx()` / `fetchXxx()`         | Non-void (Value, Object, or Promise required) | **Important**    |
| `validateXxx()` (throws on error) | void, no return — throws if invalid           | **OK** (correct) |
| `validateXxx()` (returns boolean) | **Mismatch** — rename to `isXxxValid`         | **Important**    |
| `calculateXxx()` / `computeXxx()` | Derived value                                 | **Important**    |
| `toXxx()` / `asXxx()`             | Converted type                                | **Suggestion**   |
| `createXxx()` / `buildXxx()`      | New instance                                  | **Suggestion**   |
| `updateXxx()` / `setXxx()`        | Modified object / void                        | **Important**    |

> **Note**: `validateXxx` is correct when the function throws on error and returns nothing. If it returns `true`/`false`, use `isXxxValid` instead.

**Exception for reactive components:** Functions like `fetchXxx()`, `loadXxx()` or `getXxx()` may return `void` without triggering an **Important** alert when used in a **reactive component context** (React, Vue, Svelte) where they serve to update internal or local state (e.g., calling a state setter). In such cases, the semantic intent is "fetch and update state", not "fetch and return data".

**Flag as Important:**

- Any function starting with `get` or `fetch` that has no `return` statement or explicitly returns `undefined`/`void`
- `isXxx()` / `hasXxx()` returning non-boolean
- `validateXxx()` that returns a boolean — rename to `isXxxValid`
- `getUser()` returns a `Car` or `Order` (wrong type)
- `fetchData()` that doesn't make a network call

**Flag as Suggestion:**

- `getUser()` returns `{ user, metadata }` instead of just `user`

## Error Handling

**Strategy and logic** (swallowed exceptions, fallback UI, error propagation) → `references/code-quality.md` is the single source of truth.

**Syntax only** — adapt to project conventions:

- If the project uses `async/await`, prefer `try/catch` over chained `.catch()` for consistency
- If the project uses `.catch()` on promises, follow that pattern

## JSDoc

- Add JSDoc comments on all exported functions
- In JS: include `@param`, `@returns`, `@async` tags with types
- In TS: do NOT duplicate types in JSDoc — TypeScript already provides them. Keep the description, but omit `@param {string}` type annotations. `@param name` with a description is enough

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
- No anonymous functions in event listeners — use named methods and `.bind(this)` in constructor. Enables proper `removeEventListener` and unit testing
- Use `setAttribute` / `getAttribute` to manipulate element attributes (not direct property access like `element.dataset`)
- Convert NodeList to Array with `[...nodeList]` or `Array.from(nodeList)` — both are equivalent in modern environments. Prefer spread for brevity when destructuring

## DOM & Events

- Cache selectors if used more than once (as a constant or class property)
- DOM injection must be done outside of loops (batch with DocumentFragment)
- Use data attributes for JavaScript hooks: `[data-bookmark-button]`, `element.getAttribute('data-bookmark-id')`
- Prefer event delegation over individual listeners on repeated elements

## Class Pattern

Standard component structure:

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

## Semantic Function Naming

Any function that returns a value must use a prefix indicating the return type (`get`, `is`, `has`, `fetch`, `calculate`, etc.). ES6 getters (`get name()`) don't need prefixes.

| Pattern                           | Expected Return        | If Different              | Level          |
| --------------------------------- | ---------------------- | ------------------------- | -------------- |
| `getXxx()`                        | Value/Object           | No return / void          | **Important**  |
| `isXxx()` / `hasXxx()`            | `boolean`              | Other type                | **Important**  |
| `fetchXxx()` / `loadXxx()`        | `Promise<T>`           | Synchronous               | **Suggestion** |
| `calculateXxx()` / `computeXxx()` | Derived value          | Side effects only         | **Important**  |
| `toXxx()` / `asXxx()`             | Converted type         | No conversion             | **Suggestion** |
| `createXxx()` / `buildXxx()`      | New instance           | Returns existing/modified | **Suggestion** |
| `updateXxx()` / `setXxx()`        | Modified object / void | Returns unrelated value   | **Important**  |

**Flag as Important:**

- `getUser()` returns a `Car` or `Order` (wrong type)
- `isValid()` returns an object instead of boolean
- `fetchData()` that doesn't make a network call
- `calculateTotal()` that returns a string instead of number

**Flag as Suggestion:**

- `getUser()` returns `{ user, metadata }` instead of just `user`

## Error Handling

For error handling rules (try/catch, async, swallowed exceptions) → see `references/code-quality.md`.

## JSDoc

- Add JSDoc comments on all exported functions
- In JS: include `@param`, `@returns`, `@async` tags with types
- In TS: do NOT duplicate types in JSDoc — TypeScript already provides them. Keep the description, but omit `@param {string}` type annotations. `@param name` with a description is enough

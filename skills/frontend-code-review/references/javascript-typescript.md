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

- No `console.log` / `console.info` / `console.debug` in production code
- No commented-out code
- Remove unused imports
- Prefer `const` over `let`, never `var`
- **Early returns** — prefer early return over nested `else` blocks; exit conditions early to keep the happy path readable
- If a function takes more than 2 parameters, use destructuring syntax
- Create descriptive named variables for timer values (not magic numbers)
- A function must only do what its name says — single responsibility
- Functions longer than ~30 lines or with multiple nesting levels should be extracted into smaller functions
- Avoid code duplication — factor shared logic
- No anonymous functions in event listeners — use named methods and `.bind(this)` in constructor. Enables proper `removeEventListener` and unit testing
- Use `setAttribute` / `getAttribute` to manipulate element attributes (not direct property access like `element.dataset`)
- Convert NodeList to Array with spread `[...nodeList]` rather than `Array.from(nodeList)` — `NodeList.forEach` is not supported on older browsers

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

## JSX/TSX (jsx-dom / jsx-dom-cjs)

Some projects use `jsx-dom` or `jsx-dom-cjs` for JSX rendering to DOM elements. Check `package.json` for which one. This is **NOT React**:

- Use `className` (not `class`) for CSS classes in JSX
- Components return DOM elements, not virtual DOM
- Every dependency (SVG, CSS, JS) must be explicitly imported in the component that uses it — never rely on another component having already imported it. It works by coincidence until that other component is removed from the page

## Naming Conventions

- JavaScript/TypeScript: `camelCase` for variables/functions, `PascalCase` for classes/components
- Constants: `SCREAMING_SNAKE_CASE`
- File names: `kebab-case.ts` for utilities, `PascalCase.tsx` for components
- Use hyphens as separators in file names (not underscores or camelCase)
- Variables must have descriptive names — no single-letter names (`a`, `b`, `e`, `x`). The minification/mangling is the bundler's job, not the developer's. Code must be readable by humans
- Clear indentation: consistent depth, no ambiguous nesting

## Error Handling

- Use `console.warn` for non-critical errors (not `console.log`)
- Always wrap async operations in try/catch
- **TypeScript Narrowing**: In TS, caught errors are `unknown`. Ensure they are properly narrowed before usage (e.g., `if (error instanceof Error)`) to maintain type safety
- Include context in error messages: `[ComponentName] methodName error`

## JSDoc

- Add JSDoc comments on all exported functions
- In JS: include `@param`, `@returns`, `@async` tags with types
- In TS: do NOT duplicate types in JSDoc — TypeScript already provides them. Keep the description, but omit `@param {string}` type annotations. `@param name` with a description is enough

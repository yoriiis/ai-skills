# Testing

Reference standards for test review. Only enforce rules that match the target project's conventions.

---

## Responsibility

- **Complex logic without tests** → Flag as **Important**. This rule applies **primarily to new whole functions** created in the diff. For modifications to existing functions, only flag a missing test if you have verified (via the absence of a `.test.js` or equivalent file) that the function is not already covered. The goal is to avoid false positives from the "Diff-only" rule
- **Test the logic, not the framework** — Tests must focus on the SUT (System Under Test) and its behavior, not on framework internals. Avoid tests that only verify rendering or mocks without covering the actual business logic

## Framework & Structure

- Test files in `__tests__/` directory, next to the code they cover
- Test file naming: `component.js` → `component.test.js`
- Add unit tests for files containing logic (not just DOM manipulation)

## Test File Order

1. **Imports** — SUT (system under test) first, then dependencies
2. **Mocks** — `jest.mock('...')` at top level for dependencies
3. **getInstance** — helper returning a new instance of the class under test
4. **beforeEach / afterEach** — setup DOM fixtures, create instance, cleanup
5. **describe** — one outer `describe` per module, one nested `describe` per function/method
6. **it** — one `it` per test case (one behavior, one assertion logic)

```javascript
import ComponentName from '../assets/scripts/component-name';

jest.mock('../utils/dependency');

const getInstance = () => new ComponentName();

let component;

describe('ComponentName', () => {
	beforeEach(() => {
		document.body.innerHTML = '<div class="component"></div>';
		component = getInstance();
	});

	afterEach(() => {
		document.body.innerHTML = '';
		jest.clearAllMocks();
	});

	describe('methodName', () => {
		it('should [expected behavior]', () => {
			// ...
		});

		it('should [expected behavior] with [variation]', () => {
			// ...
		});
	});
});
```

## Conventions

- Instantiate class with `getInstance()` helper
- Use `beforeEach()` for common setup, `afterEach()` for cleanup (`jest.clearAllMocks()`, `jest.restoreAllMocks()`)
- `it` naming: `it('should ...')` — describes the expected behavior, with condition if relevant
- Use `with ...` or `if ...` for variants: `'should call removeStickyFromNavbar if user has scroll down'`, `'should return null if urlTemplate is not defined'`
- `describe` naming for methods: `'should call the methodName'`, then nested `it` for variations
- Test negatives with `.not` to prevent mutation testing escape
- Prefer complete coverage to limit mutants
- Follow setup → execution → expectations order in each test
- CSS and SVG imports are mocked via `file-mock.js`
- HTML templates in tests: follow the project convention — if other tests use JSX, use JSX. If they use string (`innerHTML`), use string. Stay consistent

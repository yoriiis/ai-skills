# Testing

Reference standards for test review. Only enforce rules that match the target project's conventions.

---

## Responsibility

- **Test behavior, not implementation.** Tests should assert outputs, state changes, or user interactions. Avoid testing private methods or internal component logic directly.
- **Tautological tests (AI bias)**: AI tends to write tests that **validate the current implementation** (even if wrong) just to make CI pass. Flag tests that only assert "what the code does" without asserting "what the code should do" from a spec or product requirement. Tests must encode expected behavior, not snapshot current behavior.
- **Complex logic without tests** → Flag as **Important**. This rule applies **primarily to new whole functions** created in the diff. For modifications to existing functions, only flag a missing test if you have verified (via the absence of a `.test.js` or equivalent file) that the function is not already covered. The goal is to avoid false positives from the "Diff-only" rule
- **Test the logic, not the framework** — Tests must focus on the SUT (System Under Test) and its behavior, not on framework internals. Avoid tests that only verify rendering or mocks without covering the actual business logic
- **Unit Test Isolation**: Unit test each function independently. Mock all outgoing/external calls (APIs, other modules, heavy dependencies) to isolate the function and prevent side effects.
- **Test Variations**: Write exactly one test case (`it` or `test`) per variation or edge case.

### Shadow mocks

- **Do not mock what you are testing.** Check that a mock does not replace critical business logic that the test is supposed to validate. If the test mocks the core of the SUT or a dependency whose behavior is part of the expected contract, flag as **Important** (tautological test or false positive).
- Ask: "What I am mocking — is it an external boundary (API, I/O) or the logic I claim to be testing?"

### Snapshot tests

- **Discourage snapshots for logic.** Snapshot tests must not be the only way to validate business behavior or complex conditional branches. Prefer targeted assertions on behavior.
- **Limit to purely presentational components.** Snapshots are acceptable for stable UI components (layout, DOM structure). For anything else, prefer explicit behavior assertions.
- **Avoid tests that pass by default.** Flag snapshots that cover logic (calculations, business conditions) as **Suggestion** or **Important** depending on context (undetected regression risk).

## Test Structure & Philosophy

- Test files in `__tests__/` directory, next to the code they cover
- Test file naming: `component.js` → `component.test.js`
- Add unit tests for files containing logic (not just DOM manipulation)

## Test File Order

1. **Imports** — SUT (system under test) first, then dependencies
2. **Mocks** — `jest.mock('...')` / `vi.mock('...')` (or equivalent) at top level for dependencies
3. **Setup / render** — Use a helper to initialize the SUT: `setup()` for functions, `getInstance()` for classes, or `render()` for UI components
4. **beforeEach / afterEach** — setup DOM fixtures, create instance or render, cleanup (e.g. `clearAllMocks()`)
5. **describe** — one outer `describe` per module, one nested `describe` per function/method
6. **it / test** — one `it` or `test` per test case (one behavior, one assertion logic)

Example (Class/Jest pattern):

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

- Use a setup helper appropriate to the SUT: `setup()` for functions, `getInstance()` for classes, `render()` for UI components
- Use `beforeEach()` for common setup, `afterEach()` for cleanup (`clearAllMocks()`, `restoreAllMocks()`, or equivalent)
- `it` / `test` naming: `it('should ...')` or `test('should ...')` — describes the expected behavior, with condition if relevant
- Use `with ...` or `if ...` for variants: `'should call removeStickyFromNavbar if user has scroll down'`, `'should return null if urlTemplate is not defined'`
- `describe` naming for methods: `'should call the methodName'`, then nested `it` for variations
- Test negatives with `.not` to prevent mutation testing escape
- Prefer complete coverage to limit mutants
- Follow setup → execution → expectations order in each test
- CSS and SVG imports are mocked via `file-mock.js`
- HTML templates in tests: follow the project convention — if other tests use JSX, use JSX. If they use string (`innerHTML`), use string. Stay consistent

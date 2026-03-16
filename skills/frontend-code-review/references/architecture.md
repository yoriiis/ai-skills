# Architecture & Project Structure

Reference standards for project organization, package management, and front-end architecture (framework-agnostic).

---

## Architecture Principles

### Context Window Amnesia (AI-generated code)

- AI often produces **local** fixes that pass review but break the **global** architecture (wrong module, duplicated logic, bypassed layers). When reviewing AI-generated or AI-assisted changes, ask: "Does this fit the existing architecture? Is logic duplicated elsewhere? Are layers/abstractions respected?"

### Single Responsibility Principle (SRP)

- A function should do only what its name indicates
- If you need "and" to describe it, split it
- See `references/js-ts.md` for JS/TS detection patterns

### Dependency Inversion Principle (DIP)

- Depend on abstractions, not concrete implementations
- Do not instantiate heavy dependencies (API clients, Logger) inside functions — pass them as parameters or via constructor to enable mocking in tests
- Inject dependencies via constructor/parameters
- See `references/js-ts.md` for JS/TS patterns

### Testability by Design

- Even when no tests exist, code must be written **as if it will be tested**: pure functions when possible, clear inputs/outputs, no hidden coupling
- Prefer explicit dependencies over implicit ones

### Component Complexity (framework-agnostic)

- **Think in components.** The UI should be split into logical, reusable units regardless of the framework (React, Vue, Twig, server-side templates, etc.). If a template or component grows too large, has too many conditionals, or takes on multiple responsibilities, flag it as **Important** and suggest splitting into smaller, focused units.
- **Scope & boundaries**: Analyze if a change belongs in the current component. Flag changes that seem "out of scope" for the component's primary responsibility.

### Design Patterns to Recognize (Flag as Suggestion)

- Tight coupling between components
- God objects/classes that know too much
- Deep inheritance hierarchies (prefer composition)
- Feature envy

---

## Separation of Concerns (SoC)

- Separate business logic and data handling from DOM manipulation or UI rendering. Keep presentation and data/domain logic in distinct layers.

---

## Coupling & Cohesion

- Avoid strong coupling between distinct modules. Prefer clear boundaries and high cohesion within each module.

---

## Data Flow / Data Model

- Ensure predictable data flow and a clear data model. Prefer a single source of truth where relevant; avoid inconsistent duplication between UI and the underlying data model. (Use "data flow" or "data model" rather than framework-specific terms.)

---

## Project Structure & Tooling

### General

- Coverage directory: NOT committed to git
- `.nvmrc`: use named versions (`lts/hydrogen`, `lts/iron`)

### Package.json

- Dependency version format must follow the project convention — some projects pin exact versions, others use `^` or `~`. Check existing `package.json` and stay consistent
- If `package.json` is modified (dependency added, removed, or version changed), `package-lock.json` must be updated and committed in the same MR. Same for `composer.json` → `composer.lock`. A `package.json` change without its lockfile is a red flag
- For libraries: check `"exports"` and `"files"` fields are properly configured if the package is published

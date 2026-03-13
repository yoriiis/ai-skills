---
name: frontend-code-review
description: Review MR/PR with a senior front-end architect methodology. Use when asked to review a MR or PR on GitHub or GitLab (public or private instances). Produces high-value feedback focused on bugs, security, architecture, accessibility, and knowledge sharing. Adapts to each project's conventions.
---

# Review MR/PR

Review agent that replicates a senior front-end architect's code review methodology. Works with GitHub Pull Requests and GitLab Merge Requests.

## Review Philosophy

**Every comment must earn its place.** A review that wastes a developer's time destroys trust. Before writing any feedback, ask yourself:

1. **Does it prevent a real problem?** (bug, security issue, data loss, production incident)
2. **Does it teach something?** (pattern the dev didn't know, context from another project, known pitfall)
3. **Does it save future debugging time?** (edge case, missing error handling, integration risk)
4. **Does it improve user experience?** (accessibility, performance)

If the answer to all four is "no", it's noise. Don't report it as a primary finding.

### Feedback levels

- **Blocking**: Real problems that must be fixed. Always report.
- **Important**: Significant improvements that make the codebase better. Report with an explanation of WHY it matters.
- **Minor**: Minor issues detectable by tooling or low-impact style preferences. Mention them briefly in a dedicated section. Never let these overshadow Blocking/Important feedback.

**Golden rule**: if the project has a linter/formatter configured and a CI pipeline, trust the tooling for formatting and style. Focus human review time on what tools cannot catch.

## Workflow

Always the same flow — no mode to detect:

1. **Phase 1 (obligatory)** — Analyse + report in chat
2. **Phase 2 (optional)** — Ask the user: "Which findings would you like to post on the MR?" (e.g. All Blocking, Blocking + Important, custom selection, None)
3. **Phase 3** — Post selected findings on the MR/PR (if the user chose any) with IA disclosure

Use the Ask/question mode to display options before posting.

## Quick Start

When asked to review a MR/PR:

1. Parse the MR/PR reference (project path + MR/PR number)
2. **Access check** — verify you can reach the project and MR/PR (see below)
3. **Discover project conventions** (Step 0)
4. Fetch MR/PR metadata (GitLab MCP `get_merge_request`, or GitHub equivalent)
5. Fetch diffs via MCP
6. Fetch pipeline/CI status
7. Load relevant references based on changed file types (see Reference loading). Ignore files with unsupported extensions — no feedback.
8. Apply the review checklist (Blocking → Important → Minor), using contextual analysis and duplication detection
9. Format findings using the output template (Phase 1 — report in chat)
10. Ask which findings to post (Phase 2), then post selected ones with IA mention (Phase 3)

## Supported platforms

- **GitHub**: Pull Requests (github.com or GitHub Enterprise)
- **GitLab**: Merge Requests (gitlab.com or self-hosted instance)

The agent uses available MCPs (GitLab MCP, GitHub MCP) depending on the project. If no MCP is configured for the target platform, the user must provide the diff or modified files.

## MR/PR Reference Parsing

**Compatible with**: GitHub (Pull Requests), GitLab (Merge Requests) — public or private instances.

Accepted formats:

- GitLab: `!294`, `namespace/project!294`, full URL
- GitHub: `#123`, `owner/repo#123`, full URL

## Access check (first)

**Before any discovery**, verify access to the project and MR/PR:

1. Call `get_merge_request` (GitLab) or equivalent for GitHub — if it fails (404, 403, MCP not configured), stop and inform the user:
   - "Unable to access the MR/PR. Check: MCP configured for GitLab/GitHub? Project path correct? Permissions?"
2. Optionally, fetch a minimal diff — if diffs cannot be retrieved, stop early.
3. Only proceed to convention discovery and full review once access is confirmed.

## Step 0: Discover Project Conventions

**Before reviewing any code**, analyze the project to understand its conventions and tooling. This determines WHAT you review and WHAT you skip.

### What to discover

Use `search` (scope: `merge_requests`, project scoped, state: `merged`, per_page: 5) to check recent merged MRs:

- **Labels**: does the project use labels? Which ones?
- **Squash**: are MRs squashed on merge?
- **Reviewers**: are reviewers systematically assigned?
- **Description style**: do MRs reference tickets? How detailed?
- **Branch naming**: what pattern? (`feat/`, `fix/`, ticket IDs, etc.)

Use `search` (scope: `blobs`, project scoped) to detect project tooling:

- **Language**: `tsconfig.json` → TypeScript? Pure JS?
- **Linter**: `biome.json` or `.eslintrc` or `eslint.config` → which linter?
- **Formatter**: Biome, Prettier, or none?
- **Test framework**: `jest.config`
- **Package type**: `"type": "module"` in `package.json` → ESM or CJS?
- **CHANGELOG**: does `CHANGELOG.md` exist?
- **NVM**: does `.nvmrc` exist?
- **CI**: check `.gitlab-ci.yml` or `.github/workflows/*` for pipeline structure
- **Build stripping**: does the build strip `console.log`? (check rspack/webpack config or Biome config)

### Project-specific rules

Check if the project has its own coding rules or conventions:

- **Cursor rules**: search for `.cursor/rules/` in the project — if present, read them and use them as additional review context
- **Cursor skills**: search for `.cursor/skills/` in the project
- **Documentation**: check for `CONTRIBUTING.md`, `CODING_STANDARDS.md`, or similar

These project-specific rules take precedence over the generic references in this skill.

### Coding style detection

Detect the project's coding conventions from its configuration files (don't guess — read the config):

- **`.editorconfig`**: indentation style (tabs/spaces), indent size per file type, final newline, charset
- **`biome.json`** / **`.prettierrc`**: quotes, semicolons, trailing commas, indent style
- **`.code-workspace`** or **`.vscode/settings.json`**: editor-level overrides
- **`.eslintrc`** / **`eslint.config`**: code style rules
- **`.stylelintrc`**: CSS style rules

If none of these files exist, analyze actual source files to infer conventions.

If a file in the MR uses a different style than what the project config enforces, flag it. The MR must match the project's existing conventions, not an external standard.

### Convention profile

Build this profile before reviewing:

```
Project: [name]
Language: TypeScript | JavaScript | Mixed
Module: ESM | CJS | Unknown
Linter: Biome | ESLint | Stylelint | None detected
Formatter: Biome | Prettier | None detected
Tests: Jest | None detected
Build strips console: Yes | No | Unknown
Uses labels: Yes (list) | No
Squash on merge: Yes | No
CHANGELOG: Yes | No
Branch convention: feat/<ticket> | <TICKET-ID> | free-form
```

### Tooling calibration

Based on the profile, adjust what you report:

- **Linter detected** → formatting, unused imports, semicolons = Minor (non-blocking)
- **Build strips console.log** → console.log = Minor (or omit if build strips)
- **No linter detected** → these issues become Important since no automated safety net
- **No tests detected** → missing tests = Important, not just a suggestion

### Reference loading

Load references **after** diffs are fetched. Apply rules based on changed file types. Deduplicate when multiple file types map to the same reference.

**Base (always)**: `references/security.md` + `references/code-quality.md`

**By changed file type**:

| File pattern                                                     | References to load                                              |
| ---------------------------------------------------------------- | --------------------------------------------------------------- |
| `*.js`, `*.ts`, `*.mjs`, `*.cjs`                                 | `javascript-typescript.md`                                      |
| `*.jsx`, `*.tsx`                                                 | `javascript-typescript.md` + `accessibility.md` (UI components) |
| `*.css`, `*.scss`, `*.less`                                      | `css.md`                                                        |
| `*.html`                                                         | `html.md` + `accessibility.md`                                  |
| `*.twig`                                                         | `twig.md` + `html.md` + `accessibility.md`                      |
| `*.vue`, `*.svelte`                                              | `accessibility.md`                                              |
| `*.png`, `*.jpg`, `*.jpeg`, `*.gif`, `*.webp`, `*.avif`, `*.svg` | `images-assets.md`                                              |

**By changed content**:

| Content                                       | Reference              |
| --------------------------------------------- | ---------------------- |
| `package.json`, `tsconfig.json`, config files | `project-structure.md` |
| `.gitlab-ci.yml`, `.github/workflows/*`       | `ci-cd.md`             |

**By review scope**:

| Condition                                                                                       | Reference                                 |
| ----------------------------------------------------------------------------------------------- | ----------------------------------------- |
| Test files changed (`*.test.*`, `*.spec.*`, `**/__tests__/*`)                                   | `testing.md`                              |
| Application code changed (JS/TS, HTML, Twig, components) **without** corresponding test changes | `testing.md` (to check for missing tests) |

**Scope**: Only review files matching the patterns above. Files with unsupported extensions (e.g. `.php`, `.py`, `.go`, `.rb`, `.java`, `.kt`) are **out of scope** — do not load references for them, do not comment on them, do not flag issues. If a MR contains only out-of-scope files, state that the skill does not cover these file types and skip the code review.

## Source of truth: MR diff only

**Analysis is based ONLY on the MR and its diff.** Never on the local workspace.

- **Source of truth**: diff fetched via MCP (GitLab/GitHub). Do not read local files to compare or analyze.
- **Extra context**: if needed, use `get_repository_file` (or equivalent) to read a file on the source branch of the remote repo — not the workspace file.
- **Aligned with diff**: before asking "remove X", verify that X is still present in the diff (added/modified lines). If X only appears in removed lines (-), do not ask to remove it — it is already done. Feedback must target only what will remain after merge.
- **No confusion**: do not mix workspace state with MR state.

## Review Checklist

```
Review Progress:
- [ ] 0. Discover project conventions & tooling
- [ ] 1. MR metadata (adapted to project)
- [ ] 2. Pipeline status
- [ ] 3. Code analysis (contextual analysis + duplication detection)
- [ ] 4. Blocking (bugs, security, data loss)
- [ ] 5. Important (architecture, a11y, edge cases, perf)
- [ ] 6. Minor (non-blocking minor items)
- [ ] 7. Ce qui fonctionne bien & verdict
```

### 1. MR Metadata (adapted)

**Always check:**

- Pipeline status is visible and green
- Branch name contains the ticket ID (format varies: `TICKET-ID`, `feat/TICKET-ID`, etc. — just verify the ticket number is present)
- No conflicts with the target branch
- **Description**: do not ask for a description or ticket link when the description is empty. A description is useful only when the MR contains changes beyond the ticket (additional fixes, opportunistic refactoring, etc.) and an explanation would help the reviewer. If no ticket in the project or empty description: say nothing. Only mention when diffs clearly go beyond a single ticket AND there is no explanation — "These changes seem to go beyond the ticket — a short description would help the reviewer."

**Only if the project uses them:**

- Labels → check appropriate labels are set
- Assignee/reviewer → check they are assigned
- Ticket reference → check present in title or description
- Squash on merge → check it matches project convention

### 2. Pipeline Status

- If pipeline failed, identify the failing job and report it

### 3. Code Analysis

#### Contextual analysis

The diff alone is not always enough. When a change seems ambiguous or the surrounding code matters (HTML hierarchy, function scope, variable declarations above/below), use `get_repository_file` to fetch the full file on the source branch and verify the context around the changed lines. Typical cases:

- HTML insertion: check the parent element (e.g., a `<div>` added inside a `<ul>` is invalid)
- Function modification: check the full function to understand scope and side effects
- CSS change: check surrounding selectors for specificity or nesting context
- Variable usage: check if it's already declared/used elsewhere in the file

#### Deleted lines

**Do not provide feedback on deleted code**, unless the deletion itself causes a problem:

- Do not flag bugs, style issues, or quality issues on removed lines
- Only flag if the deletion introduces a bug, regression, or architectural break (e.g. removing a function still used elsewhere)
- Flag if the deletion leaves orphaned code or broken references

Principle: deleted code will no longer exist after merge. Feedback must focus on what remains or on the impact of the deletion.

**Aligned with diff**: before asking "remove X", verify X is still present in the diff (added/modified lines). If X only appears in removed lines (-), do not ask to remove it — it is already done.

Do not flag issues on **unchanged code** (context only) unless Blocking (e.g. security vulnerability).

#### Duplication detection

When the MR introduces new logic (utility function, pattern, component), use `search` (scope: `blobs`, project scoped) to check if similar code already exists elsewhere in the project. Flag duplication as Important with a suggestion to factor shared logic. Typical duplications:

- Helper functions that already exist in a shared utils module
- Copy-pasted event handling patterns across components
- Repeated DOM manipulation sequences that could be abstracted

### File validity

Every file touched in the MR must be syntactically valid for its type. Invalid files are Blocking:

- YAML (`.yml`, `.yaml`): valid structure, correct indentation
- JSON (`package.json`, `tsconfig.json`, etc.): valid JSON, no trailing commas
- HTML / Twig: valid markup, properly closed tags
- CSS: valid syntax, matching braces
- JS / TS: no syntax errors

### 4. Blocking

These are real problems. Always report.

→ Load `references/security.md` for detailed security checklist.

**Bugs & logic errors:**

- Inverted conditions, off-by-one, wrong comparisons
- Null/undefined dereferences that WILL crash
- Infinite loops, infinite recursion
- Wrong variable used (copy-paste errors)

**Security:**

- XSS vulnerabilities (innerHTML with user input)
- Secrets, tokens, API keys committed
- CORS misconfiguration
- Unvalidated user input used in DOM or queries

**Data integrity:**

- Race conditions on shared state
- Data loss (overwriting without backup)
- Inconsistent state after partial failure

**Production hazards:**

- Hardcoded feature branch names, localhost URLs, test API endpoints
- Debug code: `debugger`, `alert()` for debugging
- Commented-out code that disables critical functionality

### 5. Important

These make the codebase significantly better. Report with an explanation of WHY. Each finding must include the concrete consequence in one sentence.

→ Load `references/code-quality.md` for error handling, performance, and boundary conditions checklists.
→ Load `references/accessibility.md` for a11y checks.

**Accessibility:**

- Modal/overlay opened without focus trap
- SVG in button/link without `sr-only` text alternative
- SVG missing `aria-hidden="true"` and `focusable="false"` on decorative icons
- Images without `alt` attribute
- Click targets smaller than 30x30px
- `<a>` used where `<button>` is appropriate (and vice versa)
- Focus set on invisible elements (must wait for CSS transition to end)
- Heading hierarchy broken (`h1` → `h3` without `h2`)

**Architecture & design:**

- Function/class doing too many things → suggest extraction
- Tight coupling between components that should be independent
- Duplicated logic that should be factored
- Types/interfaces placed in wrong location (local vs shared)
- Component not adaptive (hardcoded dimensions instead of 100% width)
- New file using CJS in an ESM project (or vice versa)

**Edge cases & robustness:**

- Array operations without empty-array guard
- Async operations without error handling (missing try/catch or .catch)
- Optional chaining missing where data can be undefined
- DOM queries without null checks on results

**Performance:**

- DOM manipulation inside a loop (should batch or use fragment)
- Selectors queried repeatedly instead of cached
- Heavy computation in a hot path without memoization
- Unnecessary re-renders or redundant event listeners

**Integration & regression risk:**

- Changes that could break consumers of a shared library
- Missing CHANGELOG entry for a notable change (if project uses CHANGELOG)
- API contract changes without version bump
- Shared library / component integration issues (symlinks, vendor configs)
- Unintentional changes in the MR (formatting diffs, unrelated file modifications, debug leftovers) — the MR should only contain what's needed for the ticket
- Build artifacts or generated files committed (`dist/`, `build/`, `coverage/`, `.cache/`, compiled CSS/JS) — these should be in `.gitignore`

**Testing (if project has tests):**

- New logic without corresponding test
- Test that doesn't actually test anything meaningful
- Missing negative test cases (`.not` expectations to prevent mutants)

### 6. Minor (non-blocking)

Group these in a dedicated **Minor** section. One line per item.

- `console.log` / `console.info` / `console.debug` left in code — never Blocking (except if logs contain tokens, passwords, PII). If build strips them, omit or barely mention.
- Trailing empty lines, extra whitespace
- Import ordering preferences
- Minor naming improvements that don't affect readability
- CHANGELOG section title format (`### Updates` vs `### Features`)
- Minor CSS convention deviations

### 7. Ce qui fonctionne bien & Verdict

When relevant, highlight what was done well — no obligation to find something. Examples: clean separation of concerns, good error handling, well-written tests, clear naming, good use of TypeScript types. Keep it in the flow of the report, not a separate section. If nothing stands out, skip.

## Severity Levels

- **Blocking** — Must fix before merge. Bugs, security, data loss. Each finding must include the concrete consequence.
- **Important** — Should fix, significant improvement. **Must include WHY** it matters and the consequence.
- **Suggestion** — Nice to have. Lower impact. Explain the concrete benefit.
- **Minor** — Non-blocking items. One line per item in the Minor section.

## Language

Review feedback is in **English by default**. If the user requests another language (e.g. "in French", "en français"), write the feedback in that language.

## Output Template

```markdown
## Review: [MR/PR Title]

**Project**: [project path] | **MR/PR**: [link] | **Pipeline**: [status]
**Verdict**: **[APPROVE | REQUEST CHANGES | NEEDS DISCUSSION]**

> [1-2 sentences: summary and overall impression]

### Findings

#### `[filename]`

- **Blocking** — [Short description. Consequence if not fixed.]
- **Important** — [Short description. Why it matters. Consequence.]
- **Suggestion** — [Short description.] _(personal opinion)_

### Minor

- `[file]`: console.log left
- `[file]`: newline missing at end of file
- `[file]`: unused imports
```

### Writing rules

- **Constructive feedback**: specific and actionable; explain why; suggest an alternative when possible (not just "this is wrong")
- **Focused on the code, not the person** — critique the code, not the developer
- **Educational, not judgmental** — avoid "Why didn't you use X?"; use "Have you considered…?" instead
- **Consequence required**: each Blocking or Important finding must include the concrete consequence in one sentence
- **Prioritized**: clearly distinguish Blocking vs Important vs Minor
- **Consolidate**: group similar issues (e.g. "5 functions missing error handling" not 5 separate findings)
- **Short and direct**: 1-2 sentences per finding max
- **Verdict first**: the developer must know immediately if they need to act
- **Group by file**: easier to navigate than by severity
- **Minor section**: non-blocking items (log, newline, imports, etc.) go in the Minor section, one line per item — not in per-file findings
- **Subjective opinion**: if a finding is personal preference, note it ("personal opinion", "subjective"). For Suggestion/Minor: add "Not blocking if you prefer" when relevant
- **Ce qui fonctionne bien**: when relevant, in flow — not mandatory
- **Code suggestion**: when relevant, not systematic
- **GitLab suggestion syntax** for code modifications:
  ````
  ```suggestion:-0+0
  corrected code here
  ```
  ````
- **Tone**: professional, direct, constructive. Like a senior colleague, not an audit report.
- **Length**: a review should be readable in 2 minutes, not 10
- **Diff only**: never use local workspace files; analysis based solely on MR diff from MCP

## Publishing to GitLab/GitHub

Workflow: report in chat (Phase 1) → ask user which findings to post (Phase 2) → post selected findings (Phase 3).

When posting comments on the MR/PR:

1. Use `create_workitem_note` for general comments
2. Always be constructive — suggest fixes, don't just point out problems
3. Use GitLab/GitHub suggestion syntax for code modifications
4. Keep a respectful and collaborative tone
5. **Do not create a thread/note on pipeline status** — status stays in the report header only
6. **IA disclosure (mandatory)** — append to each posted comment: `---` then `*Review assisted assistée par skill frontend-code-review*` (or `*AI-assisted review (skill)*` in English)

## Resources

See **Reference loading** above for when to load each file.

| File                                  | Purpose                                          |
| ------------------------------------- | ------------------------------------------------ |
| `references/javascript-typescript.md` | JS/TS conventions, DOM, events, class patterns   |
| `references/html.md`                  | Semantics, script loading, W3C syntax            |
| `references/css.md`                   | PostCSS, BEM, custom properties, responsive      |
| `references/twig.md`                  | Twig template conventions, includes, defaults    |
| `references/accessibility.md`         | SVG a11y, focus management, ARIA, semantic HTML  |
| `references/security.md`              | XSS, third-party scripts, secrets, runtime risks |
| `references/code-quality.md`          | Error handling, performance, boundary conditions |
| `references/testing.md`               | Jest conventions, test structure                 |
| `references/project-structure.md`     | Directory layout, package.json, CHANGELOG        |
| `references/ci-cd.md`                 | Pipeline, GitHub Actions, GitLab CI              |
| `references/images-assets.md`         | Image format, size, SVG optimization, sprites    |

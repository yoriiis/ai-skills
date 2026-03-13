# Templates

Reference standards for server-side HTML template review. Generic rules applicable to Server-side HTML templating engines (Twig, Blade, Nunjucks, Liquid, etc.).

---

## General Principles (Applicable to JSX, Vue, Twig, etc.)

- **No Business Logic**: Templates must remain strictly presentational. Complex data manipulation, filtering, or business rules must be handled in controllers, services, or hooks, not in the template.
- **Component Complexity**: Think in components. If a template/component grows too large, has too many conditionals, or takes on multiple responsibilities, flag it as an **Important** architectural issue and suggest splitting it into smaller, focused components.
- **Scope & Boundaries**: Analyze if a change belongs in the current component. Flag changes that seem "out of scope" for the component's primary responsibility.

## Twig Specifics

### Include & Isolation

- Use `include()` function, not `{% include %}` tag
- Always pass `false` as third argument to prevent variable leakage into the included template:

```twig
{{ include('component/views/component.html.twig', {
    data: data,
}, false) }}
```

### Variable Defaults

- Define variable defaults at the top of the template, before any HTML:

```twig
{% set hasSidebar = hasSidebar ?? true %}
{% set additionalClass = additionalClass|default('') %}
```

- Prefer `??` (null coalescing) for booleans — it only checks if the variable is defined, not if it's falsy
- Use `|default('')` only for string fallbacks
- **Never `|default(true)` or `|default(false)` on booleans** — `|default()` treats `false`, `0`, `""`, `null` as empty and replaces them with the default. Passing `false` from a parent template becomes impossible. Use `??` instead:

```twig
{# Bad — if parent passes false, it gets overridden to true #}
{% set hasSidebar = hasSidebar|default(true) %}

{# Good — only applies if hasSidebar is not defined at all #}
{% set hasSidebar = hasSidebar ?? true %}
```

### Ternary Simplification

- Avoid unnecessary ternary with empty string fallback:

```twig
{# Bad — the empty string is useless #}
{{ isActive ? 'isActive' : '' }}

{# Good — Twig handles falsy values natively #}
{{ isActive ? 'isActive' }}
```

### Security (XSS)

- **Contextual escaping**: Use Twig's auto-escaping and the appropriate escape context for each output — `|e('html')` for HTML content, `|e('html_attr')` for attributes, `|e('js')` for JS contexts, `|raw` only when the content is explicitly trusted and already sanitized. Prevents XSS when user-controlled or dynamic data is rendered.

### Component Structure

- Avoid sub-sub-components: max 2 levels of nesting
- Import macros at the top of the file, before any HTML
- Use data attributes for JavaScript hooks (not classes)

### Class Naming in Templates

Respect the convention already present in existing template and CSS files. Detect class naming patterns (BEM, utility classes, etc.) from the codebase and match them. If no convention is detected, do not impose.

### Quotes

- Single quotes by default for all static strings
- Double quotes only when using interpolation: `"#{variable}"`
- Prefer interpolation over concatenation:

```twig
{# Bad — concatenation #}
{{ 'Hello ' ~ name ~ ', welcome!' }}

{# Good — interpolation #}
{{ "Hello #{name}, welcome!" }}
```

### Naming

- Variables must have descriptive names — no `a`, `b`, `e`, `item1`
- **Loop variables**: Avoid generic terms like `item` in `for item in items`. Prefer context-specific names like `for article in articles` to improve readability and avoid scope confusion in nested loops
- The template must be readable without external context
- Clear indentation: consistent depth, aligned with the HTML structure

### Formatting

- Indentation: follow the project convention (check existing `.twig` files — often 4 spaces, enforced by `twig-cs-fixer` if present)
- Trailing comma in multi-line structures, no trailing comma on single-line
- Final newline at end of file

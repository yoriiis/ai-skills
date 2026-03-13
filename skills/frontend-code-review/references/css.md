# CSS / PostCSS

Reference standards for CSS review. Only enforce rules that match the target project's conventions.

---

## PostCSS / CSS Features

Don't impose any specific plugin or syntax. Instead, detect what the project uses (check `postcss.config`, existing CSS files) and ensure the MR is consistent with it.

Common PostCSS plugins you may encounter:

- `postcss-nested` — nesting with `&` selector (NOT native CSS nesting)
- `postcss-custom-properties` — CSS variables
- `postcss-custom-media` — custom media queries (`@media (--media-tablet)`)
- `postcss-preset-env` — modern CSS features

If the project uses nesting (e.g., `postcss-nested`), new CSS in the MR should use nesting too — don't write flat CSS when the project convention is nested. Same logic applies to custom properties, custom media queries, etc.

## General Rules

- Follow the project's existing notation and naming conventions — detect from existing CSS files
- **Z-index management**: Avoid magic numbers (e.g., `9999`). Use a centralized system (CSS variables like `--z-index-modal`) or rely on stacking contexts to keep layering predictable
- Hex colors in lowercase: `#ff6600`, not `#FF6600`
- Use CSS variables for colors — prefer existing project variables over hardcoded hex values
- Nest as much as possible (if project uses nesting), but max 2-3 levels deep
- Prefer `margin-bottom` for spacing between components (`margin-top` only if the component is optional)
- Use `px` for `font-size`, `line-height`, `letter-spacing`
- Use numeric values for `font-weight` (400, 700, not `normal`, `bold`)
- Components must be 100% width and adapt to their parent container
- Plan for dark mode in component styles

## BEM Naming Convention

BEM with camelCase for element separators and state modifiers without block prefix. Always nested:

```css
.bookmarkButton {
	&-follow {
	}
	&-followText {
	}

	&.isActive {
	}
	&.isFollowed {
	}
	&.isDisabled {
	}
	&.isLoading {
	}
}
```

- Modifiers are standalone camelCase classes: `class="headerNav-link isActive"` (not `headerNav-link--active`)
- Common state classes: `isActive`, `isFollowed`, `isDisabled`, `isLoading`, `iconOnly`

## Nesting (postcss-nested)

Use `&` for nesting. This is postcss-nested syntax, not native CSS nesting:

```css
.toast {
	position: fixed;

	&-box {
		display: flex;
	}

	&.active {
		animation: fadeIn 0.3s ease-out forwards;
	}
}
```

## CSS Custom Properties

- Variable naming follows camelCase: `--secondaryNeutralColor`, `--tertiaryNeutralVariantColor`
- Common prefixes: `--fs-*` (font sizes), `--*Color` (colors), `--*Radius` (radii), `--transition*` (transitions)
- Dark mode SVG overrides use `_` prefix (auto-removed in production): `var(--_iconColor)`

## CSS Property Order

- Group properties logically: Positioning → Display & Box Model → Typography → Visual → Animation

## Responsive Design

- Use custom media queries: `@media (--media-tablet)`, `@media (--media-desktop)`

## File Organization

- Follow the project's file organization — detect from existing CSS files and component structure

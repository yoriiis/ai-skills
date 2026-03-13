# Project Structure

Reference standards for project organization and package management.

---

## General

- Coverage directory: NOT committed to git
- `.nvmrc`: use named versions (`lts/hydrogen`, `lts/iron`)

## Package.json

- Dependency version format must follow the project convention — some projects pin exact versions, others use `^` or `~`. Check existing `package.json` and stay consistent
- If `package.json` is modified (dependency added, removed, or version changed), `package-lock.json` must be updated and committed in the same MR. Same for `composer.json` → `composer.lock`. A `package.json` change without its lockfile is a red flag
- For libraries: check `"exports"` and `"files"` fields are properly configured if the package is published

## CHANGELOG Format

Only if the project already has a `CHANGELOG.md`. Include a link to the MR for traceability.

```markdown
# Changelog

## [2.1.0]

### Features

- Add support for playlist mode ([!123](MR_URL))

### Bug Fixes

- Fix player not loading on iOS Safari ([!124](MR_URL))

### Breaking Changes

- Remove deprecated `autoload` parameter ([!125](MR_URL))
```

- Semantic versioning
- Breaking changes clearly documented
- Link to the MR on each entry

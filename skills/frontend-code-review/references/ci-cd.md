# CI/CD

Reference standards for pipeline/workflow configuration (GitLab CI, GitHub Actions).

---

## Common (both platforms)

- YAML must be valid — syntax errors break the pipeline
- No hardcoded secrets, tokens, or credentials — use platform variables (CI/CD vars, GitHub secrets)
- No hardcoded environment-specific URLs (staging, production)
- Job/workflow names clear and descriptive
- Correct trigger conditions — ensure jobs run on the right branches/events
- Cache configuration — avoid bad patterns (e.g. caching node_modules without key)
- Job dependencies / execution order correct

---

## GitLab CI (.gitlab-ci.yml)

- Check `only` / `rules` conditions
- Verify `artifacts` and `cache` configuration
- Check `needs` / `dependencies`

---

## GitHub Actions (.github/workflows/\*)

- Check `on:` triggers (push, pull_request, workflow_dispatch)
- Verify `secrets.*` usage (no hardcoded secrets)
- Check `permissions` (avoid over-permissive)
- Validate `actions/checkout`, `actions/cache` usage
- Job dependency via `needs:`

# Git workflow

1. `git checkout main && git pull`
2. `git checkout -b feature/<task-name>`
3. Commit small and often, with clear messages.
4. `git push -u origin feature/<task-name>` then open a Pull Request.
5. The **other** member reviews and approves (real comments, not just "LGTM").
6. Merge (squash or merge commit) — never commit directly on `main`, never upload via the web UI.

Branches: `feature/setup`, `feature/data-preparation`, `feature/exploration-part1`,
`feature/exploration-part2`, `feature/data-enrichment`, `feature/streaming-wikipedia`,
`feature/open-question`, `feature/report`.

Style: Python follows PEP 8 (`ruff check .`), Markdown stays clean and consistent.

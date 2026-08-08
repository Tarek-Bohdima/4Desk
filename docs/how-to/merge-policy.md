# How to merge PRs (which button to press)

| PR type | Method | Why |
|---|---|---|
| **Upstream sync** (merging a RustDesk release tag) | **Merge commit** — never squash/rebase | Preserves shared ancestry with upstream. Squashing flattens the merge and every future upstream merge replays all conflicts again. This is the iron rule. |
| Feature / fix / docs PR | **Squash** | One issue = one PR = one commit on `main`; readable history, trivial reverts; strict-mode refresh commits disappear. |
| Refreshing a branch that's behind main | Merge main in (unstacked PRs) · rebase (inside a GitHub stack) | Merge needs no force-push; stacks require linear history. |

Repo settings enforce this: squash and merge-commit enabled, rebase-merge disabled, head branches auto-deleted on merge. Branch protection additionally requires a PR, green `rust-gates`/`flutter-gates`, and an up-to-date branch (strict mode — CI must have tested exactly what lands on main).

When a stacked PR's base merges, GitHub retargets it; if a stacked PR still auto-closes, recreate it against `main` and comment why on the closed one.

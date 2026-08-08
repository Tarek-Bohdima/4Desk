# How to add a feature flag

Every 4desk feature is toggleable and isolated. Steps (TDD — tests first):

1. **Tracking issue** with acceptance criteria (hard rule; every PR links one).
2. **Register the flag** in both registries, same key:
   - Rust: add a variant to `Flag` in `src/four_desk/feature_flags.rs` (`key()`, `default_enabled()`).
   - Dart: add an enum value in `flutter/lib/four_desk/feature_flags.dart`.
3. **Write the tests first** — extend `feature_flags` tests for the new flag, plus tests for the feature itself under `src/four_desk/<feature>/` and `flutter/test/four_desk/`.
4. **Implement the feature** in its own module: `src/four_desk/<feature>.rs` / `flutter/lib/four_desk/<feature>/`. Upstream files may only gain a minimal integration point (one call/one widget insertion) guarded by `is_enabled(...)`.
5. **Toggle at runtime** (until server-pushed config exists): the flag reads local option `4desk-flag-<key>` = `Y`/`N`; unset falls back to the compile-time default.
6. Callers never inspect config storage directly — always ask the flag service (Law of Demeter).

## UI regression: golden tests

Every `four_desk` widget ships with a golden test (`flutter_test`'s `matchesGoldenFile`; baselines under `flutter/test/four_desk/goldens/`, which are exempt from the repo's `*png` ignore). CI fails when rendering changes; updating a baseline requires a deliberate `flutter test --update-goldens` commit that reviewers see — never regenerate goldens to make a failing test pass (same hard rule as all tests). Goldens are rendered on the Linux CI runner; generate them there (or accept the CI-generated baseline) to avoid font/platform drift.

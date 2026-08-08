## Tracking issue

Closes #<!-- REQUIRED: every PR must be tracked by an issue with acceptance criteria -->

## What & why

## Checklist

- [ ] All acceptance criteria of the linked issue are met
- [ ] TDD followed: tests written first; **no existing unit/instrumentation/E2E test was modified to make it pass**
- [ ] `cargo fmt --check` + `cargo clippy -- -D warnings` clean (Rust touched)
- [ ] `dart format --set-exit-if-changed .` + `flutter analyze` clean (Dart touched)
- [ ] Upstream files touched only at minimal integration points; new 4desk code isolated in `src/four_desk/` / `flutter/lib/four_desk/`

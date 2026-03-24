# Changelog

All notable changes to `agent-signal` will be documented here.

Format: [Keep a Changelog](https://keepachangelog.com/en/1.0.0/)  
Versioning: [Semantic Versioning](https://semver.org/spec/v2.0.0.html)

## [1.0.0] — 2024-03-24

### Added
- `Signal` — named event channel with `connect`, `disconnect`, `emit`, `emit_async`, `clear`
- `SignalRegistry` — thread-safe registry of named signals
- `EventBus` — broadcast bus with glob topic filtering via `fnmatch`
- `@on_signal` — decorator for auto-connecting functions to named signals
- Full test suite (38 tests, 100% pass rate)
- Zero runtime dependencies (Python ≥ 3.10 stdlib only)

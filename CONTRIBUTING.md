# Contributing

Thank you for your interest in contributing to `agent-signal`!

## Getting Started

```bash
git clone https://github.com/darshjme-codes/agent-signal
cd agent-signal
python3 -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
```

## Running Tests

```bash
python -m pytest tests/ -v
```

All tests must pass before submitting a PR. New features require new tests.

## Code Style

- Follow PEP 8
- Use type hints throughout
- Keep zero runtime dependencies — stdlib only
- Thread-safety is non-negotiable for all shared state

## Pull Requests

1. Fork the repo and create a feature branch
2. Write tests for your change
3. Ensure `pytest` passes with no failures
4. Open a PR with a clear description of the problem and solution

## Commit Convention

```
feat: add WeakRef support to Signal
fix: race condition in EventBus.unsubscribe
docs: improve @on_signal docstring
test: add edge case for empty glob pattern
```

## Reporting Bugs

Open a GitHub issue with:
- Python version
- Minimal reproduction script
- Expected vs actual behavior

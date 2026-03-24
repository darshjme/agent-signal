# Security Policy

## Supported Versions

| Version | Supported |
|---------|-----------|
| 1.x     | ✅ Yes     |

## Reporting a Vulnerability

**Do not open a public GitHub issue for security vulnerabilities.**

Please email the maintainer directly at **darshjme@gmail.com** with:

- Description of the vulnerability
- Steps to reproduce
- Potential impact
- Suggested fix (optional)

You will receive a response within 48 hours. We aim to release a patch within 7 days of confirmation.

## Scope

`agent-signal` is a pure-Python, zero-dependency library. Known threat surfaces:

- **Thread safety:** All mutable state uses `threading.Lock`. If you find a race condition, please report it.
- **Handler exceptions:** Exceptions in handlers propagate to the caller of `emit()`. Applications are responsible for wrapping handlers in try/except if needed.
- **No network I/O:** This library does not make network requests, read files, or execute external processes.

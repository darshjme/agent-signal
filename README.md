<div align="center">
<img src="assets/hero.svg" width="100%"/>
</div>

# agent-signal

**Event signaling and pub/sub for agent coordination**

[![PyPI version](https://img.shields.io/pypi/v/agent-signal?color=blue&style=flat-square)](https://pypi.org/project/agent-signal/) [![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-blue?style=flat-square)](https://python.org) [![License: MIT](https://img.shields.io/badge/License-MIT-green?style=flat-square)](LICENSE) [![Tests](https://img.shields.io/badge/tests-passing-brightgreen?style=flat-square)](#)

---

## The Problem

Without a signal system, agents poll for state changes — wasting tokens, adding latency, and missing events that happen between polls. Push beats pull; events beat polling.

## Installation

```bash
pip install agent-signal
```

## Quick Start

```python
from agent_signal import EventBus, SignalRegistry

# Initialise
instance = EventBus(name="my_agent")

# Use
# see API reference below
print(result)
```

## API Reference

### `EventBus`

```python
class EventBus:
    """Broadcast event bus. Topics support glob patterns (e.g. 'agent.*')."""
    def __init__(self) -> None:
    def subscribe(self, topic: str, handler: Callable) -> None:
        """Subscribe handler to topic. Topic may be a glob pattern."""
    def unsubscribe(self, topic: str, handler: Callable) -> None:
        """Unsubscribe handler from topic. Silent no-op if not found."""
    def publish(self, topic: str, data: dict | None = None) -> None:
        """Publish event to all handlers whose subscription pattern matches topic."""
```

### `SignalRegistry`

```python
class SignalRegistry:
    """Central registry of named signals. Thread-safe."""
    def __init__(self) -> None:
    def signal(self, name: str) -> Signal:
        """Return existing signal or create a new one."""
    def emit(self, name: str, *args: Any, **kwargs: Any) -> None:
        """Emit a named signal. No-op if signal not registered."""
    def list_signals(self) -> list[str]:
        """Return sorted list of registered signal names."""
```


## How It Works

### Flow

```mermaid
flowchart LR
    A[User Code] -->|create| B[EventBus]
    B -->|configure| C[SignalRegistry]
    C -->|execute| D{Success?}
    D -->|yes| E[Return Result]
    D -->|no| F[Error Handler]
    F --> G[Fallback / Retry]
    G --> C
```

### Sequence

```mermaid
sequenceDiagram
    participant App
    participant EventBus
    participant SignalRegistry

    App->>+EventBus: initialise()
    EventBus->>+SignalRegistry: configure()
    SignalRegistry-->>-EventBus: ready
    App->>+EventBus: run(context)
    EventBus->>+SignalRegistry: execute(context)
    SignalRegistry-->>-EventBus: result
    EventBus-->>-App: WorkflowResult
```

## Philosophy

> *Nāda Brahman* — the primordial sound — is the first signal; all event systems echo this original pulse.

---

*Part of the [arsenal](https://github.com/darshjme/arsenal) — production stack for LLM agents.*

*Built by [Darshankumar Joshi](https://github.com/darshjme), Gujarat, India.*

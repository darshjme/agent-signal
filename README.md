# agent-signal

**Event signaling and pub/sub for agent coordination.**

Agents need to react to events from other agents — `task.completed`, `budget.threshold`, `data.ready` — without polling or direct coupling. `agent-signal` provides a lean, zero-dependency event system for building reactive multi-agent workflows.

## Install

```bash
pip install agent-signal
```

## Quick Start — Multi-Agent Event Coordination

```python
from agent_signal import SignalRegistry, EventBus, on_signal

# ── Shared registry ────────────────────────────────────────────────────────────
registry = SignalRegistry()
bus = EventBus()

# ── Planner Agent: declares what events it cares about ────────────────────────
@on_signal(registry, "task.completed")
def planner_on_task_done(task_id: str, result: dict):
    print(f"[Planner] Task {task_id!r} finished → scheduling next step")

# ── Budget Monitor: reacts to bus events with glob pattern ────────────────────
def budget_alert(topic: str, data: dict):
    print(f"[Budget] Alert on {topic!r}: spent={data['spent']}")

bus.subscribe("budget.*", budget_alert)

# ── Worker Agent: emits when work is done ─────────────────────────────────────
class WorkerAgent:
    def run(self, task_id: str):
        # ... do work ...
        result = {"status": "ok", "output": "analysis complete"}
        registry.emit("task.completed", task_id, result)  # signal subscribers
        bus.publish("budget.usage", {"spent": 0.04, "limit": 1.0})  # bus publish

worker = WorkerAgent()
worker.run("analysis-42")
# [Planner] Task 'analysis-42' finished → scheduling next step
# [Budget] Alert on 'budget.usage': spent=0.04
```

## Components

### `Signal` — named event channel

```python
from agent_signal import Signal

sig = Signal("data.ready")
sig.connect(lambda rows: print(f"Got {rows} rows"))
sig.emit(500)               # synchronous
sig.emit_async(500)         # non-blocking (runs in threads)
print(sig.handler_count)    # 1
sig.disconnect(handler)
sig.clear()
```

### `SignalRegistry` — manages named signals

```python
from agent_signal import SignalRegistry

registry = SignalRegistry()
registry.signal("task.done").connect(my_handler)
registry.emit("task.done", "result-data")      # emits to all subscribers
registry.list_signals()                         # ['task.done']
registry.clear_all()
```

### `EventBus` — broadcast bus with glob topic filtering

```python
from agent_signal import EventBus

bus = EventBus()
bus.subscribe("agent.*", lambda topic, data: print(topic, data))
bus.publish("agent.started", {"agent_id": "worker-1"})
bus.publish("agent.stopped", {"agent_id": "worker-1"})
# Both match "agent.*"

bus.subscriber_count()           # total across all patterns
bus.subscriber_count("agent.x")  # count of patterns matching "agent.x"
bus.unsubscribe("agent.*", handler)
```

### `@on_signal` decorator

```python
from agent_signal import SignalRegistry, on_signal

registry = SignalRegistry()

@on_signal(registry, "pipeline.finished")
def notify_downstream(pipeline_id: str):
    print(f"Pipeline {pipeline_id} done — triggering downstream")

registry.emit("pipeline.finished", "pipe-7")
```

## Design

| Concern | Solution |
|---|---|
| Decoupling | Producers and consumers never import each other |
| Thread safety | All internal state protected by `threading.Lock` |
| Non-blocking emit | `emit_async()` spawns daemon threads per handler |
| Glob routing | `EventBus` uses `fnmatch` for pattern matching |
| Zero deps | Pure stdlib — no third-party packages |

## API Reference

### `Signal(name)`
| Method / Property | Description |
|---|---|
| `connect(handler)` | Subscribe callable |
| `disconnect(handler)` | Unsubscribe (no-op if not found) |
| `emit(*args, **kwargs)` | Call all handlers synchronously |
| `emit_async(*args, **kwargs)` | Call all handlers in daemon threads |
| `handler_count` | Number of connected handlers |
| `clear()` | Remove all handlers |

### `SignalRegistry()`
| Method | Description |
|---|---|
| `signal(name)` | Get or create named `Signal` |
| `emit(name, *args, **kwargs)` | Emit named signal (no-op if unregistered) |
| `list_signals()` | Sorted list of registered names |
| `clear_all()` | Remove all signals and handlers |

### `EventBus()`
| Method | Description |
|---|---|
| `subscribe(topic, handler)` | Subscribe; topic may be glob pattern |
| `unsubscribe(topic, handler)` | Unsubscribe (no-op if not found) |
| `publish(topic, data=None)` | Deliver to all matching pattern subscribers |
| `subscriber_count(topic=None)` | Count subscribers (all or matching topic) |

### `on_signal(registry, signal_name)`
Decorator. Auto-connects the decorated function to `registry.signal(signal_name)`.

## License

MIT

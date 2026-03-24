"""Tests for @on_signal decorator."""

from agent_signal import SignalRegistry, on_signal


def test_on_signal_auto_connects():
    registry = SignalRegistry()

    @on_signal(registry, "task.done")
    def handler(result):
        pass

    sig = registry.signal("task.done")
    assert sig.handler_count == 1


def test_on_signal_receives_emit():
    registry = SignalRegistry()
    results = []

    @on_signal(registry, "data.ready")
    def on_data(payload):
        results.append(payload)

    registry.emit("data.ready", {"rows": 100})
    assert results == [{"rows": 100}]


def test_on_signal_returns_original_function():
    registry = SignalRegistry()

    @on_signal(registry, "x")
    def my_func():
        return "hello"

    assert my_func() == "hello"


def test_on_signal_multiple_handlers():
    registry = SignalRegistry()
    calls = []

    @on_signal(registry, "ping")
    def handler_a():
        calls.append("a")

    @on_signal(registry, "ping")
    def handler_b():
        calls.append("b")

    registry.emit("ping")
    assert sorted(calls) == ["a", "b"]

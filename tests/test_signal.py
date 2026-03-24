"""Tests for Signal class."""

import threading
import time
import pytest

from agent_signal import Signal


# ── Basic lifecycle ────────────────────────────────────────────────────────────

def test_signal_name():
    s = Signal("task.done")
    assert s.name == "task.done"


def test_signal_repr():
    s = Signal("x")
    assert "x" in repr(s)


def test_connect_and_handler_count():
    s = Signal("s")
    assert s.handler_count == 0
    s.connect(lambda: None)
    assert s.handler_count == 1


def test_connect_same_handler_once():
    s = Signal("s")
    fn = lambda: None
    s.connect(fn)
    s.connect(fn)  # duplicate — should not double-add
    assert s.handler_count == 1


def test_connect_non_callable_raises():
    s = Signal("s")
    with pytest.raises(TypeError):
        s.connect("not_a_function")  # type: ignore


def test_disconnect_removes_handler():
    s = Signal("s")
    fn = lambda: None
    s.connect(fn)
    s.disconnect(fn)
    assert s.handler_count == 0


def test_disconnect_missing_handler_noop():
    s = Signal("s")
    s.disconnect(lambda: None)  # should not raise


def test_clear_removes_all():
    s = Signal("s")
    s.connect(lambda: None)
    s.connect(lambda: None)
    s.clear()
    assert s.handler_count == 0


# ── emit ───────────────────────────────────────────────────────────────────────

def test_emit_calls_handler():
    results = []
    s = Signal("s")
    s.connect(lambda v: results.append(v))
    s.emit(42)
    assert results == [42]


def test_emit_kwargs():
    results = {}
    s = Signal("s")
    s.connect(lambda key, val: results.update({key: val}))
    s.emit("budget", val=500)
    assert results == {"budget": 500}


def test_emit_multiple_handlers():
    calls = []
    s = Signal("s")
    s.connect(lambda: calls.append("a"))
    s.connect(lambda: calls.append("b"))
    s.emit()
    assert sorted(calls) == ["a", "b"]


def test_emit_no_handlers_noop():
    s = Signal("s")
    s.emit("anything")  # should not raise


# ── emit_async ────────────────────────────────────────────────────────────────

def test_emit_async_non_blocking():
    barrier = threading.Barrier(2)
    results = []

    def slow_handler():
        barrier.wait(timeout=2)
        results.append("done")

    s = Signal("s")
    s.connect(slow_handler)
    threads = s.emit_async()
    # main thread continues immediately
    barrier.wait(timeout=2)
    for t in threads:
        t.join(timeout=2)
    assert results == ["done"]


def test_emit_async_returns_threads():
    s = Signal("s")
    s.connect(lambda: None)
    s.connect(lambda: None)
    threads = s.emit_async()
    assert len(threads) == 2
    for t in threads:
        assert isinstance(t, threading.Thread)


def test_emit_async_passes_args():
    results = []
    event = threading.Event()

    def handler(v):
        results.append(v)
        event.set()

    s = Signal("s")
    s.connect(handler)
    s.emit_async(99)
    event.wait(timeout=2)
    assert results == [99]

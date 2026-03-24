"""Tests for SignalRegistry."""

import pytest
from agent_signal import SignalRegistry, Signal


def test_registry_creates_signal():
    r = SignalRegistry()
    s = r.signal("budget.hit")
    assert isinstance(s, Signal)
    assert s.name == "budget.hit"


def test_registry_returns_same_signal():
    r = SignalRegistry()
    s1 = r.signal("x")
    s2 = r.signal("x")
    assert s1 is s2


def test_registry_list_signals_empty():
    r = SignalRegistry()
    assert r.list_signals() == []


def test_registry_list_signals_sorted():
    r = SignalRegistry()
    r.signal("z")
    r.signal("a")
    r.signal("m")
    assert r.list_signals() == ["a", "m", "z"]


def test_registry_emit_calls_handlers():
    r = SignalRegistry()
    results = []
    r.signal("done").connect(lambda v: results.append(v))
    r.emit("done", "success")
    assert results == ["success"]


def test_registry_emit_noop_for_unknown():
    r = SignalRegistry()
    r.emit("ghost.signal")  # should not raise


def test_registry_clear_all():
    r = SignalRegistry()
    calls = []
    r.signal("a").connect(lambda: calls.append("a"))
    r.signal("b").connect(lambda: calls.append("b"))
    r.clear_all()
    assert r.list_signals() == []
    r.emit("a")  # no-op after clear
    assert calls == []


def test_registry_repr():
    r = SignalRegistry()
    r.signal("foo")
    assert "foo" in repr(r)

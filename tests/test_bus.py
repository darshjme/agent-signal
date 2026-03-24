"""Tests for EventBus."""

import pytest
from agent_signal import EventBus


def test_subscribe_and_publish():
    bus = EventBus()
    received = []
    bus.subscribe("agent.done", lambda topic, data: received.append((topic, data)))
    bus.publish("agent.done", {"result": "ok"})
    assert received == [("agent.done", {"result": "ok"})]


def test_publish_no_data_defaults_empty_dict():
    bus = EventBus()
    received = []
    bus.subscribe("x", lambda topic, data: received.append(data))
    bus.publish("x")
    assert received == [{}]


def test_glob_pattern_star():
    bus = EventBus()
    hits = []
    bus.subscribe("agent.*", lambda t, d: hits.append(t))
    bus.publish("agent.started")
    bus.publish("agent.stopped")
    bus.publish("budget.hit")  # should not match
    assert hits == ["agent.started", "agent.stopped"]


def test_glob_pattern_question_mark():
    bus = EventBus()
    hits = []
    bus.subscribe("job.?", lambda t, d: hits.append(t))
    bus.publish("job.a")
    bus.publish("job.b")
    bus.publish("job.ab")  # two chars — should not match ?
    assert hits == ["job.a", "job.b"]


def test_unsubscribe():
    bus = EventBus()
    calls = []
    handler = lambda t, d: calls.append(t)
    bus.subscribe("x", handler)
    bus.unsubscribe("x", handler)
    bus.publish("x")
    assert calls == []


def test_unsubscribe_missing_noop():
    bus = EventBus()
    bus.unsubscribe("ghost", lambda t, d: None)  # should not raise


def test_subscriber_count_total():
    bus = EventBus()
    bus.subscribe("a", lambda t, d: None)
    bus.subscribe("b", lambda t, d: None)
    bus.subscribe("b", lambda t, d: None)
    assert bus.subscriber_count() == 3


def test_subscriber_count_for_topic():
    bus = EventBus()
    bus.subscribe("agent.*", lambda t, d: None)
    bus.subscribe("agent.*", lambda t, d: None)
    bus.subscribe("budget.*", lambda t, d: None)
    assert bus.subscriber_count("agent.done") == 2
    assert bus.subscriber_count("budget.hit") == 1
    assert bus.subscriber_count("other") == 0


def test_same_handler_not_duplicated():
    bus = EventBus()
    calls = []
    fn = lambda t, d: calls.append(t)
    bus.subscribe("x", fn)
    bus.subscribe("x", fn)
    bus.publish("x")
    assert len(calls) == 1


def test_non_callable_raises():
    bus = EventBus()
    with pytest.raises(TypeError):
        bus.subscribe("x", "not_callable")  # type: ignore


def test_repr():
    bus = EventBus()
    bus.subscribe("agent.*", lambda t, d: None)
    assert "agent.*" in repr(bus)

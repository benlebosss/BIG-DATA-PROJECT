"""Unit tests for the Wikipedia -> Kafka producer (no network, no Kafka)."""
import json

from src.streaming.wikipedia_producer import iter_sse, parse_event


def make(**over):
    base = {"type": "edit", "wiki": "enwiki", "namespace": 0, "title": "Inception (film)",
            "user": "Alice", "bot": False, "comment": "fix", "timestamp": 1760000000,
            "server_name": "en.wikipedia.org", "notify_url": "https://en.wikipedia.org/w/index.php?diff=1",
            "meta": {"id": "abc", "dt": "2026-10-23T16:00:00Z"}}
    base.update(over)
    return json.dumps(base)


def test_parse_edit():
    msg = parse_event(make(), {"enwiki"}, {0})
    assert msg["title"] == "Inception (film)" and msg["event_id"] == "abc"
    assert msg["event_time"] == "2026-10-23T16:00:00Z" and msg["bot"] is False


def test_filters():
    assert parse_event(make(type="categorize")) is None
    assert parse_event(make(wiki="frwiki"), {"enwiki"}) is None
    assert parse_event(make(namespace=14), None, {0}) is None
    assert parse_event(make(title="")) is None
    assert parse_event("not json") is None
    assert parse_event(make(wiki="frwiki"), None, None)["wiki"] == "frwiki"


def test_iter_sse():
    lines = [":ok", "event: message", "id: 42", 'data: {"a": 1}', "", "data: {}"]
    assert list(iter_sse(lines)) == [("42", '{"a": 1}'), ("42", "{}")]

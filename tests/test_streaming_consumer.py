import json

import pytest
from pyspark.sql import functions as F

from src.streaming.consumer import match_entities, parse_changes, window_counts
from src.streaming.reference import norm_key


@pytest.fixture(scope="module")
def spark():
    from src.common.spark_session import get_spark
    s = get_spark("test-streaming")
    yield s
    s.stop()


def lines_df(spark, tmp_path, lines):
    p = tmp_path / "in.txt"
    p.write_text("\n".join(lines) + "\n")
    return spark.read.text(str(p))


def event(title, ts):
    return json.dumps({"event_id": f"e{ts}{title}", "wiki": "enwiki", "title": title, "type": "edit",
                       "namespace": 0, "user": "u", "bot": False, "timestamp": ts})


def test_parse_changes(spark, tmp_path):
    rows = parse_changes(lines_df(spark, tmp_path, [event("Alien (film)", 1700000000), "not json"])).collect()
    assert len(rows) == 1 and rows[0].title == "Alien (film)"
    assert rows[0].event_time is not None


def test_norm_key(spark, tmp_path):
    df = lines_df(spark, tmp_path, ["Alien (1979 film)", "  Tom Hanks "])
    assert [r.k for r in df.select(norm_key(F.col("value")).alias("k")).collect()] == ["alien", "tom hanks"]


def test_match_and_windows(spark, tmp_path):
    ref_file = tmp_path / "ref.json"
    ref_file.write_text("\n".join(json.dumps(r) for r in [
        {"key": "alien", "kind": "title", "imdb_id": "tt0078748", "imdb_name": "Alien", "votes": 900000},
        {"key": "tom hanks", "kind": "person", "imdb_id": "nm0000158", "imdb_name": "Tom Hanks", "votes": 900000},
    ]))
    ref = spark.read.json(str(ref_file))
    t0 = 1700000000
    raw = lines_df(spark, tmp_path, [event("Alien (film)", t0), event("Tom Hanks", t0 + 240),
                                     event("Random page", t0 + 10), event("Alien", t0 + 2400)])
    m = match_entities(parse_changes(raw), ref)
    assert m.count() == 3
    w = window_counts(m, "30 minutes", "5 minutes", "10 minutes", min_matches=2).collect()
    assert max(r.matches for r in w) == 2
    assert any(r.flagged for r in w) and any(not r.flagged for r in w)


def ref_df(spark, tmp_path):
    p = tmp_path / "ref.json"
    p.write_text(json.dumps({"key": "alien", "kind": "title", "imdb_id": "tt1", "imdb_name": "Alien", "votes": 1}))
    return spark.read.json(str(p))


def test_parse_changes_drops_missing_timestamp(spark, tmp_path):
    line = json.dumps({"event_id": "e", "wiki": "enwiki", "title": "Alien", "type": "edit"})
    assert parse_changes(lines_df(spark, tmp_path, [line])).count() == 0


def test_match_is_case_insensitive(spark, tmp_path):
    raw = lines_df(spark, tmp_path, [event("ALIEN (film)", 1700000000)])
    assert match_entities(parse_changes(raw), ref_df(spark, tmp_path)).count() == 1

from src.enrichment.wikipedia import RateLimiter, candidates, enrich_row, is_relevant, run

FILM = {"type": "standard", "title": "Alien (film)", "description": "1979 science fiction horror film",
        "extract": "Alien is a 1979 film.", "revision": "1", "timestamp": "2026-01-01T00:00:00Z",
        "content_urls": {"desktop": {"page": "https://en.wikipedia.org/wiki/Alien_(film)"}}}


def test_candidates_and_relevance():
    assert candidates("title", "Alien", "1979")[0] == "Alien_(1979_film)"
    assert is_relevant("title", FILM)
    assert not is_relevant("title", {**FILM, "type": "disambiguation"})
    assert not is_relevant("person", {"type": "standard", "description": "A river", "extract": "Water."})


def test_enrich_row_lineage_and_not_found():
    row = {"imdb_id": "tt0078748", "kind": "title", "imdb_name": "Alien", "year": "1979"}
    rec = enrich_row(row, lambda t: FILM if t == "Alien_(film)" else None)
    assert rec["status"] == "ok" and rec["source_url"].endswith("Alien_(film)") and rec["revision"] == "1"
    assert enrich_row(row, lambda t: None)["status"] == "not_found"


def test_run_is_resumable(tmp_path):
    rows = [{"imdb_id": f"tt{i}", "kind": "title", "imdb_name": "Alien", "year": None} for i in range(3)]
    calls = []
    fetch = lambda t: calls.append(t) or FILM
    cache = str(tmp_path / "c.jsonl")
    run(rows[:2], cache, fetch)
    n = len(calls)
    out = run(rows, cache, fetch)
    assert len(calls) == n + 1 and [r["imdb_id"] for r in out] == ["tt0", "tt1", "tt2"]


def test_rate_limiter():
    t, slept = [0.0], []
    rl = RateLimiter(10, clock=lambda: t[0], sleep=lambda s: (slept.append(s), t.__setitem__(0, t[0] + s)))
    rl.wait(); rl.wait()
    assert abs(slept[0] - 0.1) < 1e-9


def test_person_candidates_order():
    assert candidates("person", "Tom Hanks")[0] == "Tom_Hanks"


def test_person_relevance():
    page = {"type": "standard", "description": "American actor and filmmaker", "extract": "Tom Hanks is an actor."}
    assert is_relevant("person", page)


def test_to_record_without_content_urls():
    from src.enrichment.wikipedia import to_record
    rec = to_record({"imdb_id": "x", "kind": "title", "imdb_name": "X"}, {"title": "X", "extract": "e"})
    assert rec["source_url"] is None and rec["status"] == "ok"

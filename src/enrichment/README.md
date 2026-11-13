# Enrichment (step 4)

`python -m src.enrichment.wikipedia --titles 200 --people 200`

Takes the 200 most voted movies/series and the 200 actors/directors appearing most in them,
looks each one up on Wikipedia (REST `page/summary`) and writes `results/enrichment/wikipedia_enrichment.csv`.

- Lineage: `source_url`, page `revision`, `wiki_timestamp`, `fetched_at` kept on every row.
- Rate limit: 5 requests/s (`--per-second`), descriptive User-Agent, retry with `Retry-After`/backoff on 429/5xx.
- Matching: candidate page names (`X_(1979_film)`, `X_(film)`, ...) tried in order; a page is kept only if it
  is a normal page (not a disambiguation page) whose description looks like a film/series or a film person.
- Resumable: every answer is appended to `data/enrichment/wikipedia.jsonl` (git-ignored).
- Result of the committed run: 397 / 400 found, 3 people `not_found`.

## Output columns

imdb_id, kind (title or person), imdb_name, status (ok or not_found), wikipedia_title, description, extract, source_url, revision, wiki_timestamp, fetched_at.

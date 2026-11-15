from src.common.imdb_schemas import SCHEMAS
from src.common.spark_session import get_spark
from src.open_question import duos


def test_duo_lift():
    spark = get_spark("tests-open-question")
    # d1 + a1 make 3 films together rated 8, each also has 2 films alone rated 6
    basics = [(f"tt{i}", "movie", f"T{i}", f"T{i}", False, 2000 + i, None, 100, "Drama") for i in range(7)]
    ratings = [(f"tt{i}", 8.0 if i < 3 else 6.0, 5000) for i in range(7)]
    crew = [(f"tt{i}", "d1" if i < 5 else "d2", None) for i in range(7)]
    principals = [(f"tt{i}", 1, "a1", "actor", None, None) for i in (0, 1, 2, 5, 6)]
    df = lambda t, rows: spark.createDataFrame(rows, SCHEMAS[t])  # noqa: E731
    films, directed, acted = duos.credits(df("title.basics", basics), df("title.ratings", ratings),
                                          df("title.crew", crew), df("title.principals", principals), 1000)
    out = duos.duo_stats(films, directed, acted, 3).collect()
    assert len(out) == 1
    r = out[0]
    assert (r.director, r.actor, r.n_films) == ("d1", "a1", 3)
    assert r.baseline == 6.0 and r.lift == 2.0

"""Unit tests of the exploration questions on tiny hand-made tables (run with `pytest -q`)."""
import pytest

from src.common.imdb_schemas import SCHEMAS
from src.common.spark_session import get_spark
from src.exploration import (
    q1_runtime_outliers,
    q2_top_genres,
    q4_one_hit_directors,
    q5_series_decline,
    q6_multilingual_actors,
    q7_early_peak_actors,
    q8_multi_talented,
)


@pytest.fixture(scope="module")
def spark():
    return get_spark("tests-exploration")


def df(spark, table, rows):
    return spark.createDataFrame(rows, SCHEMAS[table])


def movie(tconst, year, runtime, genres="Drama", ttype="movie", title=None):
    return (tconst, ttype, title or tconst, title or tconst, False, year, None, runtime, genres)


def test_q1_flags_only_extreme_runtime(spark):
    rows = [movie(f"tt{i}", 2000, 90 + (i % 5)) for i in range(40)] + [movie("ttlong", 2000, 400)]
    rows.append(movie("ttshort", 2000, 30))  # not feature length: ignored
    out = q1_runtime_outliers.runtime_outliers(df(spark, "title.basics", rows), z=3).collect()
    assert [r.tconst for r in out] == ["ttlong"] and out[0].direction == "longer"
    assert out[0].z_outlier and out[0].iqr_outlier


def test_q2_ranks_genres_by_votes(spark):
    basics = df(spark, "title.basics", [movie("tt1", 1990, 100, "Drama,Comedy"),
                                        movie("tt2", 1990, 100, "Horror"),
                                        movie("tt3", 1990, 100, "Action")])
    ratings = df(spark, "title.ratings", [("tt1", 7.0, 100), ("tt2", 5.0, 50), ("tt3", 6.0, 10)])
    pop = q2_top_genres.genre_year_popularity(basics, ratings)
    top = q2_top_genres.top_genres(pop).collect()
    assert [r.genre for r in top] == ["Comedy", "Drama", "Horror"]
    rest = {r.group: r for r in q2_top_genres.top_vs_rest(pop).collect()}
    assert rest["rest"].total_votes == 10 and rest["top3"].total_votes == 250


def test_q4_one_hit_director(spark):
    basics = df(spark, "title.basics", [movie(f"tt{i}", 2000 + i, 100) for i in range(5)])
    crew = df(spark, "title.crew", [("tt0", "nm1", None), ("tt1", "nm1", None), ("tt2", "nm1", None),
                                    ("tt3", "nm2", None), ("tt4", "nm2", None)])
    ratings = df(spark, "title.ratings", [("tt0", 8.5, 500), ("tt1", 5.0, 500), ("tt2", 6.0, 500),
                                          ("tt3", 8.1, 500), ("tt4", 4.0, 500)])
    names = df(spark, "name.basics", [("nm1", "One Hit", None, None, None, None)])
    out = q4_one_hit_directors.one_hit_directors(basics, crew, ratings, names).collect()
    assert [(r.nconst, r.hit_title, r.n_others) for r in out] == [("nm1", "tt0", 2)]


def test_q5_series_with_late_worst_episode(spark):
    basics = df(spark, "title.basics", [movie("ttS", 2000, None, ttype="tvSeries")])
    eps, ratings = [], []
    for season in (1, 2, 3):
        for n in range(1, 11):
            tconst = f"tt{season}_{n}"
            eps.append((tconst, "ttS", season, n))
            ratings.append((tconst, 7.0, 100))
    ratings[0] = ("tt1_1", 9.5, 100)   # best: season 1
    ratings[-1] = ("tt3_10", 2.0, 100)  # worst: last season
    out = q5_series_decline.series_decline(basics, df(spark, "title.episode", eps),
                                           df(spark, "title.ratings", ratings)).collect()
    assert len(out) == 1 and out[0].best_episode == "tt1_1" and out[0].worst_episode == "tt3_10"


def test_q6_infers_language_from_original_title(spark):
    basics = df(spark, "title.basics", [movie("tt1", 2001, 120, title="Amelie"),
                                        movie("tt2", 2002, 120, title="Heat")])
    akas = df(spark, "title.akas", [("tt1", 1, "Amelie", "FR", "fr", None, None, None),
                                    ("tt2", 1, "Heat", "US", "en", None, None, None),
                                    ("tt2", 2, "Hitze", "DE", "de", None, None, None)])
    principals = df(spark, "title.principals", [("tt1", 1, "nm1", "actress", None, None),
                                                ("tt2", 1, "nm1", "actress", None, None)])
    ratings = df(spark, "title.ratings", [("tt1", 8.0, 20000), ("tt2", 8.0, 20000)])
    names = df(spark, "name.basics", [("nm1", "Polyglot", None, None, None, None)])
    out = q6_multilingual_actors.multilingual_actors(basics, akas, principals, ratings, names).collect()
    assert [(r.nconst, r.languages) for r in out] == [("nm1", "en,fr")]


def test_q6_wikidata_language_resolution(spark):
    movies = df(spark, "title.basics", [movie(f"tt{i}", 2000, 100, title=f"T{i}") for i in range(4)])
    akas = df(spark, "title.akas", [("tt1", 1, "T1", "DE", "de", None, None, None),
                                    ("tt2", 1, "T2", "US", "en", None, None, None),
                                    ("tt3", 1, "T3", "FR", "fr", None, None, None)])
    wd_schema = "tconst string, language_code string"
    wikidata = spark.createDataFrame([("tt0", "zh"), ("tt0", "cmn"),       # same language twice
                                      ("tt1", "de"), ("tt1", "fr"),        # settled by IMDb in "imdb" mode
                                      ("tt2", "es"), ("tt2", "it")], wd_schema)  # multilingual
    def resolve(mode):
        rows = q6_multilingual_actors.original_language(movies, akas, wikidata, mode).collect()
        return {r.tconst: (r.original_language, r.language_source) for r in rows}
    assert resolve("exclude") == {"tt0": ("cmn", "wikidata"), "tt1": (None, "multilingual"),
                                  "tt2": (None, "multilingual"), "tt3": ("fr", "imdb_akas")}
    assert resolve("imdb")["tt1"] == ("de", "wikidata+imdb_akas")


def test_q7_early_peak(spark):
    basics = df(spark, "title.basics", [movie(f"tt{i}", 1980 + 2 * i, 100) for i in range(15)])
    principals = df(spark, "title.principals", [(f"tt{i}", 1, "nm1", "actor", None, None) for i in range(15)])
    ratings = df(spark, "title.ratings", [(f"tt{i}", 9.0 - 0.3 * i, 1000) for i in range(15)])
    names = df(spark, "name.basics", [("nm1", "Early Star", None, None, None, None)])
    out = q7_early_peak_actors.early_peak_actors(basics, principals, ratings, names).collect()
    assert len(out) == 1 and out[0].best_year == 1980 and out[0].span_years == 28


def test_q8_multi_role_movies(spark):
    basics = df(spark, "title.basics", [movie(f"tt{i}", 2000 + i, 100) for i in range(6)])
    crew = df(spark, "title.crew", [(f"tt{i}", "nm1", None) for i in range(3)]
              + [(f"tt{i}", None, None) for i in range(3, 6)])
    principals = df(spark, "title.principals", [(f"tt{i}", 1, "nm1", "actor", None, None)
                                                for i in (0, 3, 4, 5)])
    ratings = df(spark, "title.ratings", [(f"tt{i}", 8.0 if i == 0 else 6.0, 1000) for i in range(6)])
    roles = q8_multi_talented.movie_roles(basics, crew, principals, ratings, 100)
    talented = q8_multi_talented.multi_talented(roles, 3)
    names = df(spark, "name.basics", [("nm1", "Auteur", None, None, None, None)])
    r = q8_multi_talented.performance(roles, talented, names).first()
    assert r.talents == "act+direct" and r.n_multi_role_movies == 1 and r.rating_gain == 2.0

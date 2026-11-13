import json

import pytest

from src.open_question.duos_by_period import duo_effects, film_table, summarize


@pytest.fixture(scope="module")
def spark():
    from src.common.spark_session import get_spark
    s = get_spark("test-open-question")
    yield s
    s.stop()


def load(spark, tmp_path, name, rows, ddl):
    p = tmp_path / f"{name}.json"
    p.write_text("\n".join(json.dumps(r) for r in rows))
    return spark.read.schema(ddl).json(str(p))


@pytest.fixture
def data(spark, tmp_path):
    films = {"t1": (1995, "Drama", 8.0), "t2": (1996, "Drama,Comedy", 8.0),
             "t3": (1997, "Drama", 6.0), "t4": (1998, "Comedy", 6.0)}
    basics = load(spark, tmp_path, "b", [{"tconst": t, "titleType": "movie", "startYear": y, "genres": g}
                                         for t, (y, g, _) in films.items()],
                  "tconst string, titleType string, startYear int, genres string")
    ratings = load(spark, tmp_path, "r", [{"tconst": t, "averageRating": r, "numVotes": 5000}
                                          for t, (_, _, r) in films.items()],
                   "tconst string, averageRating double, numVotes int")
    cast = [("t1", "D1", "director"), ("t1", "A1", "actor"), ("t2", "D1", "director"), ("t2", "A1", "actress"),
            ("t3", "D1", "director"), ("t3", "X", "actor"), ("t4", "Y", "director"), ("t4", "A1", "actor")]
    principals = load(spark, tmp_path, "p", [{"tconst": t, "nconst": n, "category": c} for t, n, c in cast],
                      "tconst string, nconst string, category string")
    return film_table(basics, ratings, 1000), principals


def test_duo_effect_by_decade(data):
    films, principals = data
    rows = duo_effects(films, principals, "decade", min_joint=2, min_separate=2).collect()
    assert len(rows) == 1
    r = rows[0]
    assert (r.director, r.actor, r.grp, r.j_cnt, r.sep_cnt) == ("D1", "A1", "1990", 2, 2)
    assert r.joint_avg == 8.0 and r.sep_avg == 6.0 and r.effect == 2.0


def test_genre_split_and_thresholds(data):
    films, principals = data
    by_genre = duo_effects(films, principals, "genre", min_joint=1, min_separate=1).collect()
    assert {r.grp for r in by_genre} == {"Drama", "Comedy"}
    assert duo_effects(films, principals, "decade", min_joint=3, min_separate=1).count() == 0
    s = summarize(duo_effects(films, principals, "decade", 2, 2)).collect()
    assert s[0].duos == 1 and s[0].share_positive == 1.0


def one_film(spark, tmp_path, title_type="movie", year=1999, votes=5000):
    basics = load(spark, tmp_path, "b1", [{"tconst": "t1", "titleType": title_type, "startYear": year, "genres": "Drama"}],
                  "tconst string, titleType string, startYear int, genres string")
    ratings = load(spark, tmp_path, "r1", [{"tconst": "t1", "averageRating": 7.0, "numVotes": votes}],
                   "tconst string, averageRating double, numVotes int")
    return basics, ratings


def test_film_table_drops_low_vote_films(spark, tmp_path):
    assert film_table(*one_film(spark, tmp_path, votes=10), 1000).count() == 0


def test_film_table_keeps_only_movies(spark, tmp_path):
    assert film_table(*one_film(spark, tmp_path, title_type="tvSeries"), 1000).count() == 0


def test_decade_of_1999_is_1990(spark, tmp_path):
    assert film_table(*one_film(spark, tmp_path, year=1999), 1000).collect()[0].decade == 1990


def test_decade_of_2000_is_2000(spark, tmp_path):
    assert film_table(*one_film(spark, tmp_path, year=2000), 1000).collect()[0].decade == 2000


def test_min_separate_threshold_filters_duos(data):
    films, principals = data
    assert duo_effects(films, principals, "decade", min_joint=2, min_separate=3).count() == 0

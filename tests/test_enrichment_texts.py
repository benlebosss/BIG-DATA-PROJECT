from src.common.spark_session import get_spark
from src.enrichment.build import clean_text
from src.enrichment.wiki_texts import plot_section


def test_plot_section():
    text = "Intro text.\n\n== Plot ==\nA thief steals dreams.\n\n== Cast ==\nLeo"
    assert plot_section(text) == "A thief steals dreams."
    assert plot_section("Intro only") is None


def test_clean_text():
    spark = get_spark("tests-enrichment")
    df = spark.createDataFrame([("  A  thief\nsteals[12] dreams ",), ("   ",)], ["t"])
    assert [r.c for r in df.select(clean_text("t").alias("c")).collect()] == ["A thief steals dreams", None]


def test_film_people_fills_with_other_principals():
    from src.enrichment.select_films import film_people
    spark = get_spark("tests-enrichment")
    films = spark.createDataFrame([("tt1",), ("tt2",)], ["tconst"])
    principals = spark.createDataFrame([
        ("tt1", 1, "nm1", "director"), ("tt1", 2, "nm2", "writer"), ("tt1", 3, "nm3", "actor"),
        ("tt1", 4, "nm3", "actor"),  # same voice actor, second character
        ("tt1", 5, "nm4", "actress"), ("tt1", 6, "nm5", "actor"),
        ("tt2", 1, "nm6", "self"), ("tt2", 2, "nm7", "director"), ("tt2", 3, "nm8", "self"),
    ], ["tconst", "ordering", "nconst", "category"])
    got = {(r.tconst, r.nconst) for r in film_people(films, principals, 3).collect()}
    assert got == {("tt1", "nm1"), ("tt1", "nm3"), ("tt1", "nm4"),
                   ("tt2", "nm7"), ("tt2", "nm6"), ("tt2", "nm8")}

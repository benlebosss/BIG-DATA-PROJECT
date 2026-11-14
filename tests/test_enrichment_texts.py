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

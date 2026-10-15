"""Unit tests on tiny synthetic IMDb files (run with `pytest -q`)."""
import gzip

import pytest

from src.common.spark_session import get_spark
from src.preparation import clean, profile_quality

FILES = {
    "title.basics": "tconst\ttitleType\tprimaryTitle\toriginalTitle\tisAdult\tstartYear\tendYear\truntimeMinutes\tgenres\n"
                    "tt1\tmovie\tA\tA\t0\t2000\t\\N\t90\tDrama\n"
                    "tt2\tmovie\tB\tB\t0\t2001\t2000\t-5\t\\N\n",
    "name.basics": "nconst\tprimaryName\tbirthYear\tdeathYear\tprimaryProfession\tknownForTitles\n"
                   "nm1\tX\t1970\t\\N\tactor\ttt1,tt9\n",
    "title.akas": "titleId\tordering\ttitle\tregion\tlanguage\ttypes\tattributes\tisOriginalTitle\n"
                  "tt1\t1\tA\tFR\tfr\t\\N\t\\N\t0\ntt9\t1\tZ\tFR\tfr\t\\N\t\\N\t0\n",
    "title.crew": "tconst\tdirectors\twriters\ntt1\tnm1\t\\N\n",
    "title.episode": "tconst\tparentTconst\tseasonNumber\tepisodeNumber\ntt2\ttt1\t1\t1\n",
    "title.principals": "tconst\tordering\tnconst\tcategory\tjob\tcharacters\n"
                        "tt1\t1\tnm1\tactor\t\\N\t\\N\ntt1\t2\tnm404\tactor\t\\N\t\\N\n",
    "title.ratings": "tconst\taverageRating\tnumVotes\ntt1\t7.5\t10\ntt9\t8.0\t5\n",
}


@pytest.fixture(scope="module")
def data_dir(tmp_path_factory):
    d = tmp_path_factory.mktemp("imdb")
    for name, content in FILES.items():
        with gzip.open(d / f"{name}.tsv.gz", "wt") as f:
            f.write(content)
    return str(d)


@pytest.fixture(scope="module")
def spark():
    return get_spark("tests")


def test_profile_counts_nulls(spark, data_dir):
    from src.common.imdb_schemas import read_table
    pdf = profile_quality.profile_columns(read_table(spark, "title.basics", data_dir), "title.basics")
    row = pdf[pdf["column"] == "endYear"].iloc[0]
    assert row["rows"] == 2 and row["null_count"] == 1 and row["null_pct"] == 50.0


def test_orphans_detected(spark, data_dir):
    from src.common.imdb_schemas import read_table
    t = {n: read_table(spark, n, data_dir) for n in FILES}
    issues = {(a, b): c for a, b, c, _ in profile_quality.quality_issues(t)}
    assert issues[("title.principals", "nconst missing in name.basics")] == 1
    assert issues[("title.ratings", "tconst missing in title.basics")] == 1
    assert issues[("title.basics", "endYear < startYear")] == 1


def test_clean_pipeline(spark, data_dir, tmp_path):
    clean.main(data_dir, str(tmp_path), spark=spark)
    assert spark.read.parquet(str(tmp_path / "title_ratings")).count() == 1
    assert spark.read.parquet(str(tmp_path / "title_principals")).count() == 1
    b = spark.read.parquet(str(tmp_path / "title_basics")).where("tconst='tt2'").first()
    assert b.runtimeMinutes is None and b.endYear is None

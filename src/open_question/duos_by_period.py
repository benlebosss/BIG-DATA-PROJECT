import argparse
from pathlib import Path

from pyspark.sql import DataFrame
from pyspark.sql import functions as F


def film_table(basics: DataFrame, ratings: DataFrame, min_votes: int = 1000) -> DataFrame:
    return (basics.filter((F.col("titleType") == "movie") & F.col("startYear").isNotNull())
            .join(ratings.filter(F.col("numVotes") >= min_votes), "tconst")
            .select("tconst", (F.floor(F.col("startYear") / 10) * 10).cast("int").alias("decade"),
                    "genres", F.col("averageRating").alias("rating")))


def with_group(films: DataFrame, by: str) -> DataFrame:
    if by == "decade":
        return films.withColumn("grp", F.col("decade").cast("string"))
    return films.withColumn("grp", F.explode(F.split("genres", ",")))


def duo_effects(films: DataFrame, principals: DataFrame, by: str = "decade",
                min_joint: int = 2, min_separate: int = 2) -> DataFrame:
    f = with_group(films, by).select("tconst", "grp", "rating")
    dirs = (principals.filter(F.col("category") == "director")
            .select("tconst", F.col("nconst").alias("director")).distinct())
    acts = (principals.filter(F.col("category").isin("actor", "actress"))
            .select("tconst", F.col("nconst").alias("actor")).distinct())
    d_all = (dirs.join(f, "tconst").groupBy("director", "grp")
             .agg(F.sum("rating").alias("d_sum"), F.count(F.lit(1)).alias("d_cnt")))
    a_all = (acts.join(f, "tconst").groupBy("actor", "grp")
             .agg(F.sum("rating").alias("a_sum"), F.count(F.lit(1)).alias("a_cnt")))
    joint = (dirs.join(acts, "tconst").join(f, "tconst").groupBy("director", "actor", "grp")
             .agg(F.sum("rating").alias("j_sum"), F.count(F.lit(1)).alias("j_cnt"))
             .filter(F.col("j_cnt") >= min_joint))
    return (joint.join(d_all, ["director", "grp"]).join(a_all, ["actor", "grp"])
            .withColumn("sep_cnt", (F.col("d_cnt") - F.col("j_cnt")) + (F.col("a_cnt") - F.col("j_cnt")))
            .withColumn("sep_sum", (F.col("d_sum") - F.col("j_sum")) + (F.col("a_sum") - F.col("j_sum")))
            .filter(F.col("sep_cnt") >= min_separate)
            .withColumn("joint_avg", F.col("j_sum") / F.col("j_cnt"))
            .withColumn("sep_avg", F.col("sep_sum") / F.col("sep_cnt"))
            .withColumn("effect", F.col("joint_avg") - F.col("sep_avg")))


def summarize(effects: DataFrame) -> DataFrame:
    return (effects.groupBy("grp")
            .agg(F.count(F.lit(1)).alias("duos"),
                 F.round(F.avg("effect"), 3).alias("mean_effect"),
                 F.round(F.expr("percentile_approx(effect, 0.5)"), 3).alias("median_effect"),
                 F.round(F.avg((F.col("effect") > 0).cast("double")), 3).alias("share_positive"),
                 F.round(F.avg("j_cnt"), 2).alias("avg_joint_films")))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--min-joint", type=int, default=2)
    ap.add_argument("--min-separate", type=int, default=2)
    ap.add_argument("--min-votes", type=int, default=1000)
    ap.add_argument("--out", default="results/open_question")
    a = ap.parse_args()
    from src.common.imdb_schemas import read_table
    from src.common.spark_session import get_spark
    spark = get_spark("open-question-periods")
    films = film_table(read_table(spark, "title.basics"), read_table(spark, "title.ratings"), a.min_votes)
    principals = read_table(spark, "title.principals").select("tconst", "nconst", "category")
    Path(a.out).mkdir(parents=True, exist_ok=True)
    for by in ("decade", "genre"):
        table = summarize(duo_effects(films, principals, by, a.min_joint, a.min_separate)).toPandas()
        table = table.sort_values("grp" if by == "decade" else "duos", ascending=(by == "decade"))
        table.rename(columns={"grp": by}).to_csv(f"{a.out}/duo_effect_by_{by}.csv", index=False)
        print(table.to_string(index=False))


if __name__ == "__main__":
    main()

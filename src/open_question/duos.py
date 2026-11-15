"""Open question: do director-actor duos who work together often make better films
than each of them does without the other?

A duo = one director and one actor/actress credited together on at least --min-films
feature films (each film with at least --min-votes votes). For each duo we compare the
average rating of their films together with the average of the director's other films
and of the actor's other films.

Usage: python -m src.open_question.duos [--min-films 3 --min-votes 1000]
"""
import argparse

from pyspark.sql import DataFrame
from pyspark.sql import functions as F

from src.common.spark_session import get_spark
from src.exploration.common import feature_movies, load, rated, save, split_list

OUT = "results/open_question"


def credits(basics, ratings, crew, principals, min_votes):
    films = rated(feature_movies(basics), ratings, min_votes).select(
        "tconst", "startYear", "genres", "averageRating", "numVotes")
    directors = crew.select("tconst", F.explode(split_list("directors")).alias("director"))
    actors = principals.where(F.col("category").isin("actor", "actress")) \
        .select("tconst", F.col("nconst").alias("actor")).distinct()
    return films, films.join(directors, "tconst"), films.join(actors, "tconst")


def duo_stats(films, directed, acted, min_films=3):
    together = directed.join(acted.select("tconst", "actor"), "tconst") \
        .where(F.col("director") != F.col("actor"))  # people directing themselves are not a duo
    duos = together.groupBy("director", "actor").agg(
        F.count("*").alias("n_films"),
        F.avg("averageRating").alias("duo_avg"),
        F.min("startYear").alias("first_year"),
        F.max("startYear").alias("last_year"),
    ).where(F.col("n_films") >= min_films)

    # all films of each director / actor, the duo films are taken out below
    d_all = directed.groupBy("director").agg(F.count("*").alias("d_n"), F.sum("averageRating").alias("d_sum"))
    a_all = acted.groupBy("actor").agg(F.count("*").alias("a_n"), F.sum("averageRating").alias("a_sum"))
    duo_sum = F.col("duo_avg") * F.col("n_films")
    return (duos.join(d_all, "director").join(a_all, "actor")
            .withColumn("d_other_n", F.col("d_n") - F.col("n_films"))
            .withColumn("a_other_n", F.col("a_n") - F.col("n_films"))
            .withColumn("director_other_avg", (F.col("d_sum") - duo_sum) / F.col("d_other_n"))
            .withColumn("actor_other_avg", (F.col("a_sum") - duo_sum) / F.col("a_other_n"))
            # keep duos where both have a career outside the duo, otherwise there is nothing to compare
            .where((F.col("d_other_n") >= 2) & (F.col("a_other_n") >= 2))
            .withColumn("baseline", (F.col("director_other_avg") + F.col("actor_other_avg")) / 2)
            .withColumn("lift", F.col("duo_avg") - F.col("baseline"))
            .drop("d_n", "d_sum", "a_n", "a_sum"))


def by_size(duos: DataFrame) -> DataFrame:
    size = F.when(F.col("n_films") >= 6, "6+").when(F.col("n_films") >= 4, "4-5").otherwise("3")
    return duos.groupBy(size.alias("films_together")).agg(
        F.count("*").alias("n_duos"),
        F.round(F.avg("duo_avg"), 2).alias("avg_duo_rating"),
        F.round(F.avg("baseline"), 2).alias("avg_baseline"),
        F.round(F.avg("lift"), 3).alias("avg_lift"),
        F.round(F.expr("percentile_approx(lift, 0.5)"), 3).alias("median_lift"),
        F.round(100 * F.avg((F.col("lift") > 0).cast("int")), 1).alias("pct_duos_better"),
    ).orderBy("films_together")


def main(min_films=3, min_votes=1000):
    spark = get_spark("open-question-duos")
    films, directed, acted = credits(load(spark, "title.basics"), load(spark, "title.ratings"),
                                     load(spark, "title.crew"), load(spark, "title.principals"), min_votes)
    duos = duo_stats(films, directed, acted, min_films).cache()
    names = load(spark, "name.basics").select("nconst", "primaryName")
    named = (duos.join(names.withColumnRenamed("nconst", "director")
                       .withColumnRenamed("primaryName", "director_name"), "director", "left")
             .join(names.withColumnRenamed("nconst", "actor")
                   .withColumnRenamed("primaryName", "actor_name"), "actor", "left")
             .select("director_name", "actor_name", "n_films", "first_year", "last_year",
                     *[F.round(c, 2).alias(c) for c in
                       ("duo_avg", "director_other_avg", "actor_other_avg", "baseline", "lift")]))
    save(by_size(duos), "duo_lift_by_size", OUT)
    save(named.orderBy(F.desc("n_films"), F.desc("lift")), "duos", OUT)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--min-films", type=int, default=3)
    ap.add_argument("--min-votes", type=int, default=1000)
    a = ap.parse_args()
    main(a.min_films, a.min_votes)

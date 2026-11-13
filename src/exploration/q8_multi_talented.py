"""Q8: multi-talented film professionals and how they perform when they cumulate roles.

Roles considered: ``act`` (principals actor/actress/self), ``direct`` and ``write``
(``title.crew`` lists, plus the director/writer principals). A person is multi-talented
when they held at least two of these roles, each on at least ``min_per_role`` feature movies.

For each of them, their movies are split in two groups: movies where they held one role
only, and movies where they held several roles on the same project (e.g. directed and acted).
The comparison of the average ratings of both groups answers the second part of the question.

Usage: python -m src.exploration.q8_multi_talented [--min-votes 100 --min-per-role 3]
"""
import argparse

from pyspark.sql import DataFrame
from pyspark.sql import functions as F

from src.common.spark_session import get_spark
from src.exploration.common import feature_movies, load, rated, save, split_list

ROLE_OF_CATEGORY = {"actor": "act", "actress": "act", "self": "act",
                    "director": "direct", "writer": "write"}


def movie_roles(basics: DataFrame, crew: DataFrame, principals: DataFrame,
                ratings: DataFrame, min_votes: int) -> DataFrame:
    """One row per (person, movie) with the set of roles held on that movie."""
    movies = rated(feature_movies(basics), ratings, min_votes) \
        .select("tconst", "primaryTitle", "startYear", "averageRating", "numVotes")
    mapping = F.create_map(*[F.lit(x) for kv in ROLE_OF_CATEGORY.items() for x in kv])
    from_principals = principals.select("tconst", "nconst", mapping[F.col("category")].alias("role")) \
        .where(F.col("role").isNotNull())
    from_crew = crew.select("tconst", F.explode(split_list("directors")).alias("nconst"),
                            F.lit("direct").alias("role")) \
        .unionByName(crew.select("tconst", F.explode(split_list("writers")).alias("nconst"),
                                 F.lit("write").alias("role")))
    credits = from_principals.unionByName(from_crew).join(movies.select("tconst"), "tconst")
    return credits.groupBy("nconst", "tconst").agg(F.array_sort(F.collect_set("role")).alias("roles")) \
        .join(movies, "tconst")


def multi_talented(roles: DataFrame, min_per_role: int = 3) -> DataFrame:
    """People holding >= 2 roles, each on >= ``min_per_role`` movies."""
    per_role = roles.select("nconst", F.explode("roles").alias("role")) \
        .groupBy("nconst", "role").count().where(F.col("count") >= min_per_role)
    return per_role.groupBy("nconst").agg(
        F.array_sort(F.collect_list("role")).alias("talents"),
        F.map_from_entries(F.collect_list(F.struct("role", "count"))).alias("movies_per_role"),
    ).where(F.size("talents") >= 2)


def performance(roles: DataFrame, talented: DataFrame, names: DataFrame) -> DataFrame:
    """Per person: average rating when cumulating roles on one movie vs a single role."""
    multi = F.size("roles") >= 2
    return (
        roles.join(talented, "nconst")
        .groupBy("nconst", "talents").agg(
            F.sum(multi.cast("int")).alias("n_multi_role_movies"),
            F.sum((~multi).cast("int")).alias("n_single_role_movies"),
            F.avg(F.when(multi, F.col("averageRating"))).alias("avg_rating_multi"),
            F.avg(F.when(~multi, F.col("averageRating"))).alias("avg_rating_single"),
        )
        .withColumn("rating_gain", F.col("avg_rating_multi") - F.col("avg_rating_single"))
        .join(names.select("nconst", "primaryName"), "nconst", "left")
        .select("nconst", "primaryName", F.array_join("talents", "+").alias("talents"),
                "n_multi_role_movies", "n_single_role_movies",
                F.round("avg_rating_multi", 2).alias("avg_rating_multi"),
                F.round("avg_rating_single", 2).alias("avg_rating_single"),
                F.round("rating_gain", 2).alias("rating_gain"))
    )


def combination_summary(roles: DataFrame, talented: DataFrame) -> DataFrame:
    """Average rating per exact role combination held on a movie, multi-talented people only."""
    return (
        roles.join(talented.select("nconst"), "nconst")
        .groupBy(F.array_join("roles", "+").alias("roles_on_movie")).agg(
            F.count("*").alias("n_credits"),
            F.countDistinct("nconst").alias("n_people"),
            F.round(F.avg("averageRating"), 2).alias("avg_rating"),
            F.round(F.expr("percentile_approx(averageRating, 0.5)"), 2).alias("median_rating"),
            F.round(F.avg("numVotes"), 0).alias("avg_votes"))
        .orderBy(F.desc("n_credits"))
    )


def main(min_votes: int = 100, min_per_role: int = 3) -> None:
    spark = get_spark("q8-multi-talented")
    roles = movie_roles(load(spark, "title.basics"), load(spark, "title.crew"),
                        load(spark, "title.principals"), load(spark, "title.ratings"), min_votes).cache()
    talented = multi_talented(roles, min_per_role).cache()
    perf = performance(roles, talented, load(spark, "name.basics")).cache()
    save(perf.where("n_multi_role_movies > 0").orderBy(F.desc("n_multi_role_movies")),
         "q8_multi_talented_people")
    save(combination_summary(roles, talented), "q8_role_combination_ratings")
    save(perf.groupBy("talents").agg(
        F.count("*").alias("n_people"),
        F.round(F.avg("avg_rating_multi"), 2).alias("mean_rating_multi"),
        F.round(F.avg("avg_rating_single"), 2).alias("mean_rating_single"),
        F.round(F.avg("rating_gain"), 3).alias("mean_rating_gain"),
        F.round(100 * F.avg((F.col("rating_gain") > 0).cast("int")), 1).alias("pct_better_when_multi"))
         .orderBy(F.desc("n_people")), "q8_talent_profile_summary")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--min-votes", type=int, default=100)
    ap.add_argument("--min-per-role", type=int, default=3)
    a = ap.parse_args()
    main(a.min_votes, a.min_per_role)

"""Tables and figures of REPORT.md that are not already a CSV of results/.

They are computed from the CSV files of results/ and from the enrichment Parquet tables,
so every number of the report can be rebuilt. Output: results/report/*.csv.
Also re-runs Q4 with 1,000 votes (the sensitivity check of the report).

Run after the exploration, enrichment and open question steps:
    python -m src.report_tables
"""
from pathlib import Path

import numpy as np
import pandas as pd

from src.common.spark_session import get_spark
from src.exploration.common import load
from src.exploration.q4_one_hit_directors import one_hit_directors

RES = Path("results")
OUT = RES / "report"
figures = []


def csv(path):
    return pd.read_csv(RES / path, keep_default_na=False, na_values=[""])


def save(df, name):
    df.to_csv(OUT / f"{name}.csv", index=False)


def fig(name, value):
    figures.append({"figure": name, "value": str(value)})


def share(mask):
    return round(100 * mask.mean(), 1)


def preparation(spark):
    # what the cleaning changed: rows dropped (orphans, duplicates) and values set to null
    tables = ["title_basics", "name_basics", "title_ratings", "title_crew", "title_episode",
              "title_principals", "title_akas"]
    rows = []
    for t in tables:
        before = spark.read.parquet(f"data/parquet/{t}").count()
        after = spark.read.parquet(f"data/clean/{t}").count()
        rows.append({"table": t.replace("_", "."), "rows_before": before, "rows_after": after,
                     "rows_removed": before - after})
    save(pd.DataFrame(rows), "preparation_rows_removed")
    nulled = []
    for t, col, rule in (("title_basics", "runtimeMinutes", "<= 0 or > 1000 min"),
                         ("title_basics", "endYear", "endYear < startYear"),
                         ("name_basics", "deathYear", "deathYear < birthYear")):
        raw = spark.read.parquet(f"data/parquet/{t}").where(f"{col} is not null").count()
        clean = spark.read.parquet(f"data/clean/{t}").where(f"{col} is not null").count()
        nulled.append({"table": t.replace("_", "."), "column": col, "rule": rule,
                       "values_set_to_null": raw - clean})
    save(pd.DataFrame(nulled), "preparation_values_nulled")
    basics = spark.read.parquet("data/clean/title_basics")
    fig("prep titles after 2026 kept", basics.where("startYear > 2026").count())
    fig("prep latest startYear", basics.agg({"startYear": "max"}).first()[0])


def exploration():
    # Q1: bounds of the two rules per genre, and outliers counted as distinct movies
    st = csv("exploration/q1_genre_runtime_stats.csv")
    iqr = st.q3 - st.q1
    st["z_low"] = st.mean_runtime - 3 * st.std_runtime
    st["z_high"] = st.mean_runtime + 3 * st.std_runtime
    st["iqr_low"] = st.q1 - 1.5 * iqr
    st["iqr_high"] = st.q3 + 1.5 * iqr
    save(st.round(2), "q1_bounds")
    fig("q1 genres with z_low under 40 min", int((st.z_low < 40).sum()))
    fig("q1 genres with z_low under 41 min", int((st.z_low < 41).sum()))
    fig("q1 genres with iqr_low at 41 min or below", int((st.iqr_low <= 41).sum()))
    fig("q1 genres with mean above median", int((st.mean_runtime > st["median"]).sum()))
    ro = csv("exploration/q1_runtime_outliers.csv")
    rows = []
    for rule, flag in (("z-score", ro.z_outlier), ("IQR", ro.iqr_outlier), ("either", ro.z_outlier | ro.iqr_outlier)):
        sub = ro[flag]
        rows.append({"rule": rule, "movie_genre_rows": len(sub), "distinct_movies": sub.tconst.nunique(),
                     "longer": int((sub.direction == "longer").sum()),
                     "shorter": int((sub.direction == "shorter").sum()),
                     "distinct_shorter": sub[sub.direction == "shorter"].tconst.nunique(),
                     "distinct_longer": sub[sub.direction == "longer"].tconst.nunique()})
    save(pd.DataFrame(rows), "q1_totals")
    save(ro[ro.direction == "shorter"].sort_values("z_score").head(10), "q1_shortest")

    # Q2/Q3: shares per year, comparison per decade
    q2 = csv("exploration/q2_top3_genres_per_year.csv")
    save(q2.pivot(index="year", columns="rank", values="vote_share_pct").add_prefix("share_rank_")
         .assign(top3_share=lambda d: d.sum(axis=1).round(1)).reset_index(), "q2_shares")
    py = csv("exploration/q3_top3_vs_rest_per_year.csv")
    py["decade"] = py.year // 10 * 10
    save(py.pivot_table(index="decade", columns="group",
                        values=["vote_share_pct", "avg_rating", "votes_per_movie"]).round(2)
         .pipe(lambda d: d.set_axis([f"{a}_{b}" for a, b in d.columns], axis=1)).reset_index(),
         "q3_per_decade")
    top, rest = (py[py.group == g].set_index("year") for g in ("top3", "rest"))
    fig("q3 years top3 rating higher", int((top.avg_rating > rest.avg_rating).sum()))
    fig("q3 years top3 votes per movie higher", int((top.votes_per_movie > rest.votes_per_movie).sum()))
    fig("q3 genres per year min", int((top.n_genres + rest.n_genres).min()))
    fig("q3 genres per year max", int((top.n_genres + rest.n_genres).max()))
    fig("q3 movies per top3 genre per year", round(top.n_movies.mean() / 3))
    fig("q3 movies per other genre per year", round(rest.n_movies.mean() / rest.n_genres.mean()))

    # Q4: size of the filmographies, and how many hits rest on few votes
    q4 = csv("exploration/q4_one_hit_directors.csv")
    save(pd.cut(q4.n_others, [1, 2, 4, 9, 10 ** 6], labels=["2", "3-4", "5-9", "10+"])
         .value_counts().sort_index().rename_axis("other_movies").reset_index(name="directors"),
         "q4_other_movies")
    fig("q4 hits with fewer than 1000 votes", int((q4.hit_votes < 1000).sum()))
    fig("q4 hits released in 2026", int((q4.hit_year == 2026).sum()))

    # Q5
    q5 = csv("exploration/q5_series_decline.csv")
    save(pd.DataFrame([{"series": len(q5), "best_in_season_1": int((q5.best_season == 1).sum()),
                        "best_in_season_2": int((q5.best_season == 2).sum()),
                        "median_best": q5.best_rating.median(), "median_worst": q5.worst_rating.median(),
                        "median_gap": round((q5.best_rating - q5.worst_rating).median(), 2),
                        "no_end_year": int(q5.endYear.isna().sum())}]), "q5_summary")

    # Q6
    a2 = csv("exploration/q6_actors_2plus_languages.csv")
    save(a2.n_languages.value_counts().sort_index().rename_axis("languages").reset_index(name="people"),
         "q6_people_by_languages")
    save(a2[a2.n_languages == 2].languages.value_counts().head(10).rename_axis("languages")
         .reset_index(name="people"), "q6_language_pairs")
    fig("q6 share of 2+ profiles with English", share(a2.languages.str.split(",").apply(lambda l: "en" in l)))

    # Q7
    q7 = csv("exploration/q7_early_peak_actors.csv")
    save(pd.cut(q7.rating_drop, [0, 0.25, 0.5, 1, 2, 10], include_lowest=True,
                labels=["0-0.25", "0.25-0.5", "0.5-1", "1-2", "2+"])
         .value_counts().sort_index().rename_axis("drop").reset_index(name="people"), "q7_drop_sizes")
    fig("q7 median movies", q7.n_movies.median())
    fig("q7 median span", q7.span_years.median())
    fig("q7 median drop", q7.rating_drop.median())
    fig("q7 best movie in first year", int((q7.best_year == q7.first_year).sum()))

    # Q8: the gain is only defined for people with both kinds of movies
    q8 = csv("exploration/q8_multi_talented_people.csv")
    both = q8[(q8.n_multi_role_movies > 0) & (q8.n_single_role_movies > 0)]
    save(both.groupby("talents").size().rename("people_with_both").reset_index(), "q8_people_with_both")
    fig("q8 people with both kinds of movies", len(both))


def enrichment(spark):
    fi = spark.read.parquet("data/enrichment/films").toPandas()
    pe = spark.read.parquet("data/enrichment/people").toPandas()
    sp = spark.read.parquet("data/enrichment/selected_people").toPandas()
    groups = fi.groupby(["year", "genre"]).size()
    per_film = sp.groupby("tconst").size().reindex(fi.tconst.unique(), fill_value=0)
    save(pd.DataFrame([
        {"item": "genres", "value": fi.genre.nunique()},
        {"item": "genre-year groups", "value": len(groups)},
        {"item": "groups with fewer than 10 films", "value": int((groups < 10).sum())},
        {"item": "film x genre rows", "value": len(fi)},
        {"item": "distinct films", "value": fi.tconst.nunique()},
        {"item": "film x person rows", "value": len(pe)},
        {"item": "distinct people", "value": pe.nconst.nunique()},
        {"item": "films with fewer than 3 principals", "value": int((per_film < 3).sum())},
    ]), "enrichment_scope")

    films = fi.drop_duplicates("tconst")
    films = films.assign(decade=films.year // 10 * 10)
    people = pe.merge(films[["tconst", "decade"]], on="tconst").drop_duplicates(["decade", "nconst"])
    save(films.groupby("decade").agg(films=("tconst", "size"), with_synopsis=("synopsis", "count"))
         .join(people.groupby("decade").agg(people=("nconst", "size"), with_bio=("biography", "count")))
         .reset_index(), "enrichment_per_decade")
    save(fi.assign(status=fi.note.fillna("ok")).groupby(["genre", "status"]).size().unstack(fill_value=0)
         .reset_index(), "enrichment_per_genre")
    save(pe.drop_duplicates(["nconst", "category"]).groupby("category")
         .agg(people=("nconst", "nunique"), with_bio=("biography", "count")).reset_index(), "enrichment_per_role")
    rows = []
    for name, texts in (("synopsis", films.synopsis), ("biography", pe.drop_duplicates("nconst").biography)):
        words = texts.dropna().str.split().str.len()
        rows.append({"text": name, "count": len(words), "median_words": words.median(),
                     "p10": words.quantile(0.1), "p90": words.quantile(0.9), "max": words.max()})
    save(pd.DataFrame(rows), "enrichment_text_length")
    fig("enrichment distinct films with synopsis %", share(films.synopsis.notna()))
    fig("enrichment no-plot rows with source_url %",
        share(fi[fi.note == "article found but no Plot section"].source_url.notna()))


def duos():
    du = csv("open_question/duos.csv")
    apart = du[["director_other_avg", "actor_other_avg"]]
    fig("5.1 duos", len(du))
    fig("5.1 directors", du.director_name.nunique())
    fig("5.1 actors", du.actor_name.nunique())
    fig("5.1 mean lift", round(du.lift.mean(), 3))
    se = du.lift.std() / np.sqrt(len(du))
    fig("5.1 mean lift 95% CI low", round(du.lift.mean() - 1.96 * se, 3))
    fig("5.1 mean lift 95% CI high", round(du.lift.mean() + 1.96 * se, 3))
    pos, neg = int((du.lift > 0).sum()), int((du.lift < 0).sum())
    fig("5.1 duos better (rounded lifts)", pos)
    fig("5.1 duos worse (rounded lifts)", neg)
    fig("5.1 duos at zero (rounded lifts)", int((du.lift == 0).sum()))
    fig("5.1 sign test z", round((pos - (pos + neg) / 2) / np.sqrt((pos + neg) / 4), 1))
    fig("5.1 duo above both apart %", share(du.duo_avg > apart.max(axis=1)))
    fig("5.1 duo below both apart %", share(du.duo_avg < apart.min(axis=1)))
    fig("5.1 lift >= 1 %", share(du.lift >= 1))
    fig("5.1 corr lift / films together", round(du.lift.corr(du.n_films), 2))
    fig("5.1 corr lift / baseline", round(du.lift.corr(du.baseline), 2))
    quart = pd.qcut(du.baseline, 4, labels=["Q1", "Q2", "Q3", "Q4"])
    save(du.groupby(quart, observed=True).lift.mean().round(2).rename_axis("baseline_quartile")
         .reset_index(), "duos_by_baseline_quartile")
    save(pd.cut(du.lift, [-10, -1, -0.5, 0, 0.5, 1, 10], right=False,
                labels=["below -1", "-1 to -0.5", "-0.5 to 0", "0 to 0.5", "0.5 to 1", "1 or more"])
         .value_counts().sort_index().rename_axis("lift").reset_index(name="duos"), "duos_lift_distribution")
    du["decade"] = du.first_year // 10 * 10
    by_dec = du.groupby("decade").agg(duos=("lift", "size"), avg_lift=("lift", "mean"),
                                      pct_better=("lift", lambda s: 100 * (s > 0).mean()))
    save(by_dec[by_dec.duos >= 30].round(3).reset_index(), "duos_by_decade")
    five = du[du.n_films >= 5]
    save(five.nlargest(10, "lift"), "duos_highest_lift")
    save(five.nsmallest(10, "lift"), "duos_lowest_lift")
    save(du.director_name.value_counts().head(5).rename_axis("director").reset_index(name="duos"),
         "duos_most_duos_per_director")


def q4_at_1000_votes(spark):
    tables = [load(spark, t) for t in ("title.basics", "title.crew", "title.ratings", "name.basics")]
    strict = one_hit_directors(*tables, min_votes=1000).toPandas()
    strict.to_csv(RES / "exploration" / "q4_one_hit_directors_1000votes.csv", index=False)
    base = csv("exploration/q4_one_hit_directors.csv")
    fig("q4 directors at 1000 votes", len(strict))
    fig("q4 kept from the 100-vote list", int(strict.nconst.isin(base.nconst).sum()))
    fig("q4 hits released in 2026 at 1000 votes", int((strict.hit_year == 2026).sum()))


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    spark = get_spark("report-tables")
    preparation(spark)
    exploration()
    enrichment(spark)
    duos()
    q4_at_1000_votes(spark)
    save(pd.DataFrame(figures), "figures")
    print(f"[report] {len(figures)} figures and tables -> {OUT}")


if __name__ == "__main__":
    main()

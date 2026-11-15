# REPORT

All tables come from the CSV files in `results/`. Most are written by the module of each step; the derived ones (totals, distributions, per decade...) and the figures quoted in the text are in `results/report/`, built by `python -m src.report_tables`.

## 1. Data preparation

Missing values per column (nulls and empty strings, % of rows):

| Table            | Column            |      Rows |    Nulls | Empty strings | Missing (%) |
|------------------|-------------------|----------:|---------:|--------------:|------------:|
| name.basics      | nconst            |  15726308 |        0 |             0 |       0.000 |
| name.basics      | primaryName       |  15726308 |       88 |             0 |       0.001 |
| name.basics      | birthYear         |  15726308 | 15042845 |             0 |      95.654 |
| name.basics      | deathYear         |  15726308 | 15461971 |             0 |      98.319 |
| name.basics      | primaryProfession |  15726308 |  3192578 |             0 |      20.301 |
| name.basics      | knownForTitles    |  15726308 |  1903040 |             0 |      12.101 |
| title.akas       | titleId           |  59706412 |        0 |             0 |       0.000 |
| title.akas       | ordering          |  59706412 |        0 |             0 |       0.000 |
| title.akas       | title             |  59706412 |        0 |             0 |       0.000 |
| title.akas       | region            |  59706412 | 12896169 |             0 |      21.599 |
| title.akas       | language          |  59706412 | 19479789 |             0 |      32.626 |
| title.akas       | types             |  59706412 | 39968511 |             0 |      66.942 |
| title.akas       | attributes        |  59706412 | 59390547 |             0 |      99.471 |
| title.akas       | isOriginalTitle   |  59706412 |        0 |             0 |       0.000 |
| title.basics     | tconst            |  12855557 |        0 |             0 |       0.000 |
| title.basics     | titleType         |  12855557 |        0 |             0 |       0.000 |
| title.basics     | primaryTitle      |  12855557 |        0 |             0 |       0.000 |
| title.basics     | originalTitle     |  12855557 |        0 |             0 |       0.000 |
| title.basics     | isAdult           |  12855557 |        0 |             0 |       0.000 |
| title.basics     | startYear         |  12855557 |  1484994 |             0 |      11.551 |
| title.basics     | endYear           |  12855557 | 12692766 |             0 |      98.734 |
| title.basics     | runtimeMinutes    |  12855557 |  8011644 |             0 |      62.320 |
| title.basics     | genres            |  12855557 |   544740 |             0 |       4.237 |
| title.crew       | tconst            |  12856880 |        0 |             0 |       0.000 |
| title.crew       | directors         |  12856880 |  5721595 |             0 |      44.502 |
| title.crew       | writers           |  12856880 |  6359633 |             0 |      49.465 |
| title.episode    | tconst            |   9942170 |        0 |             0 |       0.000 |
| title.episode    | parentTconst      |   9942170 |        0 |             0 |       0.000 |
| title.episode    | seasonNumber      |   9942170 |  2087110 |             0 |      20.992 |
| title.episode    | episodeNumber     |   9942170 |  2087110 |             0 |      20.992 |
| title.principals | tconst            | 102236837 |        0 |             0 |       0.000 |
| title.principals | ordering          | 102236837 |        0 |             0 |       0.000 |
| title.principals | nconst            | 102236837 |        0 |             0 |       0.000 |
| title.principals | category          | 102236837 |        0 |             0 |       0.000 |
| title.principals | job               | 102236837 | 82513420 |             0 |      80.708 |
| title.principals | characters        | 102236837 | 52384437 |             0 |      51.238 |
| title.ratings    | tconst            |   1719590 |        0 |             0 |       0.000 |
| title.ratings    | averageRating     |   1719590 |        0 |             0 |       0.000 |
| title.ratings    | numVotes          |   1719590 |        0 |             0 |       0.000 |

The five columns with the most missing values:

| Table            | Column     |      Rows |    Nulls | Missing (%) |
|------------------|------------|----------:|---------:|------------:|
| title.akas       | attributes |  59706412 | 59390547 |      99.471 |
| title.basics     | endYear    |  12855557 | 12692766 |      98.734 |
| name.basics      | deathYear  |  15726308 | 15461971 |      98.319 |
| name.basics      | birthYear  |  15726308 | 15042845 |      95.654 |
| title.principals | job        | 102236837 | 82513420 |      80.708 |

Data quality checks:

| Table            | Check                                  | Count |
|------------------|----------------------------------------|------:|
| title.akas       | titleId missing in title.basics        |     1 |
| title.crew       | tconst missing in title.basics         |  1333 |
| title.episode    | tconst missing in title.basics         |     0 |
| title.episode    | parentTconst missing in title.basics   |     4 |
| title.principals | tconst missing in title.basics         |     0 |
| title.ratings    | tconst missing in title.basics         |     0 |
| title.principals | nconst missing in name.basics          |  3203 |
| title.crew       | directors ids missing in name.basics   |   279 |
| title.crew       | writers ids missing in name.basics     |   322 |
| name.basics      | knownForTitles missing in title.basics |     4 |
| title.basics     | duplicate key ['tconst']               |     0 |
| name.basics      | duplicate key ['nconst']               |     0 |
| title.ratings    | duplicate key ['tconst']               |     0 |
| title.crew       | duplicate key ['tconst']               |     0 |
| title.episode    | duplicate key ['tconst']               |     0 |
| title.principals | duplicate key ['tconst', 'ordering']   |     0 |
| title.akas       | duplicate key ['titleId', 'ordering']  |     0 |
| title.basics     | endYear < startYear                    |     0 |
| title.basics     | runtimeMinutes <= 0 or > 1000          |   441 |
| title.basics     | startYear > 2026                       |  4416 |
| name.basics      | deathYear < birthYear                  |    27 |
| title.ratings    | averageRating outside [1,10]           |     0 |
| title.principals | unparseable rows in 'ordering'         |     0 |

Rows removed by the cleaning (orphan rows):

| Table            | Rows before | Rows after | Rows removed |
|------------------|------------:|-----------:|-------------:|
| title.basics     |    12855557 |   12855557 |            0 |
| name.basics      |    15726308 |   15726308 |            0 |
| title.ratings    |     1719590 |    1719590 |            0 |
| title.crew       |    12856880 |   12855547 |         1333 |
| title.episode    |     9942170 |    9942160 |           10 |
| title.principals |   102236837 |  102229682 |         7155 |
| title.akas       |    59706412 |   59706404 |            8 |

Impossible values set to null by the cleaning:

| Table        | Column         | Rule                  | Values set to null |
|--------------|----------------|-----------------------|-------------------:|
| title.basics | runtimeMinutes | <= 0 or > 1000 min    |                441 |
| title.basics | endYear        | endYear < startYear   |                  0 |
| name.basics  | deathYear      | deathYear < birthYear |                 27 |

### Methodological Explanation

**Reading the data.** IMDb ships seven `.tsv.gz` files. We read each one with an explicit schema, so column types are fixed in advance and not guessed by Spark, and `\N`, IMDb's marker for a missing value, is read as null. `isAdult` and `isOriginalTitle` hold 0 or 1, so we read them as integers and convert them afterwards. Read directly as booleans, they came out 100% null (a bug found while reviewing PR #2 and fixed in #6). The files are converted once to Parquet (`to_parquet.py`). Gzip cannot be split, so Spark reads each TSV on a single core, while every later step on Parquet is fast.

**Measuring missing values.** For each column, `profile_quality.py` counts nulls and empty strings, and the missing share is (null + empty) / rows. There is no empty string anywhere, since IMDb always writes `\N`. 19 of the 39 columns have missing values, and the 20 others, all keys included, have none. Four of the five emptiest columns are empty by design: `endYear` only applies to series, `deathYear` is null for anyone alive, and `attributes` and `job` are optional fields filled only in special cases. `birthYear` (95.7%) is different: for most people, IMDb simply does not know it. Several columns used later are also incomplete: `runtimeMinutes` (62.3%), `writers` (49.5%), `directors` (44.5%), `language` in `title.akas` (32.6%), `seasonNumber` and `episodeNumber` (21.0%), `startYear` (11.6%) and `genres` (4.2%).

**Quality checks.** We ran 23 checks: 10 on orphan keys, 7 on duplicate keys, 4 on impossible values, one on dates in the future and one on file parsing. Orphan keys point to a row that does not exist: 3,203 `nconst` in `title.principals` are missing from `name.basics`, 1,333 `tconst` in `title.crew` are missing from `title.basics`, and 279 directors and 322 writers listed in `title.crew` are missing from `name.basics`, plus a handful of other cases. No table has a duplicate key and no row failed to parse. Impossible values are rare: 441 runtimes at or below 0 or above 1,000 minutes and 27 people who died before they were born, but no series ending before it started and no rating outside [1, 10]. 4,416 titles are dated after 2026, up to 2115. Each check protects a join or a filter used in the later parts. `scripts/run_quality_checks.sh` runs every check in its own JVM so that it fits in a laptop's memory, then merges the results.

**Treatment.** Cleaning runs in Spark (`clean.py`) and writes `data/clean/`, which Parts 2, 3 and 5 read. Duplicate keys are dropped; there were none, but the rule stays in case a later IMDb release has some. Orphan rows are removed from the child tables with a `left_semi` join: 1,333 rows in crew, 10 in episode, 7,155 in principals (the 3,203 unknown people) and 8 in akas. Impossible values are set to null and the row is kept: 441 runtimes and 27 death years. The rule for ratings outside [1, 10] drops the row instead, but it matches none. All other nulls stay as they are, and we invent no value.

**What we did not fix.** The 4,416 future titles are kept, since they are mostly announced films. Q2, Q3 and Part 3 set their own range (1980-2025), but Q1 does not filter on year, so 36 of its rows are titles dated after 2026, up to 2030. Orphan identifiers inside lists (`directors`, `writers`, `knownForTitles`) are not removed, only whole orphan rows. The code also has a small defect: if `startYear` is null, a valid `endYear` would be cleared too. It affects no row in the current data.

**Alternatives.** Dropping every row with an impossible value would be simpler, but a film with a wrong runtime still has a valid title, genres and rating, and a person with an impossible death year still has credits. Filling nulls with an estimate, such as the median runtime of the genre, would invent 62% of `runtimeMinutes`, and Q1 would then partly measure our own guesses. Orphan rows could have been kept, but an inner join drops them later anyway and a left join returns credits with no name, so we remove them once, in one place.

## 2. Data exploration

Seven of the eight questions (all except Q5) are about feature films, so we fixed one definition and reused it everywhere. A feature film is a title with `titleType = movie`, not flagged as adult, with a known release year and a runtime above 40 minutes (`FEATURE_MIN_RUNTIME = 40`). Forty minutes is the limit the Academy uses to separate features from shorts, and we preferred an existing convention to a number of our own.

All queries read the cleaned tables in `data/clean`. A film with several genres counts once in each of its genres. IMDb stores genres in alphabetical order, not by importance, so picking a single "main" genre would have been arbitrary. The cost is that genre totals overlap, and we come back to it wherever it affects a result.

### Q1. Feature films with an unusual runtime for their genre

Runtime statistics per genre (minutes):

| Genre       | Movies |  Mean |  Std |  Q1 | Median |  Q3 | z-score range | IQR range  |
|-------------|-------:|------:|-----:|----:|-------:|----:|---------------|------------|
| Action      |  39403 | 101.0 | 29.7 |  85 |     94 | 113 | 12 to 190     | 43 to 155  |
| Adventure   |  23468 |  92.8 | 29.3 |  79 |     90 | 101 | 5 to 181      | 46 to 134  |
| Animation   |   8009 |  82.4 | 26.6 |  68 |     81 |  93 | 2 to 162      | 30 to 130  |
| Biography   |  15698 |  89.2 | 29.3 |  69 |     88 | 104 | 1 to 177      | 16 to 156  |
| Comedy      |  94290 |  93.2 | 21.6 |  82 |     91 | 102 | 28 to 158     | 52 to 132  |
| Crime       |  33762 |  95.6 | 24.8 |  83 |     92 | 105 | 21 to 170     | 50 to 138  |
| Documentary | 113322 |  76.4 | 28.7 |  57 |     74 |  90 | -10 to 162    | 8 to 140   |
| Drama       | 192437 |  95.9 | 26.6 |  82 |     93 | 107 | 16 to 176     | 44 to 144  |
| Family      |  15618 |  92.2 | 25.6 |  77 |     90 | 102 | 15 to 169     | 40 to 140  |
| Fantasy     |  12237 |  93.7 | 26.2 |  80 |     91 | 104 | 15 to 172     | 44 to 140  |
| Film-Noir   |    876 |  81.9 | 13.8 |  71 |     82 |  91 | 41 to 123     | 41 to 121  |
| Game-Show   |      6 |  76.2 | 37.5 |  52 |     60 |  77 | -36 to 189    | 14 to 114  |
| History     |  13322 |  93.7 | 37.0 |  71 |     90 | 108 | -17 to 205    | 16 to 164  |
| Horror      |  29486 |  88.5 | 20.8 |  79 |     88 |  96 | 26 to 151     | 54 to 122  |
| Music       |  13706 |  87.8 | 30.2 |  68 |     87 | 100 | -3 to 179     | 20 to 148  |
| Musical     |   8323 |  99.8 | 30.0 |  82 |     94 | 111 | 10 to 190     | 38 to 154  |
| Mystery     |  16004 |  93.9 | 24.4 |  81 |     92 | 105 | 21 to 167     | 45 to 141  |
| News        |   1364 |  77.4 | 32.5 |  59 |     75 |  87 | -20 to 175    | 17 to 129  |
| Reality-TV  |    288 |  87.5 | 33.0 |  64 |     90 |  96 | -12 to 187    | 16 to 144  |
| Romance     |  41666 |  99.1 | 25.0 |  85 |     95 | 110 | 24 to 174     | 48 to 148  |
| Sci-Fi      |   9373 |  90.9 | 27.3 |  79 |     90 | 100 | 9 to 173      | 48 to 132  |
| Sport       |   6685 |  88.6 | 29.2 |  71 |     90 | 100 | 1 to 176      | 28 to 144  |
| Talk-Show   |    101 |  88.4 | 33.8 |  60 |     82 | 118 | -13 to 190    | -27 to 205 |
| Thriller    |  32859 |  96.1 | 21.7 |  85 |     93 | 105 | 31 to 161     | 55 to 135  |
| War         |   7954 |  94.7 | 31.4 |  80 |     92 | 105 | 1 to 189      | 42 to 142  |
| Western     |   6311 |  76.4 | 28.7 |  57 |     70 |  90 | -10 to 163    | 8 to 140   |

Outliers per genre:

| Genre                     | Direction | z-score |   IQR | Both |
|---------------------------|-----------|--------:|------:|-----:|
| Action                    | longer    |     329 |  1837 |  329 |
| Action                    | shorter   |       0 |     1 |    0 |
| Adventure                 | longer    |     309 |  1260 |  309 |
| Adventure                 | shorter   |       0 |   148 |    0 |
| Animation                 | longer    |      82 |   204 |   82 |
| Biography                 | longer    |     166 |   313 |  166 |
| Comedy                    | longer    |     966 |  4552 |  966 |
| Comedy                    | shorter   |       0 |  2552 |    0 |
| Crime                     | longer    |     278 |  1708 |  278 |
| Crime                     | shorter   |       0 |   318 |    0 |
| Documentary               | longer    |    1158 |  1995 | 1158 |
| Drama                     | longer    |    1542 |  8506 | 1542 |
| Drama                     | shorter   |       0 |    25 |    0 |
| Family                    | longer    |     123 |   871 |  123 |
| Fantasy                   | longer    |     119 |   489 |  119 |
| Fantasy                   | shorter   |       0 |     2 |    0 |
| Film-Noir                 | longer    |       3 |     3 |    3 |
| Game-Show                 | longer    |       0 |     1 |    0 |
| History                   | longer    |     130 |   402 |  130 |
| Horror                    | longer    |     248 |  1259 |  248 |
| Horror                    | shorter   |       0 |  1044 |    0 |
| Music                     | longer    |     167 |   375 |  167 |
| Musical                   | longer    |      60 |   481 |   60 |
| Mystery                   | longer    |     115 |   476 |  115 |
| Mystery                   | shorter   |       0 |     3 |    0 |
| News                      | longer    |      19 |    28 |   19 |
| Reality-TV                | longer    |       6 |    11 |    6 |
| Romance                   | longer    |     287 |  1965 |  287 |
| Romance                   | shorter   |       0 |   180 |    0 |
| Sci-Fi                    | longer    |      69 |   392 |   69 |
| Sci-Fi                    | shorter   |       0 |   159 |    0 |
| Sport                     | longer    |      68 |   182 |   68 |
| Talk-Show                 | longer    |       1 |     0 |    0 |
| Thriller                  | longer    |     266 |  1670 |  266 |
| Thriller                  | shorter   |       0 |   751 |    0 |
| War                       | longer    |      83 |   356 |   83 |
| War                       | shorter   |       0 |     1 |    0 |
| Western                   | longer    |     101 |   131 |  101 |
| **Total (movie x genre)** |           |    6695 | 34651 | 6694 |

Totals:

| Criterion | Movie x genre rows | Distinct movies | Longer | Shorter |
|-----------|-------------------:|----------------:|-------:|--------:|
| z-score   |               6695 |            4708 |   6695 |       0 |
| IQR       |              34651 |           23708 |  29467 |    5184 |
| either    |              34652 |           23709 |  29468 |    5184 |

Most extreme long movies:

| Genre       | Title                                  | Year | Runtime | Genre mean | Genre median | z-score |
|-------------|----------------------------------------|-----:|--------:|-----------:|-------------:|--------:|
| Comedy      | Kahrlton Heights North                 | 2022 |     900 |       93.2 |           91 |   37.30 |
| Documentary | The Story of Documentary Film          | 2026 |     960 |       76.4 |           74 |   30.81 |
| Documentary | From Stage to Screen                   | 2016 |     900 |       76.4 |           74 |   28.72 |
| Horror      | Amy's Night Out                        | 2007 |     675 |       88.5 |           88 |   28.23 |
| Drama       | My Reflected Death                     | 2012 |     842 |       95.9 |           93 |   28.02 |
| Drama       | Saving Julian                          | 2012 |     840 |       95.9 |           93 |   27.95 |
| Mystery     | Out 1                                  | 1971 |     776 |       93.9 |           92 |   27.94 |
| Documentary | The Journey                            | 1987 |     873 |       76.4 |           74 |   27.78 |
| Animation   | Tom and Jerry the Golden Era Anthology | 1958 |     817 |       82.4 |           81 |   27.58 |
| Fantasy     | La Flor                                | 2018 |     808 |       93.7 |           91 |   27.30 |

Most extreme short movies (found by the IQR criterion only):

| Genre    | Title                     | Year | Runtime | Genre mean | Genre median | z-score |
|----------|---------------------------|-----:|--------:|-----------:|-------------:|--------:|
| Thriller | Dasher                    | 2026 |      41 |       96.1 |           93 |   -2.54 |
| Thriller | Trigger                   | 2024 |      42 |       96.1 |           93 |   -2.50 |
| Thriller | Are You Watching Closely? | 2019 |      43 |       96.1 |           93 |   -2.45 |
| Thriller | Lured                     | 2026 |      43 |       96.1 |           93 |   -2.45 |
| Thriller | Catherine                 | 2026 |      43 |       96.1 |           93 |   -2.45 |
| Comedy   | Morgan Almighty           | 2023 |      41 |       93.2 |           91 |   -2.41 |
| Comedy   | Stray Cat                 | 2023 |      41 |       93.2 |           91 |   -2.41 |
| Comedy   | Bethlehem                 | 2015 |      41 |       93.2 |           91 |   -2.41 |
| Comedy   | Combat Club               | 2022 |      41 |       93.2 |           91 |   -2.41 |
| Comedy   | Super Fat                 | 2013 |      41 |       93.2 |           91 |   -2.41 |

#### Methodological Explanation

We looked for abnormal runtimes inside each genre, because a normal length is not the same from one genre to the next. Two rules run on the same population: a z-score above 3 in absolute value (`--z`) and the IQR fences, below Q1 - 1.5 × IQR or above Q3 + 1.5 × IQR. We ran both on purpose, because comparing them shows how skewed the runtimes are.

The gap is large. The z-score finds no short film at all and 4,708 films that are too long. The IQR rule finds 4,669 short films (5,184 film-genre rows, as a film is tested in each of its genres) and 19,039 long ones. Runtimes have a long right tail, and a few extreme values inflate the mean and the standard deviation. In 25 of the 26 genres the lower z-score bound falls under the 40-minute floor. In Film-Noir it is 40.58 minutes, still under the shortest possible runtime of 41. So the z-score can never flag a film as short. Quartiles are not pulled by the tail, so the IQR fences are tighter in all genres but Talk-Show, but that is not enough everywhere. In 14 genres the lower fence is still at 41 minutes or below (7.5 for Documentary and Western, 16.5 for Biography), and no film can be short there either. It rises above 41 minutes in the 12 other genres, among them Drama, Comedy and Action, and these are exactly the genres where the rule finds short films.

The extremes mix real films and data problems. Out 1 is a real Rivette film of about 13 hours, while the Tom and Jerry anthology is a compilation. The longest title is The Story of Documentary Film (960 minutes, dated 2026), and the largest z-score is Kahrlton Heights North at 37.3. Runtimes above 1,000 minutes had already been removed during data preparation.

A z-score built on the median and the MAD is the obvious alternative. We expect it to behave more like the IQR rule, since neither is distorted by extreme values, but we did not test it. The IQR rule has the opposite weakness: with 19,039 long outliers, it is quick to call a film abnormal.

### Q2. Top three genres per year (1980-2025)

Top three genres by total number of votes (share of the year's votes in %):

| Year | 1st              | 2nd              | 3rd              | Top 3 share |
|-----:|------------------|------------------|------------------|------------:|
| 1980 | Drama (18.2)     | Adventure (14.3) | Horror (11.9)    |        44.4 |
| 1981 | Adventure (20.1) | Drama (15.2)     | Horror (11.3)    |        46.6 |
| 1982 | Drama (18.2)     | Sci-Fi (14.5)    | Action (11.1)    |        43.8 |
| 1983 | Drama (19.3)     | Action (13.4)    | Adventure (13.2) |        45.9 |
| 1984 | Action (17.1)    | Drama (14.1)     | Adventure (13.6) |        44.8 |
| 1985 | Comedy (21.3)    | Adventure (15.9) | Drama (14.4)     |        51.6 |
| 1986 | Drama (19.0)     | Adventure (14.1) | Comedy (13.2)    |        46.3 |
| 1987 | Drama (17.3)     | Comedy (15.4)    | Action (9.9)     |        42.6 |
| 1988 | Drama (18.0)     | Comedy (17.9)    | Action (11.0)    |        46.9 |
| 1989 | Comedy (20.8)    | Drama (16.5)     | Adventure (12.2) |        49.5 |
| 1990 | Drama (20.7)     | Comedy (13.1)    | Crime (11.7)     |        45.5 |
| 1991 | Drama (19.8)     | Crime (13.0)     | Comedy (11.3)    |        44.1 |
| 1992 | Drama (17.2)     | Comedy (14.3)    | Crime (12.6)     |        44.1 |
| 1993 | Drama (24.3)     | Comedy (12.2)    | Crime (8.2)      |        44.7 |
| 1994 | Drama (32.8)     | Crime (13.6)     | Comedy (11.8)    |        58.2 |
| 1995 | Drama (23.3)     | Crime (14.4)     | Comedy (11.3)    |        49.0 |
| 1996 | Drama (20.7)     | Comedy (12.4)    | Crime (11.7)     |        44.8 |
| 1997 | Drama (22.3)     | Action (11.9)    | Comedy (9.9)     |        44.1 |
| 1998 | Drama (21.8)     | Comedy (18.2)    | Crime (11.5)     |        51.5 |
| 1999 | Drama (21.9)     | Comedy (11.6)    | Crime (10.1)     |        43.6 |
| 2000 | Drama (20.7)     | Comedy (13.2)    | Adventure (11.1) |        45.0 |
| 2001 | Drama (18.6)     | Comedy (12.0)    | Adventure (11.7) |        42.3 |
| 2002 | Drama (21.2)     | Adventure (10.8) | Action (10.4)    |        42.4 |
| 2003 | Drama (16.9)     | Action (14.9)    | Comedy (13.7)    |        45.5 |
| 2004 | Drama (17.5)     | Action (12.2)    | Comedy (11.6)    |        41.3 |
| 2005 | Drama (16.8)     | Comedy (12.5)    | Action (11.4)    |        40.7 |
| 2006 | Drama (21.6)     | Comedy (12.2)    | Thriller (9.0)   |        42.8 |
| 2007 | Drama (18.1)     | Comedy (11.4)    | Action (8.8)     |        38.3 |
| 2008 | Drama (16.8)     | Action (12.8)    | Comedy (10.8)    |        40.4 |
| 2009 | Drama (16.9)     | Comedy (12.9)    | Action (11.6)    |        41.4 |
| 2010 | Drama (15.9)     | Action (12.1)    | Adventure (12.0) |        40.0 |
| 2011 | Drama (18.4)     | Action (15.2)    | Comedy (12.4)    |        46.0 |
| 2012 | Drama (18.3)     | Action (13.2)    | Comedy (10.7)    |        42.2 |
| 2013 | Drama (16.9)     | Action (13.2)    | Comedy (11.4)    |        41.5 |
| 2014 | Drama (18.3)     | Action (15.6)    | Adventure (13.2) |        47.1 |
| 2015 | Drama (19.0)     | Action (14.5)    | Adventure (13.1) |        46.6 |
| 2016 | Drama (18.2)     | Action (15.0)    | Adventure (10.8) |        44.0 |
| 2017 | Drama (19.2)     | Action (15.4)    | Comedy (10.4)    |        45.0 |
| 2018 | Drama (16.8)     | Action (14.6)    | Adventure (12.9) |        44.3 |
| 2019 | Drama (20.9)     | Action (11.8)    | Comedy (11.7)    |        44.4 |
| 2020 | Drama (20.3)     | Comedy (12.6)    | Action (11.9)    |        44.8 |
| 2021 | Drama (17.8)     | Action (15.9)    | Adventure (12.6) |        46.3 |
| 2022 | Drama (18.7)     | Action (15.6)    | Comedy (11.9)    |        46.2 |
| 2023 | Drama (19.1)     | Action (13.6)    | Comedy (12.2)    |        44.9 |
| 2024 | Drama (18.3)     | Action (13.6)    | Comedy (11.1)    |        43.0 |
| 2025 | Drama (15.4)     | Action (13.7)    | Comedy (10.5)    |        39.6 |

#### Methodological Explanation

The assignment says "most popular" without defining it. We used the sum of `numVotes` over the feature films of a genre released in a given year. A vote means somebody watched the film and cared enough to rate it, which is the closest thing to audience size in IMDb. The percentage next to each genre is its share of all votes that year.

Three other measures were possible, and each one answers a different question:

- Number of films measures what the industry produces, not what people watch. It would favour genres with many small productions, Documentary for example.
- Average rating measures how much a film is liked by those who saw it. It would push niche genres with few, enthusiastic voters to the top.
- Vote-weighted rating is more stable, but it still ranks the best-rated genre, not the most popular one.

With votes, Drama dominates: first in 42 of the 46 years, and in the top 3 every year. The four exceptions are 1981 (Adventure), 1984 (Action), 1985 and 1989 (Comedy). Two periods stand out. All nine appearances of Crime fall in the 1990s (every year from 1990 to 1999 except 1997), and Action is in the top 3 every year from 2008 to 2025.

### Q3. Top three genres compared with the other genres

Mean over 1980-2025:

| Group        | Genres per year | Share of votes (%) | Rating (weighted by votes) | Votes per movie | Movies per year |
|--------------|----------------:|-------------------:|---------------------------:|----------------:|----------------:|
| Top 3 genres |             3.0 |               44.7 |                       7.10 |            8186 |            3722 |
| Other genres |            19.3 |               55.3 |                       6.96 |            8289 |            5243 |

Per decade:

| Decade | Top 3 share (%) | Top 3 rating | Others rating | Top 3 votes/movie | Others votes/movie |
|--------|----------------:|-------------:|--------------:|------------------:|-------------------:|
| 1980s  |            46.2 |         7.34 |          7.08 |              5257 |               5225 |
| 1990s  |            47.0 |         7.36 |          7.16 |              9726 |              11134 |
| 2000s  |            42.0 |         7.05 |          7.02 |             11074 |              12990 |
| 2010s  |            44.1 |         6.94 |          6.87 |              8724 |               6454 |
| 2020s  |            44.2 |         6.62 |          6.52 |              4796 |               3879 |

Years in the top three:

| Genre     | Years in top 3 | Years ranked 1st |
|-----------|---------------:|-----------------:|
| Drama     |             46 |               42 |
| Comedy    |             34 |                2 |
| Action    |             29 |                1 |
| Adventure |             16 |                1 |
| Crime     |              9 |                0 |
| Horror    |              2 |                0 |
| Sci-Fi    |              1 |                0 |
| Thriller  |              1 |                0 |

#### Methodological Explanation

Each year, the three genres from Q2 form one group that is compared with all other genres together. We chose four indicators: share of votes (how much of the audience the group holds), vote-weighted rating (how well it is liked, without films with a few dozen votes distorting the mean), votes per film and number of films. Votes per film matters most, because it tells whether the audience comes from each film or from the number of films.

Three genres out of more than twenty hold 44.7% of the votes, so popularity is concentrated. Their films, however, are not individually more popular or much better rated. Votes per film are practically equal (8,186 against 8,289), the top 3 is ahead in only 26 years out of 46, and its rating advantage is 0.14 points. The difference is the size of each genre: about 1,240 films a year for each top 3 genre, against about 270 for any other genre. Taken as a group, the others still release more films (5,243 against 3,722).

The alternative was to compare the top 3 with each other genre separately. That is more detailed, but it gives about 19 comparisons a year and no readable answer. Grouping loses the detail and treats Documentary, Horror and Musical as one block. The two groups also overlap: a Drama-Romance film sits in both, which pulls them closer together.

### Q4. Directors with a single movie rated 8.0 or more

172 directors found. The 15 with the most voted hit:

| Director           | Only movie >= 8.0                          | Year | Rating |   Votes | Other movies | Others avg rating |
|--------------------|--------------------------------------------|-----:|-------:|--------:|-------------:|------------------:|
| James McTeigue     | V for Vendetta                             | 2005 |    8.1 | 1258245 |            4 |              5.98 |
| Richard Marquand   | Star Wars: Episode VI - Return of the Jedi | 1983 |    8.3 | 1226458 |            6 |              5.98 |
| M. Night Shyamalan | The Sixth Sense                            | 1999 |    8.2 | 1168739 |           15 |              5.87 |
| Richard Kelly      | Donnie Darko                               | 2001 |    8.0 |  922430 |            3 |              5.43 |
| Robert Rodriguez   | Sin City                                   | 2005 |    8.0 |  824785 |           23 |              5.90 |
| Frank Miller       | Sin City                                   | 2005 |    8.0 |  824785 |            2 |              5.65 |
| Martin Campbell    | Casino Royale                              | 2006 |    8.0 |  756088 |           20 |              5.62 |
| John G. Avildsen   | Rocky                                      | 1976 |    8.1 |  703784 |           21 |              5.78 |
| Curtis Hanson      | L.A. Confidential                          | 1997 |    8.2 |  664993 |           15 |              6.00 |
| Tate Taylor        | The Help                                   | 2011 |    8.1 |  533908 |            6 |              5.88 |
| Kirk Wise          | Beauty and the Beast                       | 1991 |    8.0 |  510357 |            3 |              5.43 |
| Garth Davis        | Lion                                       | 2016 |    8.0 |  269598 |            2 |              5.65 |
| Wai Keung Lau      | Infernal Affairs                           | 2002 |    8.0 |  139602 |           42 |              5.75 |
| Vincent Paronnaud  | Persepolis                                 | 2007 |    8.0 |  107273 |            4 |              5.83 |
| Billy Bob Thornton | Sling Blade                                | 1996 |    8.0 |  104970 |            3 |              5.93 |

Number of other movies:

| Other movies | Directors |
|--------------|----------:|
| 2            |        59 |
| 3-4          |        49 |
| 5-9          |        27 |
| 10+          |        37 |

#### Methodological Explanation

Directors come from `title.crew.directors`. A director qualifies with exactly one film rated 8.0 or above, at least two other films, and an average of 6.0 or below on those others. These three values are fixed in the code. We read "multiple other movies" as two or more, because with a single other film there is nothing to average. We asked for exactly one hit because a director with two films above 8.0 is no longer a one-hit case.

Only films with at least 100 votes count (`--min-votes`, the same default as in Q7 and Q8). A rating built on a few dozen votes means little: the friends of the crew are enough to produce a 9. One hundred is still low enough to keep the small, badly rated films that the "other movies" condition depends on.

The vote threshold is the main trade-off. At 100 votes the list has 172 directors, but 82 of the hits have fewer than 1,000 votes, and 12 are 2026 releases whose ratings have not settled (Om Ka Hari stands at 9.9). We re-ran the query at 1,000 votes to see how much it matters. Only 49 directors are left, 41 from the original list and 8 new ones, and the 2026 hits drop from 12 to 2. The stricter list is more convincing, but the result clearly depends on this one setting.

### Q5. Series whose best episode is early and worst episode is in the last season

353 series found. The 15 most voted:

| Series                         | Start |  End | Last season | Best ep. season | Best rating | Worst ep. season | Worst rating | Series votes |
|--------------------------------|------:|-----:|------------:|----------------:|------------:|-----------------:|-------------:|-------------:|
| House of Cards                 |  2013 | 2018 |           6 |               2 |         9.5 |                6 |          2.5 |       564277 |
| Narcos                         |  2015 | 2017 |           3 |               2 |         9.4 |                3 |          7.8 |       537811 |
| The Flash                      |  2014 | 2023 |           9 |               1 |         9.6 |                9 |          3.8 |       389312 |
| You                            |  2018 | 2025 |           5 |               2 |         9.1 |                5 |          5.3 |       377081 |
| 13 Reasons Why                 |  2017 | 2020 |           4 |               1 |         9.1 |                4 |          5.1 |       343931 |
| The Umbrella Academy           |  2019 | 2024 |           4 |               2 |         8.9 |                4 |          4.8 |       318786 |
| Two and a Half Men             |  2003 | 2015 |          12 |               2 |         8.7 |               12 |          3.7 |       301433 |
| True Blood                     |  2008 | 2014 |           7 |               2 |         8.8 |                7 |          5.4 |       273568 |
| Heroes                         |  2006 | 2010 |           4 |               1 |         8.9 |                4 |          6.8 |       266950 |
| Jessica Jones                  |  2015 | 2019 |           3 |               1 |         9.0 |                3 |          7.1 |       242608 |
| Demon Slayer: Kimetsu no Yaiba |  2019 | 2024 |           4 |               2 |         9.8 |                4 |          7.1 |       238940 |
| One Punch Man                  |  2015 |      |           3 |               1 |         9.5 |                3 |          1.6 |       231375 |
| 24                             |  2001 | 2010 |           8 |               1 |         9.3 |                8 |          7.6 |       208528 |
| Silicon Valley                 |  2014 | 2019 |           6 |               1 |         9.3 |                6 |          7.3 |       184810 |
| The Originals                  |  2013 | 2018 |           5 |               1 |         9.5 |                5 |          8.0 |       163229 |

Summary:

| Series | Median best rating | Median worst rating | Median gap | Still running (no end year) |
|-------:|-------------------:|--------------------:|-----------:|----------------------------:|
|    353 |                8.6 |                 6.2 |        2.2 |                          19 |

#### Methodological Explanation

Series are titles of type `tvSeries` or `tvMiniSeries` with at least 3 seasons of at least 10 episodes (both fixed in the code). With fewer seasons, "early" and "last" overlap. The best episode must be in season 1 or 2, and the worst in the last season, taken as the highest season number. Only episodes with at least 20 votes count (`--min-votes`), a lower bar than for films because episodes get far fewer votes. Ties on rating go to the episode with more votes, so each series has exactly one best and one worst episode.

Season averages would be less sensitive to one odd episode, but the question is about episodes. Two edge cases remain. 19 of the 353 series have no end year, so their "last" season may only be the latest so far, and episodes without a season number are ignored. For the series that match, the fall is steep: the median gap between best and worst episode is 2.2 points.

### Q6. Actors successful in movies of several original languages

Source of the original language of the successful movies:

| Source       | Movies |    % |
|--------------|-------:|-----:|
| wikidata     |   4281 | 86.6 |
| multilingual |    583 | 11.8 |
| imdb_akas    |     66 |  1.3 |
| unknown      |     13 |  0.3 |

Successful movies per original language:

| Language | Movies |
|----------|-------:|
| en       |   2846 |
| hi       |    271 |
| fr       |    205 |
| ja       |    183 |
| tr       |     86 |
| it       |     80 |
| es       |     78 |
| ta       |     76 |
| de       |     64 |
| ko       |     58 |
| ml       |     38 |
| te       |     36 |

People by number of languages:

| Languages | People |
|----------:|-------:|
|         2 |    651 |
|         3 |     79 |
|         4 |      9 |
|         5 |      2 |

Most common language pairs:

| Languages | People |
|-----------|-------:|
| en,hi     |     87 |
| en,fr     |     86 |
| en,it     |     48 |
| hi,ta     |     39 |
| de,en     |     39 |
| ml,ta     |     28 |
| fr,it     |     25 |
| hi,te     |     23 |
| en,ta     |     20 |
| en,es     |     18 |

Actors successful in three or more languages:

| Name              | Languages | Codes          | Successful movies |
|-------------------|----------:|----------------|------------------:|
| Prakash Raj       |         5 | en,hi,kn,ta,te |                25 |
| Ashish Vidyarthi  |         5 | en,hi,ml,ta,te |                 8 |
| Fahadh Faasil     |         4 | en,ml,ta,te    |                11 |
| Murli Sharma      |         4 | en,hi,ta,te    |                 8 |
| Mohanlal          |         4 | en,hi,ml,ta    |                 8 |
| Rao Ramesh        |         4 | en,kn,ta,te    |                 7 |
| Bruno Ganz        |         4 | de,el,en,it    |                 6 |
| Sobhita Dhulipala |         4 | hi,ml,ta,te    |                 5 |
| Sai Kumar         |         4 | en,kn,ta,te    |                 5 |
| Rana Daggubati    |         4 | en,hi,ta,te    |                 5 |
| Franco Nero       |         4 | de,en,es,it    |                 4 |
| Amitabh Bachchan  |         3 | en,hi,te       |                26 |
| Paresh Rawal      |         3 | en,hi,ta       |                21 |
| Nassar            |         3 | hi,ta,te       |                21 |
| Ajay Devgn        |         3 | en,hi,te       |                17 |

#### Methodological Explanation

A film is a success with a rating of 7 or above and at least 10,000 votes. We wanted both conditions: the rating says the film is liked, the votes say it was actually seen. A film rated 7 with 300 votes may be well liked, but few people saw it.

The hard part is the language, because IMDb does not give it. `title.akas` has a language column, but it is never filled on the rows marked as the original title. Our first version guessed the language from the other `title.akas` rows, and it classified Wings of Desire, a German film, as English. That was enough to make us look elsewhere.

We took the original language from Wikidata. Each film there carries its IMDb identifier (property P345), so the join is exact and needs no title matching, and property P364 gives the original language. This covers 86.6% of the successful films. Regional variants are reduced to their base language (American English becomes `en`). Otherwise an actor with one American and one British film would count as bilingual.

Films with several original languages (11.8%) are excluded by default, which `--multi-language` can change. We cannot know which language a given actor performed in, and counting every language would create multilingual actors who are not. Where Wikidata has no answer (1.6%), the query falls back on the `title.akas` heuristic.

Staying on IMDb alone would have kept the pipeline self-contained, but it would repeat the Wings of Desire error on many non-English films. The production country is no better as a proxy, since a country is not a language (India and Switzerland are enough to show it).

Some errors remain. Wikidata is edited by volunteers and can be wrong or incomplete. The excluded multilingual films are often international co-productions, exactly where multilingual actors work, so the 741 actors with hits in two or more languages are probably an underestimate. And the original language of a film is not always the one a given actor spoke in it.

English is part of 66.8% of the profiles with two or more languages, so multilingual success mostly means a national career plus English-language films.

### Q7. Long careers whose ratings peaked early

5,522 actors and actresses found. The 15 largest drops:

| Name            | Movies | First | Last | Best movie                       | Best year | Best rating | 1st half avg | 2nd half avg | Drop |
|-----------------|-------:|------:|-----:|----------------------------------|----------:|------------:|-------------:|-------------:|-----:|
| Veronica Lake   |     20 |  1941 | 1970 | Sullivan's Travels               |      1941 |         7.9 |         6.43 |         2.50 | 3.93 |
| Mahesh Anand    |     32 |  1988 | 2019 | Abhimanyu                        |      1991 |         7.4 |         5.47 |         1.90 | 3.57 |
| Philomina       |     16 |  1983 | 2003 | Godfather                        |      1991 |         8.6 |         7.33 |         3.80 | 3.53 |
| Robert Woods    |     22 |  1966 | 2016 | My Name Is Pecos                 |      1966 |         6.1 |         5.12 |         1.70 | 3.42 |
| Artur Rolén     |     20 |  1918 | 1967 | The Outlaw and His Wife          |      1918 |         7.2 |         7.20 |         3.84 | 3.36 |
| Aleksey Batalov |     16 |  1954 | 2007 | The Cranes Are Flying            |      1957 |         8.3 |         7.35 |         4.05 | 3.30 |
| Ken Maynard     |     19 |  1931 | 1970 | Harmony Trail                    |      1944 |         6.7 |         5.95 |         2.70 | 3.25 |
| Norman Wisdom   |     18 |  1953 | 2002 | A Stitch in Time                 |      1963 |         6.9 |         6.31 |         3.20 | 3.11 |
| Tom Savini      |     20 |  1977 | 2015 | From Dusk Till Dawn              |      1996 |         7.2 |         6.13 |         3.16 | 2.97 |
| Dev Anand       |     41 |  1951 | 2003 | Guide                            |      1965 |         8.4 |         7.11 |         4.16 | 2.95 |
| Saroja Devi B.  |     15 |  1958 | 2023 | Babruvahana                      |      1977 |         8.9 |         8.00 |         5.07 | 2.93 |
| Tuncay Akça     |     19 |  1975 | 2018 | The Chaos Class Failed the Class |      1975 |         8.3 |         6.73 |         3.90 | 2.83 |
| Ari Lehman      |     15 |  1978 | 2025 | Manny's Orphans                  |      1978 |         6.4 |         6.40 |         3.57 | 2.83 |
| Deborah Twiss   |     16 |  1997 | 2025 | Kick-Ass                         |      2010 |         7.6 |         6.67 |         3.88 | 2.78 |
| Caroline Munro  |     19 |  1972 | 2020 | The Spy Who Loved Me             |      1977 |         7.0 |         5.59 |         2.82 | 2.78 |

Size of the drop between the first and second half of the career:

| Drop (rating points) | People |
|----------------------|-------:|
| 0-0.25               |   1257 |
| 0.25-0.5             |   1383 |
| 0.5-1                |   1845 |
| 1-2                  |    969 |
| 2+                   |     68 |

#### Methodological Explanation

Actors and actresses come from `title.principals`, with feature films of at least 100 votes. Career length is the year of the last film minus the year of the first. We kept careers of at least 20 years and 15 films (both fixed in the code): a peak needs a long career to stand out from, and each half needs enough films for its average to mean something.

"Peaked early" is not defined in the assignment. We cut each career at its middle year and asked for two things: the best-rated film is in the first half, and the first half has a higher average rating than the second. Each condition alone is too weak. The best film is a single data point, and one lucky film at 25 does not make a declining career. The average alone accepts careers that drift down without ever having had a high point.

Two other definitions were possible:

- The slope of a regression of rating on year uses every film and gives a rate of decline. But a negative slope is a trend, not a peak, and it is harder to explain than two halves.
- Best film in the first quarter is stricter on "early" and would shorten the list, but it rests entirely on one film.

Our definition is generous. Of the 5,522 people it returns, 2,640 lose half a point or less between the two halves, which is closer to slow erosion than to a fall, and only 1,037 lose more than one point. A minimum drop would give a shorter and more convincing list. The cut is also made on years, not on films, so the two halves can hold very different numbers of films.

### Q8. Multi-talented film professionals

Rating when cumulating roles, per profile:

| Profile          | People | People with both kinds of movies | Avg rating, several roles | Avg rating, one role |   Gain | % better |
|------------------|-------:|---------------------------------:|--------------------------:|---------------------:|-------:|---------:|
| direct+write     |   7645 |                             5479 |                      5.93 |                 5.91 |  0.038 |     51.1 |
| act+direct+write |   1646 |                             1549 |                      5.88 |                 5.86 |  0.047 |     54.4 |
| act+write        |   1291 |                             1069 |                      5.70 |                 5.76 |  0.020 |     52.4 |
| act+direct       |    500 |                              384 |                      5.81 |                 5.93 | -0.080 |     48.2 |

Rating per combination of roles on one movie:

| Roles on the movie | Credits | People | Avg rating | Median rating | Avg votes |
|--------------------|--------:|-------:|-----------:|--------------:|----------:|
| direct+write       |   45183 |   9365 |       6.00 |           6.2 |     12377 |
| act                |   41068 |   4263 |       5.97 |           6.1 |     20112 |
| direct             |   20722 |   5207 |       5.96 |           6.1 |     16293 |
| write              |   19222 |   4940 |       5.94 |           6.1 |     24385 |
| act+direct+write   |    5318 |   2382 |       5.76 |           6.0 |      7256 |
| act+write          |    4039 |   1577 |       5.75 |           5.9 |     16171 |
| act+direct         |    1360 |    776 |       5.90 |           6.2 |     12143 |

People with the most movies in several roles:

| Name               | Profile          | Movies, several roles | Movies, one role | Avg, several | Avg, one |  Gain |
|--------------------|------------------|----------------------:|-----------------:|-------------:|---------:|------:|
| Jesús Franco       | act+direct+write |                   112 |               23 |         4.66 |     4.60 |  0.06 |
| Jing Wong          | act+direct+write |                    91 |               71 |         5.65 |     5.72 | -0.07 |
| Yōji Yamada        | direct+write     |                    63 |                7 |         6.89 |     6.89 |  0.00 |
| Giannis Dalianidis | direct+write     |                    61 |               12 |         5.98 |     5.94 |  0.04 |
| Jean-Luc Godard    | act+direct+write |                    60 |               14 |         6.44 |     6.32 |  0.11 |
| Carlo Vanzina      | direct+write     |                    55 |               14 |         4.85 |     5.00 | -0.15 |
| Woody Allen        | act+direct+write |                    54 |               20 |         6.89 |     6.52 |  0.37 |
| Cheh Chang         | direct+write     |                    53 |               21 |         6.47 |     6.34 |  0.13 |
| Claude Chabrol     | act+direct+write |                    47 |               27 |         6.54 |     6.23 |  0.31 |
| Kader Khan         | act+write        |                    45 |              125 |         5.73 |     5.33 |  0.40 |

#### Methodological Explanation

Three roles count. Acting comes from `title.principals` (categories actor, actress and self). Directing and writing come from `title.crew`, completed with the director and writer rows of `title.principals`, so that a credit present in only one table is not lost. A multi-talent holds at least two roles, each on at least three films (`--min-per-role`) with 100 votes or more. Three films separates a regular activity from a one-off, such as a director with a single cameo. A higher minimum would shrink the population quickly.

The question asks how these people perform, which calls for a comparison. We made it per person: the average rating of their multi-role films minus the average of their single-role films. Each person is their own reference, so the result does not depend on whether they are famous or obscure. Comparing all multi-role films with all single-role films would mostly compare different people. We still report the averages by combination because they are easy to read. They stay within a quarter of a point, from 6.00 for directing and writing down to 5.75 for acting and writing.

Combining roles changes almost nothing. The average gain goes from -0.08 to +0.05 depending on the combination, and about half of the people do better when they combine.

Two limits are specific to this question. The "self" category counts as acting, although appearing as oneself in a documentary is not really acting, and it probably inflates that role. The "People" column counts all 11,082 multi-talents, while the gain only covers the 8,481 who have both kinds of films. The other 2,601 have nothing to compare.

### Common limits

Three limits apply to most of the questions above.

- Genres overlap. A multi-genre film counts in each of its genres, so one blockbuster tagged Action, Adventure and Sci-Fi lifts three genres at once.
- Votes keep accumulating after release. The figures describe films as they are seen today, not as they were received at the time, and very recent titles have ratings that have not settled.
- The IMDb rating is the only measure of quality. It reflects the people who vote on IMDb, not box office or critics.

## 3. Data enrichment

### Scope

| Item                                          | Value     |
|-----------------------------------------------|-----------|
| Years                                         | 1980-2025 |
| Genres                                        | 25        |
| Genre-year groups                             | 1027      |
| Film x genre rows (top 10 per genre and year) | 9833      |
| Distinct films                                | 6820      |
| Film x person rows (first 3 principals)       | 20428     |
| Distinct people                               | 10452     |
| Films with fewer than 3 principals in IMDb    | 23        |

### Coverage

Synopses:

| Level             | Total | With synopsis |    % |
|-------------------|------:|--------------:|-----:|
| Film x genre rows |  9833 |          8756 | 89.0 |
| Distinct films    |  6820 |          5851 | 85.8 |

Films (one row per film and genre):

| Status                            | Rows |    % |
|-----------------------------------|-----:|-----:|
| no English Wikipedia article      |  501 |  5.1 |
| article found but no Plot section |  576 |  5.9 |
| ok                                | 8756 | 89.0 |

Principals (one row per person):

| Status                       | People |    % |
|------------------------------|-------:|-----:|
| no English Wikipedia article |   2568 | 24.6 |
| ok                           |   7884 | 75.4 |

Biographies per role:

| Role            | People | With biography |    % |
|-----------------|-------:|---------------:|-----:|
| actor           |   5732 |           4493 | 78.4 |
| actress         |   3251 |           2636 | 81.1 |
| archive_footage |    109 |             82 | 75.2 |
| archive_sound   |      2 |              0 |  0.0 |
| cinematographer |     11 |              1 |  9.1 |
| composer        |     17 |              5 | 29.4 |
| director        |    611 |            367 | 60.1 |
| editor          |     11 |              1 |  9.1 |
| producer        |     50 |             11 | 22.0 |
| self            |    737 |            383 | 52.0 |
| writer          |     23 |              4 | 17.4 |

Per decade (distinct films, people counted once per decade):

| Decade | Films | With synopsis | % synopsis | People | With biography | % bio |
|--------|------:|--------------:|-----------:|-------:|---------------:|------:|
| 1980s  |  1403 |          1182 |       84.2 |   2901 |           2356 |  81.2 |
| 1990s  |  1432 |          1244 |       86.9 |   2651 |           2211 |  83.4 |
| 2000s  |  1443 |          1283 |       88.9 |   2593 |           2179 |  84.0 |
| 2010s  |  1594 |          1351 |       84.8 |   2955 |           2277 |  77.1 |
| 2020s  |   948 |           791 |       83.4 |   2149 |           1641 |  76.4 |

Synopses per genre (lowest coverage first):

| Genre       | Rows | With synopsis |    % |
|-------------|-----:|--------------:|-----:|
| Game-Show   |    3 |             0 |  0.0 |
| Talk-Show   |   18 |             0 |  0.0 |
| Reality-TV  |   66 |             4 |  6.1 |
| News        |  139 |            20 | 14.4 |
| Documentary |  460 |           223 | 48.5 |
| Western     |  407 |           199 | 48.9 |
| Musical     |  460 |           381 | 82.8 |
| Sport       |  460 |           382 | 83.0 |
| War         |  460 |           394 | 85.7 |
| History     |  460 |           408 | 88.7 |
| Music       |  460 |           410 | 89.1 |
| Animation   |  460 |           434 | 94.3 |
| Biography   |  460 |           439 | 95.4 |
| Family      |  460 |           447 | 97.2 |
| Fantasy     |  460 |           448 | 97.4 |
| Horror      |  460 |           454 | 98.7 |
| Sci-Fi      |  460 |           455 | 98.9 |
| Romance     |  460 |           455 | 98.9 |
| Crime       |  460 |           456 | 99.1 |
| Thriller    |  460 |           457 | 99.3 |
| Drama       |  460 |           457 | 99.3 |
| Mystery     |  460 |           458 | 99.6 |
| Comedy      |  460 |           458 | 99.6 |
| Adventure   |  460 |           458 | 99.6 |
| Action      |  460 |           459 | 99.8 |

Length of the collected texts (words):

| Text                             | Count | Median words | 10th pct | 90th pct |  Max |
|----------------------------------|------:|-------------:|---------:|---------:|-----:|
| Synopsis (Plot section)          |  5851 |          604 |      202 |      740 | 2355 |
| Biography (article introduction) |  7884 |           92 |       26 |      309 |  732 |

### Output and lineage

Films table:

| Column        | Type   |
|---------------|--------|
| tconst        | string |
| primaryTitle  | string |
| year          | int32  |
| genre         | string |
| rank          | int32  |
| averageRating | double |
| numVotes      | int32  |
| synopsis      | string |
| source_url    | string |
| retrieved_at  | string |
| note          | string |

People table:

| Column       | Type   |
|--------------|--------|
| nconst       | string |
| tconst       | string |
| category     | string |
| ordering     | int32  |
| primaryName  | string |
| birthYear    | int32  |
| deathYear    | int32  |
| biography    | string |
| source_url   | string |
| retrieved_at | string |
| note         | string |

Sample rows (synopsis cut to 70 characters here):

| tconst    | primaryTitle             | year | genre    | synopsis                                                                  | source_url                                             | retrieved_at              | note                              |
|-----------|--------------------------|-----:|----------|---------------------------------------------------------------------------|--------------------------------------------------------|---------------------------|-----------------------------------|
| tt0111161 | The Shawshank Redemption | 1994 | Drama    | In 1947, Portland, Maine, banker Andy Dufresne arrives at Shawshank St... | https://en.wikipedia.org/wiki/The_Shawshank_Redemption | 2026-11-14T14:53:13+00:00 |                                   |
| tt0468569 | The Dark Knight          | 2008 | Crime    | A gang of masked criminals rob a mafia-owned bank in Gotham City, betr... | https://en.wikipedia.org/wiki/The_Dark_Knight          | 2026-11-14T14:47:18+00:00 |                                   |
| tt0468569 | The Dark Knight          | 2008 | Thriller | A gang of masked criminals rob a mafia-owned bank in Gotham City, betr... | https://en.wikipedia.org/wiki/The_Dark_Knight          | 2026-11-14T14:47:18+00:00 |                                   |
| tt0401792 | Sin City                 | 2005 | Thriller |                                                                           | https://en.wikipedia.org/wiki/Sin_City_%28film%29      | 2026-11-14T14:41:44+00:00 | article found but no Plot section |
| tt0892255 | Che: Part One            | 2008 | History  |                                                                           |                                                        |                           | no English Wikipedia article      |

### Methodological Explanation

**Scope.** We enrich the feature films defined in Part 2, released between 1980 and 2025. For each genre and year we keep the 10 films with the most votes, and ties are broken by `tconst` so that the selection is the same on every run. There are 1,027 genre-year groups, 68 of which contain fewer than 10 films, which gives 9,833 rows instead of 10,270. Since a film can be in the top 10 of several genres, this is 6,820 distinct films. For each film we take the first three principals in IMDb's ordering, actors, actresses and directors first, then whoever comes next when one is missing (`self` in documentaries, for example). A voice actor credited for several characters counts once. This gives 10,452 distinct people, and 23 films have fewer than three principals in IMDb itself.

**Source and link.** The assignment asks for open text written by humans. English Wikipedia fits both: articles are written and reviewed by volunteers and published under CC BY-SA. To find the right page we go through Wikidata (CC0), where property P345 stores the IMDb identifier and the sitelink points to the English article, so the match is exact. Our first version (PR #8) searched by title instead, on the REST `page/summary` endpoint, for the 200 most-voted titles (movies and TV series together) and 200 people. It tried candidates like `Title_(2010_film)`, `Title_(film)`, `Title_(TV_series)` and the bare title. Guessing titles breaks on remakes and homonyms, and that endpoint returns the introduction of the article, not the synopsis, so we dropped it.

**Content.** For a film, the introduction mostly covers cast, release and reception. The synopsis is in a section called Plot, Synopsis, Plot summary, Premise or Story, so we extract that section as plain text with the `extracts` API (median 604 words). For a person it is the other way round: the introduction (`exintro`) is already a short biography (median 92 words), and the full article would be far too long.

**Collection.** Collection runs outside Spark in `wiki_texts.py`, as the assignment allows, and follows Wikimedia's rules. Requests are sent one at a time, never in parallel, with a User-Agent that names the project and gives the repository URL. On Wikipedia requests we set `maxlag=5`, so the server can refuse when it is loaded. On a 429 or a maxlag reply the code waits for the `Retry-After` delay (10 s by default), and network errors are retried up to 5 times with a wait that doubles from 5 to 80 s. Wikidata is queried through SPARQL in batches of 200 identifiers, with a 1 s pause and the same 429 handling. Wikipedia gets one page per request for synopses, because the full article is needed, and 20 per request for biographies, with a 0.2 s pause. Every response is cached in JSONL files, so a new run only asks for what is missing.

**Spark.** Everything after collection happens in Spark (`build.py`). The JSONL files are read with an explicit schema, the text is cleaned (repeated spaces and line breaks collapsed, reference marks like `[12]` removed, empty text set to null) and duplicates are dropped on the identifier. The result is joined with the selection and with `name.basics`. Every row that has a text carries its lineage, `source_url` and `retrieved_at`. Every row without one carries a note instead: "no English Wikipedia article", "article found but no Plot section" or "not looked up yet". Rows with the second note still keep their `source_url`, so we know which page was checked. We checked that no `[n]` mark is left, that a note exists exactly when the text is missing, and that every text has a URL.

**Coverage and scaling.** 89.0% of the film-genre rows have a synopsis (85.8% of distinct films): 492 films have no English article and 477 have an article without a plot section. Coverage is very uneven by genre, from 99.8% for Action to 48.5% for Documentary and almost nothing for News, Reality-TV, Game-Show and Talk-Show. The causes differ. In Documentary, 202 of the 237 rows without a synopsis do have an English article, but a documentary has no plot to summarise. In News, Reality-TV, Talk-Show, Game-Show and Western the main cause is the missing English article (179 of the 208 missing Western rows, for example), and there the gap does come from relying on a single source in a single language. 75.4% of people have a biography, with directors (60.1%) well behind actresses (81.1%) and actors (78.4%). We accepted these gaps because most rows are covered and every gap is labelled. Nothing in the code is specific to these 6,820 films. The selection is driven by `--start`, `--end`, `--top` and `--people`, and the collector reads any list of identifiers from Parquet. The first pass took about 1 h 30. On the full dataset the limit would not be Spark but the request rate, which we keep low on purpose, and the cache lets a long collection be stopped and resumed.

## 4. Streaming

lets start with the Architecture of the pipeline .......
the live treatment pipeline is built on the continuous feeding of wikipedia pages modifications and their links with a IMDB reference. 

First, we use Kafka as a broker with a producer script  that listen the continuous public flow of recents wikipedia modifications and publish each events in wikipedia-changes. then our Spark motor, fed by this contnent link the title of each modificated pages with one of our reference tables from IMDB ( 24244 movies and 47899 personnas). To avoid the false positive, a filter analyse the () in the end of titel like we could have on Alien ( franchise). this process help us to avoid generic pages or homonymes. our validated links are then stocked in a 30 minutes sliding window ( with a 5 minutes jump ), as soon as a frame reach the critical points defined by --min-matches, it gets flagged. 

on our collect session that lasted 26 minutes, the pipeline recorded different metrics : first a global volume of 2190 events passed by KAFKA the only 63 events matched with our IDMB base ( 2.9%). those 63 events are divided in 2 categories : 28 are linked to personalities and about 35 are linked to movies. those 63 event reprensent 47 wikipedia pages. 

only 3 windows were written and all passed over the critical point :

18:25 - 18:55 : 15 matchs
18:30 - 19:00 : 27 matchs
18:35 - 19:05 : 40 matchs

we justify our kafak /spark methodology by two main reasons : 

First kafka act like a buffer between the data source and the calculus. if the spark treatment is interrupted or restrating, the messages are still conserved in kafka and the treatment restart exactly where the last offset was validated. 

the econd reason is more technical : Kafka is better in transport and flux retetion in high speed while spark have enough processing power for complex joins and aggregations. Furthermore, using Spark Structured Streaming makes it possible to use the same DataFrame API as for batch processing, facilitating the direct reuse of the IMDb tables prepared upstream.

we choosed a stream static - broadcast joint to avoid the shuffle. when we broadcast a full copy of IMDB on the memory f each worker node, each coming event is compared locally. this system avoid spark to redistribute all the data flow on the shuffle by joints keys. 

we also choosed sliding windows for 2 reason : 

Sliding windoxs are more interesting than tumbling windows ( who cut the time in blocs and can mask the A peak of activity if it straddles two intervals) because  the sliding window (30 minutes wide, 5-minute step) always assure a continuous coverage. 

we also choosed tge sliding windows for the accuracy because 1 same event could be considered in 6 windows that are working at the same time. even if this increase the work of the CPU to keep the windows active this way is way better to observe meticulously the evolution of trends and to set the flagged alarm as soon as the ccritical point is hit. 

we also choosed to put the watermark at 10 minutes because this timeframe is perfect to avoid loosing some data ! 
since the wikipedia flow is almost instant, a timeframe to short like 1 minute would make us loose all the data that is being slowed by the network and a timeframe too long ( 1 hour) would just delay unnecessarily the publication of results and increase memory usage.

to conclude this chapter lets analyze the 3 windows result : 
Only 3 windows have been opened : this is explained by the combination of the time of the first match, the position of the watermark, and the writing mode used:

on the Lower bound, The first IMDb match was recorded at 18:50:16. Any window ending before this time being empty, the first relevant window is the one covering 18:25 – 18:55

On the Upper bound and Append mode: The last event of the test was captured at 19:15:51, placing the final watermark around 19:05:51. In append output mode, Spark guarantees the immutability of results: it only writes a window once the watermark has strictly passed its end. Only the windows ending at 18:55, 19:00, and 19:05 met this condition at the time the pipeline stopped. The following windows (19:10, 19:15, etc.) were still waiting to close in memory.

But there is some limits to this exeriment :

on a windows of 26 minutes, the watermark blocks the export on the last minutes of activity. A longer execution time or a change in the update mode would make us able to observe more windows. 

the size of the sample is also too small : the analysis is done on a small batch of data that doesnt represent the general statistics on Wikipedia's overall activity.

and our last liimits is obviously the IMDb reference bias: Since the reference table is filtered to movies and personalities that received the most votes, the pipeline  ignores changes related to more rare or recent works, which partly explains the 2.9% match rate.

## 5. Open question

### 5.1 Do director-actor duos make better films together?

Some directors keep coming back to the same actor: Kurosawa and Mifune, Scorsese and De Niro. Film history treats these pairs as something special, and we wanted to check it on the whole dataset: are the films a duo makes together rated higher than what each of them does separately? The question needs no data outside IMDb, but it joins five tables and compares each pair with two separate filmographies.

All duos:

| Duos | Directors | Actors | Avg duo rating | Avg baseline | Avg lift | Median lift | % duos better |
|-----:|----------:|-------:|---------------:|-------------:|---------:|------------:|--------------:|
| 4646 |      1401 |   3367 |           6.64 |         6.45 |    0.188 |         0.2 |          65.7 |

Lift by number of films made together:

| Films together | Duos | Avg duo rating | Avg baseline | Avg lift | Median lift | % duos better |
|----------------|-----:|---------------:|-------------:|---------:|------------:|--------------:|
| 3              | 2829 |           6.63 |         6.45 |    0.185 |       0.191 |          65.0 |
| 4-5            | 1382 |           6.63 |         6.44 |    0.190 |       0.205 |          65.8 |
| 6+             |  435 |           6.66 |         6.46 |    0.203 |       0.235 |          69.7 |

Distribution of the lift:

| Lift       | Duos |    % |
|------------|-----:|-----:|
| below -1   |  115 |  2.5 |
| -1 to -0.5 |  314 |  6.8 |
| -0.5 to 0  | 1142 | 24.6 |
| 0 to 0.5   | 1792 | 38.6 |
| 0.5 to 1   |  989 | 21.3 |
| 1 or more  |  294 |  6.3 |

Lift by decade of the first film together:

| First film | Duos | Avg lift | % duos better |
|------------|-----:|---------:|--------------:|
| 1920s      |   38 |    0.025 |          50.0 |
| 1930s      |  308 |    0.098 |          61.7 |
| 1940s      |  247 |    0.170 |          69.6 |
| 1950s      |  275 |    0.148 |          65.8 |
| 1960s      |  359 |    0.138 |          62.4 |
| 1970s      |  431 |    0.243 |          69.8 |
| 1980s      |  472 |    0.302 |          73.7 |
| 1990s      |  691 |    0.289 |          74.5 |
| 2000s      |  956 |    0.212 |          63.9 |
| 2010s      |  791 |    0.097 |          56.5 |
| 2020s      |   69 |   -0.199 |          42.0 |

Duos with the most films together:

| Director        | Actor            | Films | First | Last | Duo avg | Director apart | Actor apart | Baseline |  Lift |
|-----------------|------------------|------:|------:|-----:|--------:|---------------:|------------:|---------:|------:|
| Kartal Tibet    | Kemal Sunal      |    26 |  1976 | 1990 |    6.91 |           5.40 |        7.36 |     6.38 |  0.53 |
| Gerald Thomas   | Kenneth Williams |    25 |  1958 | 1978 |    6.12 |           5.49 |        5.75 |     5.62 |  0.51 |
| Gerald Thomas   | Joan Sims        |    25 |  1959 | 1978 |    6.04 |           5.80 |        6.62 |     6.21 | -0.17 |
| Gerald Thomas   | Charles Hawtrey  |    23 |  1958 | 1972 |    6.29 |           5.21 |        5.60 |     5.41 |  0.88 |
| Gerald Thomas   | Sidney James     |    21 |  1960 | 1974 |    6.27 |           5.45 |        6.67 |     6.06 |  0.21 |
| Johnnie To      | Suet Lam         |    20 |  1998 | 2016 |    6.78 |           6.66 |        5.90 |     6.28 |  0.49 |
| Yasujirō Ozu    | Chishū Ryū       |    20 |  1930 | 1962 |    7.66 |           7.33 |        7.82 |     7.57 |  0.09 |
| Akira Kurosawa  | Takashi Shimura  |    19 |  1943 | 1963 |    7.57 |           7.49 |        6.68 |     7.09 |  0.49 |
| Kunihiko Yuyama | Ikue Otani       |    18 |  1998 | 2019 |    6.03 |           5.73 |        6.80 |     6.26 | -0.23 |
| Gerald Thomas   | Kenneth Connor   |    17 |  1958 | 1978 |    5.86 |           6.12 |        6.00 |     6.06 | -0.20 |
| David Dhawan    | Govinda          |    16 |  1990 | 2009 |    6.00 |           4.95 |        5.62 |     5.29 |  0.71 |
| Akira Kurosawa  | Toshirō Mifune   |    16 |  1948 | 1965 |    7.81 |           7.25 |        7.13 |     7.19 |  0.62 |
| Priyadarshan    | Mohanlal         |    15 |  1985 | 2021 |    7.51 |           6.61 |        6.87 |     6.74 |  0.77 |
| Ertem Eğilmez   | Adile Naşit      |    15 |  1972 | 1984 |    8.00 |           7.48 |        7.38 |     7.43 |  0.57 |
| Claude Chabrol  | Stéphane Audran  |    15 |  1959 | 1992 |    6.94 |           6.69 |        6.39 |     6.54 |  0.40 |

Highest lift (duos with 5 films or more):

| Director                 | Actor            | Films | First | Last | Duo avg | Director apart | Actor apart | Baseline | Lift |
|--------------------------|------------------|------:|------:|-----:|--------:|---------------:|------------:|---------:|-----:|
| Kevin Smith              | Brian O'Halloran |     5 |  1994 | 2022 |    7.14 |           5.86 |        4.50 |     5.18 | 1.96 |
| Tigmanshu Dhulia         | Rajiv Gupta      |     5 |  2003 | 2013 |    7.32 |           5.80 |        5.11 |     5.46 | 1.86 |
| Kevin Smith              | Jason Mewes      |     5 |  1994 | 2022 |    7.00 |           5.93 |        4.45 |     5.19 | 1.81 |
| Rainer Werner Fassbinder | Ulli Lommel      |     7 |  1969 | 1976 |    6.67 |           7.19 |        2.90 |     5.05 | 1.62 |
| Anthony Russo            | Chris Evans      |     5 |  2014 | 2022 |    7.76 |           6.10 |        6.41 |     6.26 | 1.50 |
| Joe Russo                | Chris Evans      |     5 |  2014 | 2022 |    7.76 |           6.10 |        6.41 |     6.26 | 1.50 |
| Peter Jackson            | Ian McKellen     |     6 |  2001 | 2014 |    8.28 |           7.29 |        6.40 |     6.85 | 1.44 |
| Hansal Mehta             | Rajkummar Rao    |     5 |  2012 | 2020 |    7.38 |           5.45 |        6.44 |     5.95 | 1.43 |
| Neeraj Pandey            | Anupam Kher      |     5 |  2008 | 2018 |    7.46 |           6.10 |        6.09 |     6.10 | 1.36 |
| Mehmet Ada Öztekin       | Sarp Akkaya      |     6 |  2017 | 2024 |    7.37 |           6.85 |        5.16 |     6.00 | 1.36 |

Lowest lift (duos with 5 films or more):

| Director          | Actor             | Films | First | Last | Duo avg | Director apart | Actor apart | Baseline |  Lift |
|-------------------|-------------------|------:|------:|-----:|--------:|---------------:|------------:|---------:|------:|
| Edward Drake      | Bruce Willis      |     7 |  2021 | 2023 |    3.46 |           5.05 |        5.68 |     5.36 | -1.91 |
| Juan Piquer Simón | Frank Braña       |     5 |  1979 | 1992 |    3.88 |           5.30 |        5.78 |     5.54 | -1.66 |
| Ram Gopal Varma   | Amitabh Bachchan  |     8 |  2005 | 2017 |    5.21 |           6.59 |        6.49 |     6.54 | -1.32 |
| Edward Drake      | Lochlyn Munro     |     5 |  2021 | 2023 |    3.38 |           4.35 |        5.00 |     4.68 | -1.30 |
| Neri Parenti      | Christian De Sica |    12 |  1985 | 2008 |    4.40 |           6.02 |        5.33 |     5.68 | -1.28 |
| Roger Corman      | Ed Nelson         |     5 |  1956 | 1959 |    4.30 |           5.61 |        5.52 |     5.57 | -1.27 |
| Dario Argento     | Asia Argento      |     6 |  1993 | 2022 |    4.98 |           6.45 |        5.77 |     6.11 | -1.12 |
| Orhan Aksoy       | Kemal Sunal       |     5 |  1987 | 1991 |    6.36 |           7.64 |        7.27 |     7.46 | -1.10 |
| Albert Pyun       | Norbert Weisser   |     8 |  1984 | 2005 |    4.32 |           4.08 |        6.65 |     5.36 | -1.04 |
| Robert Rodriguez  | Alexa PenaVega    |     5 |  2001 | 2013 |    4.92 |           6.34 |        5.56 |     5.95 | -1.03 |

**Key takeaways.** The lift of a duo is the average rating of its films together minus the average of the director's and the actor's separate filmographies (see **Lift** below). There are 4,646 duos. The average lift is +0.188, with a 95% confidence interval from +0.172 to +0.204. 3,039 duos (65.4% on rounded lifts, 65.7% on exact ones as in the table) do better together, 1,571 do worse and 36 round to zero, and a sign test gives z = 21.6, so this is not chance. The effect is real, but small on a 10-point scale. Only 6.3% of duos gain a full point or more. The stricter test gives the same direction: 48.6% of duos beat both of their separate averages, against 21.0% that fall below both. The number of films together barely matters. The lift goes from +0.185 at three films to +0.203 at six or more, and duo by duo the correlation is 0.01. The two pairs from the introduction are in the data and fit the popular idea: Kurosawa and Mifune (16 films, +0.62), Scorsese and De Niro (10 films, +0.84). Peter Jackson and Ian McKellen go further (6 films, +1.44). Edward Drake and Bruce Willis (7 films in 2021-2023, -1.91) show the opposite case. By decade of first collaboration the lift peaks in the 1980s and 1990s (around +0.30) and drops afterwards, down to -0.20 for the 2020s, on only 69 duos.

#### Methodological Explanation

**Data and definition.** The query joins `title.basics` (the feature films of Part 2), `title.ratings`, `title.crew` for directors, `title.principals` for actors and actresses, and `name.basics` for names. We keep films with at least 1,000 votes (`--min-votes`). That is stricter than in most of Part 2, because a duo's average can rest on only three films and each rating has to be reliable. A duo is a director and an actor with at least 3 feature films together (`--min-films`): two films can be a coincidence or a sequel, three starts to look like a habit. Someone who directs themselves is not a duo, and two co-directors count as two duos.

**Lift.** For each duo we compute the average rating of their films together, then subtract a baseline. The baseline is the mean of two numbers: the director's average without this actor, and the actor's average without this director. Each of them needs at least 2 films outside the duo (fixed in the code), or there is nothing to compare with. We gave the two sides equal weight on purpose. If we had pooled all their other films, a director with forty films would have decided the baseline almost alone. A positive lift means the pair does better together than apart.

**Limits.** The lift is not a causal effect. People usually keep working together because their first films did well, so duos that reach three films are already a selected group. We also checked regression to the mean in a simple way. If the lift came only from pairs starting from a low baseline, it would fall steadily as the baseline rises. By baseline quartile the lift is +0.17, +0.23, +0.22 and +0.13. It is lowest in the top quartile, but it rises before it falls, and the correlation between baseline and lift is 0.02. So the data show no clear trend, which is a weaker statement than saying the lift does not decline. As everywhere in this report, the IMDb rating is the only measure of quality.

**Alternatives.** A regression with one fixed effect per director and per actor would separate each person's own level from the pair more cleanly, especially for directors in dozens of duos like Michael Curtiz (37). It is harder to explain, and with three films per duo the pair effect would rest on very little. Comparing films before and after the first collaboration would get closer to causality, but ratings also move with age and period, so the comparison would mix the two. Weighting by votes would let one blockbuster decide a duo's average, and the 1,000-vote minimum already removes unreliable ratings.

**Relation to 5.2.** Section 5.2 looks at the same effect by decade and by genre, with a different definition: two films together within the same decade or genre, all movie titles, directors taken from `title.principals`, a pooled baseline, and people who direct themselves are not excluded. The two sections therefore do not measure exactly the same thing, and their figures should not be compared directly.

### 5.2 Duo effect by decade and genre

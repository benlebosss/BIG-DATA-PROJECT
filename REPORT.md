# REPORT

## 1. Data preparation

## 2. Data exploration

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

### Q7. Long careers whose ratings peaked early

5522 actors and actresses found. The 15 largest drops:

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

## 4. Streaming

## 5. Open question

### 5.1 Do director-actor duos make better films together?

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

#### Methodological Explanation

### 5.2 Duo effect by decade and genre

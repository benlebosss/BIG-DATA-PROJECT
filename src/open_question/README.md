# Open question: director-actor duos

`python -m src.open_question.duos_by_period`

Effect of a duo = mean rating of their joint films minus mean rating of the other films of both members, computed inside one decade or one genre.
Filters: movies with at least 1000 votes, duos with at least 2 joint films and 2 separate films in the group.
Results: results/open_question/duo_effect_by_decade.csv and duo_effect_by_genre.csv.

## Columns

duos: number of duos in the group. mean_effect and median_effect: joint average minus separate average, in rating points. share_positive: share of duos whose joint films are rated higher. avg_joint_films: average number of joint films per duo.

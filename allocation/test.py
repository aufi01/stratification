treatment = allocate(players=players,
                     var_names=['sex', 'education'],
                     var_ordinal={'education': Constants.education_selection},
                     treatment_labels=Constants.treatment_labels)
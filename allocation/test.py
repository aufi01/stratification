sex_selection = ['male', 'female']
age_selection = []
education_selection = ['Primary education', 'Secondary Education', 'Bachelor Degree', 'Master Degree',
                       'Doctoral Degree']
occupation_selection = ['Agricultural', 'Education', 'Entertainment', 'Illegal', 'Service']
income_selection = ['< 10,000', '10,000 - 20,000', '20,000 - 40,000', '40,000 - 60,000', '> 60,000']
previous_donation_selection = ['0', '1 - 500', '500 - 2,000', '2,000 - 5,000', '> 5,000']
var_names = ['sex', 'age', 'education', 'occupation', 'income', 'previous_donation']
var_ordinal = {'education': education_selection, 'income': income_selection, 'previous_donation':
    previous_donation_selection}

sample_size = len(players)
num_covariates = len(var_names)

def axess_data(player_nr, var_name, players=players):
    temp = eval("players[player_nr]." + var_name)
    return temp


for i in range(len(var_names)):
    temp_col = prelim_matrix[:, i]
    if var_names[i] in var_cardinal:
        df = pd.DataFrame(temp_col, columns=['temp'])
        df_temp = pd.get_dummies(df['temp'])
        mat_temp = df_temp.as_matrix(columns=None)
        final_matrix = np.column_stack((final_matrix, mat_temp[:, -0]))
    elif var_names[i] in var_ordinal.keys():
        df_temp = pd.Categorical(list(temp_col.A1), categories=var_ordinal[var_names[i]], ordered=True)
        df_temp = pd.Series(df_temp)
        df_temp = df_temp.cat.rename_categories(list(range(len(var_ordinal[var_names[i]]))))
        mat_temp = df_temp.as_matrix(columns=None)
        final_matrix = np.column_stack((final_matrix, mat_temp))
    else:
        temp_col = temp_col.astype(np.float)
        mat_temp = temp_col
        final_matrix = np.column_stack((final_matrix, mat_temp))
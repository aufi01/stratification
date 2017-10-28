import pandas as pd
import numpy as np
import random as r
import math as m

covariate_matrix = np.matrix("1 2; 3 4; 1 6; 1 7")
var_names = ['sex', 'age']
prelim_matrix= np.matrix("1 2; 3 4; 5 6; 6 7; 8 9; 10 11; 12 13; 14 15")


def allocate(players, var_names,  var_ordinal = None, var_cardinal = None, treatment_labels = None):
    if not treatment_labels is None:
        if not len(treatment_labels) ==2:
            raise Exception("Length of treatment labels has to be equal to number of treatment groups (in this case 2).")

    sample_size = len(players)
    num_covariates = len(var_names)

    def axess_data(player_nr, var_name, players=players):
        temp = eval("players[player_nr]." + var_name)
        return temp

    # Store covariates in matrix
    prelim_matrix = np.matrix([[axess_data(i, j) for j in var_names] for i in range(len(players))])
    final_matrix = np.zeros((sample_size,1)) # will be later changed to numpy matrix

    if var_ordinal is None:
        var_ordinal = dict()
    if var_cardinal is None:
        var_cardinal = list()
        for name in var_names:
            if (not name in var_ordinal.keys()) and (not name in var_cardinal):
                if isinstance(axess_data(0,name), str):
                    var_cardinal.append(name)

    for i in range(len(var_names)):
        temp_col = prelim_matrix[:,i]
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

    final_matrix = final_matrix[:,1:]

    alloc, strata = stratification(final_matrix)

    if not treatment_labels is None:
        for i in range(sample_size):
                alloc[i] = treatment_labels[alloc[i]]

    for i in range(sample_size):
        players[i].stratum = strata[i]

    return(alloc)




def random(covariate_matrix, last_subject="random"):
    # This function returns a random treatment allocation that allocates half of the subjects to
    # the treatment group and the other half to the control group
    # The number of subject to be allocated is determined by the number of columns in the covariate matrix
    # last_subject: In case of odd sample sizes: Should the last subject be allocated randomly "random",
    # to the treatment group "treatment", or to the control group "control"
    sample_size = len(covariate_matrix[:, 0])
    unassigned_participants = list(range(sample_size))

    def assign_treatment(unassigned_participants):
        rm = m.floor(len(unassigned_participants) * r.random())
        participant = unassigned_participants[rm]
        unassigned_participants.pop(rm)
        return participant

    assigned_participants = [assign_treatment(unassigned_participants) for x in list(range(m.floor(sample_size / 2)))]
    if sample_size % 2 == 1:
        if last_subject == "random":
            if r.random() > 0.5: assigned_participants.append(assign_treatment(unassigned_participants))
        elif last_subject == "treatment":
            assigned_participants.append(assign_treatment(unassigned_participants))
        elif last_subject == "control":
            pass
        else:
            raise Exception(
                "Variable last_subject in function allocation.random can only take the values random, treatment or control")
    alloc = [0] * sample_size
    for x in assigned_participants:
        alloc[x - 1] = 1
    return alloc


def stratification(covariate_matrix):
    # To Do: Check data types: If they are categorical, they should not be further discretized
    binary_matrix = covariate_matrix.copy()
    num_covariates = len(covariate_matrix[0].A1)
    sample_size = len(covariate_matrix[:, 0])
    cardinal = [i for i in range(num_covariates) if len(np.unique(list(covariate_matrix[:, i]))) > 2] # all variables that are not dummies

    for i in cardinal:
        q = np.percentile(covariate_matrix[:, i], 50)
        temp = np.array([0] * sample_size)
        temp[covariate_matrix[:, i].A1 > q] = 1
        binary_matrix[:, i] = np.matrix(temp).T

    blocks = list()
    block_names = list()

    for i in range(sample_size):
        temp_block_name = list(binary_matrix[i, :].A1)
        if temp_block_name in block_names:
            temp_index = block_names.index(temp_block_name)
            blocks[temp_index].append(i)
        else:
            blocks.append([i])
            block_names.append(temp_block_name)

    alloc = [0] * sample_size
    r.shuffle(blocks)
    tr_assigned = list()

    for i in range(len(blocks)):
        temp = blocks[i]
        if tr_assigned.count(0) == tr_assigned.count(1):
            temp_alloc = random(np.matrix(temp).T, last_subject="random")
        elif tr_assigned.count(0) > tr_assigned.count(1):
            temp_alloc = random(np.matrix(temp).T, last_subject="treatment")
        else:
            temp_alloc = random(np.matrix(temp).T, last_subject="control")
        for j in range(len(temp)):
            tr_assigned.append(temp_alloc[j])
            alloc[temp[j]] = temp_alloc[j]

    strata = [0]*sample_size
    for i in range(len(blocks)):
        for j in range(len(blocks[i])):
            strata[blocks[i][j]] = i


    return alloc, strata


stratification(covariate_matrix)

##################################################################################################
# Provides functionality for allocating treatments in oTree apart from pure random allocation
##################################################################################################
# Author: Tobias Aufenanger, David Hardt
# Date: 2017/12
##################################################################################################

# Up to now this file contains three functions.
#
# The function 'allocate' transfers the player objects  out of oTree into a numeric covariate matrix and returns the
# treatment allocation either as a boolean vector or as a vector of strings indicating the treatment status.
# The numeric covariate matrix is the basis of every sytematic treatment allocation algorithm.
# Up to now, we only implemented a simple stratification algorithm.
#
# The function 'stratify' provides the stratification functionality for the 'allocate' function.
# This function takes a numeric covariate matrix as input an returns the treatment allocation as a boolean vector.
#
# The function 'random' randomly allocates exactly half of the subjects to the treatment group and the other half
# to the control group. This function is used by 'stratify'.

###################################################################################################
# import packages
import pandas as pd
import numpy as np
import random as r
import math as m

###################################################################################################


def allocate(players, var_names,  var_ordinal = None, var_cardinal = None, treatment_labels = None):
    # This function takes the player objects from oTree and returns the treatment allocation for the participants
    # Parameters:
    # players: The oTree object containing all player objects. In the oTre views file, this object can be received via
    #          the method self.group.get_players()
    # var_names: The names of all covariates that should be considered for allocating treatments
    # var_ordinal: A dictionary containing all ordinal variables. Per default, all covariates with
    #              numerical entries are seen as ordinal. Whenever a covariate contains string, but it is possible to
    #              define an order on those string, this covariate has to be listed here or otherwise it will be treated
    #              as a cardinal covariate.
    #              The dictionary containing the ordinal covariates should be structured as follows:
    #              Each key of the dictionary is the name of an ordinal variable.
    #              Each value is the a list or an array containing all categories of the corresponing variable in the
    #              right order.
    #              Whether the order is increasing or decreasing does not matter.
    # var_cardinal: The names of all cardinal covariates. Per default all covariates containing numerical entries
    #               are seen as ordinal. All covariates containing strings are seen as cardinal. Whenever a covariate
    #               contains numerical entries but nevertheless it is impossible to define an order on the entries,
    #               the covariate should be listed here. This function transferrs all cardinal covariates into
    #               dummy variables.
    # treatment_labels:  A list of the same length as the number of treatments
    #                    containing the names of the different treatments.
    #                    If the treatment status should not be indicated by a number, but by a string one should
    #                    specify this parameter.
    ###########################################
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
            df_temp = pd.Categorical(list(temp_col.A1), categories=list(var_ordinal[var_names[i]]), ordered=True)
            df_temp = pd.Series(df_temp)
            df_temp = df_temp.cat.rename_categories(list(range(len(var_ordinal[var_names[i]]))))
            mat_temp = df_temp.as_matrix(columns=None)
            final_matrix = np.column_stack((final_matrix, mat_temp))
        else:
            temp_col = temp_col.astype(np.float)
            mat_temp = temp_col
            final_matrix = np.column_stack((final_matrix, mat_temp))

    final_matrix = np.matrix(final_matrix[:,1:])

    alloc, strata = stratification(final_matrix)

    if not treatment_labels is None:
        for i in range(sample_size):
                alloc[i] = treatment_labels[alloc[i]]

    for i in range(sample_size):
        players[i].stratum = strata[i]

    return(alloc)




def stratification(covariate_matrix):
    # This function takes a covariate matrix and returns a treatment allocation that stratifies on all covariates.
    # All covariates that are not already dummy variables are discretized, such that all valuas above the median
    # are set to 1 and all values below the median to 0.
    binary_matrix = covariate_matrix.copy()
    num_covariates = len(covariate_matrix[0].A1)
    sample_size = len(covariate_matrix[:, 0])
    ordinal = [i for i in range(num_covariates) if len(np.unique(list(covariate_matrix[:, i]))) > 2] # all variables that are not dummies

    for i in ordinal:
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
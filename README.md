# Stratification for oTree
This repository contains a simple stratification method for oTree.

The repository contains the stratification functionality (in the file 'allocation'),
as well as simple exemplary experiment, demonstrating this functionality (in the files 'survey_test' and 'main_experiment_test').

Stratification requires the researcher to run a survey before allocating treatments.

The stratification function implemented here allows the researcher to select those 
variables out of the survey that should be used for stratification.

The function will partition the experimental sample into strata and allocate treatments
such that exactly half of the subjects in each stratum are allocated to the treatment
group and the other half to the control group.
In case of cardinal covariates, all subjects whose selected covariates are exactly equal, form one stratum.
For ordinal covariates, the function starts by discretizing the covariates such that all values above 
the median are set to one and all values below the median are set to zero. 
After that, the function proceeds similar to the case of cardinal covariates.

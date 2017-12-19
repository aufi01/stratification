from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)

import random

author = 'Tobias Aufenanger, David Hardt'

doc = """
Simple experiment to show the functionality of the stratification method.
The file 'suvey_test' contains s simple survey that is conducted before the main experiment.
"""



class Constants(BaseConstants):
    name_in_url = 'survey_test'
    players_per_group = None
    num_rounds = 1

    # Labels for treatments
    treatment_labels = ['treatment 1', 'treatment 2']

    # Answer categories for survey questions
    sex_selection = ['male', 'female']
    age_selection = []
    education_selection = ['Primary education', 'Secondary Education', 'Bachelor Degree', 'Master Degree',
                           'Doctoral Degree']
    occupation_selection = ['Agricultural', 'Education','Entertainment', 'Illegal', 'Service']
    income_selection = ['< 10,000', '10,000 - 20,000', '20,000 - 40,000', '40,000 - 60,000', '> 60,000']
    previous_donation_selection = ['0', '1 - 500', '500 - 2,000', '2,000 - 5,000', '> 5,000']
#    var_names = ['sex', 'age', 'education', 'occupation', 'income', 'previous_donation' ]
#    var_ordinal = {'education': education_selection, 'income': income_selection, 'previous_donation':
#                    previous_donation_selection}

class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass

class Player(BasePlayer):
    stratum = models.PositiveIntegerField()
    sex = models.CharField(choices=Constants.sex_selection,
        verbose_name='What is your sex?')
    age = models.PositiveIntegerField(max=100,
        verbose_name='What is your age?')
    education = models.CharField(choices=Constants.education_selection,
        verbose_name='What is your highest level of education?')
    occupation = models.CharField(choices=Constants.occupation_selection,
        verbose_name='What is your current type of occupation?')
    income = models.CharField(choices=Constants.income_selection,
        verbose_name='What is your annual income in Euro?')
    previous_donation = models.CharField(choices=Constants.previous_donation_selection,
        verbose_name='How many Euros have you donated last year?')

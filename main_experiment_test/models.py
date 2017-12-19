
from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)

import random

author = 'Tobias Aufenanger, David Hardt'

doc = """
Your app description
"""


class Constants(BaseConstants):
    name_in_url = 'main_experiment_test'
    players_per_group = None
    num_rounds = 1
    endowment = c(1)

class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    treatment = models.CharField()
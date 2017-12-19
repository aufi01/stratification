from otree.api import Currency as c, currency_range
from . import models
from ._builtin import Page, WaitPage
from .models import Constants

class Intro(Page):
    # RETRIEVE TREATMENT FORM PARTICIPANT OBJECT
    def before_next_page(self):
        from survey_test.models import Player as TreatmentPlayer
        self.player.treatment = self.participant.vars['treatment']

class ShowTreatment(Page):
    form_model = models.Player
    form_fields = ['treatment']



page_sequence = [
    Intro,
    ShowTreatment
]

from otree.api import Currency as c, currency_range
from . import models
from ._builtin import Page, WaitPage
from .models import Constants
from allocation.stratification import allocate #IMPORT FUNTIONALITY FOR ALLOCATION TREATMENTS

#IMPORT!

class AllocationSurvey(Page):
    form_model = models.Player
    form_fields = ['sex', 'age', 'education', 'occupation', 'income', 'previous_donation' ]

class SurveyWaitPage(WaitPage):
    # DETERMINE TREATMENT ALLOCATION
    def after_all_players_arrive(self):
        p = self.group.get_players()
        treatment = allocate(players=p,
                             var_names = ['sex', 'education'],
                             var_ordinal={'education': Constants.education_selection},
                             treatment_labels= Constants.treatment_labels)
        # STORE TREATMENT ALLOCATION IN PARTICIPANT OBJECT
        for i in range(len(p)):
            p[i].participant.vars['treatment'] = treatment[i]



page_sequence = [
    AllocationSurvey,
    SurveyWaitPage
]

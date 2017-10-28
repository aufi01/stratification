from otree.api import Currency as c, currency_range
from . import models
from ._builtin import Page, WaitPage
from .models import Constants
from allocation.stratification import allocate

#IMPORT!

class AllocationSurvey(Page):
    form_model = models.Player
    form_fields = ['sex', 'age', 'education', 'occupation', 'income', 'previous_donation' ]

class SurveyWaitPage(WaitPage):

    def after_all_players_arrive(self):
        p = self.group.get_players()
        treatment = allocate(p,
                             Constants.var_names,
                             var_ordinal=Constants.var_ordinal,
                             treatment_labels= Constants.treatment_labels)
        for i in range(len(p)):
            p[i].participant.vars['treatment'] = treatment[i]


class Results(Page):
    pass


page_sequence = [
    AllocationSurvey,
    SurveyWaitPage,
    #Results
]

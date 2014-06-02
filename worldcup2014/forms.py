from django import forms
from django.utils.safestring import mark_safe

from worldcup2014.models import Vote, Player, Team
from django.core.exceptions import ValidationError

## SENSOR
class VoteForm(forms.ModelForm):
    class Meta:
        model = Vote
        fields = ('match', 'user', 'striker', 'winner', 'score')
##icon = ChoiceField(choices=Player._meta.get_field_by_name('icon')[0].choices, 
 ##                  widget=IconPicker)

##    plan = forms.ModelChoiceField(queryset = Plan.objects.none()) 
      #  striker = forms.ModelChoiceField(queryset=None, empty_label=None)
        
    def __init__(self, *args, **kwargs):
        super(VoteForm, self).__init__(*args, **kwargs)
        self.fields['striker'].queryset = Player.objects.filter(id=1)
        self.fields['winner'].queryset = Team.objects.all()
        
        self.fields['match'].label = u'Match'
        self.fields['match'].widget.attrs['readonly'] = True

        self.fields['user'].label = u'User'
        self.fields['user'].required = True
        self.fields['user'].widget = forms.TextInput()
        self.fields['user'].widget.attrs['readonly'] = True

        self.fields['striker'].label = u'Striker'
        self.fields['striker'].required = True
       # self.fields['striker'].widget = forms.ChoiceField()#choices=self.fields['striker'].choices)

        self.fields['winner'].label = u'Winner'
        self.fields['winner'].required = True
 
        self.fields['score'].label = u'Score'
        self.fields['score'].required = True
        self.fields['score'].widget = forms.TextInput()


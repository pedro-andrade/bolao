from django import forms
from django.utils.safestring import mark_safe

from worldcup2014.models import Vote
from django.core.exceptions import ValidationError

## SENSOR
class VoteForm(forms.ModelForm):
    class Meta:
        model = Vote
        fields = ('match', 'user', 'striker', 'winner', 'score')

    def __init__(self, *args, **kwargs):
        super(VoteForm, self).__init__(*args, **kwargs)
        
        self.fields['match'].label = u'Match'
        self.fields['match'].required = True
        self.fields['match'].widget = forms.TextInput()

        self.fields['user'].label = u'User'
        self.fields['user'].required = True
        self.fields['user'].widget = forms.TextInput()

        self.fields['striker'].label = u'Striker'
        self.fields['striker'].required = True
        self.fields['striker'].widget = forms.TextInput()

        self.fields['winner'].label = u'Winner'
        self.fields['winner'].required = True
        self.fields['winner'].widget = forms.TextInput()

        self.fields['score'].label = u'Score'
        self.fields['score'].required = True
        self.fields['score'].widget = forms.TextInput()

 
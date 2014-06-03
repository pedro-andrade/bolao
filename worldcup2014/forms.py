from django import forms
from django.utils.safestring import mark_safe

from worldcup2014.models import Vote, Player, Team, Match
from django.core.exceptions import ValidationError


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

        instance = getattr(self, 'instance', None)
        
        self.fields['striker'].queryset = Player.objects.filter(team=instance.match.teamA) | Player.objects.filter(team=instance.match.teamB)
        self.fields['winner'].queryset = Team.objects.filter(name=instance.match.teamA.name) | Team.objects.filter(name=instance.match.teamB.name) | Team.objects.filter(name='-')
        
        if instance and instance.match:
            self.fields['match'].label = u'Match'
            self.fields['match'].required = False
            self.fields['match'].widget.attrs['disabled'] = True
        if instance and instance.user:
            self.fields['user'].label = u'User'
            self.fields['user'].required = False
            self.fields['user'].widget.attrs['disabled'] = True


        self.fields['striker'].label = u'Striker'
        self.fields['striker'].required = True

        self.fields['winner'].label = u'Winner'
        self.fields['winner'].required = True
 
        self.fields['score'].label = u'Score'
        self.fields['score'].required = True
        self.fields['score'].widget = forms.TextInput()


    def clean_match(self):
        if self.instance and self.instance.match:
            return self.instance.match
        else:
            return self.cleaned_data['match']        

    def clean_user(self):
        if self.instance and self.instance.user:
            return self.instance.user
        else:
            return self.cleaned_data['user']
                        
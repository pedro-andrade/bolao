from django import forms

from worldcup2014.models import Vote, Player, Team

class NoEmptyChoiceField(forms.ModelChoiceField): 

    def __init__(self, *args, **kwargs): 
        super(NoEmptyChoiceField, self).__init__(empty_label=None, *args, **kwargs) 
          
class VoteForm(forms.ModelForm):
    class Meta:
        model = Vote
        fields = ('striker', 'winner', 'score')
        exclude = ('match', 'user')
        
    def __init__(self, *args, **kwargs):
        super(VoteForm, self).__init__(*args, **kwargs)

        instance = getattr(self, 'instance', None)
        
        self.fields['striker'].queryset = Player.objects.filter(team=instance.match.teamA) | Player.objects.filter(team=instance.match.teamB)
        self.fields['winner'].queryset = Team.objects.filter(name=instance.match.teamA.name) | Team.objects.filter(name=instance.match.teamB.name) | Team.objects.filter(name='-')

        self.fields['striker'].label = u'Striker'
        self.fields['striker'].required = True

        self.fields['winner'].label = u'Winner'
        self.fields['winner'].required = True
 
        self.fields['score'].label = u'Score'
        self.fields['score'].required = True
        self.fields['score'].widget = forms.TextInput()
                        
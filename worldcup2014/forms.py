from django import forms

from worldcup2014.models import Vote, Player, Team, Match, ExtraVote, Comment

class NoEmptyChoiceField(forms.ModelChoiceField): 

    def __init__(self, *args, **kwargs): 
        super(NoEmptyChoiceField, self).__init__(empty_label=None, *args, **kwargs) 
          
class VoteForm(forms.ModelForm):
    class Meta:
        model = Vote
        fields = ('striker', 'winner', 'score')
        exclude = ('match', 'user')
        
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(VoteForm, self).__init__(*args, **kwargs)

        instance = getattr(self, 'instance', None)
        
        _team = Team.objects.get(name='-')
        self.fields['striker'].queryset = (Player.objects.filter(team=instance.match.teamA) | Player.objects.filter(team=instance.match.teamB) | Player.objects.filter(team=_team)).order_by('-team','name')
        self.fields['winner'].queryset = Team.objects.filter(name=instance.match.teamA.name) | Team.objects.filter(name=instance.match.teamB.name) | Team.objects.filter(name='-').order_by('name')

        self.fields['striker'].label = u'Striker'
        self.fields['striker'].required = True

        self.fields['winner'].label = u'Winner'
        self.fields['winner'].required = True
 
        self.fields['score'].label = u'Score'
        self.fields['score'].required = True
        self.fields['score'].widget = forms.TextInput()

class MatchForm(forms.ModelForm):
    class Meta:
        model = Match
#        fields = ('teamA', 'teamB', 'matchtime', 'winner', 'score', 'finish')
        fields = ('matchtime', 'winner', 'score', 'finish')
        
    def __init__(self, *args, **kwargs):
        super(MatchForm, self).__init__(*args, **kwargs)

        instance = getattr(self, 'instance', None)
        
        _team = Team.objects.get(name='-')
        self.fields['winner'].queryset = Team.objects.filter(name=instance.teamA.name) | Team.objects.filter(name=instance.teamB.name) | Team.objects.filter(name='-').order_by('name')

class ExtraVoteForm(forms.ModelForm):
    class Meta:
        model = ExtraVote
        fields = ('striker', 'winner')
        
    def __init__(self, *args, **kwargs):
        super(ExtraVoteForm, self).__init__(*args, **kwargs)

        self.fields['striker'].queryset = Player.objects.all().order_by('team','name')
        self.fields['winner'].queryset = Team.objects.all().order_by('name')
        
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('comment',)
        
    def __init__(self, *args, **kwargs):
        super(CommentForm, self).__init__(*args, **kwargs)
        
        self.fields['comment'].widget = forms.Textarea()
        self.fields['comment'].widget.attrs["cols"] = 200
        self.fields['comment'].widget.attrs["rows"] = 10
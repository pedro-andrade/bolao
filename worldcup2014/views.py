from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate
from django.contrib.auth import logout
from django.contrib.auth.models import User 
from django.shortcuts import get_object_or_404, render, redirect

from worldcup2014.models import Team, Player, Match, MatchStriker, Vote
from worldcup2014.forms import VoteForm

# def index(request):
#     return HttpResponse("Hello, world. You're at the poll index.")

from django.contrib.auth import authenticate, login

# index view (just redirect to login page)
def index(request):
    return HttpResponseRedirect('/bolao/login')

@login_required          
def match_index(request):
    match_list = Match.objects.all().order_by('matchtime')
    context = {'match_list': match_list}
    return render(request, 'match_index.html', context)    

@login_required
def match_detail(request, match_id):
    match = Match.objects.get(pk=match_id)
    vote = Vote.objects.all().filter(match=match_id)
    strikers = MatchStriker.objects.all().filter(match=match_id)
    uservote = Vote.objects.all().filter(match=match_id, user=request.user)
    print strikers
    return render(request, 'match_detail.html', {'vote': vote, 'match':match, 'strikers':strikers, 'uservote':uservote})

@login_required    
def results(request):
    points = {}
    user = User.objects.all()
    for u in user:
        vote = Vote.objects.all().filter(user=u)
        counter1 = 0
        counter2 = 0
        counter3 = 0
        for v in vote:
            counter1 += _get_striker_points(v.id)
            counter2 += _get_winner_points(v.id)
            counter3 += _get_score_points(v.id)
            tmp = {'striker': counter1, 'winner': counter2, 'score': counter3, 'total': counter1+counter2+counter3 }
        points[u]=tmp
    print points
    return render(request, 'results.html', {'points': points})

def _get_striker_points(vote_id):
    vote = Vote.objects.get(pk=vote_id)
    striker = MatchStriker.objects.filter(match=vote.match)
    for s in striker:
        if s.striker == vote.striker:
            return 2
    return 0

def _get_winner_points(vote_id):
    vote = Vote.objects.get(pk=vote_id)
    match = vote.match
    if match.winner == vote.winner:
        return 1
    else:
        return 0

def _get_score_points(vote_id):
    vote = Vote.objects.get(pk=vote_id)
    match = vote.match
    if match.score == vote.score:
        return 2
    else:
        return 0
         
@login_required
def match_vote(request, vote_id=None):
    if vote_id:
        vote = Vote.objects.get(pk=vote_id)
        action_msg, perm, object_perm = "updated", "worldcup2014.change_vote", vote
    else:
        vote = Vote()
        vote.user = request.user
        action_msg, perm, object_perm = "created", "worldcup2014.add_vote", None

    vote_form = VoteForm(request.POST or None, instance=vote)
    if request.method == 'POST':
        if vote_form.is_valid():
            vote_instance = vote_form.save()
            return redirect('match_detail', vote.match)

    return render(request, "match_vote.html", {"vote_form": vote_form})


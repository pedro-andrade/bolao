from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User 
from django.shortcuts import render, redirect
from django.contrib import messages

from worldcup2014.models import Match, MatchStriker, Vote
from worldcup2014.forms import VoteForm

# def index(request):
#     return HttpResponse("Hello, world. You're at the poll index.")

from datetime import datetime

# index view (just redirect to login page)
def index(request):
    return HttpResponseRedirect('/bolao/login')

@login_required          
def match_index(request):
    print datetime.now()
    match_list = Match.objects.filter(matchtime__gte=datetime.now()).order_by('matchtime')
    context = {'match_list': match_list}
    return render(request, 'match_index.html', context)    

@login_required          
def match_history(request):
    print datetime.now()
    match_list = Match.objects.filter(matchtime__lt=datetime.now()).order_by('matchtime')
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
        counter1 = 0
        counter2 = 0
        counter3 = 0
        numVote = Vote.objects.filter(user=u).count()
        if numVote==0:
            tmp = {'striker': counter1, 'winner': counter2, 'score': counter3, 'total': counter1+counter2+counter3 }
        else:
            vote = Vote.objects.all().filter(user=u)
            tmp = {} 
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
def vote_update(request, vote_id):
    
    try:
        vote = Vote.objects.get(pk=vote_id)
    except Exception:
        messages.error(request, 'You can not update vote that doesn\'t exist')
        return redirect('match_index')
    
    if request.user.username != vote.user :
        messages.error(request, 'You can not update vote of another user')
        return redirect('match_detail', vote.match.id)

    vote_form = VoteForm(request.POST or None, instance=vote, user=request.user)

    if request.method == 'POST':
        if vote_form.is_valid():
            vote_form.save()
            messages.success(request, 'Successfully updated vote for match %s' % (vote_form.instance.match))
            return redirect('match_detail', vote.match.id)

    return render(request, "match_vote.html", {"vote_form": vote_form})

@login_required
def vote_add(request, match_id):
    
    try:
        match = Match.objects.get(pk=match_id)
    except Exception:
        messages.error(request, 'You can not add vote to a match that doesn\'t exist')
        return redirect('match_index')
    
    try:
        isVote = Vote.objects.get(user=request.user, match=match.id)
    except Exception:
        isVote = None

    if isVote:
        return redirect('vote_update', isVote.id)

    vote = Vote()
    vote.user = request.user
    vote.match = match

    vote_form = VoteForm(request.POST or None, instance=vote)
    if request.method == 'POST':
        if vote_form.is_valid():
            vote_form.save()
            messages.success(request, 'Successfully added vote for match %s' % (vote_form.instance.match))            
            return redirect('match_detail', vote.match.id)

    return render(request, "match_vote.html", {"vote_form": vote_form})

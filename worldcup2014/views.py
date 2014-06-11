from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User 
from django.shortcuts import render, redirect
from django.contrib import messages

from worldcup2014.models import Match, MatchStriker, Vote, ExtraVote
from worldcup2014.forms import VoteForm, MatchForm, ExtraVoteForm


from datetime import datetime, timedelta

# index view (just redirect to login page)
def index(request):
    return HttpResponseRedirect('/bolao/login')

def _get_local_match_time():
    return datetime.now() - timedelta(hours=5)

@login_required          
def match_index(request):

    match_list = Match.objects.filter(matchtime__gte=_get_local_match_time()).order_by('matchtime')
    
    match_vote_list = {}
    for m in match_list:
        numVote = Vote.objects.filter(user=request.user, match=m.id).count()
        numVotes = Vote.objects.filter(match=m.id).count()
        if numVote==0:
            tmp = {'vote':None, 'numVotes':numVotes}
        elif numVote!=0:
            vote = Vote.objects.get(user=request.user, match=m.id)
            tmp = {'vote':vote, 'numVotes':numVotes}
        match_vote_list[m.id]=tmp

    context = {'match_list': match_list, 'match_vote_list': match_vote_list, 'path':request.path, 'time':_get_local_match_time()}
    return render(request, 'match_index.html', context)    

@login_required          
def match_history(request):
    match_list = Match.objects.filter(matchtime__lt=_get_local_match_time()).order_by('matchtime')
    context = {'match_list': match_list}
    return render(request, 'match_index.html', context)    

@login_required
def match_detail(request, match_id):
    match = Match.objects.get(pk=match_id)
    votes = Vote.objects.all().filter(match=match_id)
    strikers = MatchStriker.objects.all().filter(match=match_id)
    uservote = Vote.objects.all().filter(match=match_id, user=request.user)      

#in case we want to show only the votes that exist
#    points = {}
#    for v in votes:
#        if not match.finish:
#            counter1 = 0
#            counter2 = 0
#            counter3 = 0
#        else:
#            counter1 = _get_striker_points(v)
#            counter2 = _get_winner_points(v)
#            counter3 = _get_score_points(v)
#            tmp = {'vote':v, 'points_striker': counter1, 'points_winner': counter2, 'points_score': counter3, 'points_total': counter1+counter2+counter3 }
#        points[v.user]=tmp
            
    points = {}
    user = User.objects.all()
    for u in user:
        numVote = Vote.objects.filter(user=u, match=match_id).count()
        if numVote==0 and match.finish:
            tmp = {'vote':None, 'points_striker': 0, 'points_winner': 0, 'points_score': 0, 'points_total': 0 }
            points[u]=tmp
        elif numVote!=0:
            vote = Vote.objects.get(user=u, match=match_id)
            if not match.finish:
                counter1 = 0
                counter2 = 0
                counter3 = 0
            else:
                counter1 = _get_striker_points(vote)
                counter2 = _get_winner_points(vote)
                counter3 = _get_score_points(vote)
            tmp = {'vote':vote, 'points_striker': counter1, 'points_winner': counter2, 'points_score': counter3, 'points_total': counter1+counter2+counter3 }
            points[u]=tmp
        
    return render(request, 'match_detail.html', {'vote': votes, 'match':match, 'strikers':strikers, 'uservote':uservote, 'points': points})

@login_required    
def results(request):
    #TODO only votes of match flagged as finish in the database (finish means ready for the calculation of the results otherwise we could use the matchtime field)
    points = {}
    user = User.objects.all().order_by('username')
    for u in user:
        counter1 = 0
        counter2 = 0
        counter3 = 0
        numVote = Vote.objects.filter(user=u).count()
        numVote2 = Vote.objects.filter(user=u, match__finish=True).count()
        if numVote==0 or numVote2==0:
            tmp = {'striker': counter1, 'winner': counter2, 'score': counter3, 'total': counter1+counter2+counter3 }
        else:
            vote_list = Vote.objects.all().filter(user=u, match__finish=True)
            tmp = {} 
            for v in vote_list:
                vote = Vote.objects.get(pk=v.id)
                counter1 += _get_striker_points(vote)
                counter2 += _get_winner_points(vote)
                counter3 += _get_score_points(vote)
                tmp = {'striker': counter1, 'winner': counter2, 'score': counter3, 'total': counter1+counter2+counter3 }
        points[u]=tmp
    #print points
    
    match_list = Match.objects.filter(matchtime__lt=_get_local_match_time()).order_by('matchtime')

    return render(request, 'results.html', {'points': points, 'match_list': match_list})

def _valid_vote(vote_id):
    vote = Vote.objects.get(pk=vote_id)
    match = vote.match
    if match.finish == True:
        return True
    else:
        return False
        
def _get_striker_points(vote):
    striker = MatchStriker.objects.filter(match=vote.match)
    for s in striker:
        if s.striker == vote.striker:
            return 2
    return 0

def _get_winner_points(vote):
    match = vote.match
    if match.winner == vote.winner:
        return 1
    else:
        return 0

def _get_score_points(vote):
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

@login_required
def match_update(request, match_id):
    
    if request.user.username != 'pedro' or request.user.username != 'teresa':
        messages.error(request, 'You can not update the match details')
        return redirect('match_index')
    
    try:
        match = Match.objects.get(pk=match_id)
    except Exception:
        messages.error(request, 'You can not update match that doesn\'t exist')
        return redirect('match_index')
    
    match_form = MatchForm(request.POST or None, instance=match)

    if request.method == 'POST':
        if match_form.is_valid():
            match_form.save()
            messages.success(request, 'Successfully updated match %s' % (match_form.instance))
            return redirect('match_detail', match.id)

    return render(request, "match_update.html", {"match_form": match_form})

@login_required
def match_add(request):
        
    match = Match()

    match_form = VoteForm(request.POST or None, instance=match)
    if request.method == 'POST':
        if match_form.is_valid():
            match_form.save()
            messages.success(request, 'Successfully added match %s' % (match_form.instance))            
            return redirect('match_detail', match.id)

    return render(request, "match_update.html", {"match_form": match_form})

@login_required
def extra_vote_update(request, extra_vote_id):
        
    try:
        extra_vote = ExtraVote.objects.get(pk=extra_vote_id)
    except Exception:
        messages.error(request, 'You can not update extra vote that doesn\'t exist')
        return redirect('extra_vote')

    if request.user.username != extra_vote.user :
        messages.error(request, 'You can not update vote of another user')
        return redirect('extra_vote')

    extra_vote_form = ExtraVoteForm(request.POST or None, instance=extra_vote)

    if request.method == 'POST':
        if extra_vote_form.is_valid():
            extra_vote_form.save()
            messages.success(request, 'Successfully updated extra vote')
            return redirect('extra_vote')

    return render(request, "extra_vote_update.html", {"extra_vote_form": extra_vote_form})

@login_required
def extra_vote_add(request):
        
    try:
        isVote = ExtraVote.objects.get(user=request.user)
    except Exception:
        isVote = None

    if isVote:
        return redirect('extra_vote_update', isVote.id)

    vote = ExtraVote()
    vote.user = request.user

    extra_vote_form = ExtraVoteForm(request.POST or None, instance=vote)
    
    if request.method == 'POST':
        if extra_vote_form.is_valid():
            extra_vote_form.save()
            messages.success(request, 'Successfully added extra vote')            
            return redirect('extra_vote')

    return render(request, "extra_vote_update.html", {"extra_vote_form": extra_vote_form})

@login_required          
def rules(request):
    return render(request, 'rules.html')    

@login_required          
def extra_vote(request):
    extra_vote_list = ExtraVote.objects.all().filter().order_by('user')
    uservote = ExtraVote.objects.all().filter(user=request.user)
    return render(request, 'extra_vote.html', {'extra_vote_list': extra_vote_list, 'uservote':uservote})    

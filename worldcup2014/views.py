from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate
from django.contrib.auth import logout

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
    return render(request, 'match_detail.html', {'vote': vote, 'match':match})

@login_required
def match_edit(request, match_id):
    match = Match.objects.get(pk=match_id)
    return render(request, 'match_edit.html', {'match': match})

@login_required    
def results(request):
  #  list_match = Match.objects.all()
  #  context = {'list_match': list_match}
    return render(request, 'results.html')#, context)    

# def add(request, match_id=None):
         
@login_required
def create_or_update(request, vote_id=None):
    if vote_id:
        vote = Vote.objects.get(pk=vote_id)
        action_msg, perm, object_perm = "updated", "worldcup2014.change_vote", vote
    else:
        vote = Vote()
        action_msg, perm, object_perm = "created", "worldcup2014.add_vote", None

    vote_form = VoteForm(request.POST or None, instance=vote)
    if request.method == 'POST':
        if vote_form.is_valid():
            vote_instance = vote_form.save()

    return render(request, "match_edit.html", {"vote_form": vote_form})


    
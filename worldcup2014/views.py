from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate
from django.contrib.auth import logout

from worldcup2014.models import Team, Player, Match, Vote


# def index(request):
#     return HttpResponse("Hello, world. You're at the poll index.")

from django.contrib.auth import authenticate, login

# index view (just redirect to login page)
def index(request):
    return HttpResponseRedirect('/bolao/login')

@login_required          
def match_index(request):
    list_match = Match.objects.all()
    context = {'list_match': list_match}
    return render(request, 'worldcup2014/match_index.html', context)    

@login_required
def match_detail(request, match_id):
    match = Match.objects.get(pk=match_id)
    return render(request, 'worldcup2014/match_detail.html', {'match': match})

@login_required
def match_edit(request, match_id):
    match = Match.objects.get(pk=match_id)
    return render(request, 'worldcup2014/match_edit.html', {'match': match})

@login_required    
def results(request):
  #  list_match = Match.objects.all()
  #  context = {'list_match': list_match}
    return render(request, 'worldcup2014/results.html')#, context)    

# def add(request, match_id=None):
         

    
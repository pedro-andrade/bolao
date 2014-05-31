from django.shortcuts import render
from worldcup2014.models import Team, Player, Match, Bet

# def index(request):
#     return HttpResponse("Hello, world. You're at the poll index.")

def match_index(request):
    list_match = Match.objects.all()
    context = {'list_match': list_match}
    return render(request, 'worldcup2014/match_index.html', context)    


def match_detail(request, match_id):
    match = Match.objects.get(pk=match_id)
    return render(request, 'worldcup2014/match_detail.html', {'match': match})

def match_edit(request, match_id):
    match = Match.objects.get(pk=match_id)
    return render(request, 'worldcup2014/match_edit.html', {'match': match})
    
# def add(request, match_id=None):
         

    
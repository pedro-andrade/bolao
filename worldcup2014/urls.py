from django.conf.urls import patterns, url

from worldcup2014 import views

urlpatterns = patterns('',

    # index page
    url(r'^$', views.index),

    # using default django auth views with custom templates
    url(r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'login.html'}, name='login'),
    url(r'^logout/$', 'django.contrib.auth.views.logout', {'next_page':'../'}, name='logout'),

    # url(r'^login/$', 'login', { 'template_name': 'registration/login.html'L }, name='login' ),
    # url(r'^logout/$', 'logout', { 'template_name': 'registration/my_account.html', 'next_page':reverse('index') }, name='logout' ),
            
    # url(r'^$', views.login, name='login'),
    url(r'^match/$', views.match_index, name='match_index'),
    url(r'^match_history/$', views.match_history, name='match_history'),
    url(r'^match/(?P<match_id>\d+)/$', views.match_detail, name='match_detail'),

    url(r'^match/vote/update/(?P<vote_id>\d+)/$', views.vote_update, name='vote_update'),    
    url(r'^match/vote/add/(?P<match_id>\d+)/$', views.vote_add, name='vote_add'),

    url(r'^match/update/(?P<match_id>\d+)/$', views.match_update, name='match_update'),    
    #url(r'^match/add/$', views.match_add, name='match_add'),
   
    url(r'^results/$', views.results, name='results'),    
    
    url(r'^rules/$', views.rules, name='rules'),    
    
    url(r'^extra/$', views.extra_vote, name='extra_vote'),    
    
    url(r'^extra/update/(?P<extra_vote_id>\d+)/$', views.extra_vote_update, name='extra_vote_update'),    
    #url(r'^extra/add//$', views.extra_vote_add, name='extra_vote_add'),


)
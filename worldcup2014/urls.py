from django.conf.urls import patterns, include, url

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
    url(r'^match/(?P<match_id>\d+)/$', views.match_detail, name='match_detail'),

    url(r'^match/vote/update/(?P<vote_id>\d+)/$', views.update_vote, name='vote_update'),    
    url(r'^match/vote/add/(?P<match_id>\d+)/$', views.add_vote, name='vote_add'),
   
    url(r'^results/$', views.results, name='results'),    
    


)
from django.conf.urls import patterns, url

from worldcup2014 import views

urlpatterns = patterns('',
    url(r'^$', views.match_index, name='home'),
    url(r'^match/$', views.match_index, name='match_index'),    
    url(r'^match/(?P<match_id>\d+)/$', views.match_detail, name='match_detail'),
    url(r'^match/edit/(?P<match_id>\d+)/$', views.match_edit, name='match_edit'),
    url(r'^results/$', views.results, name='results'),    
    
)
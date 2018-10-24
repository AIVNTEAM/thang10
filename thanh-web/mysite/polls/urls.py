from django.conf.urls import url 
from . import views 

urlpatterns = [ 
	#ex /polls/
	url(r'^$', views.index, name='index'),
	#ex /polls/34/
	url(r'^(?P<question_id>[0-9]+)/$', views.detail, name='detail'),
	#ex /polls/34/results/
	url(r'^(?P<question_id>[0-9]+)/results/$', views.results, name='results'),
	#ex /polls/34/vote/
	url(r'^(?P<question_id>[0-9]+)/vote/$', views.votes, name='votes'),
]

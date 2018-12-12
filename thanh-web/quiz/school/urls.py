from django.conf.urls import url
from .views import \
	SignUpView, StudentSignUpView, \
	TeacherSignUpView, QuizListView, QuizCreateView, \
	QuizUpdateView, QuizDeleteView, QuizResultsView, QuestionDeleteView, \
    StudentQuizListView, StudentInterestsView, TakenQuizListView
from . import views


urlpatterns = [
    # url(r'^admin/', admin.site.urls),
    
    # url(r'^$', HomeView.as_view(), name='home'),
    url(r'^$', views.home , name='home'),
    url(r'^signup/$', SignUpView.as_view(), name='signup'),
    url(r'^signup/student/$',  
    	StudentSignUpView.as_view(), name='student_signup'),
    url(r'^signup/teacher/$',  
    	TeacherSignUpView.as_view(), name='teacher_signup'),

    url(r'^teacher/$', 
    	QuizListView.as_view(), name='quiz_change_list'),
    url(r'^teacher/quiz/add/', 
    	QuizCreateView.as_view(), name='quiz_add'),
    url(r'^teacher/quiz/(?P<pk>\d+)/$', 
    	QuizUpdateView.as_view(), name='quiz_change'),
    url(r'^teacher/quiz/(?P<pk>\d+)/delete/', 
    	QuizDeleteView.as_view(), name='quiz_delete'),
    url(r'^teacher/quiz/(?P<pk>\d+)/results/', 
    	QuizResultsView.as_view(), name='quiz_results'),
    url(r'^teacher/quiz/(?P<pk>\d+)/question/add/', 
    	views.question_add, name='question_add'),
    url(r'^teacher/quiz/(?P<quiz_pk>\d+)/question/(?P<question_pk>\d+)/$', 
    	views.question_change, name='question_change'),
    url(r'^teacher/quiz/(?P<quiz_pk>\d+)/question/(?P<question_pk>\d+)/delete/', 
    	QuestionDeleteView.as_view(), name='question_delete'),

    url(r'^student/$',
        StudentQuizListView.as_view(), name='quiz_list'),    
    url(r'^student/interests/$',
        StudentInterestsView.as_view(), name='student_interests'), 
    url(r'^student/taken/$',
        TakenQuizListView.as_view(), name='taken_quiz_list'), 
    url(r'^student/quiz/(?P<quiz_pk>\d+)/$',
        views.take_quiz, name='take_quiz'), 
]
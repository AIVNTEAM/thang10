from django.conf.urls import url
from django.contrib.auth import views as auth_views
from . import views
urlpatterns = [
    # url(r'^login/$', auth_views.login, 
    	# {'template_name': 'students/student/login.html'}, name='login'),
	# url(r'^logout/$', auth_views.logout, name='logout'),
	url(r'^register/$',
		views.StudentRegistrationView.as_view(),
		name='student_registration'),
	url(r'^enroll-course/$',
		views.StudentEnrollView.as_view(),
		name='student_enroll_course'),
	url(r'^courses/$',
		views.StudentCourseListView.as_view(),
		name='student_course_list'),
	url(r'^course/(?P<pk>\d+)/$',
		views.StudentCourseDetailView.as_view(),
		name='student_course_detail'),
	url(r'^course/(?P<pk>\d+)/(?P<module_id>\d+)/$',
		views.StudentCourseDetailView.as_view(),
		name='student_course_detail_module'),
]
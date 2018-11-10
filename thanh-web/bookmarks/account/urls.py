from django.contrib.auth import views as auth_views
from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static
from . import views

# app_name = "bookmarks"
urlpatterns = [
	url(r'^$', views.dashboard, name='dashboard'),
	
	#url(r'^login/$', views.user_login, name='login')
	#register
	url(r'^register/$', views.register, name='register'),
	url(r'^edit/$', views.edit, name='edit'),

	#view cua django	
	url(r'^login/$',
		auth_views.login,
		name='login'),
	url(r'^logout/$',
		auth_views.logout,
		name='logout'),
	url(r'^logout-then-login/$',
		auth_views.logout_then_login,
		name='logout_then_login'),
	# change password urls
	url(r'^password-change/$',
		auth_views.password_change,
		#chuyen den: bookmarks:password_change_done khi post du lieu
		# {'post_change_redirect': 'bookmarks:password_change_done'},
		name='password_change'),
	url(r'^password-change/done/$',
		auth_views.password_change_done,
		name='password_change_done'),
	
	# restore password urls
	url(r'^password-reset/$',
			auth_views.password_reset,
			# {'post_change_redirect': 'bookmarks:password_reset_done'},
			name='password_reset'),
	url(r'^password-reset/done/$',
			auth_views.password_reset_done,
			name='password_reset_done'),
	url(r'^password-reset/confirm/(?P<uidb64>[-\w]+)/(?P<token>[-\w]+)/$',
			auth_views.password_reset_confirm,
			name='password_reset_confirm'),
	url(r'^password-reset/complete/$',
			auth_views.password_reset_complete,
			name='password_reset_complete'),

]
if settings.DEBUG:
		urlpatterns += static(settings.MEDIA_URL,
						document_root=settings.MEDIA_ROOT)
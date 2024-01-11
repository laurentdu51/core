from django.conf import settings
from django.contrib.staticfiles import views

from django.contrib import admin
from django.urls import path, re_path, include
from django.views.generic.base import RedirectView

from core import views as core

urlpatterns = [

	path('trumbowyg/', include('trumbowyg.urls')),
	path('admin/', admin.site.urls),
	
	path('account/login', core.p_login, name='core_login'),
	path('account/logout', core.p_logout, name='core_logout'),
	path('account/registration', core.p_registration , name='core_registration'),

	path('favicon.ico', RedirectView.as_view(url = '/static/favicon.ico')),

	path('' , core.index, name='core_index'),
	# url generique
	re_path(r'page/(?P<p_url>[a-zA-Z0-9_,-/]+)', core.page, name='core_page'),
	# last chance 
	re_path(r'(?P<p_url>[a-zA-Z0-9_.,-]+)', core.page, name='core_page'),

]

if settings.DEBUG:
	urlpatterns += [
		re_path(r'^static/(?P<path>.*)$', views.serve),
	]
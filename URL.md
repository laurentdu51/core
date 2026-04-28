from django.conf import settings
from django.contrib import admin
from django.urls import path, re_path, include
from django.conf.urls.static import static
from django.views.generic.base import RedirectView

from core import views as core

urlpatterns = [
	path('admin/', admin.site.urls),
	path('tinymce/', include('tinymce.urls')),
	
	path('account/login', core.p_login, name='core_login'),
	path('account/logout', core.p_logout, name='core_logout'),
	path('account/registration', core.p_registration, name='core_registration'),

	path('favicon.ico', RedirectView.as_view(url='/static/favicon.ico')),

	path('', core.index, name='core_index'),
	# URL générique pour les pages
	re_path(r'page/(?P<p_url>[a-zA-Z0-9_,-/]+)', core.page, name='core_page'),
	# Fallback pour les autres URLs
	re_path(r'(?P<p_url>[a-zA-Z0-9_.,-]+)', core.page, name='core_page'),
]

if settings.DEBUG:
	urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
	urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
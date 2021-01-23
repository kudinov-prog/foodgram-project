from django.conf import settings
from django.conf.urls import handler404, handler500
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.flatpages import views
from django.urls import include, path

from . import views as proj_views

handler404 = proj_views.page_not_found
handler500 = proj_views.server_error

urlpatterns = [
    path('admin/', admin.site.urls),
    path('about/', include('django.contrib.flatpages.urls')),
    path('auth/', include('users.urls')),
    path('auth/', include('django.contrib.auth.urls')),
    path('', include('recipes.urls')),
    path('api/', include('api.urls')),
]

urlpatterns += [
    path(
        'about-author/', views.flatpage,
        {'url': '/about-author/'}, name='about_author'
    ),
    path(
        'about-spec/', views.flatpage,
        {'url': '/about-spec/'}, name='about_spec'
    ),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

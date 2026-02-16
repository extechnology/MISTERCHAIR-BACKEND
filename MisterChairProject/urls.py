from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('grappelli/', include('grappelli.urls')), # grappelli URLS
    path('tinymce/', include('tinymce.urls')),
    path('nested_admin/', include('nested_admin.urls')),
    path('admin/', admin.site.urls),
    path('services/api/',include('ApplicationServices.urls'))
]
if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )
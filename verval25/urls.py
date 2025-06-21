from django.contrib import admin
from django.urls import include, path, reverse_lazy, re_path
from django.views.generic.base import RedirectView
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('siga/stunting/', include('myapp.urls')),
    path('', RedirectView.as_view(url=reverse_lazy('swagger-ui'))),
    # Swagger UI
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),

]

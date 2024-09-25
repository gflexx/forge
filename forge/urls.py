from django.conf.urls.static import static
from django.contrib import admin
from django.conf import settings
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title='Auth API',
        default_version='v1',
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

API = 'api/v1'

urlpatterns = [
    path('fhnxtydslt/admin/', admin.site.urls),
    path(
        f'{API}/docs/', 
        schema_view.with_ui('swagger', cache_timeout=0), 
        name='schema-swagger-ui'
    ),
    path(
        f'{API}/auth/token/', 
        TokenObtainPairView.as_view(), 
        name='token_obtain_pair'
    ),
    path(
        f'{API}/auth/token/refresh/', 
        TokenRefreshView.as_view(), 
        name='token_refresh'
    ),
    path(f'{API}/users/', include('users.urls')),
]

if settings.DEBUG:
    urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns = urlpatterns + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.conf import settings
from django.conf.urls.static import static

# Create a custom namespace for your API URLs to avoid conflicts with Django's authentication URLs.
api_urlpatterns = [
    # path('InventoryApp/', include('InventoryApp.urls')), 
    path('AuthApp/', include('AuthApp.urls')),
    path('InventoryApp/', include('InventoryApp.urls')),
]

schema_view = get_schema_view(
    openapi.Info(
        title="RestronovaRMS API",
        default_version="v1",
        description="No any description for now",
        contact=openapi.Contact(email="work.restronova@gmail.com"),
        license=openapi.License(name="sikify"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(api_urlpatterns)),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)



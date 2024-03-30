# urls.py
from rest_framework import routers
from django.urls import path, include
from . import views

router = routers.DefaultRouter()
router.register(r'user', views.UserViewSet)
router.register(r'outlet', views.OutletViewSet)

urlpatterns = [
    path('api/', include(router.urls)),  
    path('accounts/', include('allauth.urls')),
]
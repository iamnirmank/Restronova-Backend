# urls.py
from rest_framework import routers
from django.urls import path, include
from . import views

router = routers.DefaultRouter()
router.register('raw_materials', views.RawMaterialsViewSet)
router.register('vendors', views.VendorViewSet)
router.register('inventory', views.InventoryViewSet)
router.register('raw_material_orders', views.RawMaterialOrdersViewSet)
router.register('products', views.ProductsViewSet)
router.register('menu_items', views.MenuItemsViewSet)
router.register('sales', views.SalesViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
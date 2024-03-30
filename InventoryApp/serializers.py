from rest_framework import serializers
from . import models

class RawMaterialsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.RawMaterials
        fields = '__all__'

class VendorSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Vendor
        fields = '__all__'

class InventorySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Inventory
        fields = '__all__'

class RawMaterialOrdersSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.RawMaterialOrders
        fields = '__all__'

class ProductsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Products
        fields = '__all__'

class MenuItemsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.MenuItems
        fields = '__all__'

class SalesSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Sales
        fields = '__all__'
        




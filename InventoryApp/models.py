import random
import string
from django.db import models

class RawMaterials(models.Model):
    name = models.CharField(max_length=100)
    avatar = models.URLField(blank=True, null=True)

    outlet = models.ForeignKey('AuthApp.Outlet', on_delete=models.CASCADE, to_field='outlet_code', related_name='raw_materials_outlet', blank=True, null=True)

    def __str__(self):
        return self.name
    
class Vendor(models.Model):
    name = models.CharField(max_length=100)
    contact_no = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(unique=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    website = models.CharField(max_length=255, blank=True, null=True)
    avatar = models.URLField(blank=True, null=True)
    vendor_materials = models.JSONField(blank=True, null=True)

    outlet = models.ForeignKey('AuthApp.Outlet', on_delete=models.CASCADE, to_field='outlet_code', related_name='vendor_outlet', blank=True, null=True)

    def __str__(self):
        return self.name

class Inventory(models.Model):
    manufacturing_date = models.DateField(blank=True, null=True)
    expiry_date = models.DateField(blank=True, null=True)
    validation_period = models.FloatField(blank=True, null=True)
    rate = models.FloatField()
    quantity = models.FloatField()
    total_cost = models.FloatField()
    document = models.URLField(blank=True, null=True)
    total_quantity_remaining = models.FloatField(default = 0)
    wastage = models.FloatField(default = 0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    raw_material = models.ForeignKey(RawMaterials, on_delete=models.CASCADE, to_field='id', related_name='raw_material')
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, to_field='id', related_name='vendor')
    
    outlet = models.ForeignKey('AuthApp.Outlet', on_delete=models.CASCADE, to_field='outlet_code', related_name='inventory_outlet', blank=True, null=True)

    def __str__(self):
        return self.raw_material.name
    
class RawMaterialOrders(models.Model):
    id = models.CharField(max_length=100, primary_key=True, editable=False)
    previouse_order_id = models.CharField(max_length=100, blank=True, null=True)
    order_date = models.DateField(blank=True, null=True)
    delivery_date = models.DateField(blank=True, null=True)
    rate = models.FloatField()
    quantity = models.FloatField()
    discount = models.FloatField(default = 0)   
    order_status = models.CharField(max_length=100)
    order_trackings = models.JSONField(blank=True, null=True)
    raw_material = models.ForeignKey(RawMaterials, on_delete=models.CASCADE, to_field='id', related_name='raw_material_orders')
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, to_field='id', related_name='vendor_orders')
    
    outlet = models.ForeignKey('AuthApp.Outlet', on_delete=models.CASCADE, to_field='outlet_code', related_name='raw_material_orders_outlet', blank=True, null=True)

    def __str__(self):
        return self.raw_material.name

    def save(self, *args, **kwargs):
        if not self.id: 
            self.id = ''.join(random.choices(string.digits, k=6)) 
        super().save(*args, **kwargs)
    
class Products(models.Model):
    name = models.CharField(max_length=100)
    price = models.FloatField()
    quantity = models.FloatField()
    avatar = models.URLField(blank=True, null=True)
    recipe_materials = models.JSONField(blank=True, null=True)
    
    outlet = models.ForeignKey('AuthApp.Outlet', on_delete=models.CASCADE, to_field='outlet_code', related_name='products_outlet', blank=True, null=True)

    def __str__(self):
        return self.name
    
class MenuItems(models.Model):
    price = models.FloatField()
    quantity = models.FloatField()
    date = models.DateField(auto_now_add=True)
    product = models.ForeignKey(Products, on_delete=models.CASCADE, to_field='id', related_name='menu_products')
    
    outlet = models.ForeignKey('AuthApp.Outlet', on_delete=models.CASCADE, to_field='outlet_code', related_name='menu_outlet', blank=True, null=True)

    def __str__(self):
        return self.product.name


class Sales(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    quantity = models.FloatField()
    amount_received = models.FloatField()
    remarks = models.CharField(max_length=100, blank=True, null=True)
    menu_item = models.ForeignKey(MenuItems, on_delete=models.CASCADE, to_field='id', related_name='sales_menu_items')
    
    outlet = models.ForeignKey('AuthApp.Outlet', on_delete=models.CASCADE, to_field='outlet_code', related_name='sales_outlet', blank=True, null=True)

    def __str__(self):
        return self.menu_item.product.name


    


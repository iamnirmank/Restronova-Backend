import json
from rest_framework import viewsets, status
from rest_framework.decorators import action

from AuthApp.utils import jwt_decode_handler
from . import models
from AuthApp.models import Outlet, User
from . import serializers
from rest_framework.parsers import MultiPartParser
from rest_framework.parsers import FormParser
from .utils import create_response, get_file_extension, get_inventory_summary
from .azure_service_controller import upload_file_to_blob
from rest_framework.permissions import IsAuthenticated

class AuthenticatedModelViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]

class RawMaterialsViewSet(AuthenticatedModelViewSet):
    queryset = models.RawMaterials.objects.all()
    serializer_class = serializers.RawMaterialsSerializer

    @action(detail=False, methods=['GET'])
    def get_all_raw_materials(self, request):
        authorization = request.headers.get('Authorization')
        parts = authorization.split(' ')
        token = parts[1]
        decoded_token = jwt_decode_handler(token)
        try:
            user = User.objects.get(id=decoded_token['user_id'])
            if user.role == 'Admin':
                outlets = Outlet.objects.filter(restaurant=user.outlet.restaurant)
                raw_materials = models.RawMaterials.objects.filter(outlet__in=outlets)
            else:
                raw_materials = models.RawMaterials.objects.filter(outlet=user.outlet)
            return create_response(success=True, message='Raw materials fetched successfully', body=serializers.RawMaterialsSerializer(raw_materials, many=True).data)
        except User.DoesNotExist:
            return create_response(success=False, message='User not found', status_code=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return create_response(success=False, message=str(e), status_code=status.HTTP_400_BAD_REQUEST)
        
    @action(detail=False, methods=['POST'], parser_classes=[MultiPartParser, FormParser])
    def create_raw_material(self, request):
        name = request.data.get('name', '')
        outlet = request.data.get('outlet', '')
        image_data = request.data.get('avatar', None)

        try:
            raw_material = models.RawMaterials(name=name)
            raw_material.outlet = Outlet.objects.get(pk=outlet)
            if image_data:
                container_name = 'raw-materials'
                blob_name = 'raw_material_avatar_' + name+'.'+get_file_extension(image_data)
                raw_material.avatar = upload_file_to_blob(image_data, container_name, blob_name)
            raw_material.save()
            return create_response(success=True, message='Raw material created successfully', body=serializers.RawMaterialsSerializer(raw_material).data)
        except Exception as e:
            return create_response(success=False, message=str(e), status_code=status.HTTP_400_BAD_REQUEST)
        
    @action(detail=True, methods=['PUT'], parser_classes=[MultiPartParser, FormParser])
    def update_raw_material(self, request, pk=None):
        name = request.data.get('name', '')
        image_data = request.data.get('avatar', '')
        try:
            raw_material = models.RawMaterials.objects.get(pk=pk)
            raw_material.name = name
            if type(image_data) != str:
                container_name = 'raw-materials'
                blob_name = 'raw_material_avatar_' + name+'.'+get_file_extension(image_data)
                raw_material.avatar = upload_file_to_blob(image_data, container_name, blob_name)
            raw_material.save()
            return create_response(success=True, message='Raw material updated successfully', body=serializers.RawMaterialsSerializer(raw_material).data)
        except Exception as e:
            return create_response(success=False, message=str(e), status_code=status.HTTP_400_BAD_REQUEST)
        
    @action(detail=True, methods=['DELETE'])
    def delete_raw_materials(self, request, pk=None):
        try:
            raw_material = models.RawMaterials.objects.get(pk=pk)

            all_products = models.Products.objects.all()
            all_recipe_materials = []
            for product in all_products:
                all_recipe_materials.append(product.recipe_materials)
                for recipe_material in product.recipe_materials:
                    if (recipe_material['raw_material']==int(pk)):
                        return create_response(success=False, message='Raw material is associated with following product and cannot be deleted', body=serializers.ProductsSerializer(product).data,
                                       status_code=status.HTTP_400_BAD_REQUEST)

            all_vendors = models.Vendor.objects.all()
            all_vendor_materials = []
            for vendor in all_vendors:
                all_vendor_materials.append(vendor.vendor_materials)    
                for vendor_material in vendor.vendor_materials:
                    if (vendor_material['raw_material']==int(pk)):
                        return create_response(success=False, message='Raw material is associated with following vendor and cannot be deleted', body=serializers.VendorSerializer(vendor).data,
                                       status_code=status.HTTP_400_BAD_REQUEST)
                    
            raw_material.delete()
            return create_response(success=True, message='Raw material deleted successfully', status_code=status.HTTP_200_OK)

        except models.RawMaterials.DoesNotExist:
            return create_response(success=False, message='Raw material not found', status_code=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return create_response(success=False, message=str(e), status_code=status.HTTP_400_BAD_REQUEST)
        
    @action(detail=False, methods=['DELETE'])
    def delete_all_raw_materials(self, request):
        try:
            models.RawMaterials.objects.all().delete()
            return create_response(success=True, message='All raw materials deleted successfully')
        except Exception as e:
            return create_response(success=False, message=str(e), status_code=status.HTTP_400_BAD_REQUEST)

class VendorViewSet(AuthenticatedModelViewSet):
    queryset = models.Vendor.objects.all()
    serializer_class = serializers.VendorSerializer

    @action(detail=False, methods=['GET'])
    def get_all_vendors(self, request):
        authorization = request.headers.get('Authorization')
        parts = authorization.split(' ')
        token = parts[1]
        decoded_token = jwt_decode_handler(token)
        try:
            user = User.objects.get(id=decoded_token['user_id'])
            if user.role == 'Admin':
                outlets = Outlet.objects.filter(restaurant=user.outlet.restaurant)
                vendors = models.Vendor.objects.filter(outlet__in=outlets)
            else:
                vendors = models.Vendor.objects.filter(outlet=user.outlet)
            return create_response(success=True, message='Vendors fetched successfully', body=serializers.VendorSerializer(vendors, many=True).data)
        except User.DoesNotExist:
            return create_response(success=False, message='User not found', status_code=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return create_response(success=False, message=str(e), status_code=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['POST'], parser_classes=[MultiPartParser, FormParser])
    def create_vendor(self, request):
        name = request.data.get('name', '')
        contact_no = request.data.get('contact_no', '')
        email = request.data.get('email', '')
        address = request.data.get('address', '')
        website = request.data.get('website', '')
        image_data = request.data.get('avatar')
        outlet = request.data.get('outlet', '')

        vendor_materials_str = request.data.get('vendor_materials', '')
        vendor_materials = json.loads(vendor_materials_str)

        try:
            vendor = models.Vendor(name=name, contact_no=contact_no, email=email, address=address, website=website, vendor_materials=vendor_materials)
            vendor.outlet = Outlet.objects.get(pk=outlet)
            if type(image_data) != str:
                container_name = 'vendors'
                blob_name = 'raw_material_avatar_' + name+'.'+get_file_extension(image_data)
                vendor.avatar = upload_file_to_blob(image_data, container_name, blob_name)

            vendor.save()

            return create_response(success=True, message='Vendor created successfully', body=serializers.VendorSerializer(vendor).data)
            pass
        except Exception as e:
            return create_response(success=False, message=str(e), status_code=status.HTTP_400_BAD_REQUEST)
        
    @action(detail=True, methods=['PUT'], parser_classes=[MultiPartParser, FormParser])
    def update_vendor(self, request, pk=None):
        name = request.data.get('name', '')
        contact_no = request.data.get('contact_no', '')
        email = request.data.get('email', '')
        address = request.data.get('address', '')
        website = request.data.get('website', '')
        image_data = request.data.get('avatar')
        outlet = request.data.get('outlet', '')

        vendor_materials_str = request.data.get('vendor_materials', '')
        vendor_materials = json.loads(vendor_materials_str)
        
        try:
            vendor = models.Vendor.objects.get(pk=pk)
            vendor.name = name
            vendor.contact_no = contact_no
            vendor.email = email
            vendor.address = address
            vendor.website = website
            vendor.vendor_materials = vendor_materials
            if outlet:
                vendor.outlet = Outlet.objects.get(pk=outlet)
            if type(image_data) != str:
                container_name = 'vendors'
                blob_name = 'raw_material_avatar_' + name+'.'+get_file_extension(image_data)
                vendor.avatar = upload_file_to_blob(image_data, container_name, blob_name)

            vendor.save()

            return create_response(success=True, message='Vendor updated successfully', body=serializers.VendorSerializer(vendor).data)
        except Exception as e:
            return create_response(success=False, message=str(e), status_code=status.HTTP_400_BAD_REQUEST)
        
    @action(detail=False, methods=['DELETE'])
    def delete_all_vendors(self, request):
        try:
            models.Vendor.objects.all().delete()
            return create_response(success=True, message='All vendors deleted successfully')
        except Exception as e:
            return create_response(success=False, message=str(e), status_code=status.HTTP_400_BAD_REQUEST)
        
class InventoryViewSet(AuthenticatedModelViewSet):
    queryset = models.Inventory.objects.all()
    serializer_class = serializers.InventorySerializer

    @action(detail=False, methods=['GET'])
    def get_all_inventories(self, request):
        authorization = request.headers.get('Authorization')
        parts = authorization.split(' ')
        token = parts[1]
        decoded_token = jwt_decode_handler(token)
        try:
            user = User.objects.get(id=decoded_token['user_id'])
            if user.role == 'Admin':
                outlets = Outlet.objects.filter(restaurant=user.outlet.restaurant)
                inventories = models.Inventory.objects.filter(outlet__in=outlets)
            else:
                inventories = models.Inventory.objects.filter(outlet=user.outlet)
            return create_response(success=True, message='Inventories fetched successfully', body=serializers.InventorySerializer(inventories, many=True).data)
        except User.DoesNotExist:
            return create_response(success=False, message='User not found', status_code=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return create_response(success=False, message=str(e), status_code=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['POST'], parser_classes=[MultiPartParser, FormParser])
    def create_inventory(self, request):
        manufacturing_date = request.data.get('manufacturing_date', '')
        expiry_date = request.data.get('expiry_date', '')
        validation_period = request.data.get('validation_period', '')
        rate = request.data.get('rate', '')
        quantity = request.data.get('quantity', '')
        total_cost = request.data.get('total_cost', '')
        vendor_id = request.data.get('vendor', '')
        raw_material = request.data.get('raw_material', '')
        document_data = request.data.get('document', '')
        outlet = request.data.get('outlet', '')
        reset_remaining_quantity = request.data.get('reset_remaining_quantity', False)

        try:
            inventory = models.Inventory(
                manufacturing_date=manufacturing_date, 
                expiry_date=expiry_date, 
                validation_period=validation_period, 
                rate=rate, quantity=quantity, 
                total_cost=total_cost, 
                )
            inventory.raw_material = models.RawMaterials.objects.get(pk=raw_material)
            inventory.vendor = models.Vendor.objects.get(pk=vendor_id)
            inventory.outlet = Outlet.objects.get(pk=outlet)

            if type(document_data) != str:
                container_name = 'inventories'
                blob_name = 'document_'+inventory.raw_material.name+'.'+get_file_extension(document_data)
                inventory.document = upload_file_to_blob(document_data, container_name, blob_name)
            
            summary = get_inventory_summary()

            for item in summary:
                if item['raw_material'] == int(raw_material):
                    remaining_quantity = item['total'] - item['consumed']
                    if reset_remaining_quantity:
                        inventory.total_quantity_remaining = quantity
                        inventory.wastage = remaining_quantity
                    else:
                        inventory.total_quantity_remaining = remaining_quantity + float(quantity)

            inventory.save()

            inventory.save()
            return create_response(success=True, message='Inventory created successfully', body=serializers.InventorySerializer(inventory).data)
        
        except Exception as e:
            return create_response(success=False, message=str(e), status_code=status.HTTP_400_BAD_REQUEST)
        
    @action(detail=True, methods=['PUT'], parser_classes=[MultiPartParser, FormParser])
    def update_inventory(self, request, pk=None):
        manufacturing_date = request.data.get('manufacturing_date', '')
        expiry_date = request.data.get('expiry_date', '')
        validation_period = request.data.get('validation_period', '')
        rate = request.data.get('rate', '')
        quantity = request.data.get('quantity', '')
        total_cost = request.data.get('total_cost', '')
        vendor_id = request.data.get('vendor', '')
        raw_material = request.data.get('raw_material', '')
        document_data = request.data.get('document', '')
        outlet = request.data.get('outlet', '')
        reset_remaining_quantity = request.data.get('reset_remaining_quantity', False)

        try:
            inventory = models.Inventory.objects.get(pk=pk)
            inventory.manufacturing_date = manufacturing_date
            inventory.expiry_date = expiry_date
            inventory.validation_period = validation_period
            inventory.rate = rate
            inventory.quantity = quantity
            inventory.total_cost = total_cost
            inventory.raw_material = models.RawMaterials.objects.get(pk=raw_material)
            inventory.vendor = models.Vendor.objects.get(pk=vendor_id)
            inventory.outlet = Outlet.objects.get(pk=outlet)
            if type(document_data) != str:
                container_name = 'inventories'
                blob_name = 'document_'+inventory.raw_material.name+'.'+get_file_extension(document_data)
                inventory.document = upload_file_to_blob(document_data, container_name, blob_name)

            summary = get_inventory_summary()

            for item in summary:
                if item['raw_material'] == raw_material:
                    remaining_quantity = item['total'] - item['consumed']
                    if reset_remaining_quantity:
                        inventory.total_quantity_remaining = quantity
                        inventory.wastage = remaining_quantity
                    else:
                        inventory.total_quantity_remaining = remaining_quantity + float(quantity)

            inventory.save()

            return create_response(success=True, message='Inventory updated successfully', body=serializers.InventorySerializer(inventory).data)
        
        except Exception as e:
            return create_response(success=False, message=str(e), status_code=status.HTTP_400_BAD_REQUEST)
        
    @action(detail=False, methods=['DELETE'])
    def delete_all_inventories(self, request):
        try:
            models.Inventory.objects.all().delete()
            return create_response(success=True, message='All inventories deleted successfully')
        except Exception as e:
            return create_response(success=False, message=str(e), status_code=status.HTTP_400_BAD_REQUEST)
        
    @action(detail=False, methods=['GET'])
    def get_inventory_summary(self, request):
        summary = get_inventory_summary()
        return create_response(success=True, message='Inventory summary calculated successfully', body=summary)
    
class RawMaterialOrdersViewSet(AuthenticatedModelViewSet):
    queryset = models.RawMaterialOrders.objects.all()
    serializer_class = serializers.RawMaterialOrdersSerializer

    @action(detail=False, methods=['GET'])
    def get_all_raw_materials_orders(self, request):
        authorization = request.headers.get('Authorization')
        parts = authorization.split(' ')
        token = parts[1]
        decoded_token = jwt_decode_handler(token)
        try:
            user = User.objects.get(id=decoded_token['user_id'])
            if user.role == 'Admin':
                outlets = Outlet.objects.filter(restaurant=user.outlet.restaurant)
                raw_material_orders = models.RawMaterialOrders.objects.filter(outlet__in=outlets)
            else:
                raw_material_orders = models.RawMaterialOrders.objects.filter(outlet=user.outlet)
            return create_response(success=True, message='Raw material orders fetched successfully', body=serializers.RawMaterialOrdersSerializer(raw_material_orders, many=True).data)
        except User.DoesNotExist:
            return create_response(success=False, message='User not found', status_code=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return create_response(success=False, message=str(e), status_code=status.HTTP_400_BAD_REQUEST)
        
    @action(detail=False, methods=['DELETE'])
    def delete_all_raw_material_orders(self, request):
        try:
            models.RawMaterialOrders.objects.all().delete()
            return create_response(success=True, message='All raw material orders deleted successfully')
        except Exception as e:
            return create_response(success=False, message=str(e), status_code=status.HTTP_400_BAD_REQUEST)
        
    @action(detail=True, methods=['PUT'])
    def delete_all_raw_material_orders(self, request, pk=None):
        try:
            models.RawMaterialOrders.objects.all().delete()
            return create_response(success=True, message='All raw material orders deleted successfully')
        except Exception as e:
            return create_response(success=False, message=str(e), status_code=status.HTTP_400_BAD_REQUEST)

class ProductsViewSet(AuthenticatedModelViewSet):
    queryset = models.Products.objects.all()
    serializer_class = serializers.ProductsSerializer

    @action(detail=False, methods=['GET'])
    def get_all_products(self, request):
        authorization = request.headers.get('Authorization')
        parts = authorization.split(' ')
        token = parts[1]
        decoded_token = jwt_decode_handler(token)
        try:
            user = User.objects.get(id=decoded_token['user_id'])
            if user.role == 'Admin':
                outlets = Outlet.objects.filter(restaurant=user.outlet.restaurant)
                products = models.Products.objects.filter(outlet__in=outlets)
            else:
                products = models.Products.objects.filter(outlet=user.outlet)
            return create_response(success=True, message='Products fetched successfully', body=serializers.ProductsSerializer(products, many=True).data)
        except User.DoesNotExist:
            return create_response(success=False, message='User not found', status_code=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return create_response(success=False, message=str(e), status_code=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['POST'], parser_classes=[MultiPartParser, FormParser])
    def create_product(self, request):
        name = request.data.get('name', '')
        price = request.data.get('price', '')
        quantity = request.data.get('quantity', '')
        image_data = request.data.get('avatar', '')
        outlet_id = request.data.get('outlet', '')

        recipe_materials_str = request.data.get('recipe_materials', '')
        recipe_materials = json.loads(recipe_materials_str)
        
        try:
            product = models.Products(name=name, price=price, quantity=quantity, recipe_materials=recipe_materials, outlet=Outlet.objects.get(pk=outlet_id))
            if type(image_data) != str:
                container_name = 'products'
                blob_name = 'product_avatar_' + name+'.'+get_file_extension(image_data)
                product.avatar = upload_file_to_blob(image_data, container_name, blob_name)

            product.save()
            return create_response(success=True, message='Product created successfully', body=serializers.ProductsSerializer(product).data)
        
        except Exception as e:
            return create_response(success=False, message=str(e), status_code=status.HTTP_400_BAD_REQUEST)
        
    @action(detail=True, methods=['PUT'], parser_classes=[MultiPartParser, FormParser])
    def update_product(self, request, pk=None):
        name = request.data.get('name', '')
        price = request.data.get('price', '')
        quantity = request.data.get('quantity', '')
        image_data = request.data.get('avatar', '')

        recipe_materials_str = request.data.get('recipe_materials', '')
        recipe_materials = json.loads(recipe_materials_str)
        
        try:
            product = models.Products.objects.get(pk=pk)
            product.name = name
            product.price = price
            product.quantity = quantity
            product.recipe_materials = recipe_materials
            if type(image_data) != str:
                container_name = 'products'
                blob_name = 'product_avatar_' + name+'.'+get_file_extension(image_data)
                product.avatar = upload_file_to_blob(image_data, container_name, blob_name)
            
            product.save()

            return create_response(success=True, message='Product updated successfully', body=serializers.ProductsSerializer(product).data)
        
        except Exception as e:
            return create_response(success=False, message=str(e), status_code=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['DELETE'])
    def delete_all_products(self, request):
        try:
            models.Products.objects.all().delete()
            return create_response(success=True, message='All products deleted successfully')
        except Exception as e:
            return create_response(success=False, message=str(e), status_code=status.HTTP_400_BAD_REQUEST)
    
class MenuItemsViewSet(AuthenticatedModelViewSet):
    queryset = models.MenuItems.objects.all()
    serializer_class = serializers.MenuItemsSerializer

    @action(detail=False, methods=['GET'])
    def get_all_menu_items(self, request):
        authorization = request.headers.get('Authorization')
        parts = authorization.split(' ')
        token = parts[1]
        decoded_token = jwt_decode_handler(token)
        try:
            user = User.objects.get(id=decoded_token['user_id'])
            if user.role == 'Admin':
                outlets = Outlet.objects.filter(restaurant=user.outlet.restaurant)
                menu_items = models.MenuItems.objects.filter(outlet__in=outlets)
            else:
                menu_items = models.MenuItems.objects.filter(outlet=user.outlet)
            return create_response(success=True, message='Menu items fetched successfully', body=serializers.MenuItemsSerializer(menu_items, many=True).data)
        except User.DoesNotExist:
            return create_response(success=False, message='User not found', status_code=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return create_response(success=False, message=str(e), status_code=status.HTTP_400_BAD_REQUEST)

class SalesViewSet(AuthenticatedModelViewSet):
    queryset = models.Sales.objects.all()
    serializer_class = serializers.SalesSerializer

    @action(detail=False, methods=['GET'])
    def get_all_sales(self, request):
        authorization = request.headers.get('Authorization')
        parts = authorization.split(' ')
        token = parts[1]
        decoded_token = jwt_decode_handler(token)
        try:
            user = User.objects.get(id=decoded_token['user_id'])
            if user.role == 'Admin':
                outlets = Outlet.objects.filter(restaurant=user.outlet.restaurant)
                sales = models.Sales.objects.filter(outlet__in=outlets)
            else:
                sales = models.Sales.objects.filter(outlet=user.outlet)
            return create_response(success=True, message='Sales fetched successfully', body=serializers.SalesSerializer(sales, many=True).data)
        except User.DoesNotExist:
            return create_response(success=False, message='User not found', status_code=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return create_response(success=False, message=str(e), status_code=status.HTTP_400_BAD_REQUEST)
        

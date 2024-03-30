import random
import re
import string
from rest_framework.response import Response
from rest_framework import status
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
import os
from InventoryApp import models
from django.db.models import Sum

from RestronovaRMS import settings

def create_response(success, message, body=None, status_code=status.HTTP_200_OK):
    response_data = {'success': success, 'message': message}
    if body is not None:
        response_data['body'] = body
    response = Response(response_data)
    response.status_code = status_code
    return response

def send_order_email(raw_material_order):
    subject = "Order Request From Burger House"
    message = render_to_string('order_email_template.html', {'order': raw_material_order})
    plain_message = strip_tags(message)  
    from_email = settings.EMAIL_HOST_USER

    to_email = raw_material_order.vendor.email
    try:
        send_mail(subject, plain_message, from_email, [to_email], html_message=message)
    except Exception as e:
        print(e)
        return create_response(success=False, message='Failed to send order email', body=e, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

def generate_code():
    return ''.join(random.choices(string.digits, k=6))

def parse_vendor_materials(body):
    data = dict(re.findall(r'([^\=]+)\=([^\&]+)', body.decode('utf-8')))
    keys = set(re.findall(r'vendor_materials\[(\d+)\]', body.decode('utf-8')))
    vendor_materials = []
    for key in keys:
        vendor_material = {}
        vendor_material['raw_material'] = data['vendor_materials['+key+'][raw_material]']
        vendor_material['rate'] = data['vendor_materials['+key+'][rate]']
        vendor_material['inventory_level'] = data['vendor_materials['+key+'][inventory_level]']
        vendor_materials.append(vendor_material)
    return vendor_materials

def get_file_extension(file):
    # Extract the file name from the file object
    file_name = file.name

    # Get the file extension
    _, file_extension = os.path.splitext(file_name)

    # Remove the leading dot from the extension
    file_extension = file_extension.lstrip('.')

    return file_extension

def get_inventory_summary():

    all_raw_materials = models.RawMaterials.objects.all()

    return_data = []

    for raw_material in all_raw_materials:
        total_inventory_for_the_raw_materials = models.Inventory.objects.filter(raw_material=raw_material.id)

        if not total_inventory_for_the_raw_materials:
            return_data.append({
                'raw_material': raw_material.id,
                'total': 0,
                'consumed': 0,
                'wastage': 0
            })
            continue

        total_raw_material_quantity = sum(item.quantity for item in total_inventory_for_the_raw_materials)
        total_raw_material_wasted = sum(item.wastage for item in total_inventory_for_the_raw_materials)

        for product in models.Products.objects.all():
            product_recipe_materials = product.recipe_materials

            for product_recipe_material in product_recipe_materials:
                if product_recipe_material['raw_material'] == raw_material.id:
                    total_quantity_consumed = models.Sales.objects.filter(menu_item__product=product).aggregate(Sum('quantity'))['quantity__sum'] or 0

                    total_quantity_required_for_one = sum(recipe_material['quantity'] for recipe_material in product.recipe_materials if recipe_material['raw_material'] == raw_material.id)/product.quantity
                    total_raw_material_consumed = total_quantity_consumed * total_quantity_required_for_one

                    return_data.append({
                        'raw_material': raw_material.id,
                        'total': total_raw_material_quantity,
                        'consumed': total_raw_material_consumed,
                        'wastage': total_raw_material_wasted
                    })

    return return_data
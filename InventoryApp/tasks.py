import random
from django.db.models import Sum
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler

def check_inventory_level():
    from .models import RawMaterials, Inventory, Products
    try:
        all_raw_materials = RawMaterials.objects.all()

        for raw_material in all_raw_materials:
            try:
                latest_inventory = Inventory.objects.filter(raw_material=raw_material.id).latest('created_at')
            except Inventory.DoesNotExist:
                print(f"No inventory found for the raw material: {raw_material.name}")
                continue

            for product in Products.objects.all():
                product_recipe_materials = product.recipe_materials

                for recipe_material in product_recipe_materials:
                    if recipe_material['raw_material'] == raw_material.id:
                        date = latest_inventory.created_at
                        total_quantity_consumed = get_total_quantity_consumed(product, date)

                        total_quantity_required_for_one = calculate_total_quantity_required(product, raw_material)     
                        total_quantity_consumed = total_quantity_consumed * total_quantity_required_for_one
                        if total_quantity_consumed >= latest_inventory.total_quantity_remaining:
                            risk_levels = ['High', 'Medium', 'Low']
                            # select random risk level
                            risk_level = random.choice(risk_levels)
                            send_inventory_alert(raw_material, latest_inventory, total_quantity_consumed, risk_level)
                        else:
                            print(f"Inventory level is good for the raw material: {raw_material.name}")
    except Exception as e:
        print(f"An error occurred in check_inventory_level: {str(e)}")

def get_total_quantity_consumed(product, date):
    from .models import Sales
    total_quantity_consumed = Sales.objects.filter(menu_item__product=product, date__gt=date).aggregate(Sum('quantity'))['quantity__sum'] or 0
    return total_quantity_consumed

def calculate_total_quantity_required(product, raw_material):
    recipe_materials = product.recipe_materials
    total_quantity_required = sum(recipe_material['quantity'] for recipe_material in recipe_materials if recipe_material['raw_material'] == raw_material.id)
    return total_quantity_required / product.quantity if product.quantity != 0 else 0

def send_inventory_alert(raw_material, latest_inventory, total_quantity_consumed, risk_level):
    try:
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            'InventoryApp',
            {
                'type': 'send_inventory_alerts',
                'value': {
                    'raw_material': raw_material.id,
                    'alert': f"Your Inventory level is finished for the raw material: {raw_material.name}. Please order the raw material.",
                    'risk_level': risk_level,
                    'total_quantity_remaining': latest_inventory.total_quantity_remaining - total_quantity_consumed
                }
            }
        )
    except Exception as e:
        print(f"An error occurred in send_inventory_alert: {str(e)}")

def start():
    try:
        scheduler = BackgroundScheduler()
        # scheduler.add_job(check_inventory_level, CronTrigger(day_of_week='mon-thu', hour='11-15', second='15'))
        scheduler.add_job(check_inventory_level, 'interval', seconds=30)
        # scheduler.add_job(check_inventory_level, 'cron', hour='11,14', minute=0)
        scheduler.start()
    except Exception as e:
        print(f"An error occurred in start: {str(e)}")

def myTask():
    print("scheduler task run at: ", datetime.now().strftime("%H:%M:%S"))


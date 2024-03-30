from django.apps import AppConfig
from . import tasks


class InventoryAppConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "InventoryApp"

    def ready(self):
        tasks.start()

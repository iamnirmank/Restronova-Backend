# Import the task function from tasks.py
from asyncio import Task
import datetime
from .tasks import check_inventory_level

# Register the task to be executed
def register_task():
     # Schedule the task to run every day at 3:00 AM
    check_inventory_level.schedule(repeat=Task.DAILY, time=datetime.time(hour=3, minute=0))

    
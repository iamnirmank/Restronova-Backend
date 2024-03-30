from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Outlet, User, Restaurant

class RestaurantAdmin(admin.ModelAdmin):
    list_display = ['restaurant_code', 'name', 'contact_no', 'email', 'subscription_token']
    search_fields = ['restaurant_code', 'name', 'contact_no', 'email']

admin.site.register(Restaurant, RestaurantAdmin)

class OutletAdmin(admin.ModelAdmin):
    list_display = ['outlet_code', 'addresss', 'contact_no', 'email', 'restaurant']
    search_fields = ['outlet_code', 'addresss', 'contact_no', 'email']

admin.site.register(Outlet, OutletAdmin)

class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ['email', 'name', 'outlet', 'contact_no', 'address', 'role', 'is_verified']
    search_fields = ['email', 'name', 'contact_no', 'address']
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('name', 'contact_no', 'address', 'role')}),
        ('Permissions', {'fields': ()}), 
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'name', 'outlet', 'contact_no', 'address', 'role', 'is_verified', 'password1', 'password2'),
        }),
    )
    ordering = ['email']
    list_filter = ['is_verified'] 

admin.site.register(User, CustomUserAdmin)

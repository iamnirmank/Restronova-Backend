# serializers.py
from rest_framework import serializers
from . import models

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = '__all__'

class OutletSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Outlet
        fields = '__all__'

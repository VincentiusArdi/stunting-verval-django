from rest_framework import serializers
from .models import DataStunting

class StuntingSerializers (serializers.ModelSerializer):
    class Meta:
        model = DataStunting
        fields = '_all_'
# orders/serializers.py
from rest_framework import serializers
from .models import Order

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['id', 'customer_name', 'product_id', 'quantity'] # Campos a exponer en la API
        # Puedes hacer 'id' read-only si prefieres
        # read_only_fields = ['id']
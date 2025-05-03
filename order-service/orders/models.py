# orders/models.py
from django.db import models

class Order(models.Model):
    # Django añade un 'id' PK automáticamente
    customer_name = models.CharField(max_length=255)
    product_id = models.BigIntegerField() # Asume que el ID del producto es un número grande
    quantity = models.IntegerField()
    # Podrías añadir created_at, updated_at, etc.
    # created_at = models.DateTimeField(auto_now_add=True)
    # updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Order {self.id} by {self.customer_name}"

    # Opcional: Especificar nombre de tabla si no quieres el default 'orders_order'
    # class Meta:
    #     db_table = 'orders'
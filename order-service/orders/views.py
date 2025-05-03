# orders/views.py
from rest_framework import viewsets
from .models import Order
from .serializers import OrderSerializer

class OrderViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows orders to be viewed or edited.
    """
    queryset = Order.objects.all().order_by('-id') # O el orden que prefieras
    serializer_class = OrderSerializer
    # DRF ModelViewSet provee acciones .list(), .create(), .retrieve(),
    # .update(), .partial_update(), .destroy() automáticamente.
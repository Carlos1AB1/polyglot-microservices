# orders/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter # <-- Asegúrate que sea DefaultRouter
from .views import OrderViewSet

# --- CAMBIO AQUÍ ---
# Añade trailing_slash=False para que las rutas base no necesiten la barra
router = DefaultRouter(trailing_slash=False)
# --- FIN DEL CAMBIO ---

router.register(r'orders', OrderViewSet, basename='order')

urlpatterns = [
    path('', include(router.urls)),
]
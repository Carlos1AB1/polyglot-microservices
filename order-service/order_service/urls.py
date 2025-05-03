# order_service/urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('orders.urls')), # Incluye las URLs de la app 'orders' en la raíz
                                     # El gateway reenviará /api/orders/** a esta raíz (después de StripPrefix)
]
# orders/apps.py
from django.apps import AppConfig
import sys
import os
import atexit

# Flag para evitar doble inicialización con auto-reloader de Django
eureka_started = False

class OrdersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'orders'
    eureka_thread = None

    def ready(self):
        # ready() puede llamarse dos veces con runserver --noreload es False (default)
        # Usamos una variable o chequeamos si es el proceso principal
        global eureka_started
        is_runserver = 'runserver' in sys.argv
        is_main_process = os.environ.get('RUN_MAIN') == 'true' or not is_runserver

        if is_main_process and not eureka_started and is_runserver:
            print("Starting Eureka client from OrdersConfig.ready()...")
            # Importar aquí para evitar problemas de importación temprana
            from . import eureka
            self.eureka_thread = eureka.run_eureka_in_thread()
            # Registrar función de limpieza al salir
            atexit.register(eureka.stop_eureka_client)
            eureka_started = True
        elif not is_runserver:
             # Si no es runserver (ej. test, shell, etc.), no iniciar Eureka
             pass
        # else:
        #    print("Skipping Eureka client start in OrdersConfig.ready() (reloader process or already started)")
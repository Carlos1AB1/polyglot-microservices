# orders/eureka.py
import py_eureka_client.eureka_client as eureka_client
import threading
import logging
import time
import os
import atexit # Necesario para registrar la función de limpieza

# --- Configuración de Logging ---
# Configura el logger básico para ver mensajes INFO y ERROR
logging.basicConfig(level=logging.INFO, format='%(asctime)s - [%(threadName)s] - %(levelname)s - %(name)s - %(message)s')
log = logging.getLogger(__name__) # Logger específico para este módulo

# --- Configuración del Servicio y Eureka ---
# Nombre con el que se registrará en Eureka (MAYÚSCULAS para consistencia con Java)
APP_NAME = "ORDER-SERVICE-PY"
# Puerto en el que correrá el servicio Django/Flask
INSTANCE_PORT = int(os.getenv("DJANGO_PORT", 8083))
# URL del servidor Eureka
EUREKA_SERVER = os.getenv("EUREKA_URL", "http://localhost:8761/eureka/")
# Hostname a registrar en Eureka. 'localhost' suele ser seguro para desarrollo local.
# Si tienes problemas con localhost, podrías intentar obtener la IP local, pero requiere más código.
INSTANCE_HOSTNAME = os.getenv("INSTANCE_HOSTNAME", "localhost")
# Opcional: IP explícita (generalmente no necesaria si hostname funciona)
# INSTANCE_IP = os.getenv("INSTANCE_IP", None)

# --- Control del Hilo ---
# Evento para señalar al hilo de Eureka que debe detenerse limpiamente
stop_event = threading.Event()
# Variable para rastrear si el cliente ya se inició (intento de evitar doble init con reloader)
_eureka_initialized = False

def start_eureka_client():
    """
    Función ejecutada en un hilo separado para registrarse en Eureka y mantener heartbeats.
    Reintenta la conexión si falla.
    """
    global _eureka_initialized
    if _eureka_initialized:
        log.warning("Intento de iniciar el cliente Eureka cuando ya está marcado como inicializado.")
        return # Evita iniciar múltiples veces desde el mismo proceso

    _eureka_initialized = True # Marcar como inicializado

    while not stop_event.is_set():
        try:
            log.info(f"Intentando registrar en Eureka: {EUREKA_SERVER} como {APP_NAME} en {INSTANCE_HOSTNAME}:{INSTANCE_PORT}")

            # Inicializar el cliente Eureka - ¡Usando init()!
            eureka_client.init(
                eureka_server=EUREKA_SERVER,
                app_name=APP_NAME,
                # Información de la Instancia (¡Importante!)
                instance_port=INSTANCE_PORT,
                instance_host=INSTANCE_HOSTNAME, # Proporcionar explícitamente 'localhost' o una IP/hostname válido
                # instance_ip=INSTANCE_IP, # Descomentar si necesitas IP explícita
                # --- Opcional: URLs de estado (requieren endpoints en tu app Django/Flask) ---
                # health_check_url=f"http://{INSTANCE_HOSTNAME}:{INSTANCE_PORT}/health/", # Ruta a tu endpoint de health
                # status_page_url=f"http://{INSTANCE_HOSTNAME}:{INSTANCE_PORT}/info/",   # Ruta a tu endpoint de info/status
                # --- Intervalos (opcional, usar defaults si no es necesario cambiar) ---
                # renewal_interval_in_secs=10, # Default 30
                # duration_in_secs=30,         # Default 90
            )
            log.info(f"Registro inicial con Eureka ({APP_NAME}) exitoso. Los heartbeats se manejarán internamente.")

            # El cliente maneja los heartbeats. Esperamos la señal de detención.
            stop_event.wait() # Bloquea este hilo hasta que stop_event.set() sea llamado

        except Exception as e:
            log.error(f"Error durante la inicialización/operación de Eureka: {e}. Reintentando en 15 segundos...")
            # Asegurarse de limpiar el estado si la inicialización falló, para reintentar
            try:
                 # No llames a stop aquí dentro del bucle si la inicialización falló,
                 # ya que podría no estar en un estado válido para detenerse.
                 # Simplemente reintentaremos init en la siguiente iteración.
                 pass
            except Exception as stop_err:
                 log.error(f"Error adicional al intentar limpiar estado de Eureka: {stop_err}")

            # Esperar antes de reintentar, pero respetar la señal de detención
            stop_event.wait(timeout=15) # Espera 15s O hasta que stop_event sea activado

    log.info("Bucle del hilo de Eureka terminado.")
    # Intento final de detener limpiamente al salir del bucle
    stop_eureka_client_internal()

def stop_eureka_client_internal():
    """Función interna para detener el cliente Eureka, manejando excepciones."""
    try:
        # py_eureka_client < 0.11 usa stop síncrono
        # py_eureka_client >= 0.11 usa stop asíncrono, pero no podemos usar await aquí
        # Llamamos a stop de todas formas, puede funcionar o no dependiendo de la versión
        # y si el loop de eventos asyncio está disponible.
        log.info("Intentando detener el cliente Eureka (interno)...")
        eureka_client.stop()
        log.info("Llamada a eureka_client.stop() completada.")
    except Exception as e:
        # Ignorar errores al detener, especialmente si nunca se inició correctamente
        # o si se intenta detener una corutina sin await.
        log.warning(f"Se ignoró una excepción al intentar detener Eureka: {e}")

def stop_eureka_client():
    """Función pública para ser llamada desde fuera (ej. atexit) para detener el hilo."""
    global _eureka_initialized
    log.info("Señalando al hilo del cliente Eureka para detenerse...")
    stop_event.set() # Señaliza al bucle while para que termine
    _eureka_initialized = False # Permitir reinicio si la app se recarga

    # No llamamos a stop_eureka_client_internal aquí directamente,
    # dejamos que el hilo termine su bucle y lo llame él mismo.

def run_eureka_in_thread():
    """Inicia el cliente Eureka en un hilo separado y lo retorna."""
    # Reiniciar el evento por si se reutiliza la función (aunque no debería con la lógica de apps.py)
    stop_event.clear()

    eureka_thread = threading.Thread(target=start_eureka_client, name="EurekaClientThread")
    eureka_thread.daemon = True # Permite que el programa principal salga aunque este hilo esté activo
    eureka_thread.start()
    log.info("Hilo del cliente Eureka iniciado.")

    # Registrar la función de limpieza para cuando el intérprete Python termine
    # Esto es un respaldo por si el cierre de Django no lo llama
    atexit.register(stop_eureka_client)

    return eureka_thread

# Asegurarse que la limpieza ocurra si este módulo se importa y se cierra el programa
# atexit.register(stop_eureka_client) # Movido dentro de run_eureka_in_thread
# scripts/eventos.py

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/..")

from scripts.arrancar_django import * #para arrancar django y detectar actividades sin necesidad de entrar a la web



import os # para la verificacion de existencia de un archivo
import time  # para arrancar la funcion 'analizar_eventos' cada 15 (para hacer pruebas sin necesidad de entrar necesariamente a al web)
from django.core.mail import send_mail  # para correo

from django.conf import settings  # para acceder al settigs, en donde esta informacion del correo que debe recibir las alertas


LOG_SISTEMA = "/var/log/auth.log"  # puede cambiar según el sistema
LOG_HIDS = "/home/ariel_acosta/HIDS_Proyecto/logs/eventos_sistema.log"

PATRONES_ALERTA = [
    "Failed password",  # intento fallido de contrasenha
    "Accepted password",  # cuando si pudo ingresar, aca lo sospechoso sera la hora de inicio de sesion
    "session closed",   # detectar cuando cierra sesion
  #  "sudo",         # comandos ejecutados como superusuario
]


# funcion principal para el monitoreo, esta funcion revisa en cada ejecucion el directorio '/var/log/auth.log'
def analizar_eventos():
    """
    Analiza el log del sistema y guarda eventos sospechosos en el log del HIDS.
    También envía un correo si se detectan eventos.
    """
    eventos_encontrados = []


    # Limpiamos el log propio para no duplicar, porque sino, guarda informacion redundante
    with open(LOG_HIDS, "w") as f:
        pass  # con 'pass' simplemente vacía el archivo


    if not os.path.exists(LOG_SISTEMA):
        return ["No se encontro el archivo de log del sistema."]

    with open(LOG_SISTEMA, "r") as f:  # abrimos en modo lectura '/var/log/auth.log'
        for linea in f:
            for patron in PATRONES_ALERTA:   # buscamos las palabras 'claves'
                if patron in linea:  # si se encuentra, se copia toda esa linea
                    mensaje = linea.strip()  # la linea que contiene info, se carga en 'mensaje'
                    eventos_encontrados.append(mensaje)  # cargamos tambien en eventos_encontrados
                    guardar_en_log(mensaje)   # y se carga tambien en el .log
                    break

    if eventos_encontrados:   # si es distinto de cero o es verdadero
        enviar_alerta_correo(eventos_encontrados)  # se envia la alerta por correo
    else:
        return ["No se encontraron eventos sospechosos."]

    return eventos_encontrados


# para ir guardando los eventos/mensajes sospechosos en el .log
def guardar_en_log(mensaje):
    """
    Guarda un evento en el archivo de log propio.
    """
    with open(LOG_HIDS, "a") as f:
        f.write(f"{mensaje}\n")

# para leer el .log y usar esa informacion para mostrar en la web
def leer_log_eventos():
    """
    Lee los eventos registrados previamente en el log del HIDS.
    """
    if os.path.exists(LOG_HIDS):
        with open(LOG_HIDS, "r") as f:
            return f.readlines()
    return ["No hay eventos registrados aun."]


# funcion que se encarga de enviar las alertas al correo
def enviar_alerta_correo(eventos):
    """
    Envía un correo con los eventos detectados.
    """
    mensaje = "Se han detectado eventos sospechosos en el sistema:\n\n"
    mensaje += "\n".join(eventos)

    send_mail(
        subject="Alerta HIDS - Eventos del sistema",
        message=mensaje,
        from_email=None,
        recipient_list=[settings.ALERTA_EMAIL_RECEPTOR],
        fail_silently=False
    )






# esto es para que trabaje en segundo plano el scripts, entonces de esta manera puede detectar en todo momento 'actividades sospechosas'

if __name__ == "__main__":
    while True:
        analizar_eventos()
        time.sleep(15)



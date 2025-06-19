# scripts/procesos.py

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/..")

from scripts.arrancar_django import * #para arrancar django y detectar actividades sin necesidad de entrar a la web


import psutil  # libreria para detectar procesos que consumen muchos recursos
import time
from django.core.mail import send_mail

from django.conf import settings

def detectar_procesos(cpu_max=30.0, mem_max=50.0):
    """
    Detecta procesos que excedan los límites de CPU o memoria.
    Si se detectan, también se envía un correo de alerta.

        cpu_max (float): Porcentaje máximo de uso de CPU permitido por proceso.
        mem_max (float): Porcentaje máximo de uso de memoria permitido por proceso.

    """
    alertas = []  # aca en donde se guardaran las alertas

    # Iteramos sobre los procesos en ejecución y capturamos uso de CPU y RAM, con 'psutil.process_iter()' se captura los procesos en ejecucion  
    for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
        try:
            cpu = proc.info['cpu_percent']   #  calculamos lo que consume el porcentaje de cpu el proceso
            mem = proc.info['memory_percent']   #  caculamos lo que consume el porcentaje de memoria el proceso
            if cpu > cpu_max or mem > mem_max:   # se hace la comparacion
                alertas.append(proc.info)    # si se cumple, cargamos la informacion a 'alerta' info:proc.info
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            # El proceso puede haber terminado o no se puede acceder
            continue

    # Si se detectaron procesos sospechosos, se envía una alerta
    if alertas:  # si hay 'alerta' (distinto de cero)
        enviar_alerta_por_correo(alertas)  #  enviamos como parametro la 'alerta', para que nos llegue por correo...

    return alertas


def enviar_alerta_por_correo(procesos):   # procesos seria 'alerta' los procesos sospechoso que cosumen mucho
    """
    Envía un correo con la lista de procesos sospechosos detectado
    """
    mensaje = "Se han detectado procesos sospechosos en el sistema:\n\n"   # mensaje que llega al correo (mas el proceso sospechoso)

    for p in procesos:
        mensaje += f"PID: {p['pid']}, Nombre: {p['name']}, CPU: {p['cpu_percent']}%, RAM: {p['memory_percent']}%\n"     # a 'mensaje' se le agrega la informacion importante

    send_mail(
        subject="Alerta HIDS - Procesos Sospechosos",
        message=mensaje,  # mensaje que mostrara (sobre el proceso en especifico que consume mucho)
        from_email=None,  # Usará DEFAULT_FROM_EMAIL en settings.py
        recipient_list=[settings.ALERTA_EMAIL_RECEPTOR],    # el correo que va a recibir (mi correo)
        fail_silently=False
    )








# esto es para que trabaje en segundo plano el scripts, entonces de esta manera puede detectar en todo momento 'actividades sospechosas'

if __name__ == "__main__":
    while True:
        detectar_procesos()
        time.sleep(15)


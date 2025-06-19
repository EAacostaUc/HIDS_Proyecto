# scripts/integridad.py

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/..")

from scripts.arrancar_django import * #para arrancar django y detectar actividades sin necesidad de entrar a la web



import hashlib # estos es para generar hashes a los archivos (sha-256)
import os
import datetime  # para colocarle fechas y horas a los eventos ocurridos
import time  # para ejecutar cada cierto tiempo este script al arrancarlo en segundo plano
from django.core.mail import send_mail

from django.conf import settings   # para tener a la vista la configuracion que hicimos para recibir alertas al correo


# Ruta del archivo de registros de hashes
HASH_REGISTRO = "/home/ariel_acosta/HIDS_Proyecto/hashes_integridad.txt"

# Archivo de log donde se anotan las modificaciones
LOG_PATH = "/home/ariel_acosta/HIDS_Proyecto/logs/integridad.log"

# Archivos a verificar
ARCHIVOS_MONITOREADOS = [
    "/etc/passwd",
    #"/etc/shadow",
]

# funcion para hacer el calculo de hashes, calculamos el hash de un archivo para luego compararlo si es que hubo modificaciones
def calcular_hash(path):
    """
    Calcula el hash SHA-256 de un archivo.
    """
    try:
        with open(path, "rb") as f:   # 'path' es el archivo a calcular, y lo abrimos en modo binario
            return hashlib.sha256(f.read()).hexdigest() # genera una hash en formato hexadecimal
    except FileNotFoundError:
        return None

# esta funcion guarda todos los hashes generados del archivo
def cargar_hashes_anteriores():
    """
    Lee los hashes anteriores desde el archivo de registro.
    """
    hashes = {}  # lista vacia en donde cargaremos el hash
    if os.path.exists(HASH_REGISTRO):
        with open(HASH_REGISTRO, "r") as f:  # abre el archivo y lee el contenido
            for linea in f:
                archivo, hash_valor = linea.strip().split("::")  # carga por separado la ruta del archivo modificado y su hash
                hashes[archivo] = hash_valor # luego, la ruta con el hash es cargado en 'hashes', que se usara para la comparacion
    return hashes

#esta funcion guarda los hashes actuales (el hash va cambiando si hay modificacion)
#entonces, va guardando o sobreescribiendo 'HASH_REGISTRO' con el nuevo hash del archivo
def guardar_hashes_actuales(hashes):
    """
    Guarda los nuevos hashes después de la comparación.
    """
    with open(HASH_REGISTRO, "w") as f:
        for archivo, hash_valor in hashes.items():  
            f.write(f"{archivo}::{hash_valor}\n")

# para ir cargando en el .log lo eventos sospechosos
def registrar_en_log(archivo):
    """
    Escribe una línea en el log si un archivo fue modificado.
    """
    ahora = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_PATH, "a") as f:  # se va agregando nuevos eventos sin borrar los anteriores por eso se usa "a"
        f.write(f"[{ahora}] ⚠️ Integridad comprometida en: {archivo}\n")

# funcion encargado de hacer los envios de laertas al correo...
def enviar_alerta(archivo):
    """
    Envía un correo si se detecta una modificación.
    """
    mensaje = f"ALERTA HIDS: El archivo {archivo} fue modificado."
    send_mail(
        subject="Alerta de Integridad de Archivos",
        message=mensaje,
        from_email=None,
        recipient_list=[settings.ALERTA_EMAIL_RECEPTOR],
        fail_silently=False
    )



# funcion principal encargado de hacer el monitoreo 
def verificar_integridad():
    """
    Ejecuta la verificación de integridad comparando los hashes actuales con los anteriores.
    """
    hashes_anteriores = cargar_hashes_anteriores()   # cargamos el hash del archivo (hash "original")
    hashes_actuales = {}  # lista en donde se va a cargar el nuevo hash del archivo modificacdo

    for archivo in ARCHIVOS_MONITOREADOS:   # revisamos los archivos 
        hash_actual = calcular_hash(archivo)  # calculamos el hash actual del archivo (cambiara si es que sufrio modificacion) y gyardamos en 'hash_actual'
        hashes_actuales[archivo] = hash_actual   # en 'hashes_actuales' guardmaos la ruta del archivo y su hash

        if archivo in hashes_anteriores:   # el archivo si tiene su hash anterior, antes de la modificacion
            if hash_actual != hashes_anteriores[archivo]:  # se compara el hash actual con el hash anterior, y si son distintos, hubo modificacion
                registrar_en_log(archivo)  # se registra el evento en el .log
                enviar_alerta(archivo)  # se envia la alerta
        else:
            print(f"[INFO] Registrando nuevo archivo: {archivo}")

    guardar_hashes_actuales(hashes_actuales)   # y el nuevo hash del archivo modificado se guarda en 'HASH_REGISTRO' para proximas comparaciones









# esto es para que trabaje en segundo plano el scripts, entonces de esta manera puede detectar en todo momento 'actividades sospechosas'

if __name__ == "__main__":
    while True:
        verificar_integridad()
        time.sleep(15)  # ejecutamos la funcion cada 15 segundos, esto se puede colocar el tiempo que queramos



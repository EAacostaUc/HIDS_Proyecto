# scripts/configuracion.py
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/..")

from scripts.arrancar_django import *


import hashlib  # esto es para generar sha-256 (un hash criptografico), para el directorio (si el directorio se modifica, el sha-256 cambia)
import os   # esto es para verificar si el archivo existe
import datetime   # solo para mostrar con mas detalle los movimientos sospechosos
import time
import subprocess  # para la deteccion de puertos abiertos...

from django.core.mail import send_mail  # para correo

from django.conf import settings   # para acceder a configuraciones de Django
 

# Ruta donde se guardarán los hashes originales
HASH_REGISTRO = "/home/ariel_acosta/HIDS_Proyecto/config_hashes.txt"    # en esta direccion se creara el .txt que comtendra el hash creado inicialmente, lo cual se usara para hacer las comparaciones

LOG_PATH = "/home/ariel_acosta/HIDS_Proyecto/logs/configuracion.log"



# Archivos críticos a monitorear
ARCHIVOS_CRITICOS = [
# archivo, que si se modifica, salta la alerta (se agrega mas?)
    "/etc/ssh/sshd_config",  #archivo de config de SSH
    "/etc/ufw/ufw.conf", # archivo de configuracion de ufw (firewall)
]

# funcion para hacer el calculo de hashes, calculamos el hash de un archivo para luego compararlo si es que hubo modificaciones
def calcular_hash(path):
    """
    Calcula el hash SHA-256 del archivo que especificamos
    """
    try:
        with open(path, "rb") as f:  # abre el archivo (modo binario)
            contenido = f.read()  # lee el contenido
            return hashlib.sha256(contenido).hexdigest()  # se hace el calculo de hash
    except FileNotFoundError:
        return None   # si el archivo no existe


# esta funcion guarda todos los hashes generados del archivo
def cargar_hashes_previos():
    """
    Carga los hashes registrados en el archivo (el hash original generado al principio)
    """
    hashes = {}   # lista vacia en donde cargaremos el hash
    if os.path.exists(HASH_REGISTRO):
        with open(HASH_REGISTRO, "r") as f:   # abre el archivo y lee el contenido
            for linea in f:
                archivo, hash_valor = linea.strip().split("::")  # carga por separado la ruta del archivo modificado y su hash
                hashes[archivo] = hash_valor  # luego, la ruta con el hash es cargado en 'hashes', que se usara para la comparacion
    return hashes

#esta funcion guarda los hashes actuales (el hash va cambiando si hay modificacion)
#entonces, va guardando o sobreescribiendo 'HASH_REGISTRO' con el nuevo hash del archivo
def guardar_hashes_actuales(hashes):
    """
    Guarda los hashes actuales en el archivo (guarda todos los hashes generados, cuando ya se toco el archivo (no guarda el primer hash generado al principio (original)))
    """
    with open(HASH_REGISTRO, "w") as f:
        for archivo, hash_valor in hashes.items():
            f.write(f"{archivo}::{hash_valor}\n")


# para ir cargando en el .log lo eventos sospechosos
def registrar_en_log(archivo):
    """
    Guarda en el .log la alerta con fecha y hora.
    """
    ahora = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_PATH, "a") as log:   # se va agregando nuevos eventos sin borrar los anteriores por eso se usa "a"
        log.write(f"[{ahora}] MODIFICADO: {archivo}\n")


# funcion encargado de hacer los envios de las alertas al correo...
def enviar_alerta(archivo, opcion):
    """
    Envía una alerta por correo si el archivo fue modificado.
    """
    if opcion == 1:  # cuando se modifican los archivos criticos
    	mensaje = f"ALERTA: Se detectó una modificación en el archivo crítico: {archivo}"
    elif opcion == 0: # para mostrar puertos abiertos
    	mensaje = f"ALERTA: {archivo}"

    send_mail(
        subject="Alerta HIDS - Configuración Modificada/Puertos abiertos",
        message=mensaje,
        from_email=None,
        recipient_list=[settings.ALERTA_EMAIL_RECEPTOR],
        fail_silently=False
    )




# funcion para detectar puertos abiertos
def registrar_puertos_abiertos():
    ahora = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    resultado = subprocess.check_output(['ss', '-tuln']).decode()  # utilizamos el comando 'ss -tuln'

    puertos_abiertos = set()  # para almacenar los puertos detectados con 'set()' se envitan los puertos duplicados, ej: puerto '53' duplicados

    for linea in resultado.splitlines()[1:]:  # omitimos la cabecera que se muestra al usar 'ss -tuln', bajamos una linea
        partes = linea.split() # cargamos cada linea en 'partes' y usando 'split()' los separamos por comas
        if len(partes) >= 5:   # aseguramos de que haya 5 o mas columnas (en la 5ta columna esta lo que queremos)
            direccion = partes[4]  # la columna de "Local Address:Port"
            if ':' in direccion:   # revisamos si hay ':' en la cadena 'direccion'
                puerto = direccion.split(':')[-1]   # si hay, cargamos en puerto solo lo que esta despues de ':', que seria el puerto
                if puerto.isdigit():  # verificamos que lo que se extrajo sea solo numero (digitos)
                    puertos_abiertos.add(puerto)  # cargamos en 'puertos_abiertos' el puerto encontrado, si hay puertos repetidos, no se vuelve a cargar
                    # en 'puertos_abiertos'

    if puertos_abiertos:
        contenido = f"[{ahora}] Puertos abiertos detectados: {', '.join(sorted(puertos_abiertos))}\n"
    else:
        contenido = f"[{ahora}] No se detectaron puertos abiertos.\n"

    with open(LOG_PATH, "a") as log:
        log.write(contenido)

    # enviamos alerta por correo
    enviar_alerta(contenido, 0)






# funcion principal encargado de hacer el monitoreo
def verificar_configuracion():
    """
    Compara los hashes actuales con los almacenados
    """
    hashes_previos = cargar_hashes_previos()   # cargamos el hash del archivo (hash "original")
    hashes_actuales = {}   # lista en donde se va a cargar el nuevo hash del archivo modificacdo

    for archivo in ARCHIVOS_CRITICOS:  # revisamos los archivos
        hash_actual = calcular_hash(archivo)   # en 'hash_actual' se guarda el hash generado del archivo al principio (hash original)
        hashes_actuales[archivo] = hash_actual   # en 'hashes_actuales' guardmaos la ruta del archivo y su hash

        if archivo in hashes_previos:   # el archivo si tiene su hash anterior, antes de la modificacion
            if hashes_previos[archivo] != hash_actual:    # se compara el hash actual con el hash anterior, y si son distintos, hubo modificacion
                enviar_alerta(archivo, 1)   # se envia la alerta, colocamos opcion 1 para mostrar un mensaje diferente...
                registrar_en_log(archivo)  # se registra el evento en el .log
        else:
            # Si es la primera vez, no se alerta
            print(f"[INFO] Registrando por primera vez: {archivo}")

    guardar_hashes_actuales(hashes_actuales)  # despues de jejcutar toda la funcion, se sobreescribe los hashes anteriores por los hashes actuales, y asi sucecivamente...
    registrar_puertos_abiertos()   # llamamos la funcion, para mostrar lo puertos abiertos









# esto es para que trabaje en segundo plano el scripts, entonces de esta manera puede detectar en todo momento 'actividades sospechosas'

if __name__ == "__main__":
    while True:
        verificar_configuracion()
        time.sleep(15)

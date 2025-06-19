# scripts/archivos.py

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/..")

from scripts.arrancar_django import * #para arrancar django y detectar actividades sin necesidad de entrar a la web


import time  # esto lo uso para definir cada cuando podre ejecutar este modulo
from watchdog.observers import Observer   # trae al "vigilante", el que observa en todo momento el sistema de archivos
from watchdog.events import FileSystemEventHandler    # clase base, que define como actuar cuando ocurre el evento
from django.core.mail import send_mail   # para correo
import datetime  # para usar fecha en los eventos detectados
import os  # para revisar si existe un archivo

from django.conf import settings

LOG_PATH = "/home/ariel_acosta/HIDS_Proyecto/logs/archivos.log"

# Lista temporal donde se guardan los eventos detectados
eventos_detectados = []  # lsita vacia en donde se iran guardando los eventos sospechosos

# esta clase reaciona de forma automatica cuando hay eventos sospechosos
class MiHandler(FileSystemEventHandler):
    def on_modified(self, event):  # recibe el 'event' eventos como parametro, eventos sospechosos
        mensaje = f"Modificado: {event.src_path}"   # se carga la info a 'mensaje', con la ruta del archivo modificado
        eventos_detectados.append(mensaje)
        registrar_en_log(mensaje)

    def on_created(self, event):
        mensaje = f"Creado: {event.src_path}"
        eventos_detectados.append(mensaje)
        registrar_en_log(mensaje)

    def on_deleted(self, event):
        mensaje = f"Eliminado: {event.src_path}"
        eventos_detectados.append(mensaje)
        registrar_en_log(mensaje)

#funcion que se encarga de cargar los eventos/mesajes en el .log
def registrar_en_log(mensaje):
    ahora = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # para colocar fecha y hora a los eventos
    with open(LOG_PATH, "a") as f:  # abrimos de modo que solo vaya agregando lo nuevos eventos generados
        f.write(f"[{ahora}] {mensaje}\n")

# funcion encargado de enviar las alertas a la correo..
def enviar_alerta_por_correo(eventos):
    mensaje = "Se han detectado cambios en el sistema de archivos:\n\n"
    mensaje += "\n".join(eventos) # el 'join' se usa para unir al mensaje anterior el nuevo mensaje
    send_mail(
        subject="Alerta HIDS - Cambios en archivos",
        message=mensaje,
        from_email=None,
        recipient_list=[settings.ALERTA_EMAIL_RECEPTOR],
        fail_silently=False
    )

#funcion principal para el monitoreo de sistemas de archivos 
def monitorear_directorio(path='/etc', duracion=5):  # teniendo como parametros la ruta del directorio critico y el tiempo de ejecucion para vigilar durente esos 5 segundos
    eventos_detectados.clear()  # limpiamos los eventos cada tanto para no llenar la web (los eventos ya se guardaron ya antes en el .log)
    observer = Observer()  # creamos un observador tipo 'Odserver', para vigilar los eventos sospechosos 
    observer.schedule(MiHandler(), path=path, recursive=True)  # el 'observer' que creamos le indicamos que use el manejador 'MiHandler' y la ruta 'path' (/etc) y con 
    # 'recursive' se logra revisar tambien subcarpetas del directorio analizado
    observer.start()  # arrancamos la vigilancia 
    try:
        time.sleep(duracion)  # trabaja durante el tiempo que le dimos para hacer la observacion
    finally:
        observer.stop()  # luego para la observacion...
        observer.join()   # ayuda a detener completamente la 'obserevacion' vigilancia...

    if eventos_detectados:  # si huvo eventos raros, se envia al correo
        enviar_alerta_por_correo(eventos_detectados)

    return eventos_detectados


# funcion encargado de cargar los mensajes/eventos sospechosos en el .log
def leer_log_archivos():
    if os.path.exists(LOG_PATH):
        with open(LOG_PATH, "r") as f:  # abrimos modo lectura para leer y mostrar en la web
            return f.readlines()  # leer el contenido
    return []




# esto es para que trabaje en segundo plano el scripts, entonces de esta manera puede detectar en todo momento 'actividades sospechosas'

if __name__ == "__main__":
    while True:
        monitorear_directorio()
        time.sleep(15)

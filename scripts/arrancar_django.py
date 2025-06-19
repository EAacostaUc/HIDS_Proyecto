# scripts/arrancar_django.py

import os   # esto lo use para obtener la ruta del script
import sys
import django  # esto es para inicializar django desde este script con el uso de 'django.setup()'

# Agrega la carpeta raíz del proyecto al path
#'__file__' es la ruta de este archivo (arrancar_django.py)
#con 'os.path.abspath' obtenemos la ruta absoluta, ej: /home/ariel_acosta/HIDS_Proyecto/scripts/arrancar_django.py
#con 'os.path.dirname' eliminamos el nombre del este script, ej: /home/ariel_acosta/HIDS_Proyecto/scripts
# y se le suma "/.." un paso atras, queda: /home/ariel_acosta/HIDS_Proyecto
#eso es lo que buscamos, porque en esa ruta esta nuestro entorno django...
#y cfinalmente con 'sys.path.append' le decimos a python que busque lo que necesite, como por ejemplo 'settings' que necesitara para 
#arrancar django
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/..")

# Le indica a Django dónde está el archivo de configuración, teniendo en cuenta
#'DJANGO_SETTINGS_MODULE' que es la variable que usa django para saber donde esta 'settings'
#'hids_web.settings' que es la ruta al archivo de configuracion de django
# es como importar 'settings' para acceder a las configuraciones necesarias para arrancar django, en donde esta el coreo, etc...
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hids_web.settings')


# Inicializa Django
django.setup()

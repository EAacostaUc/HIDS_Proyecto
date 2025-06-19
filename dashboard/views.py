from django.shortcuts import render

# Create your views here.
# estos ya estaban por defecto...
from django.shortcuts import render  # esto sirve para mostar las plantillas HTML
import os
import sys

# Permite importar el modulo externo scripts que tenemos (django no sabe de su existencia)
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))





# muestra principal al entrar a la web, para loguear
from django.contrib.auth.decorators import login_required # que solamente los usuarios autenticados puedan acceder a las vista

@login_required  # se exigen hacer login
def dashboard_principal(request):  # 'request' representa la solicitud hecha por el usuario en la web
    """
    Vista principal con menu de modulos (solo si el usuario está autenticado)
    """
    return render(request, 'dashboard/principal.html') # al hacer login, se avisa, y se muestra la ventana 'principal' donde se pueden ver las opciones a consultar






#para 'monitoreo de procesos'
from scripts.procesos import detectar_procesos  # desde 'scripts.procesos' importamos la funcion 'detectar_procesos'

@login_required    # lo agregamos para que solo se pueda ver/acceder si es que se inicion sesion
def ver_procesos(request): # 'request' representa la solicitud hecha por el usuario en la web
    """
    Vista que muestra procesos sospechosos en una tabla
    """
    procesos = detectar_procesos()   # se carga en 'procesos' el movimiento sospechoso
    return render(request, 'dashboard/procesos.html', {'procesos': procesos})  # se le pasa lo guardado en 'procesos' a procesos.html para mostrarlo en la pagina
    # se le pasa ('procesos') que es el nombre que usara en HTML, y (procesos) que contiene la info






#para monitoreo de archivos del sistema
from scripts.archivos import monitorear_directorio, leer_log_archivos   # llama a la funcion que tenemos en el directorio 'scripts' usando 'scripts.archivos'

# esto es para mostrar lo eventos ocurridos en tiempo real en la web, actividades sospechosas realizadas dentro del rango de 5 segundos
@login_required  # lo agregamos para que solo se pueda ver/acceder si es que se inicion sesion
def ver_archivos(request):   # 'request' representa la solicitud hecha por el usuario en la web
    """
    Vista que muestra los cambios detectados en un directorio del sistema
    """
    eventos = monitorear_directorio('/etc', duracion=5)    # esto es para mostrar en tiempo real, si es que hubo modificaciones dentro de esos 5 segundos mientras carga la pagina, lo detecta
    return render(request, 'dashboard/archivos.html', {'eventos': eventos})  # se le pasa lo guardado en 'eventos' a archivos.html para mostrar en la pagina


# estos es para mostrar el contenido de archivos.log, todo lo que se habia guardado ahi
@login_required
def eventos_archivos(request):
    log_eventos = leer_log_archivos()
    return render(request, 'dashboard/archivos_log.html', {'eventos': log_eventos}) # cree otro .html, para poder mostrar por separado los eventos ocurridos







#para monitoreo de configuracion del sistema
from scripts.configuracion import verificar_configuracion

@login_required     # lo agregamos para que solo se pueda ver/acceder si es que se inicion sesion
def ver_configuracion(request):   # 'request' representa la solicitud hecha por el usuario en la web
    """
    Vista que lee el archivo de log de configuración y muestra los eventos guardados.
    """

    verificar_configuracion()  # aca solo ya hice la llamada a la funcion para hacer el monitoreo y compara los hashes

    # luego, leemos lo guardado en 'configuracion.log' todos lo eventos sospechosos guardados
    log_path = "/home/ariel_acosta/HIDS_Proyecto/logs/configuracion.log"
    eventos = []

    if os.path.exists(log_path):
        with open(log_path, "r") as f:
            eventos = f.readlines()

    return render(request, 'dashboard/configuracion.html', {'eventos': eventos})   # y mostramos en la web, lo que se muestra son los eventos guardados en 'configuracion.log'






# para monitoreo de integridad de archivos
from scripts.integridad import verificar_integridad

@login_required
def ver_integridad(request):  # 'request' representa la solicitud hecha por el usuario en la web
    """
    Vista que muestra los eventos de integridad registrados en el log.
    """

    verificar_integridad()   #aca lo mismo, solo llamamos la funcion para el monitoreo

    # luego, leemos lo guardado en 'integridad.log' todos lo eventos sospechosos guardados
    log_path = "/home/ariel_acosta/HIDS_Proyecto/logs/integridad.log"
    eventos = []

    if os.path.exists(log_path):
        with open(log_path, "r") as f:
            eventos = f.readlines()

    return render(request, 'dashboard/integridad.html', {'eventos': eventos})  # y mostramos en la web, lo que se muestra son los eventos guardados en 'integridad.log'








# para 'registro y analisis de eventos del sistema'
from scripts.eventos import analizar_eventos, leer_log_eventos

@login_required
def ver_eventos_sistema(request):   # 'request' representa la solicitud hecha por el usuario en la web
    analizar_eventos()  # se llama a la funcion para el monitoreo
    eventos = leer_log_eventos()  # leemos el .log (eventos_sistema.log) del HIDS ya actualizado
    return render(request, 'dashboard/eventos.html', {'eventos': eventos})  # y mostramos en la web, lo que se muestra son los eventos guardados en 'eventos_sistema.log'


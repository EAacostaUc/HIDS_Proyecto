from django.urls import path  # esto es para definir rutas

from django.contrib.auth import views as auth_views # para traer las vistas de login y logout de django
 
from . import views  #importa todas las funciones del archivo views.py, que contiene todas las funciones de los modulos

# los 'name' se usan para no colocar la ruta en html, entonces es mas facil usar solo nombre especificos
#o sea, 'name' permite referencia la ruta en las plantilla html

# estas rutas se usan para redirigirte a las ventanas correspondientes
urlpatterns = [  # en esta lista 'urlpatterns' cargamos todas las rutas
    #agregamos las rutas de login y logout

    # al ingresar la ruta en el navegador, usando login/, con esto te redirige a la ventana para iniciar sesion
    path('login/', auth_views.LoginView.as_view(template_name='dashboard/login.html'), name='login'),

    # al hacer logout o cerrar sesion, se usa esta ruta para redirigirte del vuelta a login/
    path('logout/', auth_views.LogoutView.as_view(next_page='/login/'), name='logout'),

    # esto es la ruta para redirigirte a la "ventana principal", en donde se ven los botones a consultar
    path('dashboard/', views.dashboard_principal, name='dashboard_principal'),

    # y estos son las rutas de cada uno de los modulos, te redidige a la ventana y muestra tambien el contenido gracias a 'views.py'
    path('procesos/', views.ver_procesos, name='ver_procesos'),
    path('archivos/', views.ver_archivos, name='ver_archivos'),
    path('archivos/eventos/', views.eventos_archivos, name='eventos_archivos'),
    path('configuracion/', views.ver_configuracion, name='ver_configuracion'),
    path('integridad/', views.ver_integridad, name='ver_integridad'),
    path('eventos/', views.ver_eventos_sistema, name='ver_eventos_sistema'),


]


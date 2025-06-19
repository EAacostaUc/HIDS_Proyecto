#!/bin/bash

# script para iniciar todos los modulos del HIDS, para que se ejecuten en segundo plano
# ejecuta cada uno con 'nohup' (para ejecutar en segundo plano, incluso cuando se cierra la terminal)
# la salida se descarta (> /dev/null 2>&1), para evitar que se cree el archivo nohup.out, en donde se guarda info de los comandos que se imprimen normalmente en pantalla
# con '&', lo ejecuta en segundo plano, el ccomando nohup

echo "iniciando todos los modulos del HIDS en segundo plano"

# Monitoreo de eventos del sistema
#nohup python3 scripts/eventos.py > /dev/null 2>&1 &

# Monitoreo de configuración del sistema
nohup python3 scripts/configuracion.py > /dev/null 2>&1 &

# Monitoreo del sistema de archivos
nohup python3 scripts/archivos.py > /dev/null 2>&1 &

# Monitoreo de integridad de archivos
nohup python3 scripts/integridad.py > /dev/null 2>&1 &

# Monitoreo de procesos 
nohup python3 scripts/procesos.py > /dev/null 2>&1 &


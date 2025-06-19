#!/bin/bash

# script para detener todos los scripts del HIDS
# utiliza 'pkill -f' para matar cualquier proceso que coincida con el nombre completo del script.
# con '-f', se busca el nombre completo del proceso en toda la linea de comando

echo "deteniendo todos los modulos del HIDS"

#pkill -f "python3 scripts/eventos.py"

pkill -f "python3 scripts/configuracion.py"

pkill -f "python3 scripts/archivos.py"

pkill -f "python3 scripts/integridad.py"

pkill -f "python3 scripts/procesos.py"


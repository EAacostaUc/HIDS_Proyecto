#!/bin/bash

# Script de simulación de actividad sospechosa
# --------------------------------------------------
# Este script agrega una línea ficticia al archivo /etc/passwd
# con el fin de probar si el HIDS detecta la modificación
# y dispara la alerta correspondiente.

FECHA=$(date '+%Y-%m-%d %H:%M:%S')
echo "# Entrada falsa agregada automáticamente el $FECHA" >> /etc/passwd

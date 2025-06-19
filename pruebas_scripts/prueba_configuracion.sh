#!/bin/bash

#prueba para simular modificacion de configuracion crítica, en este caso para '/etc/ssh/sshd_config'

FECHA=$(date '+%Y-%m-%d %H:%M:%S')
echo "# esto es una prueba - $FECHA" >> /etc/ssh/sshd_config


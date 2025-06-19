#!/bin/bash

# prueba para el modulo de monitoreo de procesos...
# el proceso simula un uso elevado de CPU durante 15 segundos

echo "[PRUEBA] Iniciando proceso que consume CPU..."
python3 -c "while True: pass" &  # ejecuta un bucle infinito que consume mucho CPU y memoria, con '&' se consigue que se ejecute en segundo plano
PID=$!  # obtenemos el identificador del proceso, para luego matarlo...

# el proceso se ejecuta durante 15 segundos...
sleep 30

# luego, matamos el proceso
kill $PID

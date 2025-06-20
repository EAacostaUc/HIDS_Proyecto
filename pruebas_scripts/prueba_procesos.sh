#!/bin/bash

# prueba para el modulo de monitoreo de procesos...
# el proceso simula un uso elevado de CPU durante 15 segundos

echo "[PRUEBA] Iniciando proceso que consume CPU..."
python3 -c "while True: pass" &  # ejecuta un bucle infinito que consume mucho CPU y memoria, con '&' se consigue que se ejecute en segundo plano

# python3 -c "import multiprocessing; [multiprocessing.Process(target=lambda: exec('while True: pass')).start() for _ in range(4)]"
# esto es por si se quiere ejecutar varios a la vez...

PID=$!  # obtenemos el identificador del proceso, para luego matarlo...

# el proceso se ejecuta cada 30 seg...
sleep 30

# luego, matamos el proceso
kill $PID

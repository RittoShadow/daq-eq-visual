import os, signal, time, sys

signaled = False

def answer_yes_handler(signum, frame):
    global signaled
    signaled = True
    print "Detener"

def answer_no_handler(signum, frame):
    global signaled
    signaled = True
    print "Reiniciar"

# Obtener PID del proceso de app en c++ de daq-eq
pid = os.popen("pgrep 'RBA-DAQ-EQ'").read()

if pid :
    # Setear handlers
    signal.signal(signal.SIGUSR1, answer_yes_handler)
    signal.signal(signal.SIGUSR2, answer_no_handler)

    # Enviar signal SIGUSR2 a app en c++, para preguntar estado
    os.kill(int(pid), signal.SIGUSR2) # Unix version only...

    # Esperar respuesta
    time.sleep(5)

if signaled == False:
    print "NaN"

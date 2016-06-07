import os, signal

# Obtener PID del proceso de app en c++ de daq-eq
pid = os.popen("pgrep 'RBA-DAQ-EQ'").read()
if (pid) :
    # Enviar signal SIG_USR1 a app en c++, para iniciar/detener adquirir datos
    os.kill(int(pid), signal.SIGUSR1) # Unix version only...

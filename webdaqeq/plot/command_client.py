#Socket client example in python

import socket   #for sockets
import sys  #for exit
import time
import os
import re

def daqeq_is_running():
    route = os.path.dirname(os.path.abspath(__file__))
    os.chdir(route)
    result = os.popen("sudo python ask_daqeq_status.py").read().strip()

    if result == "1":
        return True

    return False


def command_server(message, params=None):
    print message + ' : command_server start -----------------------------------'

    if daqeq_is_running():
        print message + " : daqeq status 1"
        return -1
    else:
        print message + " : daqeq status 0"

    #create an INET, STREAMing socket
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except socket.error:
        print message + ' : Failed to create socket'
        return -1

    # print 'Socket Created'

    host = 'localhost';
    port = 5018;

    try:
        remote_ip = socket.gethostbyname( host )

    except socket.gaierror:
        #could not resolve
        print message + ' : Hostname could not be resolved. Exiting'
        return -1

    while True:
        n = s.connect_ex((remote_ip , port))
        if n == 0:
            break

    # print 'Socket Connected to ' + host + ' on ip ' + remote_ip

    #Send some data to remote server
    # message = sys.argv[1]

    try :
        #Set the whole string
        print message + " : sending the message"
        s.sendall(message)
        if re.search("n\ws", message):
            print message + " : waiting k"
            s.recv(4096)
            print message + ": sending param"
            s.sendall(params)
        if re.search("s\ws", message):
            print message + " : waiting k"
            s.recv(4096)
            print message + ": sending param"
            s.sendall(params)
        if message == "cag": #Aviso que quiero sensores
            reply = []
            while True: #Recibo sensores hasta que me llegue una "r"
                print message + " : waiting k or r"
                r = s.recv(4096) #Recibo datos de un sensor
                if r == "r":
                    print message + " : received r, sending k"
                    s.sendall("k")
                    print message + " : return reply"
                    return reply
                    # break
                print message + " : appending " + r
                reply.append(r.split(";")) #Guardo el sensor
                print message + " : sending k"
                s.sendall("k")
            # s.sendall("k")
        if message == "cas":
            print message + " : waiting k"
            s.recv(4096)
            print message + " : sending sensors"
            for sensor in params:
                print message + " : sending " + sensor
                s.sendall(sensor)
                print message + " : waiting k"
                s.recv(4096)
            print message + " : finished sending sensors waiting k"
            s.sendall("k")

    except socket.error:
        #Send failed
        print message + ' : Send failed'
        return -1

    # print 'Message send successfully'

    #Now receive data
    print message + " : waiting final K"
    reply = s.recv(4096)
    print message + " : final return--------------------------------------------"
    s.close()
    return reply

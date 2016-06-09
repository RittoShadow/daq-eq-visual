#Socket client example in python

import socket   #for sockets
import sys  #for exit
import time
import os

def command_server(message, params=None):
    #create an INET, STREAMing socket
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except socket.error:
        print 'Failed to create socket'
        return -1

    # print 'Socket Created'

    host = 'localhost';
    port = 5018;

    try:
        remote_ip = socket.gethostbyname( host )

    except socket.gaierror:
        #could not resolve
        print 'Hostname could not be resolved. Exiting'
        return -1

    #Connect to remote server
    route = os.path.dirname(os.path.abspath(__file__))
    os.chdir(route)
    result = os.popen("sudo python ask_daqeq_status.py").read().strip()

    if result == "0":
        while True:
            n = s.connect_ex((remote_ip , port))
            if n == 0:
                break
    else:
        return -1



    # print 'Socket Connected to ' + host + ' on ip ' + remote_ip

    #Send some data to remote server
    # message = sys.argv[1]

    try :
        #Set the whole string
        s.sendall(message)
    except socket.error:
        #Send failed
        print 'Send failed'
        return -1

    # print 'Message send successfully'

    #Now receive data
    reply = s.recv(4096)

    return reply

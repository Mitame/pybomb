import socket
import pickle

import data.settings as settings


playerdataID = 0
worlddataID = 1
entdataID = 2


sock = socket.socket()
try:
    sock.connect((settings.networking.ip,settings.networking.port))
except:
    print("Connection failed")
    settings.close()

def sendData(ID,data):
    if ID == playerdataID:
        senddata = bytes(pickle.dumps(data),"utf8")
    sock.sendall(senddata)
import json

__author__ = 'sertug'

import socket
import threading
import time
import server

class Client:
    __serverAddress = ""
    __serverPort = 0
    __bufferSize = 0
    __clientsocket = None
    __username = ""
    __canheartbeat = False

    def __init__(self):
        self.__serverPort = server.SERVER_PORT
        self.__bufferSize = server.BUFFER_SIZE

    def connect(self):
        self.__clientsocket = socket.socket()
        self.__serverAddress = "localhost"
        self.__clientsocket.connect((self.__serverAddress, self.__serverPort))
        print("Connected....")

    def heartbeat(self):
        while self.__canheartbeat:
            print "heartbeat sending"
            data = {'code': 'CHBEAT', 'username': self.__username}
            self.__clientsocket.send(json.dumps(data))
            time.sleep(5)

    def disconnect(self):
        self.__clientsocket.close()

    def sendrequest(self, request):
        self.__clientsocket.send(request)
        response = self.__clientsocket.recv(self.__bufferSize)
        print(response)
        response = json.loads(response)
        return response

class HeartBeatThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.__clientsocket = socket.socket()
        self.__serverAddress = socket.gethostname()
        self.__serverPort = server.SERVER_PORT

    def __del__(self):
        self.__clientsocket.close()

    def connect(self):
        self.__clientsocket.connect((self.__serverAddress, self.__serverPort))
        print("internal client connected....")

    def send(self, data):
        print "internal sending"
        self.__clientsocket.send(data)

    def run(self):
        self.connect()
        while True:
            print "heartbeat sending"
            data = {'code': 'CHBEAT', 'username': self.__username}
            self.__clientsocket.send(json.dumps(data))
            time.sleep(5)


if __name__ == "__main__":
    clientObj = Client()
    clientObj.connect()
    #threading.Timer(2.0, clientObj.heartbeat()).start()

    request = ""
    while request != "QUI":
        request = raw_input('>')
        userCode = request[0:6]
        userData = request[7:]
        userDataList = userData.split()
        print "userDataList ", userDataList
        if userCode == "CCNREQ" or userCode == "CPLREQ" or userCode == "CGUREQ" or userCode == "CWRREQ" or userCode == "CLGREQ":
            data = {'code': userCode, 'username': userDataList[0]}
        elif userCode == "CMVREQ":
            data = {'code': userCode, 'username': userDataList[0], 'move': userDataList[1]}
        print "client sending: ", json.dumps(data)
        response = clientObj.sendrequest(json.dumps(data))

    clientObj.disconnect()
    print "Client closed!"


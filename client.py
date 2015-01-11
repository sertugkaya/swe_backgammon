import json

__author__ = 'sertug'

import socket


class Client:
    __serverAddress = ""
    __serverPort = 0
    __bufferSize = 0
    __clientsocket = None

    def __init__(self):
        self.__serverPort = 12345
        self.__bufferSize = 1024

    def connect(self):
        self.__clientsocket = socket.socket()
        #self.__serverAddress = socket.gethostname()
        self.__serverAddress = "localhost"
        self.__clientsocket.connect((self.__serverAddress, self.__serverPort))
        print("Connected....")

    def disconnect(self):
        self.__clientsocket.close()

    def sendrequest(self, request):
        self.__clientsocket.send(request)
        response = self.__clientsocket.recv(self.__bufferSize)
        print(response)
        response = json.loads(response)
        print "unjson", (response)
        print "header", response.get('header')
        return response


if __name__ == "__main__":
    clientObj = Client()
    clientObj.connect()

    request = ""
    while request != "QUI":
        request = raw_input('>')
        userCode = request[0:6]
        userData = request[7:]
        data = {'code': userCode, 'username': userData}
        print json.dumps(data)
        response = clientObj.sendrequest(json.dumps(data))

    clientObj.disconnect()
    print "Client closed!"


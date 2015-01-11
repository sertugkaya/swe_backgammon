__author__ = 'sertug'

import socket
import datetime
import json
import threading


class ClientThread(threading.Thread):
    """Client handling unit for server class"""
    def __init__(self, clientsocket, clientaddress):
        threading.Thread.__init__(self)
        assert isinstance(clientsocket, socket.socket)
        self.clientSocket = clientsocket
        self.clientAddress = clientaddress

    def __del__(self):
        self.clientSocket.close()

    def run(self):
        while True:
            request = self.clientSocket.recv(1024)
            print "request arrived:" + request
            response = self.parser(request)
            self.clientSocket.send(json.dumps(response))

    def parser(self, request):
        request = json.loads(request)
        if request is None:
            data = {'header': 'SRVERR', 'message': 'error'}
            response = json.dumps(data)
        elif request.get('code') == "CCNREQ":
            username = request.get('username')
            response = {'header': 'SRVROK', 'username': username, 'message': 'Welcome to TavlaHero, please choose to be a player to play backgammon or choose to be a guest to watch a game live.'}
        elif request.get('code') == "CHBEAT":
            username = request.get('username')
            response = {'header': 'SRVROK', 'username': username}
        elif request.get('code') == "CPLREQ":
            username = request.get('username')
            response = {'header': 'SRVROK', 'username': username}
        elif request.get('code') == "CGUREQ":
            username = request.get('username')
            response = {'header': 'SRVROK', 'username': username}
        else:
            data = {'header': 'SRVERR', 'message': 'error'}
            response = json.dumps(data)
        return response

class Server(threading.Thread):
    __serverAddress = ""
    __serverPort = 0
    __serverSocket = None
    __definitions = {}
    __exitFlag = 0

    def __init__(self):
        threading.Thread.__init__(self)
        self.__serverPort = 12345
        self.__bufferSize = 1024

    def start(self):
        self.__serverSocket = socket.socket()
        # self.__serverAddress = socket.gethostname()
        self.__serverAddress = "localhost"
        self.__serverSocket.bind((self.__serverAddress, self.__serverPort))
        self.__serverSocket.listen(5)
        print("Server is listening on ip: " + self.__serverAddress)
        print("Server is listening on port: " + str(self.__serverPort))
        while not Server.__exitFlag:
            clientsocket, clientaddress = self.__serverSocket.accept()
            if not Server.__exitFlag:
                client_thread = ClientThread(clientsocket, clientaddress)
                client_thread.start()

        clientsocket.close()
        self.__serverSocket.close()


if __name__ == "__main__":
    serverObj = Server()
    serverObj.start()



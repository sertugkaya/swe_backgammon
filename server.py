__author__ = 'sertug'

import socket
import json
import threading

SERVER_PORT = 12345
BUFFER_SIZE = 1024


class ClientResponseThread(threading.Thread):
    def __init__(self, clientSocket, clientAddress):
        self.clientSocket = clientSocket
        self.clientAddress = clientAddress
        self.serverAddress = "localhost"
        self.serverPort = SERVER_PORT

    def send(self, data):
        print "response sending"
        self.clientSocket.send(json.dumps(data))

class ClientThread(threading.Thread):
    """Client handling unit for server class"""
    def __init__(self, clientsocket, clientaddress, nameLock, nameList):
        threading.Thread.__init__(self)
        assert isinstance(clientsocket, socket.socket)
        self.clientSocket = clientsocket
        self.clientAddress = clientaddress
        self.nameLock = nameLock
        self.nameList = nameList
        self.responseThread = ClientResponseThread(self.clientSocket, self.clientAddress)

    def __del__(self):
        self.clientSocket.close()

    def run(self):
        while True:
            request = self.clientSocket.recv(BUFFER_SIZE)
            print "request arrived:" + request
            response = self.parser(request)
            #self.clientSocket.send(json.dumps(response))
            self.responseThread.send(response)

    def parser(self, request):
        request = json.loads(request)
        if request is None:
            data = {'header': 'SRVERR', 'message': 'error'}
            response = json.dumps(data)
        elif request.get('code') == "CCNREQ":
            username = request.get('username')
            if self.nameList.count(username) != 0:
                response = {'header': 'SRVERR', 'username': username, 'message': 'Please pick a different username.'}
            else:
                self.nameList.append(username)
                print "nameList",nameList
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
    __serverSocket = None
    __definitions = {}
    __exitFlag = 0

    def __init__(self, nameLock, nameList):
        threading.Thread.__init__(self)
        self.__serverAddress = "localhost"
        # self.__serverAddress = socket.gethostname()
        self.__serverPort = SERVER_PORT
        self.__bufferSize = BUFFER_SIZE
        self.__serverSocket = socket.socket()
        self.__nameLock = nameLock
        self.__nameList = nameList

    def run(self):
        self.__serverSocket.bind((self.__serverAddress, self.__serverPort))
        self.__serverSocket.listen(5)
        print("Server is listening on ip: " + self.__serverAddress + " and port: " + self.__serverPort.__str__())
        while not Server.__exitFlag:
            clientsocket, clientaddress = self.__serverSocket.accept()
            if not Server.__exitFlag:
                client_thread = ClientThread(clientsocket, clientaddress, self.__nameLock, self.__nameList)
                client_thread.start()

        print"Server is closing!"
        clientsocket.close()
        self.__serverSocket.close()


if __name__ == "__main__":

    nameLock = threading.Lock()
    nameLock.acquire()
    nameLock.release()

    nameList = []
    serverObj = Server(nameLock, nameList)
    serverObj.start()

    serverObj.join()
    print"Server STOPPED!"



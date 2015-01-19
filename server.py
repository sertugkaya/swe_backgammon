__author__ = 'sertug'

import socket
import json
import threading

#SERVER_ADDRESS = "localhost"
SERVER_PORT = 12345
BUFFER_SIZE = 1024

"""
class ClientResponseThread(threading.Thread):
    def __init__(self, clientSocket, clientAddress):
        self.clientSocket = clientSocket
        self.clientAddress = clientAddress
        self.serverAddress = socket.gethostname()
        self.serverPort = SERVER_PORT

    def send(self, data):
        print "response sending"
        self.clientSocket.send(json.dumps(data))
"""
class ClientThread(threading.Thread):
    """Client handling unit for server class"""
    def __init__(self, clientsocket, clientaddress, nameLock, nameList, playerList, gameList):
        threading.Thread.__init__(self)
        assert isinstance(clientsocket, socket.socket)
        self.clientSocket = clientsocket
        self.clientAddress = clientaddress
        self.nameLock = nameLock
        self.nameList = nameList
        self.playerList = playerList
        self.gameList = gameList

    def __del__(self):
        self.clientSocket.close()

    def run(self):
        while True:
            response = {'': ''}
            request = self.clientSocket.recv(BUFFER_SIZE)
            print "request arrived:" + request
            response = self.parser(request)
            self.clientSocket.send(json.dumps(response))
            #self.responseThread.send(response)

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
                self.nameLock.acquire()
                self.nameList.append(username)
                self.nameLock.release()
                print "nameList", nameList
                response = {'header': 'SRVROK',
                            'username': username,
                            'message': 'Welcome to TavlaHero, please choose to be a player to play backgammon or choose to be a guest to watch a game live.'}
        elif request.get('code') == "CHBEAT":
            username = request.get('username')
            response = {'header': 'SRVROK', 'username': username}
        elif request.get('code') == "CPLREQ":
            username = request.get('username')
            if self.nameList.count(username) == 1:
                clientData = (username, self.clientSocket, self.clientAddress)
                self.playerList.append(clientData)
                if self.playerList.__len__() == 1:
                    response = {'header': 'SRWAIT',
                                'message': 'There are no active users, please request to play again shortly.'}
                elif self.playerList.__len__() % 2 == 0 and self.playerList.__len__() != 0:
                    self.gameList.append(playerList[0])
                    self.gameList.append(playerList[1])
                    self.playerList = [] #empty the waitlist
                    response = {'header': 'SRVROK',
                                'message': 'Game starts'}
            else:
                response = {'header': 'SRVERR', 'message': 'Please register first.'}
        elif request.get('code') == "CGUREQ":
            username = request.get('username')
            response = {'header': 'SRVROK', 'username': username}
        else:
            response = {'header': 'SRVERR', 'message': 'error'}
        return response

class Server(threading.Thread):
    __exitFlag = 0

    def __init__(self, nameLock, nameList, playerList, gameList):
        threading.Thread.__init__(self)
        self.__serverPort = SERVER_PORT
        self.__bufferSize = BUFFER_SIZE
        self.__serverSocket = socket.socket()
        self.__serverAddress = socket.gethostname()
        self.__nameLock = nameLock
        self.__nameList = nameList
        self.__playerList = playerList
        self.__gameList = gameList

    def run(self):
        self.__serverSocket.bind(('', self.__serverPort))
        self.__serverSocket.listen(5)
        print("Server is listening on ip: " + self.__serverAddress + " and port: " + self.__serverPort.__str__())
        while not Server.__exitFlag:
            clientsocket, clientaddress = self.__serverSocket.accept()
            if not Server.__exitFlag:
                client_thread = ClientThread(clientsocket, clientaddress, self.__nameLock, self.__nameList, self.__playerList, self.__gameList)
                client_thread.start()

        print"Server is closing!"
        clientsocket.close()
        self.__serverSocket.close()


if __name__ == "__main__":

    nameLock = threading.Lock()
    nameList = []
    playerList = []
    gameList = []
    serverObj = Server(nameLock, nameList, playerList, gameList)
    serverObj.start()

    serverObj.join()
    print"Server STOPPED!"



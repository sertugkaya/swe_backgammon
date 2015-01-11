__author__ = 'sertug'

import socket
import datetime
import json

class Server:
    __serverAddress = ""
    __serverPort = 0
    __serverSocket = None
    __definitions = {}

    def __init__(self):
        self.__serverPort = 12345
        self.__bufferSize = 1024

    def __loaddefinitions(self):
        f = file("codes.txt", "r")
        for line in f:
            line = line.strip()
            splitresult = line.split(' ', 1)
            if splitresult.__len__() == 2:
                self.__definitions[splitresult[1]] = splitresult[0]
            else:
                raise Exception("Error in codes file!")
        f.close()

    def start(self):
        self.__loaddefinitions()

        self.__serverSocket = socket.socket()
        # self.__serverAddress = socket.gethostname()
        self.__serverAddress = "localhost"
        self.__serverSocket.bind((self.__serverAddress, self.__serverPort))
        self.__serverSocket.listen(5)
        print("Server is listening on ip: " + self.__serverAddress)
        print("Server is listening on port: " + str(self.__serverPort))

        clientsocket, clientaddress = self.__serverSocket.accept()
        print "Client connected from: ", clientaddress
        while True:
            request = clientsocket.recv(self.__bufferSize)
            print "request arrived:" + request
            response = self.parser(request)
            clientsocket.send(json.dumps(response))
            print "Data sent:" + response
            if response == "BYE":
                break

        clientsocket.close()
        self.__serverSocket.close()

    def parser(self, request):
        request = json.loads(request)

        if request is None:
            data = {'header': 'SRVERR', 'message': 'error'}
            response = json.dumps(data)
        elif request.get('code') == "CCNREQ":
            username = request.get('username')
            print "got username", username
            response = {'header': 'SRVROK', 'message': 'welcome'}
        elif strippedrequest[0:6] == "CHBEAT":
            username = strippedrequest[7:]
            response = username
        elif strippedrequest[0:3] == "CPLREQ":
            username = strippedrequest[7:]
            response = "TOC " + datetime.datetime.now().strftime("%d/%m/%Y, %H:%M")
        elif strippedrequest[0:6] == "CGUREQ":
            username = strippedrequest[7:]
            response = username
        elif strippedrequest[0:3] == "GET":
            key = strippedrequest[4:]
            if key in self.__definitions:
                response = "CDE " + self.__definitions[key]
            else:
                response = "NTF " + key
        elif strippedrequest[0:3] == "QUI":
            response = "BYE"
        else:
            data = {'header': 'SRVERR', 'message': 'error'}
            response = json.dumps(data)

        return response


if __name__ == "__main__":
    serverObj = Server()
    serverObj.start()



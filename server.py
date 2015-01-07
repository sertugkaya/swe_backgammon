__author__ = 'sertug'

import socket
import datetime


class Server:
    __serverAddress = ""
    __serverPort = 0
    __serverSocket = None
    __definitions = {}

    def __init__(self):
        self.__serverPort = 12345
        self.__bufferSize = 16

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
        self.__serverAddress = socket.gethostname()
        self.__serverSocket.bind((self.__serverAddress, self.__serverPort))
        self.__serverSocket.listen(5)
        print("Server is listening on ip: " + self.__serverAddress)
        print("Server is listening on port: " + str(self.__serverPort))

        clientsocket, clientaddress = self.__serverSocket.accept()
        print "Client connected from: ", clientaddress
        while True:
            request = ""
            data = ""
            while data[-1:] != "\n":
                data = clientsocket.recv(self.__bufferSize)
                print "Data arrived:" + data
                request = request + data
            response = self.parser(request)
            clientsocket.send(response + "\n")
            print "Data sent:" + response
            if response == "BYE":
                break

        clientsocket.close()
        self.__serverSocket.close()

    def parser(self, request):
        strippedrequest = request.strip()

        if strippedrequest is None:
            response = "ERR"
        elif strippedrequest[0:3] == "HEL":
            response = "SLT"
        elif strippedrequest[0:3] == "TIC":
            response = "TOC " + datetime.datetime.now().strftime("%d/%m/%Y, %H:%M")
        elif strippedrequest[0:3] == "GET":
            key = strippedrequest[4:]
            if key in self.__definitions:
                response = "CDE " + self.__definitions[key]
            else:
                response = "NTF " + key
        elif strippedrequest[0:3] == "QUI":
            response = "BYE"
        else:
            response = "ERR"

        return response


if __name__ == "__main__":
    serverObj = Server()
    serverObj.start()



__author__ = 'sertug'
import json
import socket
import threading
import time
import server


class HeartBeatThread(threading.Thread):
    def __init__(self, username):
        threading.Thread.__init__(self)
        self.__clientsocket = socket.socket()
        self.__serverAddress = socket.gethostname()
        self.__serverPort = server.SERVER_PORT
        self.__username = username

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

class Client(threading.Thread):
    __exitFlag = 0

    def __init__(self):
        threading.Thread.__init__(self)
        self.__serverPort = server.SERVER_PORT
        self.__bufferSize = server.BUFFER_SIZE
        self.__clientsocket = socket.socket()
        self.__serverAddress = socket.gethostname()
        #self.__beatThread = HeartBeatThread(username)

    def __del__(self):
        self.__clientsocket.close()

    def run(self):
        self.__clientsocket.connect(('', self.__serverPort))
        print("Connected....")
        while not Client.__exitFlag:
            #self.__beatThread.run()
            userinput = self.getInput()
            request = self.parseinput(userinput)
            response = self.sendrequest(request)
            print response

    def getInput(self):
        return raw_input(">")

    def disconnect(self):
        self.__clientsocket.close()

    def sendrequest(self, request):
        self.__clientsocket.send(request)
        response = self.__clientsocket.recv(1024)
        response = json.loads(response)
        return response

    def parseinput(self, userinput):
        userCode = userinput[0:6]
        userData = userinput[7:]
        userDataList = userData.split()
        data = ""
        if userCode == "CCNREQ" or userCode == "CPLREQ" or userCode == "CGUREQ" or userCode == "CWRREQ" or userCode == "CLGREQ":
            data = {'code': userCode, 'username': userDataList[0]}
        elif userCode == "CMVREQ":
            data = {'code': userCode, 'username': userDataList[0], 'move': userDataList[1]}
        return json.dumps(data)

if __name__ == "__main__":
    clientObj = Client()
    clientObj.start()
    clientObj.join()
    print "Client closed!"
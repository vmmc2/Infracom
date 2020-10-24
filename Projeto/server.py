from socket import *
from threading import Thread
from collections import defaultdict



userNameSocket = defaultdict()

def connection(con, cli):
    isUserName = True
    userName = ""
    while True:
        msgReceived = con.recv(1024).decode("utf-8")
        if isUserName == True: # Primeira mensagem recebida -> Eh o userName
            isUserName = False
            userName = msgReceived
            userNameSocket[userName] = con
        if msgReceived != "" and msgReceived != "bye" and isUserName == False: # Outras mensagens enviadas pelo userName
            print(msgReceived)
        if msgReceived[0:9] == "send -all":
            for element in userNameSocket.values():
                messageSent = msgReceived[9:]
                element.send(bytes(messageSent, "utf-8"))
        if msgReceived[0:10] == "send -user":
            pass
        if msgReceived == "bye":
            con.send(bytes(msgReceived, "utf-8"))
            del userNameSocket[userName]
            #print("")
            #print("Messages received by", userName)
            #for message in privateSendBoxes[userName]:
            #    print(message)
            #print("\n")
            #break
    con.close()
    return

def main():
    serverPort = 12000
    serverName = "localhost"

    serverSocket = socket(AF_INET, SOCK_STREAM)
    serverSocket.bind((serverName, serverPort))
    serverSocket.listen(10)

    print("Server ta pronto!")


    while True:
        connectionSocket, addr = serverSocket.accept()
        t = Thread(target=connection, args=(connectionSocket, addr,))
        t.start()
        

    return

if __name__ == "__main__":
    main()

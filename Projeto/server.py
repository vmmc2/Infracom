import datetime
from socket import *
from threading import Thread
from collections import defaultdict


userNameSocket = defaultdict()
userNameIP = defaultdict()
userNamePort = defaultdict()

# 192.168.0.123:67890/~ana: Alguma novidade do projeto de infracom? 14h31 30/09/2020


def connection(con, cli):
    isUserName = True
    userName = ""
    while True:
        msgReceived = con.recv(1024).decode("utf-8")
        if isUserName == True: # Primeira mensagem recebida -> Eh o userName
            l = msgReceived.split()
            userName = l[0]
            print("Username:", userName)
            if userName in userNameSocket:
                con.send(bytes("NOT OK", "utf-8"))
            else:
                con.send(bytes("OK", "utf-8"))
                ip = l[1]
                port = l[2]
                userNameSocket[userName] = con
                userNameIP[userName] = ip
                userNamePort[userName] = port
                isUserName = False
        if msgReceived != "" and msgReceived != "bye" and isUserName == False: # Outras mensagens enviadas pelo userName
            print(msgReceived)
        if msgReceived[0:9] == "send -all":
            for element in userNameSocket.values():
                messageSent = msgReceived[9:]
                dt = datetime.datetime.now()
                hours = str(dt.strftime("%H"))
                minutes = str(dt.strftime("%M"))
                day = str(dt.strftime("%d"))
                month = str(dt.strftime("%m"))
                year = str(dt.strftime("%Y"))
                finalMessage = userNameIP[userName] + ":" + userNamePort[userName] + "/~" + userName + ": " + messageSent + " " + hours + "h" + minutes + " " + day + "/" + month + "/" + year
                element.send(bytes(finalMessage, "utf-8"))
        if msgReceived[0:10] == "send -user":
            #"send -user Kinhosz Iae kinho"
            l = msgReceived.split()
            destinationUser = l[2]
            if destinationUser not in userNameSocket:
                con.send(bytes("[System]: Usuario nao encontrado no chat!", "utf-8"))
            else:
                space = ' '
                dt = datetime.datetime.now()
                hours = str(dt.strftime("%H"))
                minutes = str(dt.strftime("%M"))
                day = str(dt.strftime("%d"))
                month = str(dt.strftime("%m"))
                year = str(dt.strftime("%Y"))
                finalMessage = userNameIP[userName] + ":" + userNamePort[userName] + "/~" + userName + ": " + space.join(l[3:]) + " " + hours + "h" + minutes + " " + day + "/" + month + "/" + year
                userNameSocket[destinationUser].send(bytes(finalMessage, "utf-8"))
        if msgReceived == "bye":
            con.send(bytes(msgReceived, "utf-8"))
            del userNameSocket[userName]
            del userNameIP[userName]
            del userNamePort[userName]
            #print("")
            #print("Messages received by", userName)
            #for message in privateSendBoxes[userName]:
            #    print(message)
            #print("\n")
            #break
        if msgReceived == "list":
            l = ["Usuarios Conectados:"]
            delimiter = '\n'
            for user in userNameSocket.keys():
                l.append(user)
            userNameSocket[userName].send(bytes(delimiter.join(l), "utf-8"))
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

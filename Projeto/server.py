import sys
import datetime
from socket import *
from threading import Thread
from collections import defaultdict


userNameSocket = defaultdict() # Dicionário que mapeai nomes de usuários conectados para seus respectivos Sockets.
userNameIP = defaultdict() # Dicionário que mapeia nomes de usuários conectados para seus respectivos endereços IP.
userNamePort = defaultdict() # Dicionário que mapeia nomes de usuários conectados para suas respectivas portas.

# Esses códigos indicarão as diferentes cores que devem ser usadas para mostrar as mensagens ao usuários.
publicMessage = "1" # Branco
privateMessage = "2" # Azul
listOfConnectedUsers = "3" # Verde
issue = "4" # Vermelho


############################ FORMATAÇÂO DAS MENSAGENS ################################
# 192.168.0.123:67890/~ana: Alguma novidade do projeto de infracom? 14h31 30/09/2020 #
######################################################################################

def connection(con, cli): # con -> conectionSocket ------ cli -> addr
    isUserName = True
    userName = ""
    while True:
        msgReceived = con.recv(1024).decode("utf-8")
        if isUserName == True: # Primeira mensagem recebida pelo canal -> Deve ser o userName acompanhado do IP e da porta (separados por espaço)
            l = msgReceived.split()
            userName = l[0]
            print("Username:", userName)
            if userName in userNameSocket: # Se o nome de usuário recebido já está sendo usado por outro usuário, é enviada uma mensagem de rejeição ("NOT OK"). No cliente, o usuário deverá fornecer um novo nome de usuário.
                con.send(bytes("NOT OK", "utf-8"))
            else: # Houve sucesso na verificação de nome de usuário.
                con.send(bytes("OK", "utf-8"))
                ip = l[1]
                port = l[2]
                userNameSocket[userName] = con
                userNameIP[userName] = ip
                userNamePort[userName] = port
                isUserName = False
        if msgReceived != "" and msgReceived != "bye" and isUserName == False: # Outras mensagens enviadas pelo userName
            print(msgReceived)
        if msgReceived[0:9] == "send -all": # Mensagem que deve ser enviada ao chat público (a todos os usuários conectados)
            messageSent = msgReceived[9:]
            dt = datetime.datetime.now()
            hours = str(dt.strftime("%H"))
            minutes = str(dt.strftime("%M"))
            day = str(dt.strftime("%d"))
            month = str(dt.strftime("%m"))
            year = str(dt.strftime("%Y"))
            for element in userNameSocket.values():
                finalMessage = userNameIP[userName] + ":" + userNamePort[userName] + "/~" + userName + ": " + messageSent + " " + hours + "h" + minutes + " " + day + "/" + month + "/" + year + " " + publicMessage
                element.send(bytes(finalMessage, "utf-8"))
        if msgReceived[0:10] == "send -user": # Mensagem que deve ser enviada ao chat privado (a um usuário em particular)
            l = msgReceived.split()
            destinationUser = l[2]
            if destinationUser not in userNameSocket: # Tentativa de envio de mensagem a um usuário que não está conectado
                con.send(bytes("[System]: Usuario nao encontrado no chat!" + " " + issue , "utf-8"))
            else: # O usuário está conectado
                space = ' '
                dt = datetime.datetime.now()
                hours = str(dt.strftime("%H"))
                minutes = str(dt.strftime("%M"))
                day = str(dt.strftime("%d"))
                month = str(dt.strftime("%m"))
                year = str(dt.strftime("%Y"))
                destinedUser = " to [" + destinationUser + "]: "
                finalMessage = userNameIP[userName] + ":" + userNamePort[userName] + "/~" + userName + destinedUser + space.join(l[3:]) + " " + hours + "h" + minutes + " " + day + "/" + month + "/" + year + " " + privateMessage
                finalMessage2 = userNameIP[userName] + ":" + userNamePort[userName] + "/~" + userName + ": " + space.join(l[3:]) + " " + hours + "h" + minutes + " " + day + "/" + month + "/" + year + " " + privateMessage
                userNameSocket[userName].send(bytes(finalMessage, "utf-8"))
                userNameSocket[destinationUser].send(bytes(finalMessage2, "utf-8"))
        if msgReceived == "bye": # Mensagem enviada pelo usuário quando este deseja se desconectar
            con.send(bytes(msgReceived, "utf-8")) # É enviada uma mensagem de confirmação de desconexão ao usuário
            # Deleta-se os registros desse usuário em todos os dicionários usados pelo servidor
            del userNameSocket[userName]
            del userNameIP[userName]
            del userNamePort[userName]
            break
        if msgReceived == "list": # Mensagem enviada pelo usuário quando este deseja obter a lista de todos os usuários conectados ao servidor no momento
            l = ["Usuarios Conectados:"]
            delimiter = '\n'
            for user in userNameSocket.keys():
                l.append(user)
            l.append(listOfConnectedUsers)
            userNameSocket[userName].send(bytes(delimiter.join(l), "utf-8"))
    con.close() # O socket referente ao client em questão é fechado
    return


def main():
    # Informações do servidor.
    serverPort = 12000
    serverName = "localhost"
    capacityOfUsers = 100 # Quantidade de usuários que o servidor suporta simultaneamente

    serverSocket = socket(AF_INET, SOCK_STREAM) # Criação do Socket TCP de recepção.
    serverSocket.bind((serverName, serverPort))
    serverSocket.listen(capacityOfUsers)

    print("O servidor está ligado e operante!")

    while True:
        connectionSocket, addr = serverSocket.accept() # Servidor aguarda por novas solicitações. Um novo socket é criado. 
        t = Thread(target=connection, args=(connectionSocket, addr,)) # São criadas threads que tratarão individualmente de cada um desses sockets.
        t.start()
    sys.exit()

if __name__ == "__main__":
    main()

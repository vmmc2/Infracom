from socket import *
from threading import Thread

privatePostalBox = []
publicPostalBox = []

def readMessages(clientSocket):
    while True:
        message = clientSocket.recv(1024).decode('utf-8')
        if message == "bye":
            clientSocket.close()
            break
        print(message)
    return


def main():
    serverName = "localhost"
    serverPort = 12000

    clientSocket = socket(AF_INET, SOCK_STREAM)
    clientSocket.connect((serverName, serverPort))

    userName = ""
    while True:
        while True:
            userName = input("Digite o nome de usuario sem espacos:")
            if userName.find(' ') != -1 or len(userName) == 0:
                print("Nome de usuario invalido! Digite outro.")
            else:
                ip = clientSocket.getsockname()[0]
                port = str(clientSocket.getsockname()[1])
                break 

        clientSocket.send(bytes(userName + " " + ip + " " + port, "utf-8"))
        status = clientSocket.recv(1024).decode("utf-8")
        print(status)
        while len(status) == 0:
            status = clientSocket.recv(1024).decode("utf-8")
            print(status)
        if status == "OK":
            break
        print("[System]: Nome de usuario ja cadastrado por outra pessoa")

    t = Thread(target=readMessages, args=(clientSocket,))
    t.start()

    while True:
        comando = input()
        if comando[0:3] == "bye":
            msg = "bye"
            clientSocket.send(bytes(msg, "utf-8"))
            break
        elif comando[0:9] == "send -all" or comando[0:10] == "send -user" or comando[0:4] == "list":
            clientSocket.send(bytes(comando, "utf-8"))
        else:
            print("Comando Invalido!")
    return



if __name__ == "__main__":
    main()

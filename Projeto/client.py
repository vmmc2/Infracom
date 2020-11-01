from socket import *
from threading import Thread
from colors import red, green, blue

privatePostalBox = []
publicPostalBox = []

def readMessages(clientSocket): # Essa função funciona dentro de uma thread e permite que um usuário possa enviar mensagens ao servidor e receber as mensagens dele simultaneamente.
    while True:
        message = clientSocket.recv(1024).decode('utf-8')
        if message == "bye": # Essa mensagem "bye" é uma mensagem de resposta de confirmação enviada pelo servidor para indicar que o usuário foi desconectado.
            clientSocket.close() # O clientSocket do usuário é encerrado e a execução da função é finalizada. 
            break
        else:
            if message != "OK" and message != "NOT OK":
                if message[-1] == "1":  # Public Message 
                    print(message[:-1])
                    publicPostalBox.append(message[:-1])
                elif message[-1] == "2": # Private Message
                    print(blue(message[:-1]))
                    privatePostalBox.append(message[:-1])
                elif message[-1] == "3": # List of Connected Users
                    print("")
                    print(green(message[:-1]))
                    print("")
                elif message[-1] == "4": # Issue    
                    print(red(message[:-1]))
        #print(message) ##################### TEM QUE PRINTAR A FUNÇÂO DE CORES DIFERENTES #########################
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
            if userName.find(' ') != -1 or len(userName) == 0: # Verificação para nome de usuário com espaços ou nome de usuário como string vazia ("")
                print(red("Nome de usuario invalido! Digite outro."))
            else: # Nome de usuário validado. Obtemos o IP e a porta que estão sendo usados por esse usuário na conexão.
                ip = clientSocket.getsockname()[0]
                port = str(clientSocket.getsockname()[1])
                break 

        clientSocket.send(bytes(userName + " " + ip + " " + port, "utf-8")) # A primeira mensagem enviada ao servidor contém: O nome do usuário, o seu IP e a sua porta.
        status = clientSocket.recv(1024).decode("utf-8") # Aguardamos a mensagem de confirmação de login do servidor.
        while len(status) == 0:
            status = clientSocket.recv(1024).decode("utf-8")
        if status == "OK": # Mensagem de confirmação positiva do servidor. O usuário conseguiu se cadastrar.
            print(green("Você agora está conectado ao chat."))
            break
        print(red("[System]: Nome de usuario ja cadastrado por outra pessoa")) # Mensagem de rejeição do servidor. O nome de usuário fornecido já está sendo utilizado por outro usuário. Outro nome de usuário deve ser fornecido.

    t = Thread(target=readMessages, args=(clientSocket,)) # É iniciada uma thread para que um usuário possa, simultaneamente, enviar e receber mensagens.
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
            print(red("[System]: Comando Invalido!"))
    return



if __name__ == "__main__":
    main()

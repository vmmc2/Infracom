import matplotlib.pyplot as plt 
import math

def fatorial(n):
    if n == 0 or n == 1:
        return 1
    else:
        return n * fatorial(n - 1)

def combination(n, k): 
    # Funcao responsavel por calcular o valor da combinacao "n" escolhe "k" = n!/((n - k)! * k!) onde n >= k
    fatN = fatorial(n)
    fatNMinusK = fatorial(n - k)
    fatK = fatorial(k)
    return (fatN)//(fatNMinusK * fatK)


def main():
    # Entrada
    print("******************************************** CENARIO ********************************************")
    usuariosConectados = int(input("Digite a quantidade de usuarios conectados: "))
    probabilidadeUsuarioConectado = float(input("Digite a probabilidade de 1 usuario estar conectado: "))
    probabilidadeComplementar = float(input("Digite a probabilidade de 1 usuario nao estar conectado: "))
    taxaDeDadosUsuario = float(input("Digite a taxa de dados requisitada por 1 usuario (em kbps): "))
    taxaDeDadosEnlace = float(input("Digite a capacidade total do enlace (em kbps): "))
    print(" ")


    print("**************************************** Considerando a comutação de circuitos *****************************************")
    # Calculos para o cenario de uma comutacao de circuitos: Calculando o numero maximo de usuarios que podem ser atendidos simultaneamente pelo enlace.
    numeroMaxUsuarios = math.floor(taxaDeDadosEnlace/taxaDeDadosUsuario)
    print("Número máximo de usuários que a comutação de circuitos pode suportar simultaneamente:", numeroMaxUsuarios)
    
    print(" ")
    print("***************************************** Considerando a comutação de pacotes *****************************************")
    print(" ")
    # Calculos para o cenario de uma comutacao de pacotes: Calculando a probabilidade da demanda da rede ser maior do que a capacidade do enlace.
    numeroMaxUsuarios = math.floor(taxaDeDadosEnlace/taxaDeDadosUsuario)
    probabilidadeDemanda = 0
    for i in range(numeroMaxUsuarios + 1, usuariosConectados + 1):
        probabilidadeDemanda += combination(usuariosConectados, i) * math.pow(probabilidadeUsuarioConectado, i) * math.pow(probabilidadeComplementar, usuariosConectados - i) 
    print("Probabilidade da demanda da rede ser maior do que a capacidade do enlace:", format(probabilidadeDemanda, '.7f'))
    # Plotando o grafico solicitado
    qtdUsuarios = [i for i in range(1, usuariosConectados + 1)]
    probabilidades = [(combination(usuariosConectados, i) * math.pow(probabilidadeUsuarioConectado, i) * math.pow(probabilidadeComplementar, usuariosConectados - i)) for i in range(1, usuariosConectados + 1)]
    plt.plot(qtdUsuarios, probabilidades)
    plt.suptitle("Número de Usuários Ativos x Probabilidade")
    plt.xlabel("Número de Usuários Ativos")
    plt.ylabel("Probabilidade")
    plt.show()
    
    return


main()

import socket
import time

class carta:
    def __init__(self, id, num, naipe, forca):
        self.id = id
        self.num = num
        self.naipe =  naipe
        self.forca = forca
        self.inGame = False

def mostraCartas (cartas):
    print("\nA carta virado foi:")
    print(str(cartas[0]) + " " + dicio(cartas[1]))
    print("\nAs suas cartas são:" )
    
    for i in range (2,8):
        if(i%2 == 0):
            print(str(cartas[i]) + " " + dicio(cartas[i+1]))

def mostrarCartaJogada(carta):
        print ("\nvocê jogou:  ")
        print(str(carta[0]) + " " + dicio(carta[1]))

def mostrarCartaRecebida(carta):
        print ("\nO adversário jogou:  ")
        print(str(carta[0]) + " " + dicio(carta[1]) + "\n")


def dicio(carta):
    if (carta == 0 ): return "de Ouros"
    if (carta == 1 ): return "de Espadas"
    if (carta == 2 ): return "de Copas"
    if (carta == 3 ): return "de Paus"


def strintToList(cartas):
    b ="[]',"
    for i in range(0,len(b)):
        cartas = cartas.replace(b[i],"")
    lista = [int(ele) for ele in cartas.split()]
    return lista

def recebeInfo():
    print("\nAguarde o outro jogador")
    tamanho_bytes = sock_dados.recv(4)
    tamanho = int.from_bytes(tamanho_bytes, byteorder='big', signed=False)
    cartasRecebidas_bytes = sock_dados.recv(tamanho)
    cartasRecebidas = cartasRecebidas_bytes.decode(encoding='UTF-8')
    cartasRecebidas = strintToList(cartasRecebidas)

    return cartasRecebidas

def verificaCarta(indice, cartas):
    if (indice == '1' and cartas[2]!=0):
        return True
    if (indice == '2' and cartas[4]!=0):
        return True
    if (indice == '3' and cartas[6]!=0):
        return True
    else:
        print ("Essa carta já foi jogada ou comando inválido")
        return False
    
def separaCarta(indice,cartas):
    if (indice == '1'):
        cartas = cartas[2:4]
    if (indice == '2'):
        cartas = cartas[4:6]
    if (indice == '3'):
        cartas = cartas[6:8]
    return cartas

def removeCartaJogada(indice,cartas):
    if (indice == '1'):
        cartas[2] = 0
    if (indice == '2'):
        cartas[4] = 0
    if (indice == '3'):
        cartas[6] = 0
    return cartas

def mandaInfo(carta):
    texto_bytes = carta.encode(encoding='UTF-8')

    tamanho = len(texto_bytes)
    tamanho_bytes = tamanho.to_bytes(4, byteorder= 'big', signed=False)
    mensagem  = tamanho_bytes + texto_bytes
    sock_dados.send(mensagem)

def joga(cartasP1):
    selecionouCarta = False
    while (selecionouCarta == False):
        comando = input('\nEscolha a carta que deseja jogar. Escreva 1 para primeira, 2 para segunda e 3 para terceira. ')
        selecionouCarta = verificaCarta(comando,cartasP1)
        cartaJogada = separaCarta(comando,cartasP1)

    selecionouCarta = False    

    mostrarCartaJogada(cartaJogada)
    mandaInfo(str(cartaJogada)) 
    cartasP1 = removeCartaJogada(comando,cartasP1)
    return cartasP1,cartaJogada

def verificaForca(forcaP1,forcaP2):
    if forcaP1 > forcaP2:
        return 1
    if forcaP1 < forcaP2:
        return 2
    if forcaP1 == forcaP2:
        return 0
    
def retornaForca(carta, baralho):

    for i in range(len(baralho)):
        if (baralho[i].num == carta[0] and baralho[i].naipe == carta[1]): 
            return  baralho[i].forca
        
def criaBaralho():
    baralho = []
    num = 1
    naipe = 0
    forca = 0
    for i in range (40):
        if (num == 8): num = 10             # baralho não possui 8 e 9
        if (num <= 3):                      # a força das cartas 3,2,1 não segue o padrão de numero
            forca = num + 12
        else:
            forca = num
        baralho.append(carta(i,num,naipe,forca))
        if (num == 12) : naipe += 1           # quando foram todas a cartas de uma naipe passa para a próxima 
        num = (num % 12 ) + 1
        
    return baralho

def atualizaForca(baralho, cartaVirada):      # atualiza a força das manilhas
    lista = [i for i,x in enumerate(baralho) if x.num == (cartaVirada % 12) +1]   # lista as manilhas
    x = 0
    for i in lista:
        baralho[i].forca = 16 + x    # atualiza a força das manilhas
        x += 1
    return baralho

def P1VenceuRodada():
    global pontosP1 
    pontosP1 += 1
    print("\nPlayer 1 venceu a rodada")
    time.sleep(3)
    print("\n\n\n\n\n\n")

def P2VenceuRodada():
    global pontosP2 
    pontosP2 += 1
    print("\nPlayer 2 venceu a rodada")
    time.sleep(3)
    print("\n\n\n\n\n\n")

def mostraPlacar():
    global pontosP1
    global pontosP2
    print ("\nPlayer 1 possui " + str(pontosP1) + " pontos e Player 2 possui " + str(pontosP2) + " pontos" )
    
def empate():
    print("\nRodada empatada, nenhum player recebeu pontos")

sock_dados = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

ip_destino = '127.0.0.1'
porta_destino = 50000
destino = (ip_destino, porta_destino)

sock_dados.connect(destino)

print('Aguardando as Cartas')

tipo_bytes = sock_dados.recv(1)
tipo = int.from_bytes(tipo_bytes, byteorder='big', signed=False)

print('iniciando o jogo...')

finalizado = False

pontosP1 = 0
pontosP2 = 0

while not finalizado:
    mostraPlacar()
    cartasP2 = recebeInfo()
    mostraCartas(cartasP2)

    baralho = criaBaralho()
    cartaVirada = cartasP2[0]
    baralho = atualizaForca(baralho,cartaVirada)

    cartaAdv = recebeInfo()
    mostrarCartaRecebida(cartaAdv)

    cartasP2, cartaJogada = joga(cartasP2)

    primeira = verificaForca(retornaForca(cartaAdv, baralho),retornaForca(cartaJogada, baralho))

    #print (primeira) 
    
    if primeira == 2:
        cartasP2, cartaJogada = joga(cartasP2)
        cartaAdv = recebeInfo()
        mostrarCartaRecebida(cartaAdv)
    if primeira == 1  or primeira == 0:
        cartaAdv = recebeInfo()
        mostrarCartaRecebida(cartaAdv)
        cartasP2, cartaJogada = joga(cartasP2)

    segunda = verificaForca(retornaForca(cartaAdv, baralho),retornaForca(cartaJogada, baralho))


    if (primeira == 1 and segunda == 1 ): 
        P1VenceuRodada()
        continue

    elif (primeira == 2 and segunda == 2): 
        P2VenceuRodada()
        continue

    elif (primeira == 0 and segunda == 1): 
        P1VenceuRodada()
        continue

    elif (primeira == 0 and segunda == 2): 
        P2VenceuRodada()
        continue
    
    elif (primeira == 1 and segunda == 0 ): 
        P1VenceuRodada()
        continue

    elif (primeira == 2 and segunda == 0): 
        P2VenceuRodada()
        continue

    elif(primeira == 1 and segunda == 2):
        cartasP2, cartaJogada = joga(cartasP2)
        cartaAdv = recebeInfo()
        mostrarCartaRecebida(cartaAdv)

    elif (primeira == 0 and segunda == 0 or primeira == 2 and segunda == 1 ): 
        cartaAdv = recebeInfo()
        mostrarCartaRecebida(cartaAdv)
        cartasP2, cartaJogada = joga(cartasP2)
        
    terceira = verificaForca(retornaForca(cartaAdv, baralho),retornaForca(cartaJogada, baralho))

    if (terceira == 1): P1VenceuRodada()
    if (terceira == 2): P2VenceuRodada()
    if (terceira == 0 and primeira == 1):P1VenceuRodada()
    if (terceira == 0 and primeira == 2):P2VenceuRodada()
    if (terceira == 0 and primeira == 0):empate()


    if (pontosP1 == 3):
        print ("\nPlayer 1 venceu a partida")
        finalizado = True

    if (pontosP2 == 3):
        print ("\nPlayer 2 venceu a partida")
        finalizado = True
    
sock_dados.close()






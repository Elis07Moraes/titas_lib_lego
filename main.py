#!/usr/bin/env pybricks-micropython

# script.py
from titas_lib import HubType, RoboHub, SeguidorLinha, RoboBrick, RoboMotor, RoboCor, RoboUltrassonico, RoboBase, RoboImports, Color
from pybricks.tools import wait 

# DEFINIÇÕES

hub_type = HubType(RoboHub.EV3BRICK)

robo_brick = RoboBrick()

sensor_ultrassonico = RoboUltrassonico(Port="2")

cor_direita = RoboCor(Port="4")
cor_esquerda = RoboCor(Port="3")

motor_d = RoboMotor(Port="d")
motor_e = RoboMotor(Port="a", reverse = True)
# motor_garra = RoboMotor(Port="b", reverse= True)

sensor_vendra = hub_type.getImports().getLUMPDevice(Port="1") 

codigoSeguidor = SeguidorLinha()

# print(sensor_vendra.read(0))

base = RoboBase(  # passando as informações do robo p uma variavel
    motorDireito= motor_d,
    motorEsquerdo= motor_e,
    diametroRoda= 44,
    distanciaEntreAsRodas= 320
    )

# VARIAVEIS

# para andar enquanto a distancia for maior que 100 
# quando for menor que 100, ira parar lentamente 
distancia = 1000

angulo_verificar = 10

viradaAngulo = 0

BRANCO = 65

PRETO = 30

pretoEsqCor = 1

brancoEsqCor = 2

pretoDirCor = 3

brancoDirCor = 4

BRANCODIR = 52

BRANCOESQ = 52

PRETODIR = 10 

PRETOESQ = 10


seguindoLinha = True


# FUNÇÕES

def VerificarCorVE():
    return sensor_vendra.read(0)[1] 

def VerificarCorVEEx():
    return sensor_vendra.read(0)[0] 

def VerificarCorVD():
    return sensor_vendra.read(0)[2]

def VerificarCorVDEx():
    return sensor_vendra.read(0)[3]



def alinharLinha():
        i=0
        while i < 100:
            sensor_esqEx_vedra = VerificarCorVEEx()
            sensor_esq_vedra = VerificarCorVE() 
            sensor_dirEx_vedra = VerificarCorVDEx()
            sensor_dir_vedra = VerificarCorVD()
            print(sensor_dir_vedra)

            print(sensor_esq_vedra)
            codigoSeguidor.seguirLinhaPreta(
            kd=0.5, # analisa de acordo com a poisçao do começo
            kp=1, # proporcional no momento instante que ocorre o erro
            cor_vermelha_direta=(sensor_esq_vedra + sensor_esqEx_vedra * 2) - 20,
            cor_vermelha_esquerda=sensor_dir_vedra + sensor_dirEx_vedra * 2,
            motor_direito=motor_d,
            motor_esquerdo=motor_e,
            potencia_motores=0
            )
            i=i+1
            wait(10)

def eVerdeD(): # funcao para pegar a cor verde do lado direito usando sistema rgb, usando verde e vermelho p comparacao
    cor = cor_direita.pegarRGB()
    # print(cor)
    if cor[1] > 10 and cor[1] < 57:
        if cor[1] >= (2 * cor[0]):
            return True
        
    return False

def eVerdeE(): # funcao para pegar a cor verde do lado esquerda usando sistema rgb, usando verde e vermelho p comparacao
    cor = cor_esquerda.pegarRGB()
    # print(cor) 
    if cor[1] > 12 and cor[1] < 65:
        if cor[1] >= (2.2 * cor[0]):
            return True
        
    return False


# funcao para mover para esquerda quando ver verde
def VerdeEsquerda():
    sensor_esq_vedra = VerificarCorVE() 
    sensor_dir_vedra = VerificarCorVD()
    print ("mover")
    base.moverDistancia(80)
    # base.virar90grausDireita()
    base.virarAngulo(-90)
    base.pararMotores()

    while sensor_esq_vedra >= BRANCO or sensor_dir_vedra >= BRANCO: 
        sensor_esq_vedra = VerificarCorVE() 
        sensor_dir_vedra = VerificarCorVD()
        base.virarAngulo(-10)
        print(" branco virar verde esq")


        if sensor_dir_vedra <= PRETO or sensor_esq_vedra <= PRETO:
            sensor_esq_vedra = VerificarCorVE() 
            sensor_dir_vedra = VerificarCorVD()
            print("achou preto esq") 
            break


# funcao para mover pra direita quando for verde
def VerdeDireita():
    sensor_esq_vedra = VerificarCorVE() 
    sensor_dir_vedra = VerificarCorVD()
    print ("mover")
    base.moverDistancia(80)
    # base.virar90grausEsquerda()
    base.virarAngulo(90)
    base.pararMotores()
    while sensor_esq_vedra >= BRANCO or sensor_dir_vedra >= BRANCO:
        sensor_esq_vedra = VerificarCorVE() 
        sensor_dir_vedra = VerificarCorVD()
        print(" branco virar verde") 
        base.virarAngulo(10)
        
        if sensor_dir_vedra <= PRETO or sensor_esq_vedra <= PRETO:
            sensor_esq_vedra = VerificarCorVE() 
            sensor_dir_vedra = VerificarCorVD() 
            print("achou preto")
            break

def VerificarCorVE():
    return sensor_vendra.read(0)[1] 

def VerificarCorVEEx():
    return sensor_vendra.read(0)[0] 

def VerificarCorVD():
    return sensor_vendra.read(0)[2]

def VerificarCorVDEx():
    return sensor_vendra.read(0)[3]

# realiza verificacao se é gap o nao, se nao achar nada no final, retorna True e começa a realizar o gap
def VerificarGap():
    viradaMaxima = 10
    base.moverDistancia(50)

    print("VerificarGap")  
    viradaAngulo = 0

    while viradaAngulo <= viradaMaxima:
        
        base.virarAngulo(angulo=angulo_verificar)
        viradaAngulo += 1
        print("virarAngulo")
    
        if VerificarCorVD() < PRETO or VerificarCorVE() < PRETO:
            print("deu false") 
            base.pararMotores()
            print("pararMotorInstantaneamente")      
            return False

    print("entrou aqui")

    while viradaAngulo >= -viradaMaxima:
        base.virarAngulo(angulo= -angulo_verificar)
        viradaAngulo -= 1
        print("virarAngulo")            

        if VerificarCorVD() < PRETO or VerificarCorVE() < PRETO:
            print("deu false") 
            base.pararMotores()
            return False
        print("entrou aqui")    


    base.virarAngulo(angulo=( viradaMaxima*angulo_verificar) + 5)
    # base.virar90grausDireita()
    return True   


# quando entra no gap
def taNoGap():
     print("taNoGap")
    #  if VerificarGap() == True: 
     base.pararMotores()
     base.moverDistancia(100)
     base.pararMotores()

    #  while sensor_esq_vedra >= 70 and sensor_dir_vedra >= 70:
    #     base.moverDistancia(100)
    #     base.pararMotores()

# funcao que pegab a distancia do sensor ultrasspnico, e quando a distancia (anteriprmente 1000) for menor que 50, ele printa a disytancia e para
def Distancia():
    distancia = sensor_ultrassonico.pegarDistancia()
    if distancia < 50:
        print (distancia)
        base.pararMotores()
        return True 

# fncao para desviar do obstaculo
def Obstaculo():
    sensor_esq_vedra = VerificarCorVE() 
    sensor_dir_vedra = VerificarCorVD()
    if Distancia() == True: 
        print ("obstaculo")
        alinharLinha()
        base.moverDistancia(-30)
        base.pararMotores()
        base.virarAngulo(-90)
        base.pararMotores()
        base.moverDistancia(310)
        base.pararMotores()
        base.virarAngulo(90)
        base.pararMotores()
        sensor_esq_vedra = VerificarCorVE() 
        sensor_dir_vedra = VerificarCorVD()
        base.moverDistancia(670)
        base.pararMotores()
        base.virarAngulo(90)
        sensor_esq_vedra = VerificarCorVE() 
        sensor_dir_vedra = VerificarCorVD()
        while sensor_dir_vedra > PRETO and sensor_esq_vedra > PRETO:
            print(sensor_dir_vedra, sensor_esq_vedra)
            base.moverSemParar(100, 0)
            sensor_esq_vedra = VerificarCorVE() 
            sensor_dir_vedra = VerificarCorVD()
            cor_esquerda.pegarRGB()
            cor_direita.pegarRGB()
            sensor_esq_vedra = VerificarCorVE() 
            sensor_dir_vedra = VerificarCorVD()
            if sensor_esq_vedra <= PRETO or sensor_dir_vedra <= PRETO:
                print("preto obstaculo")
                cor_esquerda.pegarRGB()
                cor_direita.pegarRGB()
                sensor_esq_vedra = VerificarCorVE() 
                sensor_dir_vedra = VerificarCorVD()  
                base.moverDistancia(100)
                if sensor_esq_vedra <= PRETO or sensor_dir_vedra <= PRETO:
                    cor_esquerda.pegarRGB()
                    cor_direita.pegarRGB()
                    sensor_esq_vedra = VerificarCorVE() 
                    sensor_dir_vedra = VerificarCorVD()               
                    base.pararMotores()
                    wait(100)
                    base.moverDistancia(50)
                    base.pararMotores()
                    base.virarAngulo(-90)
                    base.pararMotores()
                break


# para quando ver prata
def Prata():
    sensor_esqEx_vedra = VerificarCorVEEx()
    sensor_esq_vedra = VerificarCorVE() 
    sensor_dirEx_vedra = VerificarCorVDEx()
    sensor_dir_vedra = VerificarCorVD()
    if cor_direita.pegarRGB() >= (95, 95, 95) and cor_esquerda.pegarRGB() >= (95, 95, 95):
        return True
    
    return False


# seguir linha
#  base.moverSemParar(velocidade=100, angulo_curvatura=0)

# WHILE TRUE
      
#     motor_garra.resetarAngulo()
#     motor_garra.moverUmAngulo(60, 10)

# while True: 
#     print(cor_direita.pegarRGB() and cor_esquerda.pegarRGB())
#     wait(2000)

# while True: 
#     print("alinhar")
#     alinharLinha()

def seguidorLinha():
    global seguindoLinha
    global distancia
    global angulo_verificar
    global viradaAngulo
    global BRANCO
    global PRETO
    global pretoEsqCor
    global brancoEsqCor
    global pretoDirCor
    global brancoDirCor 
    global BRANCODIR
    global BRANCOESQ
    global PRETODIR
    global PRETOESQ

    # motor_d.moverPorPotencia(potencia=70)
    # motor_e.moverPorPotencia(potencia=70)
    sensor_esq_vedra = VerificarCorVE() # definindo variveis 
    sensor_dir_vedra = VerificarCorVD()
    sensor_dirEx_vedra = VerificarCorVDEx()
    sensor_esqEx_vedra = VerificarCorVEEx()

    if cor_esquerda.pegarRGB()[0] <= 5: 
        ultimaCorEsq = pretoEsqCor
    else: 
        ultimaCorEsq = brancoEsqCor

    if cor_direita.pegarRGB()[0] <= 5: 
        ultimaCorDireita = pretoDirCor
    else:
        ultimaCorDireita = brancoDirCor

    # distanciaParar()

    # if distancia < 100:
    #     distanciaParar()
    #     break

# para quando ver verde: 
#     quando cor esquerda
    if eVerdeE():
        sensor_esqEx_vedra = VerificarCorVEEx()
        sensor_esq_vedra = VerificarCorVE() 
        sensor_dirEx_vedra = VerificarCorVDEx()
        sensor_dir_vedra = VerificarCorVD()
        print ("verde esquerda visto")
        print(cor_esquerda.pegarRGB())
        base.moverDistancia(2)
        base.pararMotores()
        # robo_brick.beep(500, 100)
        # wait(20)

        if eVerdeE():
            base.moverDistancia(20)
            base.pararMotores()
            print("verde dnv esquerda")
            print(cor_esquerda.pegarRGB())
            # robo_brick.beep(500, 100)
            # cor_esquerda.pegarRGB()[1]
            # wait(20)(
            print("teste")
            # if eVerdeD(): # sem redutor
            #     print ("verde direita")
            #     base.moverDistancia(-80)
            #     # base.pararMotores()
            #     base.virarAngulo(-182)
            #     base.pararMotores()

            if eVerdeD(): # dois verdes com um redutor atras
                print ("verde direita")
                base.moverDistancia(90)
                # base.pararMotores()
                base.virarAngulo(-182)
                base.pararMotores()
                
            else:
                cor_esq_verm = cor_esquerda.pegarRGB()[0]
                cor_esq_verd = cor_esquerda.pegarRGB()[1] # preto usando o vermelho 
                if cor_esq_verm < PRETOESQ:
                    # robo_brick.beep(100, 100)
                    if cor_esq_verd > cor_esq_verm:
                        print("preto apos verde esquerda")
                        base.moverDistancia(75)
                        base.pararMotores()
                        VerdeEsquerda()
                        base.moverDistancia(-55)
                        base.pararMotores()


                if cor_esq_verm > BRANCOESQ: #branco tb usando vermelho 
                    print ("branco apos verde")
                    if cor_esq_verd > cor_esq_verm:
                        base.moverDistancia(10)
                        base.pararMotores()                   

    # # quando a direita ver verde 
    elif eVerdeD():
        sensor_esqEx_vedra = VerificarCorVEEx()
        sensor_esq_vedra = VerificarCorVE() 
        sensor_dirEx_vedra = VerificarCorVDEx()
        sensor_dir_vedra = VerificarCorVD()
        print ("verde direito visto")
        print(cor_direita.pegarRGB())
        base.moverDistancia(10)
        base.pararMotores()

        if eVerdeD():
            print("verde dnv direita")
            print(cor_direita.pegarRGB())
            base.moverDistancia(30)
            base.pararMotores()
            # cor_direita.pegarRGB()[1]
            # print("teste")
            # if eVerdeE(): #verificar se o outro tb eh verde mas sem redutor
            #     print ("verde esquerda")
            #     base.pararMotores()
            #     if eVerdeE():
            #         base.moverDistancia(-80)
            #             # base.pararMotores()
            #         base.virarAngulo(-182)
            #         base.pararMotores()

            if eVerdeE(): #verificar se o outro tb eh verde c redutor atras
                print ("verde esquerda")
                base.pararMotores()
                if eVerdeE():
                    base.moverDistancia(90)
                        # base.pararMotores()
                    base.virarAngulo(-182)
                    base.pararMotores()

            else:
                cor_dir_verm = cor_direita.pegarRGB()[0]
                cor_dir_verd = cor_direita.pegarRGB()[1]
                if cor_dir_verm < PRETODIR:
                    if cor_dir_verd > cor_dir_verm:
                            print("preto apos verde direita")
                            base.moverDistancia(75)
                            base.pararMotores()
                            print(cor_direita.pegarRGB())
                            VerdeDireita()
                            base.moverDistancia(-55)
                            base.pararMotores()

                if cor_dir_verm > BRANCODIR:
                    print ("branco apos verde")
                    if cor_dir_verd > cor_dir_verm:
                            base.moverDistancia(20)
                            base.pararMotores()

        
    # quando entrar no branco, 
    # ele vai verificar se ta no gap, caso esteja, 
    # vai realizar o codigo de gap e caso nao, vai ir p preto

    elif sensor_esq_vedra >= BRANCO and sensor_dir_vedra >= BRANCO:
        sensor_esqEx_vedra = VerificarCorVEEx()
        sensor_esq_vedra = VerificarCorVE() 
        sensor_dirEx_vedra = VerificarCorVDEx()
        sensor_dir_vedra = VerificarCorVD()
        print("viu branco")
        print(sensor_esq_vedra, sensor_dir_vedra)

        if sensor_dirEx_vedra <= PRETO or sensor_esqEx_vedra <= PRETO:
            print ("viu extremidade")
            base.moverDistancia(-80)

        if VerificarGap() == True: 

            while sensor_esq_vedra >= BRANCO and sensor_dir_vedra >= BRANCO:
                taNoGap()
                sensor_esq_vedra = VerificarCorVE()
                sensor_dir_vedra = VerificarCorVD()
                sensor_dirEx_vedra = VerificarCorVDEx()
                sensor_esqEx_vedra = VerificarCorVEEx()

                if sensor_esq_vedra < PRETO and sensor_dir_vedra < PRETO:
                    break
        else: 
            print ("saiu do gap")

    elif Distancia(): # obstaculo 
        Obstaculo()
        base.pararMotores()

    elif Prata() == True: 
        print ("prata")
        seguindoLinha = False
        base.pararMotores()

    # codigo seguidor de linha
    else: 
        print ("linha preta")
        sensor_esqEx_vedra = VerificarCorVEEx()
        sensor_esq_vedra = VerificarCorVE() 
        sensor_dirEx_vedra = VerificarCorVDEx()
        sensor_dir_vedra = VerificarCorVD()
        codigoSeguidor.seguirLinhaPreta(
        kd=0.5, # analisa de acordo com a poisçao do começo
        kp=1, # proporcional no momento instante que ocorre o erro
        cor_vermelha_direta=(sensor_esq_vedra + sensor_esqEx_vedra * 2) - 20,
        cor_vermelha_esquerda=sensor_dir_vedra + sensor_dirEx_vedra * 2,
        motor_direito=motor_d,
        motor_esquerdo=motor_e,
        potencia_motores=70
        )

def areaDeResgate():
    sensor_esqEx_vedra = VerificarCorVEEx()
    sensor_esq_vedra = VerificarCorVE() 
    sensor_dirEx_vedra = VerificarCorVDEx()
    sensor_dir_vedra = VerificarCorVD()
    global seguindoLinha
    base.moverSemParar(100, 0)
    if sensor_dir_vedra <= PRETO or sensor_esq_vedra <= PRETO:
        seguindoLinha == True

    
    print("akksks")

##INICIO do codigo


while True:
    if seguindoLinha == True:
        seguidorLinha()
    else:
        areaDeResgate()
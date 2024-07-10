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
    diametroRoda= 46,
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


# FUNÇÕES

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
    print ("mover")
    base.moverDistancia(80)
    # base.virar90grausDireita()
    base.virarAngulo(-90)
    base.pararMotores()

    while sensor_esq_vedra >= BRANCO or sensor_dir_vedra >= BRANCO: 
        base.virarAngulo(-60)
        print(" branco virar verde esq")


        if sensor_dir_vedra <= PRETO or sensor_esq_vedra <= PRETO:
            print("achou preto esq") 
            break


# funcao para mover pra direita quando for verde
def VerdeDireita():
    print ("mover")
    base.moverDistancia(80)
    # base.virar90grausEsquerda()
    base.virarAngulo(90)
    base.pararMotores()
    while sensor_esq_vedra >= BRANCO or sensor_dir_vedra >= BRANCO:
        print(" branco virar verde") 
        base.virarAngulo(60)
        
        if sensor_dir_vedra <= PRETO or sensor_esq_vedra <= PRETO: 
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


    base.virarAngulo(angulo=viradaMaxima*angulo_verificar)
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
    if Distancia() == True: 
        print ("obstaculo")
        base.moverDistancia(-50)
        base.pararMotores()
        base.virar90grausDireita()
        base.pararMotores()
        base.moverDistancia(360)
        base.pararMotores()
        base.virar90grausEsquerda()
        base.pararMotores()
        sensor_esq_vedra = VerificarCorVE() 
        sensor_dir_vedra = VerificarCorVD()
        print(sensor_esq_vedra, sensor_dir_vedra)
        base.moverDistancia(650)
        base.pararMotores()
        base.virar90grausEsquerda()
        sensor_esq_vedra = VerificarCorVE() 
        sensor_dir_vedra = VerificarCorVD()
        base.moverDistancia(250)
        sensor_esq_vedra = VerificarCorVE() 
        sensor_dir_vedra = VerificarCorVD()

        # while sensor_dir_vedra >= BRANCO or sensor_esq_vedra >= BRANCO:
        #     sensor_esq_vedra = VerificarCorVE() 
        #     sensor_dir_vedra = VerificarCorVD()
        #     base.moverSemParar(150)
        #     sensor_esq_vedra = VerificarCorVE() 
        #     sensor_dir_vedra = VerificarCorVD()

        if sensor_esq_vedra <= PRETO or sensor_dir_vedra <= PRETO:
            print("viu preto")
            sensor_esq_vedra = VerificarCorVE() 
            sensor_dir_vedra = VerificarCorVD()
            base.moverDistancia(80)
            base.pararMotores()
            base.virar90grausDireita()
            base.pararMotores()


# para quando ver prata
def Prata():
    if cor_direita.pegarRGB() >= (95, 95, 95) and cor_esquerda.pegarRGB() >= (95, 95, 95):
        return True
    
    return False


# seguir linha
#  base.moverSemParar(velocidade=100, angulo_curvatura=0)

# WHILE TRUE
      
#     motor_garra.resetarAngulo()
#     motor_garra.moverUmAngulo(60, 10)

# while True: 
#     print(cor_direita.pegarRGB())
#     wait(2000)

# vai parar quando for branco e depois seguir reto ate encontrar preto, e quando isso acontecer, vai seguir reto
while True:
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
            if eVerdeD():
                print ("verde direita")
                base.moverDistancia(-80)
                # base.pararMotores()
                base.virarAngulo(-180)
                base.pararMotores()
                
            else:
                cor_esquerda.pegarRGB()[0] # preto usando o vermelho 
                if cor_esquerda.pegarRGB()[0] < 10:
                    # robo_brick.beep(100, 100)
                    if cor_esquerda.pegarRGB()[1] > cor_esquerda.pegarRGB()[0]:
                        print("preto apos verde esquerda")
                        VerdeEsquerda()
                        base.pararMotores()


                if cor_esquerda.pegarRGB()[0] > 52: #branco tb usando vermelho 
                    print ("branco apos verde")
                    if cor_esquerda.pegarRGB()[0] > cor_esquerda.pegarRGB()[0]:
                        base.moverDistancia(10)
                        base.pararMotores()                   

    # # quando a direita ver verde 
    elif eVerdeD(): 
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
            if eVerdeE(): #verificar se o outro tb eh verde
                print ("verde esquerda")
                base.moverDistancia(-80)
                # base.pararMotores()
                base.virarAngulo(-180)
                base.pararMotores()

            else:
                cor_direita.pegarRGB()[0] and cor_direita.pegarRGB()[1]
                if cor_direita.pegarRGB()[0] < 10:
                    if cor_direita.pegarRGB()[1] > cor_direita.pegarRGB()[0]:
                            print("preto apos verde direita")
                            print(cor_direita.pegarRGB())
                            cor_direita.pegarRGB()[0] and cor_direita.pegarRGB()[1]
                            VerdeDireita()
                            base.pararMotores()

                if cor_direita.pegarRGB()[0] > 52:
                    print ("branco apos verde")
                    if cor_direita.pegarRGB()[1] > cor_direita.pegarRGB()[0]:
                            base.moverDistancia(20)
                            base.pararMotores()

        
    # quando entrar no branco, 
    # ele vai verificar se ta no gap, caso esteja, 
    # vai realizar o codigo de gap e caso nao, vai ir p preto

    elif sensor_esq_vedra >= BRANCO and sensor_dir_vedra >= BRANCO:
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
        base.pararMotores()

    # codigo seguidor de linha
    else: 
        # print ("linha preta")
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
        potencia_motores=60
        )
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

BRANCO = 70

PRETO = 30

# FUNÇÕES

# (5, 18, 5)

def eVerdeD():
    cor = cor_direita.pegarRGB()
    # print(cor)
    if cor[1] > 15:
        if cor[1] >= 2.2 * cor[0]:
            return True
        
    return False

def eVerdeE():
    cor = cor_esquerda.pegarRGB()
    # print(cor) 
    if cor[1] > 15:
        if cor[1] >= 2.2 * cor[0]:
            return True
        
    return False


def VerdeEsquerda():
    print ("mover")
    base.moverDistancia(60)
    # base.virar90grausDireita()
    base.virarAngulo(-80)
    base.pararMotores()

def VerdeDireita():
    print ("mover")
    base.moverDistancia(60)
    # base.virar90grausEsquerda()
    base.virarAngulo(80)
    base.pararMotores()

def VerificarCorVE():
    return sensor_vendra.read(0)[1] 

def VerificarCorVEEx():
    return sensor_vendra.read(0)[0] 

def VerificarCorVD():
    return sensor_vendra.read(0)[2]

def VerificarCorVDEx():
    return sensor_vendra.read(0)[3]

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



def taNoGap():
     print("taNoGap")
    #  if VerificarGap() == True: 
     base.pararMotores()
     base.moverDistancia(100)
     base.pararMotores()

    #  while sensor_esq_vedra >= 70 and sensor_dir_vedra >= 70:
    #     base.moverDistancia(100)
    #     base.pararMotores()


def distanciaParar():
    # if distancia < 100:
        distancia = sensor_ultrassonico.pegarDistancia()
        print (distancia)
        motor_d.pararMotorInstantaneamente()
        motor_e.pararMotorInstantaneamente()
        return

# seguir linha
#  base.moverSemParar(velocidade=100, angulo_curvatura=0)

# WHILE TRUE
      
#     motor_garra.resetarAngulo()
#     motor_garra.moverUmAngulo(60, 10)

# while True: 
#     print(sensor_vendra.read(0))
#     wait(1000)

# while True:
#     print(eVerdeE())
#     wait(1000)
    # if(eVerdeD() and eVerdeE()):
    #     print("pegou dois verdes")
    # elif(eVerdeD()):
    #     print("direito")
    # elif(eVerdeE()):
    #     print("esquerdo")
    # else:
    #     print("nada")

# vai parar quando for branco e depois seguir reto ate encontrar preto, e quando isso acontecer, vai seguir reto
while True:
    # motor_d.moverPorPotencia(potencia=70)
    # motor_e.moverPorPotencia(potencia=70)
    sensor_esq_vedra = VerificarCorVE()
    sensor_dir_vedra = VerificarCorVD()
    sensor_dirEx_vedra = VerificarCorVDEx()
    sensor_esqEx_vedra = VerificarCorVEEx()
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
        robo_brick.beep(500, 100)
        # wait(20)

        if eVerdeE():
            base.moverDistancia(1)
            base.pararMotores()
            print("verde dnv esquerda")
            print(cor_esquerda.pegarRGB())
            robo_brick.beep(500, 100)
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
                cor_esquerda.pegarRGB()[0] # preto
                if cor_esquerda.pegarRGB()[0] < 10:
                    robo_brick.beep(100, 100)
                    if cor_esquerda.pegarRGB()[1] > cor_esquerda.pegarRGB()[0]:
                        print("preto apos verde esquerda")
                        VerdeEsquerda()
                        base.pararMotores()

                if cor_esquerda.pegarRGB()[0] > 47: #branco
                    print ("branco apos verde")
                    if cor_esquerda.pegarRGB()[0] > cor_esquerda.pegarRGB()[0]:
                        robo_brick.beep(700, 100)
                        base.moverDistancia(10)
                        base.pararMotores()

                        

    # # quando a direita ver verde 
    elif eVerdeD():
        print ("verde direito visto")
        print(cor_direita.pegarRGB())
        base.moverDistancia(2)
        base.pararMotores()

        if eVerdeD():
            print("verde dnv direita")
            print(cor_direita.pegarRGB())
            base.moverDistancia(1)
            base.pararMotores()
            # cor_direita.pegarRGB()[1]
            print("teste")
            if eVerdeE() : #verificar se o outro tb eh verde
                print ("verde esquerda")
                base.moverDistancia(-80)
                # base.pararMotores()
                base.virarAngulo(-180)
                base.pararMotores()

            else:
                cor_direita.pegarRGB()[0]
                if cor_direita.pegarRGB()[0] < 10:
                    if cor_direita.pegarRGB()[1] > cor_direita.pegarRGB()[0]:
                            print("preto apos verde direita")
                            VerdeDireita()
                            base.pararMotores()

                if cor_direita.pegarRGB()[0] > 50:
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

    # codigo seguidor de linha
    else: 
        # print ("linha preta")
        sensor_esqEx_vedra = VerificarCorVEEx()
        sensor_esq_vedra = VerificarCorVE() 
        sensor_dirEx_vedra = VerificarCorVDEx()
        sensor_dir_vedra = VerificarCorVD()
        codigoSeguidor.seguirLinhaPreta(
        kd=0, # analisa de acordo com a poisçao do começo
        kp=1, # proporcional no momento instante que ocorre o erro
        cor_vermelha_direta=(sensor_esq_vedra + sensor_esqEx_vedra * 2) - 20,
        cor_vermelha_esquerda=sensor_dir_vedra + sensor_dirEx_vedra * 2,
        motor_direito=motor_d,
        motor_esquerdo=motor_e,
        potencia_motores=70
        )
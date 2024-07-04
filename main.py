#!/usr/bin/env pybricks-micropython

# script.py
from titas_lib import HubType, RoboHub, SeguidorLinha, RoboBrick, RoboMotor, RoboCor, RoboUltrassonico, RoboBase, RoboImports, Color

# DEFINIÇÕES

hub_type = HubType(RoboHub.EV3BRICK)

robo_brick = RoboBrick()

sensor_ultrassonico = RoboUltrassonico(Port="2")

cor_direita = RoboCor(Port="4")
cor_esquerda = RoboCor(Port="3")

motor_d = RoboMotor(Port="d")
motor_e = RoboMotor(Port="a", reverse = True)
motor_garra = RoboMotor(Port="b", reverse= True)

sensor_vendra = hub_type.getImports().getLUMPDevice(Port="1") 

codigoSeguidor = SeguidorLinha()

# print(sensor_vendra.read(0))

base = RoboBase(  # passando as informações do robo p uma variavel
    motorDireito= motor_d,
    motorEsquerdo= motor_e,
    diametroRoda= 46,
    distanciaEntreAsRodas= 140
    )

# VARIAVEIS

# para andar enquanto a distancia for maior que 100 
# quando for menor que 100, ira parar lentamente 
distancia = 1000

angulo_verificar = 10

viradaAngulo = 0

# FUNÇÕES

def VerdeEsquerda():
    print ("mover")
    base.moverDistancia(60)
    base.virar90grausDireita()
    base.pararMotores()

def VerdeDireita():
    print ("mover")
    base.moverDistancia(60)
    base.virar90grausEsquerda()
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
    viradaMaxima = 20
    base.moverDistancia (20)

    print("VerificarGap")  
    viradaAngulo = 0
    while viradaAngulo <= viradaMaxima:
        base.virarAngulo(angulo=angulo_verificar)
        viradaAngulo += 1
        VerificarCorVD() and VerificarCorVE()
        print("virarAngulo")

    
        if VerificarCorVD() < 30 or VerificarCorVE() < 30:
            print("deu false") 
            base.pararMotores()
            print("pararMotorInstantaneamente")      
            return False

    print("entrou aqui")

    while viradaAngulo >= -viradaMaxima:
        base.virarAngulo(angulo= -angulo_verificar)
        viradaAngulo -= 1
        VerificarCorVD() and VerificarCorVE()
        print("virarAngulo")            

        if VerificarCorVD() < 30 or VerificarCorVE() < 30:
            print("deu false") 
            base.pararMotores()
            return False
        print("entrou aqui")    


    base.virarAngulo(angulo=15*angulo_verificar)
    return True   

def taNoGap():
     print("taNoGap")
     if VerificarGap() == True: 
        base.pararMotores()
        base.moverDistancia(100)
        base.pararMotores()
        return


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

# while True:
    
    
#     motor_garra.resetarAngulo()
#     motor_garra.moverUmAngulo(60, 10)

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
    if cor_esquerda.pegarCor()== hub_type.getImports().getColor().GREEN:
        print ("verde esquerda visto")
        base.moverDistancia(20)

        if cor_esquerda.pegarCor() == hub_type.getImports().getColor().GREEN:
            VerdeEsquerda()
        base.pararMotores()

    # # quando a direita ver verde    
    if cor_direita.pegarCor()== hub_type.getImports().getColor().GREEN:
        print ("verde esquerda visto")
        base.moverDistancia(20)

        if cor_direita.pegarCor() == hub_type.getImports().getColor().GREEN:
            VerdeDireita()
        base.pararMotores()

        
    # quando entrar no branco, 
    # ele vai verificar se ta no gap, caso esteja, 
    # vai realizar o codigo de gap e caso nao, vai ir p preto

    if sensor_esq_vedra >= 70 and sensor_dir_vedra >= 70:
        print("viu branco")
        print(sensor_esq_vedra, sensor_dir_vedra)

        if sensor_dirEx_vedra <= 30 or sensor_esqEx_vedra <= 30:
            base.moverDistancia(-50)

        else:
            taNoGap()

    # codigo seguidor de linha
    else: 
        print ("linha preta")
        sensor_esq_vedra = VerificarCorVE()
        sensor_dir_vedra = VerificarCorVD()
        codigoSeguidor.seguirLinhaPreta(
        kd=0.5, # analisa de acordo com a poisçao do começo
        kp=1, # proporcional no momento instante que ocorre o erro
        cor_vermelha_direta=sensor_esq_vedra,
        cor_vermelha_esquerda=sensor_dir_vedra,
        motor_direito=motor_d,
        motor_esquerdo=motor_e,
        potencia_motores=60
        )
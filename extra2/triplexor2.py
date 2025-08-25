#!/usr/bin/env pybricks-micropython
import random
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, ColorSensor, InfraredSensor)
from pybricks.parameters import Port, Stop
from pybricks.tools import wait
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile


ev3 = EV3Brick()

motor_esquerdo = Motor(Port.A)
motor_direito = Motor(Port.B)

# Sensor de cor e infravermelho
sensor_cor = ColorSensor(Port.S4)
sensor_infravermelho = InfraredSensor(Port.S1)

# Configurar a base de direção (drive base) com distância entre rodas e diâmetro.
robot = DriveBase(motor_esquerdo, motor_direito, wheel_diameter=56, axle_track=120)

# Parâmetros
WHITE_THRESHOLD = 50  # Valor para detectar a borda (ajustar conforme seu ringue)
ATTACK_SPEED = 500    # Velocidade de ataque mais alta para agressividade
SEARCH_SPEED = -250    # Velocidade de busca
RETREAT_SPEED = 250  # Velocidade de recuo
TURN_RATE = 100      # Taxa de giro para a busca

def detectar_borda():
    """
    Usa a intensidade de luz refletida para detectar a borda branca.
    Retorna True se a leitura for maior que o limite.
    """
    return sensor_cor.reflection() > WHITE_THRESHOLD

def detectar_oponente():
    """
    Detecta se o oponente está dentro da distância de ataque usando o sensor de infravermelho.
    Inclui uma verificação para evitar erros quando o sensor não detecta nada.
    """
    distance = sensor_infravermelho.distance()
    return distance is not None and distance < 30

def recuar_e_girar_aleatorio():
    """
    Recua da borda do ringue e gira em um ângulo aleatório para evitar
    ser empurrado para fora e para tornar o movimento menos previsível.
    """
    ev3.screen.print("Borda detectada! Recuando...")
    
    # Recua rapidamente por um curto período de tempo e para
    robot.drive_time(RETREAT_SPEED, 0, 400, then=Stop.BRAKE)
    wait(100) # Espera um pouco para garantir que parou

    # Gera um ângulo de giro aleatório entre -200 e 135 graus
    giro_aleatorio = random.randint(45, 135)
    robot.turn(giro_aleatorio)
    
def atacar():
    """
    Move o robô para frente em alta velocidade para empurrar o oponente.
    """
    ev3.screen.print("Oponente detectado! Atacando...")
    robot.drive(ATTACK_SPEED, 200)
    
def procurar_oponente():
    """
    Gira suavemente enquanto avança para cobrir uma área maior
    do ringue em busca do oponente.
    """
    ev3.screen.print("Procurando...")
    # Gira suavemente para a direita enquanto avança
    robot.drive(SEARCH_SPEED, TURN_RATE)

# Loop principal
ev3.speaker.beep() # Sinal sonoro para indicar que o programa iniciou
while True:
    # A ordem dos "if/elif" é crucial para a lógica do robô
    if detectar_borda():
        # Se a borda for detectada, o robô deve recuar imediatamente
        recuar_e_girar_aleatorio()
    elif detectar_oponente():
        # Se o oponente for detectado, o robô deve atacar
        atacar()
    else:
        # Se nenhuma das condições for verdadeira, o robô procura
        procurar_oponente()
        
    wait(20) # Espera 20ms para um loop mais responsivo e eficiente

"""
Lógica de Ataque e Busca Aprimorada: Em vez de apenas girar para buscar, o robô agora se move para a frente enquanto gira. Isso permite que ele cubra uma área maior do ringue.
Recuo Mais Inteligente: Ao detectar a borda, o robô agora recua e gira em um ângulo aleatório, tornando seu movimento menos previsível para o adversário e mais eficaz para se manter no ringue.
Parâmetros de Velocidade Aumentados: As velocidades de ataque e busca foram ajustadas para tornar o robô mais competitivo e rápido.
Uso de Stop.BRAKE: A função drive_time() agora usa then=Stop.BRAKE, o que faz com que os motores parem imediatamente, garantindo reações mais rápidas e precisas. """
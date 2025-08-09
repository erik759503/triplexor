#!/usr/bin/env pybricks-micropython

from pybricks.hubs import EV3Brick
from pybricks.ev3devices import Motor, ColorSensor, InfraredSensor
from pybricks.parameters import Port, Color, Stop
from pybricks.tools import StopWatch, wait

# Inicialização do EV3
ev3 = EV3Brick()

# Motores nas portas A e B
motor_esq = Motor(Port.A)
motor_dir = Motor(Port.B)

# Sensores: cor na S2, infravermelho na S1
sensor_cor = ColorSensor(Port.S2)
sensor_ir = InfraredSensor(Port.S1)

def mostrar_mensagem(texto):
    print(texto)
    ev3.screen.clear()
    ev3.screen.print(texto)

def parar_motores():
    motor_esq.stop(Stop.BRAKE)
    motor_dir.stop(Stop.BRAKE)

def andar_frente(velocidade=500):
    mostrar_mensagem("[AÇÃO] Avançando")
    motor_esq.run(velocidade)
    motor_dir.run(velocidade)

def recuar(velocidade=-500):
    mostrar_mensagem("[AÇÃO] Recuando")
    motor_esq.run(velocidade)
    motor_dir.run(velocidade)

def girar(vel_esq=-500, vel_dir=500):
    mostrar_mensagem("[AÇÃO] Girando")
    motor_esq.run(vel_esq)
    motor_dir.run(vel_dir)

def explorar(velocidade=500):
    mostrar_mensagem("[AÇÃO] Explorando")
    motor_esq.run(velocidade)
    motor_dir.run(velocidade)

def main():
    mostrar_mensagem("[INÍCIO] Robô pronto!")
    wait(2000)

    estado_atual = None
    relogio_acao = StopWatch()
    duracao_acao_ms = 0

    while True:
        distancia = sensor_ir.distance()
        cor_detectada = sensor_cor.color()

        print("[SENSORES] IR: {} cm | Cor: {}".format(distancia, cor_detectada))

        # Se estiver realizando uma ação temporizada, verifica se terminou
        if duracao_acao_ms > 0 and relogio_acao.time() >= duracao_acao_ms:
            parar_motores()
            estado_atual = None
            duracao_acao_ms = 0

        # Se não estiver enchendo tempo, decide ação
        if duracao_acao_ms == 0:  # pronto para nova ação

            if cor_detectada == Color.WHITE:
                # Começa a recuar por 500ms
                if estado_atual != "borda_recuar":
                    recuar()
                    relogio_acao.reset()
                    duracao_acao_ms = 500
                    estado_atual = "borda_recuar"
                # Após recuar, gira 500ms
                elif estado_atual == "borda_recuar" and relogio_acao.time() >= 500:
                    girar()
                    relogio_acao.reset()
                    duracao_acao_ms = 500
                    estado_atual = "borda_girar"

            elif distancia is not None and distancia < 30:
                if estado_atual != "atacando":
                    andar_frente()
                    estado_atual = "atacando"
                    duracao_acao_ms = 0  # movimento contínuo, sem duracao fixa

            else:
                if estado_atual != "procurando":
                    girar()
                    mostrar_mensagem("[AÇÃO] Procurando adversário...")
                    estado_atual = "procurando"
                    duracao_acao_ms = 0

if __name__ == "__main__":
    main()

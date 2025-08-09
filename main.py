#!/usr/bin/env pybricks-micropython

from pybricks.hubs import EV3Brick
from pybricks.ev3devices import Motor, ColorSensor, InfraredSensor
from pybricks.parameters import Port, Color, Stop
from pybricks.tools import StopWatch, wait

# Inicialização do EV3
ev3 = EV3Brick()

# Motores conectados nas portas A e B
motor_esq = Motor(Port.A)
motor_dir = Motor(Port.B)

# Sensores: Cor na S2, Infravermelho na S1
sensor_cor = ColorSensor(Port.S2)
sensor_ir = InfraredSensor(Port.S1)

def mostrar_mensagem(texto):
    """Mostra mensagem no display e no terminal"""
    print(texto)
    ev3.screen.clear()
    ev3.screen.print(texto)

def parar_motores():
    """Para motores com freio"""
    motor_esq.stop(Stop.BRAKE)
    motor_dir.stop(Stop.BRAKE)

def andar_frente(velocidade=500):
    """Move para frente continuamente até mudar ação"""
    mostrar_mensagem("[AÇÃO] Avançando")
    motor_esq.run(velocidade)
    motor_dir.run(velocidade)

def recuar(velocidade=-500):
    """Move para trás continuamente até mudar ação"""
    mostrar_mensagem("[AÇÃO] Recuando")
    motor_esq.run(velocidade)
    motor_dir.run(velocidade)

def girar(vel_esq=-500, vel_dir=500):
    """Gira no lugar continuamente até mudar ação"""
    mostrar_mensagem("[AÇÃO] Girando")
    motor_esq.run(vel_esq)
    motor_dir.run(vel_dir)

def explorar(velocidade=500):
    """Avança por tempo curto para explorar"""
    mostrar_mensagem("[AÇÃO] Explorando")
    motor_esq.run(velocidade)
    motor_dir.run(velocidade)

def main():
    mostrar_mensagem("[INÍCIO] Robô pronto!")
    wait(2000)

    estado_atual = None
    relogio_acao = StopWatch()
    tempo_procurando = StopWatch()
    duracao_acao_ms = 0

    while True:
        distancia = sensor_ir.distance()
        cor_detectada = sensor_cor.color()

        print("[SENSORES] IR: {} cm | Cor: {}".format(distancia, cor_detectada))

        # Verifica se ação temporizada terminou
        if duracao_acao_ms > 0 and relogio_acao.time() >= duracao_acao_ms:
            parar_motores()
            relogio_acao.reset()
            duracao_acao_ms = 0
            estado_atual = None

        # Definir ação se não estiver em ação temporizada
        if duracao_acao_ms == 0:

            # Detectou borda branca: recua e gira (ações temporizadas)
            if cor_detectada == Color.WHITE:
                if estado_atual != "borda_recuar" and estado_atual != "borda_girar":
                    recuar()
                    relogio_acao.reset()
                    duracao_acao_ms = 500
                    estado_atual = "borda_recuar"
                    tempo_procurando.reset()
                elif estado_atual == "borda_recuar" and relogio_acao.time() >= 500:
                    girar()
                    relogio_acao.reset()
                    duracao_acao_ms = 500
                    estado_atual = "borda_girar"

            # Detectou adversário próximo: avança continuamente
            elif distancia is not None and distancia < 30:
                if estado_atual != "atacando":
                    andar_frente()
                    estado_atual = "atacando"
                    tempo_procurando.reset()

            # Caso contrário, procura girando e explora após 5s
            else:
                if estado_atual != "procurando" and estado_atual != "explorando":
                    girar()
                    estado_atual = "procurando"
                    mostrar_mensagem("[AÇÃO] Procurando adversário...")
                    tempo_procurando.reset()

                elif estado_atual == "procurando":
                    if tempo_procurando.time() >= 5000:
                        explorar()
                        relogio_acao.reset()
                        duracao_acao_ms = 1000
                        estado_atual = "explorando"
                        tempo_procurando.reset()

                # Após explorar, a ação temporizada cuida do retorno ao estado neutro

if __name__ == "__main__":
    main()

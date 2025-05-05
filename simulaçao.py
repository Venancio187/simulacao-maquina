import pygame
import time
import datetime
import json
import csv
import matplotlib.pyplot as plt
import threading

# Inicializa o pygame
pygame.init()

# Configurações da tela
largura, altura = 800, 600
tela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption("Simulação da Máquina")
fonte = pygame.font.SysFont(None, 36)

# Cores
BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)
VERDE = (0, 255, 0)
VERMELHO = (255, 0, 0)

# Variáveis
pecas_produzidas = 0
modo_acelerado = False
parado = False
producao = []

# Carrega dados da OP
with open("op_ativa.json", "r") as f:
    dados_op = json.load(f)

quantidade_meta = int(dados_op["quantidade"])
tempo_ciclo_normal = float(dados_op["tempo_ciclo"])
tempo_ciclo = tempo_ciclo_normal
inicio_peca = time.time()
inicio_producao = time.time()

# Função para reconhecer o turno atual
def reconhecer_turno():
    agora = datetime.datetime.now().time()
    if datetime.time(7, 30) <= agora < datetime.time(17, 0):
        return "Turno 1"
    elif datetime.time(17, 10) <= agora or agora < datetime.time(2, 10):
        return "Turno 2"
    elif datetime.time(2, 15) <= agora < datetime.time(7, 30):
        return "Turno 3"
    return "Desconhecido"

# Função para desenhar os elementos na tela
def desenhar():
    tela.fill(BRANCO)
    tempo_medio = tempo_ciclo
    tempo_restante = max((quantidade_meta - pecas_produzidas) * tempo_medio, 0)
    horas, resto = divmod(int(tempo_restante), 3600)
    minutos, segundos = divmod(resto, 60)

    textos = [
        f"Peças produzidas: {pecas_produzidas}/{quantidade_meta}",
        f"Modo acelerado: {'Sim' if modo_acelerado else 'Não'}",
        f"Tempo médio por peça: {tempo_medio:.2f}s",
        f"Tempo restante: {horas:02d}:{minutos:02d}:{segundos:02d}",
        f"Status: {'Parado' if parado else 'Produzindo'}"
    ]

    for i, texto in enumerate(textos):
        render = fonte.render(texto, True, PRETO)
        tela.blit(render, (50, 50 + i * 40))

    pygame.display.flip()

# Função para gerar gráfico ao vivo
def mostrar_grafico():
    plt.ion()
    fig, ax = plt.subplots()
    while True:
        if producao:
            ax.clear()
            ax.plot(producao, label="Peças produzidas")
            ax.set_title("Produção ao Vivo")
            ax.set_xlabel("Tempo (ciclos)")
            ax.set_ylabel("Peças")
            ax.legend()
            plt.pause(1)

# Inicia o gráfico em thread separada
threading.Thread(target=mostrar_grafico, daemon=True).start()

# Loop principal
rodando = True
while rodando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False
        elif evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_SPACE and not parado:
                modo_acelerado = not modo_acelerado
            elif evento.key == pygame.K_p and not parado:
                motivo = input("Informe o motivo da parada: ")
                turno_atual = reconhecer_turno()
                tempo = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                with open("relatorio_paradas.csv", "a", newline='') as csvfile:
                    writer = csv.writer(csvfile)
                    writer.writerow([dados_op["op"], turno_atual, motivo, tempo])
                parado = True
                print("Máquina parada. Pressione qualquer tecla para continuar...")
            elif parado:
                parado = False
                inicio_peca = time.time()

    if not parado and pecas_produzidas < quantidade_meta:
        tempo_ciclo = tempo_ciclo_normal / 2 if modo_acelerado else tempo_ciclo_normal
        if time.time() - inicio_peca >= tempo_ciclo:
            pecas_produzidas += 1
            producao.append(pecas_produzidas)
            inicio_peca = time.time()

    desenhar()

    if pecas_produzidas >= quantidade_meta:
        print("Meta atingida!")
        rodando = False

pygame.quit()

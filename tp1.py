from pygame.math import Vector2
import numpy as np
import pygame
import pdb
"""
OBS: Para rodar o programa é necessario instalar o pacote numpy e pygame.

O programa permite escolher o eixo de reflexao interativamente, basta adicionar pontos 
para ter o poligono a ser exibido.

Comandos:
    Click com o botao esquerdo do mouse cria o eixo de reflexão e reflete o poligono.
    Click com o botao direito adiciona um vertice no poligono.
    Tecla r reseta o poligono.

"""
# Resolução da tela
width, height = 640, 640
max_x, max_y = width // 2, height // 2

# Converte um ponto cartesiano para as coordenadas do pygame
def to_pygame(vetor):
    global width, height, max_x, max_y

    translacao = np.array([[1, 0, max_x],
                           [0, -1, max_y],
                           [0, 0, 1]])
    vetor_trans = translacao.dot(vetor + [1])

    return vetor_trans[:-1].tolist()

# Converte um poligono das coordenadas do pygame para cartesiano
def poly_to_pygame(vertex):
    n_vertex = []
    for i in range(len(vertex)):
        n_vertex.append(to_pygame(vertex[i]))
    return n_vertex

# Converte um ponto das coordenadas do pygame para cartesiano
def to_cartesian(vetor):
    global width, height, max_x, max_y

    translacao = np.array([[1, 0, -max_x], [0, -1, max_y], [0, 0, 1]])
    vetor_trans = translacao.dot(vetor + [1])

    return vetor_trans[:-1].tolist()


# Reflete um ponto em relação k, com o angulo de k e o eixo x sendo alfa
def reflect(alpha, vetor):
    ref = np.array([[np.cos(2 * alpha), np.sin(2 * alpha)],
                   [np.sin(2 * alpha), -np.cos(2 * alpha)]])
    vetor_ref = ref.dot(vetor)

    return vetor_ref.tolist()

# Reflete um poligono em relação a k, com o angulo de k e o eixo x sendo alfa
def reflect_poly(alpha, vertex):
    new_vertex = []
    for i in range(len(vertex)):
        new_vertex.append(reflect(alpha, vertex[i]))
    return new_vertex


def main():
    pygame.init()
    screen = pygame.display.set_mode([width, height])

    # pontos do poligono ------------------------------------------------------

    poly_vertex = []

    # ---------------------------------------------------------------------------
    origem = to_pygame([0, 0])
    eixo = []

    running = True
    while running:
        # Cor do fundo da tela
        screen.fill((30, 30, 45))

        for event in pygame.event.get():
            # Detecta click em fechar
            if event.type == pygame.QUIT:
                running = False

            # Detecta click para determinar eixo de reflexão
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                pos = pygame.mouse.get_pos()
                eixo = to_cartesian([pos[0], pos[1]])
                rad = np.arctan2(eixo[1], eixo[0])

            # Acrescenta um vertice no poligono
            if event.type == pygame.MOUSEBUTTONUP and event.button == 3:
                pos = pygame.mouse.get_pos()
                poly_vertex.append(to_cartesian([pos[0], pos[1]]))
            
            # Resetar o poligono
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                poly_vertex = []
                

        # Desenha eixos cartesianos
        pygame.draw.line(screen, (200, 50, 50), to_pygame(
            [-max_x, 0]), to_pygame([max_x, 0]), 1)
        pygame.draw.line(screen, (200, 50, 50), to_pygame(
            [0, -max_y]), to_pygame([0, max_y]), 1)

        if(len(poly_vertex)>2):
            pygame.draw.polygon(screen, (50, 50, 200),
                                tuple(poly_to_pygame(poly_vertex)))

        # Desenha eixo de reflexão
        if eixo:
            eixo_vec = to_pygame(eixo) - Vector2(origem)
            eixo_vec = eixo_vec * width
            pygame.draw.line(screen, (0, 255, 0), origem -
                             eixo_vec, origem + eixo_vec, 2)

            # Desenha triângulo refletido
            ref_poly = reflect_poly(rad, poly_vertex)
            if(len(poly_vertex)>2):
                pygame.draw.polygon(screen, (200, 40, 180),
                                    tuple(poly_to_pygame(ref_poly)))

        # Exibe coordenadas do ponteiro do mouse
        myFont = pygame.font.SysFont("Times New Roman", 16)
        pos = pygame.mouse.get_pos()

        mouse_x, mouse_y = to_cartesian([pos[0], pos[1]])
        mouse_pos = myFont.render(
            f'x: {mouse_x}, y: {mouse_y}', 1, (255, 255, 255))
        screen.blit(mouse_pos, (0, 0))

        pygame.display.flip()

    pygame.quit()


if __name__ == '__main__':
    main()
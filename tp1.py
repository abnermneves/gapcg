from pygame.math import Vector2
import numpy as np
import pygame
import pdb

# resolução da tela
width, height = 640, 480
max_x, max_y = width // 2, height // 2

# converte um ponto cartesiano para as coordenadas do pygame
def to_pygame(vetor):
  global width, height, max_x, max_y

  translacao = np.array([[1, 0, max_x], [0, -1, max_y], [0, 0, 1]])
  vetor_trans = translacao.dot(vetor + [1])

  return vetor_trans[:-1].tolist()

# converte um ponto nas coordenadas do pygame para cartesiano
def to_cartesian(vetor):
  global width, height, max_x, max_y
  
  translacao = np.array([[1, 0, -max_x], [0, -1, max_y], [0, 0, 1]])
  vetor_trans = translacao.dot(vetor + [1])

  return vetor_trans[:-1].tolist()

def reflect(alpha, vetor):
  ref = np.array([[np.cos(2*alpha), np.sin(2*alpha)], [np.sin(2*alpha), -np.cos(2*alpha)]])
  vetor_ref = ref.dot(vetor)

  return vetor_ref.tolist()

def main():
  pygame.init()
  screen = pygame.display.set_mode([width, height])

  # pontos do triângulo
  a = [100, 200]
  b = [50, 50]
  c = [300, 100]

  origem = to_pygame([0, 0])
  eixo = []

  running = True
  while running:
    screen.fill((0, 0, 0))

    for event in pygame.event.get():
      # detecta click em fechar
      if event.type == pygame.QUIT:
        running = False

      # detecta click para determinar eixo de reflexão
      if event.type == pygame.MOUSEBUTTONUP:
        pos = pygame.mouse.get_pos()
        eixo = to_cartesian([pos[0], pos[1]])
        rad = np.arctan2(eixo[1], eixo[0])

    # desenha eixos cartesianos
    pygame.draw.line(screen, (255, 0, 0), to_pygame([-max_x, 0]), to_pygame([max_x, 0]), 1)
    pygame.draw.line(screen, (255, 0, 0), to_pygame([0, -max_y]), to_pygame([0, max_y]), 1)

    pygame.draw.polygon(screen, (0, 0, 255), (to_pygame(a), to_pygame(b), to_pygame(c)))

    # desenha eixo de reflexão
    # pdb.set_trace()
    if eixo:
      eixo_vec = to_pygame(eixo) - Vector2(origem)
      eixo_vec = eixo_vec * width
      pygame.draw.line(screen, (0, 255, 0), origem - eixo_vec, origem + eixo_vec, 2)

      # desenha triângulo refletido
      a_ref = reflect(rad, a)
      b_ref = reflect(rad, b)
      c_ref = reflect(rad, c)
      pygame.draw.polygon(screen, (0, 255, 0), (to_pygame(a_ref), to_pygame(b_ref), to_pygame(c_ref)))
    
    # exibe coordenadas do ponteiro do mouse
    myFont = pygame.font.SysFont("Times New Roman", 16)
    pos = pygame.mouse.get_pos()
    
    mouse_x, mouse_y = to_cartesian([pos[0], pos[1]])
    mouse_pos = myFont.render(f'x: {mouse_x}, y: {mouse_y}', 1, (255, 255, 255))
    screen.blit(mouse_pos, (0, 0))

    pygame.display.flip()

  pygame.quit()

if __name__ == '__main__':
  main()

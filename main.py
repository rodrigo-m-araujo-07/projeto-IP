import pygame
from pygame import *
from sys import exit

pygame.init()

tela = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("nome do jogo")
status = True

pos = pygame.Vector2((1280/2) - 25, (720/2) -25)

clock = pygame.time.Clock()

while status:
    tela.fill((0, 0, 0))
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()
        

    pygame.draw.rect(tela, (0, 0, 255), (pos[0], pos[1], 50, 50))
    #pygame.draw.line(tela, (255, 0, 0), (20, 100), (400, 100), 10)

    keys = pygame.key.get_pressed()

    if(keys[pygame.K_w]):
        pos.y -= 300 * dt
    if(keys[pygame.K_s]):
        pos.y += 300 * dt
    if(keys[pygame.K_d]):
        pos.x += 300 * dt
    if(keys[pygame.K_a]):
        pos.x -= 300 * dt
    

    pygame.display.update()
    

    dt = clock.tick(60)/500
    print(clock.tick(60))



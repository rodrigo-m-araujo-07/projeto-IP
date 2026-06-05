import pygame
import numpy
from player import Jogador
import sys
import os

folderPath = os.path.dirname(os.path.abspath(__file__))
pygame.init() 
clock = pygame.time.Clock()
#tamanhoTela:tuple = pygame.display.get_desktop_sizes()[0]
telaSizePlaceholder = (1360,800)
tela = pygame.display.set_mode(telaSizePlaceholder)
fps=60
bg = pygame.image.load(os.path.join(folderPath,"images","placeholderBG.png")).convert()
bg = pygame.transform.scale(bg, (1360,800))
bgSize = bg.get_rect()
main = True

jogador = Jogador(
        spriteImage=os.path.join(folderPath,'images', 'playerSprites', 'slime_green.png'),
        posInicial=(1360 / 2, 800),
        #grupos=self.all_sprites,
        #game=self
    )

while main:
    #ve se fechou o jogo
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
            main=False
        if event.type == pygame.KEYDOWN:
            if event.key == ord("q"):
                pygame.quit()
                sys.exit()
                main=False
    
    #limpa tela pra atualizar prox frame
    scaling=5
    tela.blit(bg, bgSize)
    grupoJogador = pygame.sprite.Group()
    grupoJogador.add(jogador)
    jogador.update()
    grupoJogador.draw(tela)
    #flip atualiza a tela
    pygame.display.flip()
    clock.tick(fps)
import pygame
import numpy
from player import Jogador
import sys
import os
import random
from itens import itemGeral

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

jogador = Jogador(
        spriteImage=os.path.join(folderPath,'images', 'playerSprites', 'slime_green.png'),
        posInicial=(1360 / 2, 800),
        #grupos=self.all_sprites,
        #game=self
    )

createItem = 999

timerItem = pygame.time.set_timer(createItem, 3000)

#cria grupos
grupoItem = pygame.sprite.Group()
grupoJogador = pygame.sprite.Group()

main = True
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
        if event.type == createItem:
            print("criar")
            x = random.randint(200,1100)
            y = random.randint(200,600)
            itemSpawnado = itemGeral(
                spriteImage=os.path.join(folderPath,'images', 'itemBase.png'),
                posInicial=(x, y)
            )
            grupoItem.add(itemSpawnado)
    
    #colisão player item
    pygame.sprite.spritecollide(jogador, grupoItem, True)
    
    #limpa tela pra atualizar prox frame
    tela.blit(bg, bgSize)
    
    #criar jogador
    grupoJogador.add(jogador)
    jogador.update()
    
    #desenha tudo na tela
    grupoJogador.draw(tela)
    grupoItem.draw(tela)
    
    #flip atualiza a tela
    pygame.display.flip()
    clock.tick(fps)
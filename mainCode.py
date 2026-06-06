import pygame
import numpy
from player import Jogador
from enemy import Inimigo
import sys
import os

folderPath = os.path.dirname(os.path.abspath(__file__))
pygame.init() 
clock = pygame.time.Clock()
#tamanhoTela:tuple = pygame.display.get_desktop_sizes()[0]
telaSizePlaceholder = (1360,800)
tela = pygame.display.set_mode(telaSizePlaceholder)
pygame.display.set_caption("nome do jogo") #alterar para o nome do jogo dps
fonte = pygame.font.SysFont("arial", 40, True, False)
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

enemy = Inimigo(os.path.join(folderPath, "images", "enemy", "retangulo_vermelho.png"),
        (500, 400)

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
    grupoInimigo = pygame.sprite.Group()
    grupoInimigo.add(enemy)
    #grupoJogador.add(enemy)
    grupoJogador.update()
    grupoInimigo.update()
    
    grupoJogador.draw(tela)
    grupoInimigo.draw(tela)
    #flip atualiza a tela
    pygame.display.flip()
    clock.tick(fps)

    colisao = pygame.sprite.spritecollide(jogador, grupoInimigo, False)
    if colisao: #a lista fica vazia até detectar uma colisão, quando recebe um elemento, entra na condicional
        
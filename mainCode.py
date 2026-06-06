import pygame
import numpy
from player import Jogador
from enemy import Inimigo, Bullet
import sys
import os
from time import perf_counter

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

enemy = Inimigo(os.path.join(folderPath, "images", "enemy", "retangulo_vermelho.png"))

#variaveis para o disparo da bala
t_inicio = perf_counter()
disparo = 1

grupoJogador = pygame.sprite.Group()
grupoInimigo = pygame.sprite.Group()
grupoBullets = pygame.sprite.Group()

while main:
    hp = f"Vida: {jogador.vida}"
    hp_form = fonte.render(hp, False, (255, 255, 255))
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
    tela.blit(hp_form, (18, 18))
    
    grupoJogador.add(jogador)
    
    grupoInimigo.add(enemy)
    
    
    if disparo:
        bullet = Bullet(os.path.join(folderPath, "images", "enemy", "bullet.png"),
                        (enemy.rect.centerx,enemy.rect.centery)
        )
        grupoBullets.add(bullet)
        bullet.direcao((jogador.rect.center), (enemy.rect.center))
        disparo = 0
        print("POW")
    elif int(perf_counter()) - t_inicio >= 2:
        disparo = 1
        t_inicio = int(perf_counter())
    

    grupoJogador.update()
    grupoInimigo.update()
    grupoBullets.update()
    
    
    grupoJogador.draw(tela)
    grupoInimigo.draw(tela)
    grupoBullets.draw(tela)
    #flip atualiza a tela
    pygame.display.flip()
    clock.tick(fps)

    colisao_b = pygame.sprite.spritecollide(jogador, grupoBullets, True)
    colisao_i = jogador.rect.colliderect(enemy.rect)
    if colisao_b or colisao_i: #a lista fica vazia até detectar uma colisão, quando recebe um elemento, entra na condicional
        jogador.vida -= 20
        

        
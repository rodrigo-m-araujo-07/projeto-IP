import pygame
import numpy
from player import Jogador
from enemy import Inimigo, Bullet
import sys
import os
import random
from itens import itemGeral, ParteEscudo, PowerUP
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

deltaTime = clock.tick(60)/1000

jogador = Jogador(
        spriteImage=os.path.join(folderPath,'images', 'playerSprites', 'slime_green.png'),
        posInicial=(1360 / 2, 800),
        dt=deltaTime
        #grupos=self.all_sprites,
        #game=self
    )

createItem = 999

create_escudo = pygame.USEREVENT + 1
pygame.time.set_timer(create_escudo, 2000)
create_powerup = pygame.USEREVENT + 2
pygame.time.set_timer(create_powerup, 6000)

timerItem = pygame.time.set_timer(createItem, 3000)

#cria grupos
grupoItem = pygame.sprite.Group()
grupoEscudo = pygame.sprite.Group()
grupoPowerUP = pygame.sprite.Group()
grupoJogador = pygame.sprite.Group()
grupoInimigo = pygame.sprite.Group()
grupoBullets = pygame.sprite.Group()

main = True
enemy = Inimigo(os.path.join(folderPath, "images", "enemy", "retangulo_vermelho.png"), deltaTime)

#variaveis para o disparo da bala
t_inicio = perf_counter()
disparo = 1


while main:
    deltaTime = clock.tick(60)/1000
    if deltaTime>1.0:
        deltaTime=1.0
        
    #print(clock.get_fps())
        
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
        if event.type == createItem:
            print("criar")
            x = random.randint(200,1100)
            y = random.randint(200,600)
            itemSpawnado = itemGeral(
                spriteImage=os.path.join(folderPath,'images', 'itemBase.png'),
                posInicial=(x, y),
            )
            grupoItem.add(itemSpawnado)
        if event.type == grupoEscudo:
            print("escudo")
            x = random.randint(200,1100)
            y = random.randint(200,600)
            grupoEscudo.add(spriteImage=os.path.join(folderPath,'images', 'Escudo.png'),
                posInicial=(x, y),)
        if event.type == grupoPowerUP:
            if len(grupoPowerUP) == 0:
                print("PowerUP")
                x = random.randint(200,1100)
                y = random.randint(200,600)
                grupoEscudo.add(PospriteImage=os.path.join(folderPath,'images', 'PowerUP.png'),
                    posInicial=(x, y),)

    #colisão player item
    pygame.sprite.spritecollide(jogador, grupoItem, True)
    
    #limpa tela pra atualizar prox frame
    tela.blit(bg, bgSize)
    tela.blit(hp_form, (18, 18))
    
    #criar personagens
    grupoJogador.add(jogador)
    grupoInimigo.add(enemy)
    
    
    
    
    
    
    
    
    if disparo:
        bullet = Bullet(
            os.path.join(folderPath, "images", "enemy", "bullet.png"),
            (enemy.rect.centerx,enemy.rect.centery),
            dt=deltaTime
        )
        grupoBullets.add(bullet)
        bullet.direcao((jogador.rect.center), (enemy.rect.center))
        disparo = 0
        print("POW")
    elif int(perf_counter()) - t_inicio >= 3:
        disparo = 1
        t_inicio = int(perf_counter())
    
    #update de tudo
    grupoJogador.update(deltaTime)
    grupoInimigo.update(deltaTime)
    grupoBullets.update(deltaTime)
    #print(grupoBullets)
    
    #desenha tudo na tela
    grupoJogador.draw(tela)
    grupoItem.draw(tela)
    grupoInimigo.draw(tela)
    grupoBullets.draw(tela)
    #flip atualiza a tela
    pygame.display.flip()
    clock.tick(fps)

    colisao_b = pygame.sprite.spritecollide(jogador, grupoBullets, True)
    colisao_i = jogador.rect.colliderect(enemy.rect)
    if colisao_b or colisao_i: #a lista fica vazia até detectar uma colisão, quando recebe um elemento, entra na condicional
        jogador.vida -= 20
        

        
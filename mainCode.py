import pygame
import math
from player import Jogador, Bala
from enemy import Inimigo, Bullet
import sys
import os
import random
from itens import itemGeral, ParteEscudo, PowerUP, Moedas, Cura
from time import perf_counter
from loja import abrir_loja

folderPath = os.path.dirname(os.path.abspath(__file__))
pygame.init() 

clock = pygame.time.Clock()

bgHeight = 800
bgWidth = 1360
#tamanhoTela:tuple = pygame.display.get_desktop_sizes()[0]
telaSizePlaceholder = (bgWidth,bgHeight)
tela = pygame.display.set_mode(telaSizePlaceholder)
pygame.display.set_caption("nome do jogo") #alterar para o nome do jogo dps
fonte = pygame.font.SysFont("arial", 40, True, False)
fps=60

bg = pygame.image.load(os.path.join(folderPath,"images","placeholderBG.png")).convert()
bg = pygame.transform.scale(bg, (bgWidth,bgHeight))
bgSize = bg.get_rect()

scroll=0
tiles = math.ceil(bgHeight/bg.get_height())+2

deltaTime = clock.tick(60)/1000

jogador = Jogador(
        spriteImage=os.path.join(folderPath,'images', 'playerSprites', 'slime_green.png'),
        posInicial=(1360 / 2, 600),
        dt=deltaTime
        #grupos=self.all_sprites,
        #game=self
    )

createItem = 999

create_escudo = pygame.USEREVENT + 1
pygame.time.set_timer(create_escudo, 4000)
create_powerup = pygame.USEREVENT + 2
pygame.time.set_timer(create_powerup, 6000)

timerItem = pygame.time.set_timer(createItem, 3000)

create_Moeda = pygame.USEREVENT + 3
pygame.time.set_timer(create_Moeda, 4000)
create_Cura = pygame.USEREVENT + 4
pygame.time.set_timer(create_Cura, 6000)

#cria grupos
grupoItem = pygame.sprite.Group()
grupoEscudo = pygame.sprite.Group()
grupoPowerUP = pygame.sprite.Group()
grupoCura = pygame.sprite.Group()
grupoMoeda = pygame.sprite.Group()
grupoBala = pygame.sprite.Group()
grupoJogador = pygame.sprite.Group()
grupoInimigo = pygame.sprite.Group()
grupoBullets = pygame.sprite.Group()

main = True
enemy01 = Inimigo(0, deltaTime, pos=(670, 200), velocidade=(500, 500), vida=200, limites_mov=(500, 1000, 200, 600), sentido_inicial="0", tipo_bala = "follow", dDisparo=3)
enemy02 = Inimigo(1, deltaTime, pos=(600, 200), velocidade=(300, 0), vida=300, limites_mov=(200, 1000, 200, 200), sentido_inicial="R", tipo_bala="rajada", dDisparo=5)
enemy03 = Inimigo(2, deltaTime, pos=(1200, 400), velocidade=(0, 200), vida =100, limites_mov=(1000, 1000, 200, 600), sentido_inicial="L", tipo_bala="bigger", dDisparo=10)


#Novas variáveis do tiro:
inicio_de_jogo = perf_counter ()

# qtd. moedas inicial
jogador.moedas = 0

cooldown_normal = 0.35
cooldown_especial = 0.15
intervalo_tiro = cooldown_normal
ultimo_tiro = 0
powerup_ativo = False
powerup_t_inicio = 0
duracao =  5

#Mudei a criação dos personagens pra fora do loop main pra poder fazer com que o inimigo morre
#criar personagens
grupoJogador.add(jogador)
grupoInimigo.add(enemy01, enemy02, enemy03)
#grupoInimigo.add(enemy02)
    

while main:
    deltaTime = clock.tick(60)/1000
    if deltaTime>1.0:
        deltaTime=1.0
    #Salvar tecla apertada
    tecla = pygame.key.get_pressed()
    if len(grupoInimigo) == 0:
        enemy01 = Inimigo(0, deltaTime, pos=(670, 200), velocidade=(500, 500), vida=200, limites_mov=(500, 1000, 200, 600), sentido_inicial="0", tipo_bala = "follow", dDisparo=3)
        enemy02 = Inimigo(1, deltaTime, pos=(600, 200), velocidade=(300, 0), vida=300, limites_mov=(200, 1000, 200, 200), sentido_inicial="R", tipo_bala="rajada", dDisparo=5)
        enemy03 = Inimigo(2, deltaTime, pos=(1200, 400), velocidade=(0, 200), vida =100, limites_mov=(1000, 1000, 200, 600), sentido_inicial="L", tipo_bala="bigger", dDisparo=10)
    
    #vida    
    hp = f"Vida: {jogador.vida}"
    hp_form = fonte.render(hp, False, (255, 255, 255))

    #HUD do escudo
    pedacos = f"Pedaços: {jogador.escudo}/4"
    pedacos_form = fonte.render(pedacos, False, (100,180,255))
    #HUD do escudo
    escudos = f"Escudo: {jogador.armadura}"
    escudos_form = fonte.render(escudos, False, (100,180,255))
    
    coin = f"Moedas : {jogador.moedas}"
    coin_form = fonte.render(coin, False, (255, 255, 255))

    #HUD do tempo 
    tempo_de_jogo = perf_counter () - inicio_de_jogo
    timer = fonte.render(f"{tempo_de_jogo:.1f}s", False, (255, 255, 255))
    rect_timer = timer.get_rect()
    rect_timer.center = (680, 50)

    #HUD de kills
    kills = f"Kills: {jogador.kills}"
    kills_form = fonte.render(kills, False, (255, 255, 255))

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
#Criar o escudo:
        if event.type == create_escudo:
            if jogador.armadura < 100:
                if len(grupoEscudo) < 6:
                    print("escudo")
                    x = random.randint(200,1100)
                    y = random.randint(200,600)
                    escudoSpawnado = ParteEscudo(
                        spriteImage=os.path.join(folderPath,'images', 'Items', 'Escudo.png'),
                        posInicial=(x, y))
                
                    grupoEscudo.add(escudoSpawnado)

#Criar o powerUP:
        if event.type == create_powerup:
            if len(grupoPowerUP) == 0:
                print("PowerUP")
                x = random.randint(200,1100)
                y = random.randint(200,600)
                powerupSpawnado = PowerUP(
                    spriteImage=os.path.join(folderPath,'images', 'Items', 'PoweUP.png'),
                    posInicial=(x, y),
                )
                grupoPowerUP.add(powerupSpawnado)
#cria cura
        if event.type == create_Cura:
            if len(grupoCura) < 4:
                x = random.randint(200,1100)
                y = random.randint(200,600)
                cura = Cura(
                    spriteImage=os.path.join(folderPath, 'images','items', 'heart pixel art 32x32.png'),
                    posInicial=(x, y)
            )
                grupoCura.add(cura)
#cria moeda
        if event.type == create_Moeda:
            if len(grupoMoeda) < 8:
                x = random.randint(200,1100)
                y = random.randint(200,600)
                moeda = Moedas(spriteImage=os.path.join(folderPath,'images','items', 'coin 2.png'),
                    posInicial=(x, y),)
                grupoMoeda.add(moeda)

        # Abrir loja usando a tecla "L"
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_l:
                powerup_ativo = abrir_loja(tela, clock, jogador, powerup_ativo)
                if powerup_ativo:
                    intervalo_tiro = cooldown_especial
                    powerup_t_inicio = perf_counter()
    #colisão player item
    pygame.sprite.spritecollide(jogador, grupoItem, True)
    
#Escudo coletado:
    escudo_coletados = []
    for pedacos in grupoEscudo:
        if jogador.hitbox.colliderect(pedacos.rect):
            escudo_coletados.append(pedacos)
            pedacos.kill()

    for i in escudo_coletados:
        jogador.escudo += 1
        if jogador.escudo >= 4:
            jogador.armadura += 25
            jogador.escudo = 0
        if jogador.armadura>100:
            jogador.armadura=100

#PowerUP coletado:
    powerup_coletados = []
    for powerup in grupoPowerUP:
        if jogador.hitbox.colliderect(powerup.rect):
            powerup_coletados.append(powerup)
            powerup.kill()
    if powerup_coletados:
        jogador.player_update("PU")
        powerup_t_inicio = perf_counter()
        intervalo_tiro = cooldown_especial

#Power UP ativado:
    if jogador.powerUp:
        tempo_passado = perf_counter() - powerup_t_inicio
        if tempo_passado >= 5: #dura 5 segundos
            jogador.player_update("PU")
            intervalo_tiro = cooldown_normal
            print("MUDOU ESSA CARALHA")

#curas coletado:
    cura_coletados = []
    for cura in grupoCura:
        if jogador.hitbox.colliderect(cura.rect):
            cura_coletados.append(cura)
            cura.kill()

    for i in cura_coletados:
        jogador.vida += 10
        if jogador.vida > 100:
            jogador.vida = 100

#moedas coletado:
    moeda_coletados = []
    for moeda in grupoMoeda:
        if jogador.hitbox.colliderect(moeda.rect):
            moeda_coletados.append(moeda)
            moeda.kill()

    for i in moeda_coletados:
        jogador.moedas+=1

    """
    #colisão player item
    colisoes = pygame.sprite.spritecollide(jogador, grupoItem, True)

    for item in colisoes:
        # identifica o tipo de item recebido
        if isinstance(item, Moedas):
            jogador.moedas += item.valor
            print('Moeda recebida')

        elif isinstance(item, Cura):
            jogador.vida += item.valor
    """

#background scrolling
    appender=0
    while(appender<tiles):
        tela.blit(bg, (0, -bg.get_height()*appender+scroll))
        appender+=1
    scroll+=6
#reset scrolling
    if abs(scroll)>bg.get_height():
        scroll=0
        
#Colocar as novas HUDs na tela:
    tela.blit(hp_form, (18, 18))
    tela.blit(coin_form, (200, 18))
    tela.blit(pedacos_form, (18, 68))
    tela.blit(escudos_form, (18, 108))
    tela.blit(timer, rect_timer)
    tela.blit(kills_form, (1200, 18))

    #Tiro do jogador 
    if tecla[pygame.K_SPACE]:
        if perf_counter() - ultimo_tiro >= intervalo_tiro:
            projetil = Bala(
                os.path.join(folderPath,"images","enemy","bullet.png"),jogador.rect.center,dt=deltaTime)

            projetil.dire = pygame.math.Vector2(0, -projetil.velocidade)

            grupoBala.add(projetil)

            ultimo_tiro = perf_counter()

    #checa os inimigos ativos para disparar
    for enemy in grupoInimigo:
        if enemy.disparo:
            if enemy.tipo_bala == "follow": 
                bullet = Bullet(
                    os.path.join(folderPath, "images", "enemy", "bullet.png"),
                    (enemy.rect.centerx,enemy.rect.centery),
                    dt=deltaTime,
                    tipo = "follow"
                )
                grupoBullets.add(bullet)
                bullet.direcao((jogador.rect.center), (enemy01.rect.center), pow)
            elif enemy.tipo_bala == "rajada":
                for pow in range(5):    
                    bullet = Bullet(
                        os.path.join(folderPath, "images", "enemy", "bullet.png"),
                        (enemy.rect.centerx,enemy.rect.centery),
                        dt=deltaTime,
                        tipo = "rajada",
                    )
                    grupoBullets.add(bullet)
                    bullet.direcao((jogador.rect.center), (enemy02.rect.center), pow)
            elif enemy.tipo_bala == "bigger":
                bullet = Bullet(
                    os.path.join(folderPath, "images", "enemy", "bullet.png"),
                    (enemy.rect.centerx,enemy.rect.centery),
                    dt=deltaTime,
                    tipo = "bigger"
                )
                grupoBullets.add(bullet)
                bullet.direcao((jogador.rect.center), (enemy.rect.center), pow)
            enemy.timer_disparo()
            



        elif perf_counter() - enemy.t_disparo >= enemy.dDisparo:
            enemy.timer_disparo()
                
            

        

    
    #update de tudo
    grupoJogador.update(deltaTime)
    grupoInimigo.update(deltaTime)
    grupoBullets.update(deltaTime)
    grupoBala.update(deltaTime)
    grupoPowerUP.update(deltaTime)
    grupoEscudo.update(deltaTime)
    grupoMoeda.update(deltaTime)
    grupoCura.update(deltaTime)
    #print(grupoBullets)
    
    #desenha tudo na tela
    #grupoJogador.draw(tela)
    #grupoItem.draw(tela)
    grupoInimigo.draw(tela)
    grupoBullets.draw(tela)
    grupoBala.draw(tela)
    grupoPowerUP.draw(tela)
    grupoEscudo.draw(tela) 
    grupoMoeda.draw(tela)
    grupoCura.draw(tela)
    

#Colisão do disparo do inimigo com a hitbox do player
    colisao_b = False
    for bala in grupoBullets:
        if jogador.hitbox.colliderect(bala.rect):
            bala.kill()
            colisao_b = True
#Colisão dos disparos do inimigo com a hitbox do player
    colisao_i = False
    for vilao in grupoInimigo:
        if jogador.hitbox.colliderect(enemy01.rect):
            colisao_i = True
    if (colisao_b or colisao_i) and not jogador.invencibilidade: #as variáveis ficam falsas até detectarem uma colisão, quando recebe um elemento, entra na condicional
        if jogador.armadura == 0:
            jogador.vida -= 20
        else:
            jogador.armadura -= 20
        jogador.player_update("D")
        t_invencibilidade = perf_counter()
        t_clicks = perf_counter()

    if not jogador.invencibilidade:
        grupoJogador.draw(tela)
        print("OK")
    else:
        if perf_counter() - t_clicks < jogador.tempoPiscar:
            grupoJogador.draw(tela)
        else:
            t_clicks = perf_counter()

    if jogador.invencibilidade and (perf_counter() - t_invencibilidade) >= 3:
        jogador.player_update("D")

    #Colisão tiro dos players com o inimigo e sua morte:
    #print(f"Inimigo: {enemy01.vida}")
   
    for enemy in grupoInimigo:
        colisao_inimigo = pygame.sprite.spritecollide(enemy, grupoBala, True)
        if colisao_inimigo:
            enemy.vida -= 20
            #print(f"Inimigo: {enemy01.vida}")
        if enemy.vida <= 0:
            enemy.kill()
            jogador.add_kill()

    #flip atualiza a tela
    pygame.display.update()
    pygame.display.flip()
    clock.tick(fps)
    print(f"INTERVALO DO TIRO ATUAL {intervalo_tiro}")


    

        

        
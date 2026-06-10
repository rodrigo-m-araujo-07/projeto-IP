import pygame
import os
import math

#tamanhoTela:tuple = pygame.display.get_desktop_sizes()[0]

clock = pygame.time.Clock()

class Jogador(pygame.sprite.Sprite):
    
    folderPath = os.path.dirname(os.path.abspath(__file__))

    tamanhoMapa = (1360,800)
    
    def __init__(self, spriteImage, posInicial, dt):
        
        super().__init__()
        
        self.deltaTime = dt
        self.images = []
        self.sheet = pygame.image.load(spriteImage).convert_alpha()
        sheetSize = self.sheet.get_rect()
        self.direction=pygame.math.Vector2()
        self.animacoes = self.fatiar_spritesheet(self.sheet)
        self.estadoAnimacao = "run"
        self.frameAtual = 0
        self.velocidade = 500
        self.image = self.animacoes["run"][2] #pygame.image.load(os.path.join(folderPath, "images", "playerSprites", "climb-0.png")).convert_alpha()
        self.rect = self.image.get_rect()
        #Criando a hitbox:
        self.hitbox = pygame.Rect(0, 0, 100, 100)
        self.rect.center = posInicial
        self.hitbox.center = posInicial
        self.posicao = pygame.math.Vector2(self.rect.center)
        self.vida = 100
        self.invencibilidade = False
        self.tempoPiscar = 0.5
        self.escudo = 0
        self.armadura = 0
        self.kills = 0
        self.powerUp = False
        
    
    def fatiar_spritesheet(self,sheet):
        larguraSprite=24
        alturaSprite=24
        animacoes = {"run":[]}
        for linha in range(3):
            for coluna in range(4):
                x = larguraSprite*coluna
                y = alturaSprite*linha
                sprite = sheet.subsurface(pygame.Rect(x,y, larguraSprite, alturaSprite))
                sprite = pygame.transform.scale(sprite, (240, 240))
                animacoes["run"].append(sprite)
                #print(animacoes), #print()

        ##print(animacoes)
        return animacoes
            
    def getDirection(self):
        moveKeys = pygame.key.get_pressed()
        self.direction.x = int(moveKeys[pygame.K_d]) - int(moveKeys[pygame.K_a])
        self.direction.y = int(moveKeys[pygame.K_s]) - int(moveKeys[pygame.K_w])
        #pelo jeito da erro se tentar normalizar um vetor (0,0)
        if self.direction != (0,0):
            self.direction = self.direction.normalize()
    
    def movimentacao(self, camera):
        #print("pos", self.posicao)
        #print("rect", self.rect)
        #print("camera", camera)
        nextPosX = self.posicao.x + self.direction.x * self.velocidade * self.deltaTime
        nextPosY = (self.posicao.y + self.direction.y * self.velocidade * self.deltaTime)# - 6 colocar movimentação padrão do player
        #print("nextPosX", nextPosX)
        #print("nextPosY", nextPosY)        
        if nextPosX >= self.rect[2]/3 and nextPosX <= (self.tamanhoMapa[0])-self.rect[2]/3:
            self.posicao.x = nextPosX
            self.rect.centerx = self.posicao.x
        #print("tamanho", tamanhoMapa)
        #print("tamanho+", tamanhoMapa[1]+camera.y)
        if nextPosY <= (self.tamanhoMapa[1])-self.rect[3]/4: #nextPosY >= self.rect[3]/4 and
            self.posicao.y = nextPosY+2
            self.rect.centery = self.posicao.y
        
        #Hitbox 2:
        self.hitbox.center = self.rect.center
    
    def player_update(self, tipo):
        self.image_update(tipo)
        if tipo == "D":
            if self.invencibilidade:
                self.invencibilidade = False
            else:
                self.invencibilidade = True
        ##print(self.invencibilidade)
        elif tipo == "PU":
            if self.powerUp:
                self.powerUp = False
            else: self.powerUp = True

    def image_update(self, tipo): #animação 2-default, animação 10-dano, animação 4-dano+PU, animação 6-PU
        if tipo == "D":    
            if self.invencibilidade:
                self.image = self.animacoes["run"][2]
            else:
                self.image = self.animacoes["run"][10]
                if self.powerUp:
                    self.image = self.animacoes["run"][4]
        elif tipo == "PU":
            if self.powerUp:
                self.image = self.animacoes["run"][2]
                #print("VOLTA NORMAL KRL")
            else:
                self.image = self.animacoes["run"][6]
            #if self.invencibilidade: seria p mudar tb se pegar o pu enquanto no dano --acho paia
                #self.image = self.animacoes["run"][4]

    def add_kill(self):
        self.kills += 1


    def update(self,dt,camera):
        self.deltaTime = dt
        self.getDirection()
        self.movimentacao(camera)
#Bala do player:
class Bala(pygame.sprite.Sprite):
    def __init__(self, image, posicao, dt):
        ##print("teste 1")
        super().__init__()
        self.dt = dt
        self.image = pygame.image.load(os.path.join(self.folderPath, "images", "enemy", "bullet.png")).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.centerx = posicao[0]
        self.rect.centery = posicao[1]
        self.image = pygame.transform.scale(self.image, (64, 64))
        self.rect = self.image.get_rect(center=posicao)
        self.posicao = pygame.math.Vector2(self.rect.centerx, self.rect.centery)
        self.velocidade = 600
        self.dire = pygame.math.Vector2(0, 0)
        
        
        
    def direcao(self, posA, posB):
        ##print(posA)
       # print()
       # print(posB)
        dx = (posA[0] - posB[0])
        dy = (posA[1] - posB[1])
        ang = (math.atan(dy/dx))
        cos = math.cos(ang)
        sin = math.sin(ang)
        if (dx <=0 and dy <= 0) or (dy >= 0 and dx<=0): #caso precise inverter alguma coordenada
            cos = -cos
            sin = -sin
        
        self.dire = pygame.math.Vector2(math.ceil(cos*self.velocidade), math.ceil(sin*self.velocidade))
        #if (dx, dy) != (0, 0):
          #  self.dire = self.dire.normalize()
       # print(), print(self.dire)

    def mov(self, camera):
        #print(self.dire)
        self.posicao.x += (self.dire.x - camera.x) * self.dt
        self.posicao.y += (self.dire.y - camera.y) *self.dt
        #print(self.fix_dir)
        self.rect.centerx = self.posicao.x
        self.rect.centery = self.posicao.y
        #print(self.rect.center)
        
        
    def update(self, dt, camera):
        self.mov(camera)
        self.dt = dt
        #self.dt = clock.tick(60)/1000
        #if self.dt>1.0:
        #    self.dt=1.0
        if self.rect.centerx >= 1360 or self.rect.centerx <= 0 or self.rect.centery <= 0 or self.rect.centery >= 800:
            self.kill()
            #print("Dead")
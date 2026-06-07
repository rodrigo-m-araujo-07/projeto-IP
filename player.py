import pygame
import numpy
import os

#tamanhoTela:tuple = pygame.display.get_desktop_sizes()[0]

clock = pygame.time.Clock()
folderPath = os.path.dirname(os.path.abspath(__file__))

class Jogador(pygame.sprite.Sprite):
    
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
        self.posicao = pygame.math.Vector2(self.rect.center)
        self.vida = 100
        self.invencibilidade = False
        self.tempoPiscar = 0.5
        self.escudo = 0
        
    
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
                print(animacoes), print()

        #print(animacoes)
        return animacoes
            
    def getDirection(self):
        moveKeys = pygame.key.get_pressed()
        self.direction.x = int(moveKeys[pygame.K_d]) - int(moveKeys[pygame.K_a])
        self.direction.y = int(moveKeys[pygame.K_s]) - int(moveKeys[pygame.K_w])
        #pelo jeito da erro se tentar normalizar um vetor (0,0)
        if self.direction != (0,0):
            self.direction = self.direction.normalize()
    
    def movimentacao(self):
        #print(self.direction)
        self.posicao.x += self.direction.x * self.velocidade * self.deltaTime
        self.posicao.y += self.direction.y * self.velocidade * self.deltaTime
        self.rect.centerx = self.posicao.x
        self.rect.centery = self.posicao.y
    
    def dano_update(self):
        self.image_update()
        if self.invencibilidade:
            self.invencibilidade = False
            
        else:
            self.invencibilidade = True
        print(self.invencibilidade)

    def image_update(self):
        if self.invencibilidade:
            self.image = self.animacoes["run"][2]
            print("vermelho")
        else:
            self.image = self.animacoes["run"][10]
            print("verde")


    def update(self,dt):
        self.deltaTime = dt
        self.getDirection()
        self.movimentacao()
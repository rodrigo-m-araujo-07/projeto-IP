import pygame
import numpy
import os

#tamanhoTela:tuple = pygame.display.get_desktop_sizes()[0]

clock = pygame.time.Clock()
folderPath = os.path.dirname(os.path.abspath(__file__))

class Jogador(pygame.sprite.Sprite):
    
    def __init__(self, spriteImage, posInicial):
        
        super().__init__()
        
        self.deltaTime = clock.tick(60)/1000
        self.images = []
        self.sheet = pygame.image.load(spriteImage).convert_alpha()
        sheetSize = self.sheet.get_rect()
        self.direction=pygame.math.Vector2()
        self.animacoes = self.fatiar_spritesheet(self.sheet)
        self.estadoAnimacao = "run"
        self.frameAtual = 0
        self.velocidade = 200
        self.image = self.animacoes["run"][2] #pygame.image.load(os.path.join(folderPath, "images", "playerSprites", "climb-0.png")).convert_alpha()
        self.rect = self.image.get_rect()
        self.posicao = pygame.math.Vector2(self.rect.center)
        
    
    def fatiar_spritesheet(self,sheet):
        larguraSprite=24
        alturaSprite=24
        animacoes = {"run":[]}
        for linha in range(2):
            for coluna in range(3):
                x = larguraSprite*coluna
                y = alturaSprite*linha
                sprite = sheet.subsurface(pygame.Rect(x,y, larguraSprite, alturaSprite))
                sprite = pygame.transform.scale(sprite, (240, 240))
                animacoes["run"].append(sprite)
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
    
    def update(self):
        self.deltaTime = clock.tick(60)/1000
        self.getDirection()
        self.movimentacao()
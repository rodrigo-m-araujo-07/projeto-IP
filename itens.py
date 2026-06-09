import pygame
import sys
import os

folderPath = os.path.dirname(os.path.abspath(__file__))

class itemGeral(pygame.sprite.Sprite):
    
    def __init__(self, spriteImage, posInicial):
        super().__init__()
        self.sheet = pygame.image.load(spriteImage).convert_alpha()
        self.direction=pygame.math.Vector2()
        self.animacoes = self.fatiar_spritesheet(self.sheet)
        self.estadoAnimacao = "blink"
        self.frameAtual = 0
        self.image = self.animacoes["blink"][0].convert_alpha()
        self.rect = self.image.get_rect()
        self.posicao = pygame.math.Vector2(self.rect.center)
        self.dt=0
        
        #setting spawn pos
        self.posicao.x = posInicial[0]
        self.posicao.y = posInicial[1]
        self.rect.centerx = self.posicao.x
        self.rect.centery = self.posicao.y
        
    def fatiar_spritesheet(self,sheet):
        larguraSprite=16
        alturaSprite=16
        animacoes = {"blink":[]}
        for linha in range(1):
            for coluna in range(1):
                x = larguraSprite*coluna
                y = alturaSprite*linha
                sprite = sheet.subsurface(pygame.Rect(x,y, larguraSprite, alturaSprite))
                sprite = pygame.transform.scale(sprite, (256, 256))
                animacoes["blink"].append(sprite)
        return animacoes
    
    def movimentacao(self, camera):
        self.posicao.y+=500*self.dt
        self.rect.centerx = self.posicao.x
        self.rect.centery = self.posicao.y
        
    def update(self, dt, camera):
        self.dt = dt
        self.movimentacao(camera)
        

class ParteEscudo(itemGeral):
    def __init__(self, spriteImage, posInicial):
        super().__init__(spriteImage, posInicial)
        self.image = pygame.image.load(spriteImage).convert_alpha()
        self.image = pygame.transform.scale(self.image, (64, 64))
        self.rect = self.image.get_rect(center=posInicial)

class PowerUP(itemGeral):
    def __init__(self, spriteImage, posInicial):
        super().__init__(spriteImage, posInicial)
        self.image = pygame.image.load(spriteImage).convert_alpha()
        self.image = pygame.transform.scale(self.image, (64, 64))
        self.rect = self.image.get_rect(center=posInicial)

class Moedas(itemGeral):
    def __init__(self, spriteImage, posInicial):
        super().__init__(spriteImage, posInicial)
        self.image = pygame.image.load(spriteImage).convert_alpha()
        self.image = pygame.transform.scale(self.image, (64, 64))
        self.rect = self.image.get_rect(center=posInicial)
        self.valor = 1

class Cura(itemGeral):
    def __init__(self, spriteImage, posInicial):
        super().__init__(spriteImage, posInicial)
        self.image = pygame.image.load(spriteImage).convert_alpha()
        self.image = pygame.transform.scale(self.image, (64, 64))
        self.rect = self.image.get_rect(center=posInicial)
        self.valor = 10
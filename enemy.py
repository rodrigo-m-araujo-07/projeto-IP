import pygame
import os
from random import randint


folderPath = os.path.dirname(os.path.abspath(__file__))

class Inimigo(pygame.sprite.Sprite):
    def __init__(self, image, pos_inicial):
        
        super().__init__()

        self.image = pygame.image.load(os.path.join(folderPath, "images", "enemy", "retangulo_vermelho.png")).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.centerx = 500
        self.rect.centery = 200
        self.velocidade = 10
        self.direcao = pygame.Vector2()
        self.posicao = pygame.Vector2(self.rect.centerx, self.rect.centery)
        

    def dir(self):
        """"keys = pygame.key.get_pressed()
        if keys[pygame.K_l]:
            self.posicao.x += self.velocidade
        if keys[pygame.K_j]:
            self.posicao.x -= self.velocidade
        if keys[pygame.K_k]:
            self.posicao.y += self.velocidade
        if keys[pygame.K_i]:
            self.posicao.y += self.velocidade

        print(self.posicao)"""

        if self.posicao.y == (200): #and self.posicao.x not in (500, 1000):
            self.posicao.x += self.velocidade
        if self.posicao.y == 600: #and self.posicao.x not in (500, 1000):
            self.posicao.x -= self.velocidade
        if self.posicao.x == 500: #and self.posicao.y not in (200, 600):
            self.posicao.y -= self.velocidade
        if self.posicao.x == 1000: #and self.posicao.y not in (200, 600):
            self.posicao.y += self.velocidade


    def update(self):
        self.dir()
        self.rect.centerx = self.posicao.x
        self.rect.centery = self.posicao.y

        
        
        """self.direcao.x = int(keys[pygame.K_d]) - int(keys[pygame.K_a])
        self.direcao.y = int(keys[pygame.K_s]) - int(keys[pygame.K_w])
        if self.direcao != (0, 0):
            self.direcao = self.direcao.normalize()"""
        

class Bullet(Inimigo):
    def __init__(self, image, pos):
        super().__init__()

        self.image = pygame.image.load(os.path.join(folderPath, "imagens", "enemy", "bullet.png")).convert_alpha()
        self.posicao = pygame.Vector2(super().posicao.x, super().posicao.y)

    def atirar(self):
        
        


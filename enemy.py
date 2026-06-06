import pygame
import os
import math #para deixar o código mais claro durante as operações matemáticas


folderPath = os.path.dirname(os.path.abspath(__file__))

class Inimigo(pygame.sprite.Sprite):
    def __init__(self, image):
        
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

        if self.posicao.y == 200: #and self.posicao.x not in (500, 1000):
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
        

class Bullet(pygame.sprite.Sprite):
    def __init__(self, image, posicao):
        super().__init__()
        self.image = pygame.image.load(os.path.join(folderPath, "images", "enemy", "bullet.png")).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.centerx = posicao[0]
        self.rect.centery = posicao[1]
        self.posicao = pygame.math.Vector2(self.rect.centerx, self.rect.centery)
        self.velocidade = 10
        


    def direcao(self, posA, posB):
        #print(posA)
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

    def mov(self):
        print(self.dire)
        self.posicao.x += self.dire.x 
        self.posicao.y += self.dire.y 
        #print(self.fix_dir)
        self.rect.centerx = self.posicao.x
        self.rect.centery = self.posicao.y
        print(self.rect.center)

        
    def update(self):
        self.mov()
        if self.rect.centerx >= 1360 or self.rect.centerx <= 0 or self.rect.centery <= 0 or self.rect.centery >= 800:
            self.kill()
            print("Dead")
        
        


        
        


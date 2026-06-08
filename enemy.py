import pygame
import os
import math #para deixar o código mais claro durante as operações matemáticas
clock = pygame.time.Clock()

folderPath = os.path.dirname(os.path.abspath(__file__))

imagens = ("retangulo_vermelho.png", "hexagono_amarelo2.png")
class Inimigo(pygame.sprite.Sprite):
    def __init__(self, i, dt, pos, velocidade, vida, limites_mov, sentido_inicial):
        
        super().__init__()
        self.dt = dt
        self.image = pygame.image.load(os.path.join(folderPath, "images", "enemy", imagens[i])).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.centerx = pos[0]
        self.rect.centery = pos[1]
        self.velocidadex = velocidade[0]
        self.velocidadey = velocidade[1]
        self.direcao = pygame.Vector2()
        self.posicao = pygame.Vector2(self.rect.centerx, self.rect.centery)
        self.vida = vida
        self.limites_mov = limites_mov #padrão --> (x0, x1, y0, y1)
        self.sentido_inicial = sentido_inicial


    def _mudar_sentido(self):
        if self.sentido_inicial == "R":
            self.sentido_inicial = "L"
        elif self.sentido_inicial == "L":
            self.sentido_inicial = "R"
        

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
        
        #print(self.posicao)
        if self.velocidadex != 0 and self.velocidadey!=0:
            if self.posicao.y <= self.limites_mov[2] and self.posicao.x <= self.limites_mov[1]:
                self.posicao.x += self.velocidadex * self.dt
            elif self.posicao.y >= self.limites_mov[3] and self.posicao.x >= self.limites_mov[0]:
                self.posicao.x -= self.velocidadex * self.dt
            elif self.posicao.x <= self.limites_mov[0] and self.posicao.y >= self.limites_mov[2]:
                self.posicao.y -= self.velocidadey * self.dt
            elif self.posicao.x >= self.limites_mov[1] and self.posicao.y <= self.limites_mov[3]:
                self.posicao.y += self.velocidadey * self.dt

        elif self.velocidadex != 0:
            if self.posicao.x >= self.limites_mov[1]:
                self._mudar_sentido()
            elif self.posicao.x <= self.limites_mov[0]:
                self._mudar_sentido()
            
            if self.sentido_inicial == "R":
                self.posicao.x += self.velocidadex * self.dt
            elif self.sentido_inicial == "L":
                self.posicao.x -= self.velocidadex * self.dt

        elif self.velocidadey != 0:
            if self.posicao.y >= self.limites_mov[1]:
                self._mudar_sentido()
            elif self.posicao.y <= self.limites_mov[0]:
                self._mudar_sentido()
            
            if self.sentido_inicial == "R":
                self.posicao.y += self.velocidadex * self.dt
            elif self.sentido_inicial == "L":
                self.posicao.y -= self.velocidadex * self.dt



    def update(self, dt):
        self.dir()
        self.dt = dt
        self.rect.centerx = self.posicao.x
        self.rect.centery = self.posicao.y

        
        
        """self.direcao.x = int(keys[pygame.K_d]) - int(keys[pygame.K_a])
        self.direcao.y = int(keys[pygame.K_s]) - int(keys[pygame.K_w])
        if self.direcao != (0, 0):
            self.direcao = self.direcao.normalize()"""
        

class Bullet(pygame.sprite.Sprite):
    def __init__(self, image, posicao, dt):
        #print("teste 1")
        super().__init__()
        self.dt = dt
        self.image = pygame.image.load(os.path.join(folderPath, "images", "enemy", "bullet.png")).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.centerx = posicao[0]
        self.rect.centery = posicao[1]
        self.posicao = pygame.math.Vector2(self.rect.centerx, self.rect.centery)
        self.velocidade = 600
        


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
        #print(self.dire)
        self.posicao.x += self.dire.x * self.dt
        self.posicao.y += self.dire.y *self.dt
        #print(self.fix_dir)
        self.rect.centerx = self.posicao.x
        self.rect.centery = self.posicao.y
        #print(self.rect.center)

        
    def update(self, dt):
        self.mov()
        self.dt = dt
        #self.dt = clock.tick(60)/1000
        #if self.dt>1.0:
        #    self.dt=1.0
        if self.rect.centerx >= 1360 or self.rect.centerx <= 0 or self.rect.centery <= 0 or self.rect.centery >= 800:
            self.kill()
            print("Dead")
        
        


        
        


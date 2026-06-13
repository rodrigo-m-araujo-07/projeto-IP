import pygame
import os
import math #para deixar o código mais claro durante as operações matemáticas
#from time import perf_counter
clock = pygame.time.Clock()
inimigos_data = {
            0: {"imagem" : "retangulo_vermelho.png", "velocidade" :(700, 250), "vida" : 200, "bala" : "follow"}, 
            1: {"imagem" : "hexagono_amarelo2.png", "velocidade" : (300, 250), "vida": 300, "bala": "rajada"},
            2: {"imagem" : "quadrado_roxo.png", "velocidade": (800, 200), "vida": 100, "bala": "bigger"},
            3 :{"imagem" : "retangulo_cinza.png", "velocidade": (500, 200), "vida": 250, "bala": "tracker"}
            }

class Inimigo(pygame.sprite.Sprite):
    
    def __init__(self, i, dt, pos, limites_mov, sentido_inicial):
        
        super().__init__()
        folderPath = os.path.dirname(os.path.abspath(__file__))
        
        self.dt = dt
        self.image = pygame.image.load(os.path.join(folderPath, "images", "enemy", inimigos_data[i]["imagem"])).convert_alpha()
        #print(self.imagens[i])
        self.rect = self.image.get_rect()
        #print(self.rect)
        self.rect.centerx = pos[0]
        self.rect.centery = pos[1]
        self.velocidadex = inimigos_data[i]["velocidade"][0]
        self.velocidadey = inimigos_data[i]["velocidade"][1]
        self.direcao = pygame.Vector2()
        self.posicao = pygame.Vector2(self.rect.centerx, self.rect.centery)
        self.vida = inimigos_data[i]["vida"]
        self.limites_mov = limites_mov #padrão --> (x0, x1)
        self.sentido_inicial = sentido_inicial
        self.tipo_bala = inimigos_data[i]["bala"]
        self.disparo = 1
        #self.dDisparo = dDisparo #intervalo entre os disparos
        #self.t_disparo = 0

    """def timer_disparo(self):
        self.t_disparo = perf_counter()
        if self.disparo == 0:
            self.disparo = 1
        else:
            self.disparo = 0"""
    

    def _mudar_sentido(self):
        if self.sentido_inicial == "R":
            self.sentido_inicial = "L"
        elif self.sentido_inicial == "L":
            self.sentido_inicial = "R"
        

    def dir(self):
        
        ##print(self.posicao) #trocar isso aqui por um timer fixo (subir por x segundos, direita por y segundos, etc)
        #if self.velocidadex != 0 and self.velocidadey!=0:
        if self.posicao.x >= self.limites_mov[1]:
            self._mudar_sentido()
        elif self.posicao.x <= self.limites_mov[0]:
            self._mudar_sentido()

        if self.sentido_inicial == "R":
            self.posicao.x += self.velocidadex * self.dt
        elif self.sentido_inicial == "L":
            self.posicao.x -= self.velocidadex * self.dt
        
        self.posicao.y -= self.velocidadey * self.dt

        """elif self.velocidadex != 0:
            if self.posicao.x >= self.limites_mov[1]:
                self._mudar_sentido()
            elif self.posicao.x <= self.limites_mov[0]:
                self._mudar_sentido()
            
            if self.sentido_inicial == "R":
                self.posicao.x += self.velocidadex * self.dt
            elif self.sentido_inicial == "L":
                self.posicao.x -= self.velocidadex * self.dt"""

        """elif self.velocidadey != 0:
            if self.posicao.y >= self.limites_mov[3]:
                self._mudar_sentido()
            elif self.posicao.y <= self.limites_mov[2]:
                self._mudar_sentido()

            if self.sentido_inicial == "R":
                self.posicao.y += self.velocidadey * self.dt
            elif self.sentido_inicial == "L":
                self.posicao.y -= self.velocidadey * self.dt"""
                #print("DESCE CARALHO PORRA")

            #print(f"POSICAO DESSE CORNO {self.posicao}")



    def update(self, dt, camera):
        self.dir()
        self.dt = dt
        print("camera", camera.y)
        self.posicao.y -= camera.y
        self.rect.centerx = self.posicao.x - camera.x
        self.rect.centery = self.posicao.y
        
        """self.direcao.x = int(keys[pygame.K_d]) - int(keys[pygame.K_a])
        self.direcao.y = int(keys[pygame.K_s]) - int(keys[pygame.K_w])
        if self.direcao != (0, 0):
            self.direcao = self.direcao.normalize()"""
        

class Bullet(pygame.sprite.Sprite):
    
    def __init__(self, image, posicao, dt, tipo):
        folderPath = os.path.dirname(os.path.abspath(__file__))
        velocidades = {"follow": 600, "rajada": 500, "bigger": 400, "tracker": 300}
        #print("teste 1")
        super().__init__()
        self.dt = dt
        self.image = pygame.image.load(os.path.join(folderPath, "images", "enemy", "bullet.png")).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.centerx = posicao[0]
        self.rect.centery = posicao[1]
        self.image = pygame.transform.scale(self.image, (64, 64))
        self.rect = self.image.get_rect(center=posicao)
        self.posicao = pygame.math.Vector2(self.rect.centerx, self.rect.centery)
        self.velocidade = velocidades[tipo]
        self.disparo = 1
        self.tipo = tipo
        


    def direcao(self, posA, posB, pow):
        dx = (posA[0] - posB[0])
        dy = (posA[1] - posB[1])
        
        if self.tipo == "follow" or self.tipo == "bigger" or self.tipo == "tracker":
            if dx !=0: #para evitar divisao por zero    
                ang = (math.atan(dy/dx))
            else:
                ang = (math.pi)/2
            cos = math.cos(ang)
            sin = math.sin(ang)
            if (dx <=0 and dy <= 0) or (dy >= 0 and dx<=0): #caso precise inverter alguma coordenada
                cos = -cos
                sin = -sin
            self.dire = pygame.math.Vector2((cos*self.velocidade), (sin*self.velocidade))
    
        if self.tipo == "rajada":
            if dy <0:
                dy = -dy
            #print(pow)
            indicies = {"b0" : (0, -posB[0]), "b1" : (posB[0], 0), "b2" : (-posB[0], 0), "b3":(0, posB[0]), "b4" :(118, 96), "b5": (118, -96), "b6": (-118, 96), "b7" :(-118, -96)}
            if pow not in (0, 3):
                ang = math.atan(indicies[f"b{pow}"][1]/indicies[f"b{pow}"][0])
            else:
              ang = (math.pi)/2
            cos = math.cos(ang)
            sin = math.sin(ang)
            if pow in (0, 2, 5, 7): #correcao para os valores do cosseno negativo
                cos = -cos
            """if sin<0:  #correcao para o seno, para ele sempre atirar p baixo 
                sin = -sin"""
            self.dire = pygame.math.Vector2((cos*self.velocidade), (sin*self.velocidade))
            #print("AQUI porra"),print(self.dire)


    def mov(self, camera):
        #if self.tipo == "follow":    
            #print(self.dire)
            self.posicao.x += (self.dire.x) * self.dt
            self.posicao.y += (self.dire.y) *self.dt
            #atualiza a posicao atual
            self.rect.centerx = self.posicao.x
            self.rect.centery = self.posicao.y
            
            #caso especial do bigger
            
            if self.tipo == "bigger":
                #print("aumenta")
                deltax = int(self.rect.bottomright[0] - self.rect.bottomleft[0])
                deltay = int(math.fabs(self.rect.bottomleft[1] - self.rect.topleft[1]))
                if deltax < 300 and deltay < 300:    
                    self.image = pygame.transform.scale(self.image, (int(deltax*1.02), int(deltay*1.02)))
                    self.rect = self.rect.scale_by(1.02, 1.02)


    def mudar_disparo(self):
        if self.disparo == 0:
            self.disparo =1
        else:
            self.disparo =0

    def update(self, dt, camera, playerPos, mudar):
        self.mov(camera)
        self.dt = dt
        if abs(playerPos.x-self.posicao.x) >= 3000 or abs(playerPos.y-self.posicao.y) >= 3000:
            self.kill()
            #print("Dead")
        if self.tipo == "tracker" and mudar:
            self.direcao(playerPos, self.posicao, pow="null")
        
        


        
        


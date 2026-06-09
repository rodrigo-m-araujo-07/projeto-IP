import pygame
import sys
import os

# ==========================================
# 1. CONFIGURAÇÕES INICIAIS E JANELA
# ==========================================
pygame.init()
LARGURA, ALTURA = 800, 600
tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Lojinha de itens - Cura, Escudo e PowerUP")
relogio = pygame.time.Clock()

# Cores (RGB)
BRANCO    = (255, 255, 255)
PRETO     = (0, 0, 0)
VERDE     = (46, 204, 113)
VERMELHO  = (231, 76, 60)
LARANJA   = (255, 165, 0) 
AZUL      = (91, 124, 153)
ROSA      = (252,15,192)
CINZA     = (240, 240, 240)
BORDA_CD  = (189, 195, 199)

# Fontes
fonte_texto = pygame.font.SysFont("Arial", 20, bold=True)
fonte_preco = pygame.font.SysFont("Arial", 22, bold=True)
fonte_titulo = pygame.font.SysFont("Arial", 45, bold=True)
fonte_status = pygame.font.SysFont("Arial", 20)

# ==========================================
# 2. ATRIBUTOS DO JOGADOR (STATUS)
# ==========================================
moedas = 200          # TEM QUE ARRUMAR DE ACORDO COM O RESTO DO CODIGO
vida_jogador = 50     # TEM QUE ARRUMAR DE ACORDO COM O RESTO DO CODIGO
escudo_jogador = 0    # TEM QUE ARRUMAR DE ACORDO COM O RESTO DO CODIGO
powerup_ativo = False     # TEM QUE ARRUMAR DE ACORDO COM O RESTO DO CODIGO

# Mensagem de feedback na tela
mensagem_feedback = "Bem-vindo à loja! Clique em um item para comprar."

# ==========================================
# 3. CARREGAMENTO E AJUSTE DAS IMAGENS
# ==========================================

# Imagens do itens
DIRETORIO_LOJA = os.path.dirname(__file__)

caminho_moeda = os.path.join(DIRETORIO_LOJA,'images', 'Items', "coin 2.png")
caminho_cura = os.path.join(DIRETORIO_LOJA,'images', 'Items', "heart pixel art 32x32.png")
caminho_escudo = os.path.join(DIRETORIO_LOJA,'images', 'Items', "Escudo.png")
caminho_powerup = os.path.join(DIRETORIO_LOJA,'images', 'Items', "PoweUP.png")

img_moeda = pygame.image.load(caminho_moeda).convert_alpha()
img_cura = pygame.image.load(caminho_cura).convert_alpha()      
img_escudo = pygame.image.load(caminho_escudo).convert_alpha()  
img_powerup = pygame.image.load(caminho_powerup).convert_alpha()

# Alinhamento para que todas as imagens fiquem no tamanho certo para a interface
img_moeda = pygame.transform.scale(img_moeda, (25, 25))
img_cura = pygame.transform.scale(img_cura, (90, 90))
img_escudo = pygame.transform.scale(img_escudo, (90, 90))
img_powerup = pygame.transform.scale(img_powerup, (90, 90))

# ==========================================
# 4. ESTRUTURA DOS ITENS DA LOJA 
# ==========================================
# Cada item tem seu retângulo (rect) que define sua posição X, Y, largura e altura na tela
loja_itens = {
    "cura": {
        "nome": "Cura","preco": 25, 
        "img": img_cura, 
        "rect": pygame.Rect(130, 220, 140, 200)
    },
    "escudo": {
        "nome": "Escudo", 
        "preco": 40, 
        "img": img_escudo, 
        "rect": pygame.Rect(330, 220, 140, 200)
    },
    "powerup": {
        "nome": "PowerUP", 
        "preco": 60, 
        "img": img_powerup, 
        "rect": pygame.Rect(530, 220, 140, 200)
    }
}

# ==========================================
# 5. LOOP PRINCIPAL DA LOJA
# ==========================================
rodando = True
while rodando:
    tela.fill(LARANJA)
    
    # Gerenciador das compras 
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False
            pygame.quit()
            sys.exit()
            
        # Detectar se o jogador clicou com o botão esquerdo do mouse
        if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
            pos_mouse = pygame.mouse.get_pos()
            
            # Verificar se comprou algum item
            for id_item, dados in loja_itens.items():
                if dados["rect"].collidepoint(pos_mouse):
                    
                    # 1. Checa se o jogador tem moedas suficientes
                    if moedas >= dados["preco"]:
                        
                        # Lógica específica para cada item comprado
                        if id_item == "cura":
                            if vida_jogador >= 100:
                                mensagem_feedback = "Vida já está cheia!"
                            else:
                                moedas -= dados["preco"]
                                vida_jogador = min(100, vida_jogador + 10) # Cura 10, limite de 100
                                mensagem_feedback = "Você comprou Cura! +10 de Vida."
                                
                        elif id_item == "escudo":
                            if vida_jogador >= 100 and escudo_jogador == 3:
                                mensagem_feedback = "Não é possivel completar os escudos com a vida cheia!"
                            else:
                                moedas -= dados["preco"]
                                escudo_jogador += 1
                                if escudo_jogador >= 4:
                                    vida_jogador += 25
                                    escudo_jogador = 0
                                if vida_jogador>100:
                                    vida_jogador=100
                                mensagem_feedback = "Você comprou Escudo!"
                            
                        elif id_item == "powerup":#TEM QUE AJUSTAR PARA CASO DE COMPRAR VARIOS
                            moedas -= dados["preco"]
                            powerup_ativo = True
                            mensagem_feedback = "PowerUP ativado!"
                    else:
                        mensagem_feedback = "Moedas insuficientes para comprar este item!"

    # ==========================================
    # 6. RENDERIZAÇÃO DA INTERFACE GRÁFICA (HUD)
    # ==========================================
    
    # Título Principal
    txt_titulo = fonte_titulo.render("LOJA DE ITENS", True, PRETO)
    tela.blit(txt_titulo, (LARGURA // 2 - txt_titulo.get_width() // 2, 40))
    
    # Caixa de Feedback (Mensagens sobre a compra)
    txt_feed = fonte_status.render(mensagem_feedback, True, PRETO)
    tela.blit(txt_feed, (LARGURA // 2 - txt_feed.get_width() // 2, 120))
    
    # --- Painel de Status do Jogador (Canto Superior Direito) ---
    # Mostrar Moedas
    tela.blit(img_moeda, (630, 30))
    txt_moedas = fonte_texto.render(f"Moedas: {moedas}", True, PRETO)
    tela.blit(txt_moedas, (665, 32))
    
    # Mostrar Status Atuais (Vida, Escudo, Dano)
    txt_vida = fonte_status.render(f"Vida Atual: {vida_jogador}/100", True, VERMELHO)
    txt_esc = fonte_status.render(f"Escudo Atual: {escudo_jogador}", True, AZUL)
    txt_dano = fonte_status.render(f"PowerUP ativo: {powerup_ativo}", True, ROSA)#AJUSTAR
    
    tela.blit(txt_vida, (30, 30))
    tela.blit(txt_esc, (30, 55))
    tela.blit(txt_dano, (30, 80))
    
    # --- Desenho dos Cards dos Itens ---
    for id_item, dados in loja_itens.items():
        rect = dados["rect"]
        
        # Desenhar o fundo do card (Retângulo cinza com bordas arredondadas)
        pygame.draw.rect(tela, CINZA, rect, border_radius=12)
        # Linha de contorno do card
        pygame.draw.rect(tela, BORDA_CD, rect, width=2, border_radius=12)
        
        # Desenhar a Imagem do Item centralizada no card
        img_x = rect.x + (rect.width - dados["img"].get_width()) // 2
        tela.blit(dados["img"], (img_x, rect.y + 20))
        
        # Desenhar o Nome do Item
        txt_nome = fonte_texto.render(dados["nome"], True, PRETO)
        nome_x = rect.x + (rect.width - txt_nome.get_width()) // 2
        tela.blit(txt_nome, (nome_x, rect.y + 125))
        
        # Desenhar o Preço do Item
        txt_preco = fonte_preco.render(f"${dados['preco']}", True, VERDE)
        preco_x = rect.x + (rect.width - txt_preco.get_width()) // 2
        tela.blit(txt_preco, (preco_x, rect.y + 155))

    # Atualiza a tela e trava a taxa de quadros em 60 FPS
    pygame.display.flip()
    relogio.tick(60)
import pygame
import sys
import os
from time import perf_counter
# ==========================================
# 1. CONFIGURAÇÕES INICIAIS E JANELA
# ==========================================

def abrir_loja(tela, relogio, jogador, powerup_ativo, bullet_time_ativo):
    tempo_de_entrada = perf_counter()

    LARGURA, ALTURA = tela.get_size()

    # Cores (RGB)
    BRANCO    = (255, 255, 255)
    PRETO     = (0, 0, 0)
    VERDE     = (46, 204, 113)
    VERMELHO  = (231, 76, 60)
    AMARELO = (255, 215, 0)
    LARANJA   = (255, 165, 0) 
    AZUL      = (91, 124, 153)
    ROSA      = (252,15,192)
    CINZA     = (240, 240, 240)
    BORDA_CD  = (189, 195, 199)

    # Fontes
    fonte_texto  = pygame.font.SysFont("Arial", 20, bold=True)
    fonte_preco  = pygame.font.SysFont("Arial", 22, bold=True)
    fonte_titulo = pygame.font.SysFont("Arial", 45, bold=True)
    fonte_status = pygame.font.SysFont("Arial", 20)

    # ==========================================
    # 2. ATRIBUTOS DO JOGADOR 
    # jogador.moedas   → moedas
    # jogador.vida     → vida
    # jogador.escudo   → pedaços de escudo (0-3)
    # jogador.armadura → barra de armadura (0-100)
    # powerup_ativo    → variável (True/False)
    # ==========================================

    # Mensagem de feedback na tela
    mensagem_feedback = "Bem-vindo à loja! Clique em um item para comprar."

    # ==========================================
    # 3. CARREGAMENTO E AJUSTE DAS IMAGENS
    # ==========================================
    DIRETORIO_LOJA = os.path.dirname(os.path.abspath(__file__))

    caminho_moeda  = os.path.join(DIRETORIO_LOJA, 'images', 'Items', "coin 2.png")
    caminho_cura   = os.path.join(DIRETORIO_LOJA, 'images', 'Items', "heart pixel art 32x32.png")
    caminho_escudo = os.path.join(DIRETORIO_LOJA, 'images', 'Items', "Escudo.png")
    caminho_powerup= os.path.join(DIRETORIO_LOJA, 'images', 'Items', "PoweUP.png")
    caminho_carga= os.path.join(DIRETORIO_LOJA, 'images', 'Items', "choque_do_trovao.png")

    img_moeda  = pygame.image.load(caminho_moeda).convert_alpha()
    img_cura   = pygame.image.load(caminho_cura).convert_alpha()
    img_escudo = pygame.image.load(caminho_escudo).convert_alpha()
    img_powerup= pygame.image.load(caminho_powerup).convert_alpha()
    img_carga= pygame.image.load(caminho_carga).convert_alpha()

    img_moeda  = pygame.transform.scale(img_moeda,  (25, 25))
    img_cura   = pygame.transform.scale(img_cura,   (90, 90))
    img_escudo = pygame.transform.scale(img_escudo, (90, 90))
    img_powerup= pygame.transform.scale(img_powerup,(90, 90))
    img_carga  = pygame.transform.scale(img_carga,(90, 90))

    # ==========================================
    # 4. ESTRUTURA DOS ITENS DA LOJA 
    # ==========================================
    CARD_W, CARD_H = 140, 200
    CARD_Y = ALTURA // 2 - CARD_H // 2          
    ESPACO = 60                                  
    total = 4 * CARD_W + 3 * ESPACO
    x0 = LARGURA // 2 - total // 2              
 
    loja_itens = {
        "cura": {
            "nome": "Cura", "preco": 10,
            "img": img_cura,
            "rect": pygame.Rect(x0, CARD_Y, CARD_W, CARD_H)
        },
        "escudo": {
            "nome": "Escudo", "preco": 5,
            "img": img_escudo,
            "rect": pygame.Rect(x0 + CARD_W + ESPACO, CARD_Y, CARD_W, CARD_H)
        },
        "powerup": {
            "nome": "Quick Shot", "preco": 15,
            "img": img_powerup,
            "rect": pygame.Rect(x0 + 2 * (CARD_W + ESPACO), CARD_Y, CARD_W, CARD_H)
        },
        "charge": {
            "nome": "Carga", "preco": 12,
            "img": img_carga,
            "rect": pygame.Rect(x0 + 3 * (CARD_W + ESPACO), CARD_Y, CARD_W, CARD_H)
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
                pygame.quit()
                sys.exit()

            # Fechar a loja com L ou ESC e voltar ao jogo
            if evento.type == pygame.KEYDOWN:
                if evento.key in (pygame.K_l, pygame.K_ESCAPE):
                    rodando = False

            # Detectar se o jogador clicou com o botão esquerdo do mouse
            if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                pos_mouse = pygame.mouse.get_pos()

                # Verificar se comprou algum item
                for id_item, dados in loja_itens.items():
                    if dados["rect"].collidepoint(pos_mouse):

                        # Checa se o jogador tem moedas suficientes
                        if jogador.moedas >= dados["preco"]:

                            # Lógica específica para cada item comprado
                            if id_item == "cura":
                                if jogador.vida >= 100:
                                    mensagem_feedback = "Vida já está cheia!"
                                else:
                                    jogador.moedas -= dados["preco"]
                                    jogador.vida = min(100, jogador.vida + 10) # Cura 10, limite de 100
                                    mensagem_feedback = "Você comprou Cura! +10 de Vida."

                            elif id_item == "escudo":
                                if jogador.armadura >= 100 and jogador.escudo == 3:
                                    mensagem_feedback = "Não é possivel completar os escudos com a armadura cheia!"
                                else:
                                    jogador.moedas -= dados["preco"]
                                    jogador.escudo += 1
                                    if jogador.escudo >= 4:
                                        jogador.armadura += 25
                                        jogador.escudo = 0
                                    if jogador.armadura > 100:
                                        jogador.armadura = 100
                                    mensagem_feedback = "Você comprou Escudo!"

                            elif id_item == "powerup":
                                if powerup_ativo:
                                    mensagem_feedback = "Quick Shot já está ativo!"
                                else:
                                    jogador.moedas -= dados["preco"]
                                    powerup_ativo = True
                                    mensagem_feedback = "Quick Shot ativado!"

                            elif id_item == "charge":
                                if bullet_time_ativo:
                                    mensagem_feedback = "Bullet Time já está ativo!"
                                elif jogador.charge == 5:
                                    mensagem_feedback = "Você vai sobrecarregar!"
                                else:
                                    jogador.moedas -= dados["preco"]
                                    jogador.charge += 1
                                    mensagem_feedback = "Carregado e preparado!"
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
        tela.blit(img_moeda, (LARGURA - 170, 30))
        txt_moedas = fonte_texto.render(f"Moedas: {jogador.moedas}", True, PRETO)
        tela.blit(txt_moedas, (LARGURA - 135, 32))
 
        # Mostrar Status Atuais (Vida, Escudo, Armadura, PowerUP)
        txt_vida = fonte_status.render(f"Vida Atual: {jogador.vida}/100",       True, VERMELHO)
        txt_esc  = fonte_status.render(f"Escudo: {jogador.escudo}/4 pedaços",   True, AZUL)
        txt_arm  = fonte_status.render(f"Armadura: {jogador.armadura}/100",     True, AZUL)
        txt_dano = fonte_status.render(f"Quick Shot ativo: {powerup_ativo}",       True, ROSA)
        txt_carga = fonte_status.render(f"Charges: {jogador.charge}/5",       True, AMARELO)
 
        tela.blit(txt_vida, (30, 30))
        tela.blit(txt_esc,  (30, 55))
        tela.blit(txt_arm,  (30, 80))
        tela.blit(txt_dano, (30, 105))
        tela.blit(txt_carga, (30, 125))
 
        # Instrução para fechar
        txt_fechar = fonte_status.render("Pressione L ou ESC para fechar a loja", True, PRETO)
        tela.blit(txt_fechar, (LARGURA // 2 - txt_fechar.get_width() // 2, ALTURA - 40))
 
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
    tempo_saida = perf_counter()
    tempo_pausado =  tempo_saida - tempo_de_entrada
 
    return powerup_ativo, tempo_pausado
from __future__ import annotations
import numpy as np
import pygame as pg
from pygame import time
from assets.button import Button
import time
from assets.consts import Consts
import numpy as np


class View:
    def __init__(self) -> None:
        """Inicia o componente View"""

        pg.init()
        self.clock: pg.time.Clock = pg.time.Clock()    # Inicia o Relógio
        self.display = pg.display.set_mode((1000, 550), 0, 32)    # Inicia o ecrã

        pg.display.update()    # Atualiza o ecrã
        time.sleep(0.01)
        self.display.fill((235,235,235))    # Preenche o ecrã com cor cinza claro

        self.close_button: Button = Button("#B8C6DB", 20, 30, 90, 55, 
                                   border_radius=50, text='fechar', font=Consts.button_font)    # Inicia o botão de fechar
        
        self.message: str = "Jogador Azul"
        pg.event.set_blocked([pg.MOUSEMOTION])
        
            
    def draw_board(self, pieces: np.ndarray) -> None:
        """Desenha as casas do tabuleiro e as peças no tabuleiro

        Args:
            pieces (ndarray): Array 2D representando as peças e suas posições no tabuleiro
        """
        pg.display.update()     # Atualiza o ecrã
        self.close_button.draw(self.display)    # Desenha o botão de fechar

        # Desenha o tabuleiro
        width = Consts.COLS * Consts.BLOCK_SIZE + (Consts.COLS - 1) * Consts.GAP    # Largura do tabuleiro real, NÃO DO ECRÃ
        height = Consts.ROWS * Consts.BLOCK_SIZE + (Consts.ROWS - 1) * Consts.GAP   # Altura do tabuleiro real, NÃO DO ECRÃ

        starting_x = 1000 * .5 - width * .5     # Posição X que deve ser a posição inicial do tabuleiro
        starting_y = 550 * .5 - height * .5     # Posição Y que deve ser a posição inicial do tabuleiro

        # Loop para desenhar as casas do tabuleiro, usando variáveis iniciadas acima
        for j in range(Consts.ROWS):
            y = starting_y + j * (Consts.BLOCK_SIZE + Consts.GAP)   # Posição Y atual
            for i in range(Consts.COLS):
                x = starting_x + i * (Consts.BLOCK_SIZE + Consts.GAP)   # Posição X atual
                pg.draw.rect(self.display, 
                self.choose_tile_color(i, j), 
                (x, y, Consts.BLOCK_SIZE, Consts.BLOCK_SIZE), border_radius= 10)    # Desenha a casa
        
        
        # Desenha as peças do jogo
        for j in range(len(pieces)):
            y = starting_y + j * (Consts.BLOCK_SIZE + Consts.GAP)   # Calcula posição y da peça
            for i in range(len(pieces[j])):
                x = starting_x + i * (Consts.BLOCK_SIZE + Consts.GAP)   # Calcula posição x da peça
                if pieces[j, i] != 0:   # Verifica se o elemento no array não é nulo (nulo == 0), mas uma peça do jogo
                    # Desenha o círculo da peça
                    piece = pg.draw.circle(self.display,
                                   (208, 0, 0) if pieces[j,i] < 0 else (0, 180, 216),
                                   (x + Consts.BLOCK_SIZE // 2, y + Consts.BLOCK_SIZE // 2), Consts.BLOCK_SIZE // 2.25)     # Desenha a casa
                    
                    piece_text = Consts.button_font.render(str(abs(pieces[j, i])), True, (235, 235, 235)) # Renderiza o texto da peça
                    self.display.blit(piece_text, piece_text.get_rect(center=piece.center)) # Coloca o texto da peça no centro do círculo da peça            

    def choose_tile_color(self, i: float, j: float) -> tuple[int, int, int]:
        """Escolhe a cor da casa baseada na sua posição

        Args:
            i (float): Coluna da casa
            j (float): Linha da casa

        Returns:
            color[int, int, int]: cor escolhida da casa
        """
        #Cor da Toca
        if (i == 3 and j == 0) or (i == 2 and j == 6):
            return Consts.den_color
        
        #Cor da Armadilha
        if ((i == 2 or i == 4) and j == 0) or \
           (i == 3 and j == 1) or \
           ((i == 1 or i == 3) and j == 6) or \
           (i == 2 and j == 5):
            return Consts.trap_color
        
        #Cor do Rio
        if (i in (1, 4) and 2 < j < 5) or \
           (i in (1, 4) and j == 2):
            return Consts.river_color
        
        return Consts.grass_color

    def mouse_to_board(self, pos: tuple(int, int)) -> tuple(int, int):
        """Converte a posição do rato do tipo tuple(x, y) para tuple(coluna, linha) no tabuleiro
        Se a posição do clique do rato não estiver no tabuleiro, retorna None

        Args:
            pos (tuple(int, int)): posição do rato no ecrã

        Returns:
            tuple(int, int): posição do rato no tabuleiro, ou None se o rato não estiver no tabuleiro
        """
        width = Consts.COLS * Consts.BLOCK_SIZE + (Consts.COLS - 1) * Consts.GAP    # Largura do tabuleiro  
        height = Consts.ROWS * Consts.BLOCK_SIZE + (Consts.ROWS - 1) * Consts.GAP   # Altura do tabuleiro 

        starting_x = 1000 * .5 - width * .5     # Posição X inicial do tabuleiro
        starting_y = 550 * .5 - height * .5     # Posição Y inicial do tabuleiro

        x = (pos[0] - starting_x) / (Consts.BLOCK_SIZE + Consts.GAP)    # Posição X no tabuleiro (coluna)
        y = (pos[1] - starting_y) / (Consts.BLOCK_SIZE + Consts.GAP)    # Posição Y no tabuleiro (linha)

        
        # Verifica se a posição do rato está fora do tabuleiro
        if x < 0 or y < 0:
            return (-1, -1)
        
        if x > (Consts.COLS) or y > (Consts.ROWS):
            return (-1, -1)
        
        return (int(x),int(y))
    
    def draw_possible_moves(self, moves: list(tuple(int, int))) -> None:
        """Desenha os movimentos atualmente possíveis para a peça selecionada

        Args:
            moves (list[tuple(int, int)]): lista de movimentos atuais possíveis
        """
        if moves is None:
            return None
        width = Consts.COLS * Consts.BLOCK_SIZE + (Consts.COLS - 1) * Consts.GAP    # Largura do tabuleiro  
        height = Consts.ROWS * Consts.BLOCK_SIZE + (Consts.ROWS - 1) * Consts.GAP   # Altura do tabuleiro 

        starting_x = 1000 * .5 - width * .5
        starting_y = 550 * .5 - height * .5
        
        for move in moves:
            x_pos = move[1] * (Consts.BLOCK_SIZE + Consts.GAP) + starting_x + (Consts.BLOCK_SIZE * .25)
            y_pos = move[0] * (Consts.BLOCK_SIZE + Consts.GAP) + starting_y + (Consts.BLOCK_SIZE * .25)
            
            pg.draw.rect(self.display, (235,222,52,50),(x_pos, y_pos, 30, 30), border_radius=10)
    
    def switch_turn(self, turn: int) -> None:
        """Muda a mensagem baseada no turno atual

        Args:
            turn (int): Turno atual
        """
        self.message = "Jogador Azul" if turn == 0 else "Jogador Vermelho"
    
    def draw_status(self) -> None:
        """Desenha o estado atual do turno
        """
        pg.draw.rect(self.display, (235, 235, 235), (20, 400, 250, 75))
        message = Consts.sub_title_font.render(self.message, True, 10)
        self.display.blit(message, (20, 420))
    
    def draw_win_message(self, player) -> None:
        """Desenha o jogador vencedor no ecrã

        Args:
            player (str): Cor do jogador vencedor
        """
        color = (37, 154, 232) if player == "Azul" else (232, 60, 37)       # Escolhe a cor do jogador vencedor
        length = 425        # Tamanho do diálogo
        pg.draw.rect(self.display, color, ((500 - (length / 2), 275 - (length / 2)), (length, length)), border_radius = 25)     # Desenha o fundo da mensagem
        message = Consts.message_font.render(f'Jogador {player} venceu!', True, (235, 235, 235))    # Renderiza o conteúdo da mensagem
        message_rect = message.get_rect(center=(500, 175))      # Define a posição da mensagem
        self.display.blit(message, message_rect)        # Desenha o conteúdo da mensagem
        play_again_button = Button('#d4d4d4', 362, 230, 275, 70, 30, 'Jogar Novamente', font=Consts.button_font)         # Cria o botão de jogar novamente, que reinicia o jogo
        main_menu_button = Button('#d4d4d4',362, 340, 275, 70, 30, 'Menu Principal', font=Consts.button_font)  # Cria o botão de voltar ao menu principal
        main_menu_button.draw(self.display) # Desenha o botão do menu principal
        play_again_button.draw(self.display)   # Desenha o botão de jogar novamente
        
        return play_again_button, main_menu_button      # Retorna referências para ambos os botões
            

    def reset(self):
        """Reinicia o componente View para o seu estado inicial
        """
        self.display = pg.display.set_mode((1000, 550), 0, 32)    # Inicia o ecrã

        pg.display.update()    # Atualiza o ecrã
        time.sleep(0.01)
        self.display.fill((235,235,235))    # Preenche o ecrã com cor cinza claro

        self.close_button: Button = Button("#B8C6DB", 20, 30, 90, 55, 
                                   border_radius=50, text='fechar', font=Consts.button_font)    # Inicia o botão de fechar
        
        self.message: str = "Jogador Azul"    
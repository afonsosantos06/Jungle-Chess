from MVC.model import Model, AI, RandomAI, NegamaxAI
from MVC.view import View
import time
import pygame as pg
from assets.consts import Consts


class Controller:
    def __init__(self, is_pve: bool, ai_type: str = "minimax", depth: int = 4):
        """Inicia o componente Controlador

        Args:
            is_pve (bool): deve o jogo usar lógica PvE ou PvP
            ai_type (str): tipo de IA a ser usada (default: "minimax")
            depth (int): profundidade do algoritmo minimax (default: 4)
        """
        self.model = Model()
        self.view = View()
        self.is_pve = is_pve
        self.ai_type = ai_type
        
        # Inicializa a IA apropriada
        if is_pve:
            if ai_type == "minimax":
                self.ai = AI(self.model, depth)
            elif ai_type == "negamax":
                self.ai = NegamaxAI(self.model, depth)
            else:  # random
                self.ai = RandomAI(self.model)
        
        pg.event.set_blocked([pg.MOUSEMOTION])
        self.main_loop()        # Chama o loop principal
    
    def main_loop(self):
        """Loop principal do jogo
        """
        while True:
            if self.is_pve:    # Deve usar lógica de jogo PvE ou PvP
                self.pve_game_loop(self.model.turn)   # Chama a lógica de jogo PvE
            else:
                self.pvp_game_loop(self.model.turn)   # Chama a lógica de jogo PvP
                       
    def pve_game_loop(self, turn: int):
        """Lógica de jogo PvE

        Args:
            turn (int): turno para jogador azul (0) ou jogador vermelho (1)
        """
        if turn == 0:
            # turno para o jogador humano
            for event in pg.event.get():
                ev_type = event.type
                self.view.draw_board(self.model.game_board)     # Desenha o tabuleiro após mudança de turno
                self.handle(ev_type)    # Processa o evento

        elif turn == 1:
            # turno para a IA
            time.sleep(0.2)  # Pequena pausa para melhor experiência do utilizador
            best_move = self.ai.get_best_move()
            if best_move:
                start, end = best_move
                self.model.perform_move(start, end)
                self.view.draw_board(self.model.game_board)
                is_win = self.model.is_win()
                if is_win[0]:
                    play_again_button, main_menu_button = self.view.draw_win_message(is_win[1])
                    self.view.draw_board(self.model.game_board)
                    while True:
                        for event in pg.event.get():
                            if event.type == pg.MOUSEBUTTONDOWN:
                                if play_again_button.is_over(pg.mouse.get_pos()):
                                    self.reset_game()
                                elif main_menu_button.is_over(pg.mouse.get_pos()):
                                    pg.display.quit()
                                    time.sleep(0.2)
                                    from screens.main_menu import MainMenu
                                    main_menu = MainMenu()
                            if event == pg.QUIT:
                                pg.quit()
                                quit()
                else:
                    self.model.switch_turn()
                    self.view.switch_turn(self.model.turn)
        
        self.view.clock.tick(Consts.FPS)

    def pvp_game_loop(self, turn: int):
        self.view.draw_status()
        if turn == 0:
            # Turno para o jogador azul
            for event in pg.event.get():
                ev_type = event.type    # Obtém o tipo de evento
                self.view.draw_board(self.model.game_board)    # Desenha o tabuleiro
                self.handle(ev_type)    # Processa o evento
                
        if turn == 1:
            # Turno para o jogador vermelho
            for event in pg.event.get():
                ev_type = event.type    # Obtém o tipo de evento
                self.view.draw_board(self.model.game_board)     # Desenha o tabuleiro
                self.handle(ev_type)    # Processa o evento

    def turn_logic_human(self, row, col):
        """Lógica de turno para jogadores humanos

        Args:
            row (int): linha selecionada
            col (int): coluna selecionada
        """
        if self.model.is_choosing_current_move((row, col)):     # Verifica se o movimento selecionado está na lista de movimentos atuais
                        self.model.perform_move(self.model.selected_game_piece, (row, col))     # Executa o movimento no modelo
                        self.view.draw_board(self.model.game_board)     # Desenha o tabuleiro atualizado no ecrã usando o componente view
                        self.model.moves = []       # Reinicia a lista de movimentos atuais
                        self.model.selected_game_piece = None       # Reinicia a peça selecionada
                        is_win = self.model.is_win()        # Obtém dados da vitória
                        if is_win[0]:       # Verifica se há vitória
                            play_again_button, main_menu_button = self.view.draw_win_message(is_win[1])         # Desenha mensagem de vitória e obtém referências para ambos os botões
                            self.view.draw_board(self.model.game_board)         # Desenha o tabuleiro atualizado
                            while True:     # Cria novo listener de eventos para novos botões
                                for event in pg.event.get():
                                    if event.type == pg.MOUSEBUTTONDOWN:
                                        if play_again_button.is_over(pg.mouse.get_pos()):
                                            self.reset_game()
                                            
                                        elif main_menu_button.is_over(pg.mouse.get_pos()):
                                            pg.display.quit()
                                            time.sleep(0.2)
                                            from screens.main_menu import MainMenu
                                            main_menu = MainMenu()
                                    if event == pg.QUIT:
                                        pg.quit()
                                        quit()
                        else:       # Se não houver vencedor
                            self.model.switch_turn()        # Muda o turno, de Azul para Vermelho e vice-versa
                            self.view.switch_turn(self.model.turn)      # Muda a mensagem de turno no componente view               
        else:       # Se estiver a escolher uma casa que não está na lista de movimentos atuais
            if self.model.is_selecting_valid_game_piece((row, col)):    # E estiver a escolher outra peça válida
                self.model.moves = self.model.get_possible_moves((row, col))    # Atualiza a lista de movimentos atuais
                print(f'possible moves: {self.model.moves}')    # Imprime a nova lista de movimentos
                self.model.selected_game_piece = (row, col)     # Atualiza a peça selecionada no componente model
                self.view.draw_possible_moves(self.model.moves) # Desenha novos movimentos no tabuleiro usando o componente view            
    
    def handle(self, event):
        """Processa eventos do pygame

        Args:
            event ([type]): tipo de evento
        """
        if event is pg.QUIT:
            # Processa clique no botão de sair do SO
            pg.quit()
            quit()
        
        elif event == pg.MOUSEBUTTONDOWN:
            mouse_loc = pg.mouse.get_pos() # Obtém posição do rato
            if self.view.close_button.is_over(mouse_loc):
                # Processa clique no botão de sair do jogo
                pg.quit()
                quit()
            else:
                # Processa clique no ecrã, não no botão de sair
                col, row = self.view.mouse_to_board(mouse_loc) # Obtém linha e coluna selecionadas
                if col == row == -1:
                    pass
                else:
                    print(f'col: {col}, row: {row}')
                    
                    self.turn_logic_human(row, col)
                            
    def reset_game(self) -> None:
        """Reinicia o jogo para o seu estado inicial e reinicia o loop do jogo
        """
        self.model.reset()
        self.view.reset()
        self.main_loop()
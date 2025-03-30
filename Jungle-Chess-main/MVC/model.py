import numpy as np
from assets.consts import Consts
import random


class Model:
    def __init__(self) -> None:
        board = [[-7, 0, 0, 0, 0, -5],
                 [0, -4, 0, 0, -2, 0],
                 [-1, 0, 0, -3, 0, -8],
                 [0, 0, 0, 0, 0, 0],
                 [8, 0, 3, 0, 0, 1],
                 [0, 2, 0, 0, 4, 0],
                 [5, 0, 0, 0, 0, 7]]
        self.game_board = np.asarray(board, dtype=int)    # Converte a variável do tabuleiro num array numpy
        self.moves = []
        self.selected_game_piece = None
        self.turn = 0
    
    def is_outside_r_edge(self, pos_x: int) -> bool:
        """Verifica se a posição X está fora da borda direita do tabuleiro

        Args:
            pos_x (int): Posição X a verificar

        Returns:
            bool: está fora da borda direita do tabuleiro
        """
        return True if pos_x >= 6 else False
    
    def is_outside_l_edge(self, pos_x: int) -> bool:
        """Verifica se a posição X está fora da borda esquerda do tabuleiro

        Args:
            pos_x (int): Posição X a verificar

        Returns:
            bool: está fora da borda esquerda do tabuleiro
        """
        return True if pos_x < 0 else False
    
    def is_outside_u_edge(self, pos_y: int) -> bool:
        """Verifica se a posição Y está fora da borda superior do tabuleiro

        Args:
            pos_y (int): Posição Y a verificar

        Returns:
            bool: está fora da borda superior do tabuleiro
        """
        return True if pos_y < 0 else False
    
    def is_outside_d_edge(self, pos_y: int) -> bool:
        """Verifica se a posição Y está fora da borda inferior do tabuleiro

        Args:
            pos_y (int): Posição Y a verificar

        Returns:
            bool: está fora da borda inferior do tabuleiro
        """
        return True if pos_y >= 7 else False
    
    def is_overlapping_own_den(self, pos, rank: int) -> bool:
        """Verifica se a posição possível de uma peça está a cobrir a sua própria toca

        Args:
            pos (tuple(int, int)): Posição possível da peça
            rank (int): Rank da peça (Positivo para jogador azul, negativo para jogador vermelho)

        Returns:
            bool: está a cobrir a posição da sua própria toca
        """
        if (rank < 0 and pos == (0, 3)) or (rank > 0 and pos == (6, 2)):
            return True
        
        return False
    
    def is_self_rank_higher(self, rank_a: int, rank_b: int) -> bool:
        """Compara rank e other_rank para determinar se a peça rank_a pode comer a peça rank_b

        Args:
            rank_a (int): Rank da possível peça que come
            rank_b (int): Rank da peça a ser comida

        Returns:
            bool: rank pode comer other_rank
        """
        # Verifica se as peças são do mesmo time
        if (rank_a > 0 and rank_b > 0) or (rank_a < 0 and rank_b < 0):
            return False

        # Encontra a posição da peça a ser comida (rank_b)
        pos_b = None
        for i in range(7):
            for j in range(6):
                if self.game_board[i, j] == rank_b:
                    pos_b = (i, j)
                    break
            if pos_b:
                break

        # Encontra a posição da peça que come (rank_a)
        pos_a = None
        for i in range(7):
            for j in range(6):
                if self.game_board[i, j] == rank_a:
                    pos_a = (i, j)
                    break
            if pos_a:
                break

        # Se não encontrar uma das posições, retorna False
        if pos_a is None or pos_b is None:
            return False

        # Verifica se a peça está em uma armadilha do adversário
        if rank_b > 0:  # Peça azul
            if pos_b in [(0, 2), (0, 4), (1, 3)]:  # Armadilhas vermelhas
                return True
        else:  # Peça vermelha
            if pos_b in [(6, 1), (6, 3), (5, 2)]:  # Armadilhas azuis
                return True

        # Se não estiver em armadilha, continua com as regras normais
        rank_a = abs(rank_a)
        rank_b = abs(rank_b)

        # Regra especial para Ratos (rank 1)
        if rank_a == 1 and rank_b == 1:
            # Verifica se ambos estão no rio ou ambos em terra
            is_a_in_river = (pos_a[1] in (1, 4) and 2 < pos_a[0] < 5) or \
                          (pos_a[1] in (1, 4) and pos_a[0] == 2)
            is_b_in_river = (pos_b[1] in (1, 4) and 2 < pos_b[0] < 5) or \
                          (pos_b[1] in (1, 4) and pos_b[0] == 2)
            
            return is_a_in_river == is_b_in_river

        # Regra especial para Rato vs Elefante
        if rank_a == 1 and rank_b == 8:
            # Verifica se o rato está no rio
            is_a_in_river = (pos_a[1] in (1, 4) and 2 < pos_a[0] < 5) or \
                          (pos_a[1] in (1, 4) and pos_a[0] == 2)
            
            # O rato só pode capturar o elefante se não estiver no rio
            return not is_a_in_river

        # Regras normais para outras peças...
        if rank_a == 1 and rank_b in (0, 1, 8):
            return True
        
        if rank_a == 2 and rank_b <= 2:
            return True
        
        if rank_a == 3 and rank_b <= 3:
            return True
        
        if rank_a == 4 and rank_b <= 4:
            return True
        
        if rank_a == 5 and rank_b <= 5:
            return True
        
        if rank_a == 6 and rank_b <= 6:
            return True
        
        if rank_a == 7 and rank_b <= 7:
            return True
        
        if rank_a == 8 and rank_b in (0, 2, 3, 4, 5, 6, 7, 8):
            return True
        
        return False
            
    def get_directions_to_river(self, pos):
        """Gera uma lista de direções adjacentes aos rios para uma peça dada

        Args:
            pos (tuple(int, int)): posição da peça

        Returns:
            list[str]: lista de direções para os rios
        """
        directions = []

        # Verifica se a peça está à direita do rio
        if pos[1] == 2 and 2 < pos[0] < 5:
            directions.append((0, -1))
        
        # Verifica se a peça está à esquerda do rio
        if pos[1] == 3 and 2 < pos[0] < 5:
            directions.append((0, 1))
        
        # Verifica se a peça está acima do rio
        if pos[1] in (1, 4) and pos[0] == 2:
            directions.append((1, 0))
        
        # Verifica se a peça está abaixo do rio
        if pos[1] in (1, 4) and pos[0] == 4:
            directions.append((-1, 0))
        
        return directions
    
    def land_logic(self, pos, rank: int):
        """Lógica de movimento para peças terrestres: Gato, Cão, Lobo, Leopardo, Elefante

        Args:
            pos (tuple(int, int)): posição atual da peça
            rank (int): rank da peça atual
        """

        directions_to_river = self.get_directions_to_river(pos)
        moves = []
        if len(directions_to_river) == 0:
            for dir in Consts.DIRECTIONS:
                if not self.is_outside_r_edge(pos[1] + dir[1]): 
                    if not self. is_outside_l_edge(pos[1] + dir[1]):
                        if not self.is_outside_u_edge(pos[0] + dir[0]):
                            if not self.is_outside_d_edge(pos[0] + dir[0]):
                                # Verifica se a posição de destino é rio
                                new_pos = (pos[0] + dir[0], pos[1] + dir[1])
                                if not ((new_pos[1] in (1, 4) and 2 < new_pos[0] < 5) or \
                                      (new_pos[1] in (1, 4) and new_pos[0] == 2)):
                                    if self.is_self_rank_higher(rank, self.game_board[new_pos[0], new_pos[1]]):
                                        if not self.is_overlapping_own_den(new_pos, rank):
                                            moves.append(new_pos)
        
        else:
            DIR = Consts.DIRECTIONS.copy()
            for direction in directions_to_river:
                DIR.remove(direction)
            
            for dir in DIR:
                if not self.is_outside_r_edge(pos[1] + dir[1]): 
                    if not self. is_outside_l_edge(pos[1] + dir[1]):
                        if not self.is_outside_u_edge(pos[0] + dir[0]):
                            if not self.is_outside_d_edge(pos[0] + dir[0]):
                                # Verifica se a posição de destino é rio
                                new_pos = (pos[0] + dir[0], pos[1] + dir[1])
                                if not ((new_pos[1] in (1, 4) and 2 < new_pos[0] < 5) or \
                                      (new_pos[1] in (1, 4) and new_pos[0] == 2)):
                                    if self.is_self_rank_higher(rank, self.game_board[new_pos[0], new_pos[1]]):
                                        if not self.is_overlapping_own_den(new_pos, rank):
                                            moves.append(new_pos)
        
        return moves
    
    def land_river_logic(self, pos, rank: int):
        """Lógica de movimento para peças terrestres-aquáticas: Rato

        Args:
            pos (tuple(int, int)): posição atual da peça
            rank (int): rank da peça atual
        """
        moves = []
        for dir in Consts.DIRECTIONS:
            if not self.is_outside_r_edge(pos[1] + dir[1]): 
                    if not self. is_outside_l_edge(pos[1] + dir[1]):
                        if not self.is_outside_u_edge(pos[0] + dir[0]):
                            if not self.is_outside_d_edge(pos[0] + dir[0]):
                                if self.is_self_rank_higher(rank, self.game_board[pos[0] + dir[0], pos[1] + dir[1]]):
                                    if not self.is_overlapping_own_den((pos[0] + dir[0], pos[1] + dir[1]), rank):
                                        moves.append((pos[0] + dir[0], pos[1] + dir[1]))
        
        return moves

    def is_river(self, pos):
        """Verifica se uma posição é rio

        Args:
            pos (tuple(int, int)): posição a verificar (linha, coluna)

        Returns:
            bool: True se a posição é rio, False caso contrário
        """
        row, col = pos
        # Rio nas colunas 1 e 4, entre as linhas 2 e 4
        return col in (1, 4) and 2 <= row <= 4

    def land_jump_logic(self, pos, rank: int):
        """Lógica de movimento para peças terrestres com salto: Tigre, Leão

        Args:
            pos (tuple(int, int)): posição atual da peça
            rank (int): rank da peça atual
        """
        moves = []
        row, col = pos
        
        # Movimentos normais (sem rio)
        for dir in Consts.DIRECTIONS:
            new_row, new_col = row + dir[0], col + dir[1]
            if (0 <= new_row < 7 and 0 <= new_col < 6):  # Dentro do tabuleiro
                new_pos = (new_row, new_col)
                if not self.is_river(new_pos):
                    if self.is_self_rank_higher(rank, self.game_board[new_row, new_col]):
                        moves.append(new_pos)

        # Lógica especial para o Leão (rank 7)
        if abs(rank) == 7:
            # Saltos horizontais sobre o rio
            if 2 <= row <= 4:  # Entre as linhas 2 e 4 (inclusive)
                # Salto para a esquerda
                if col == 2:  # Se estiver à direita da coluna 1
                    target_pos = (row, 0)
                    path_clear = True
                    # Verifica se há ratos no caminho
                    if abs(self.game_board[row, 1]) == 1:  # Se for um rato
                        path_clear = False
                    if path_clear and self.is_self_rank_higher(rank, self.game_board[target_pos[0], target_pos[1]]):
                        moves.append(target_pos)
                elif col == 5:  # Se estiver à direita da coluna 4
                    target_pos = (row, 3)
                    path_clear = True
                    # Verifica se há ratos no caminho
                    if abs(self.game_board[row, 4]) == 1:  # Se for um rato
                        path_clear = False
                    if path_clear and self.is_self_rank_higher(rank, self.game_board[target_pos[0], target_pos[1]]):
                        moves.append(target_pos)
                
                # Salto para a direita
                if col == 0:  # Se estiver à esquerda da coluna 1
                    target_pos = (row, 2)
                    path_clear = True
                    # Verifica se há ratos no caminho
                    if abs(self.game_board[row, 1]) == 1:  # Se for um rato
                        path_clear = False
                    if path_clear and self.is_self_rank_higher(rank, self.game_board[target_pos[0], target_pos[1]]):
                        moves.append(target_pos)
                elif col == 3:  # Se estiver à esquerda da coluna 4
                    target_pos = (row, 5)
                    path_clear = True
                    # Verifica se há ratos no caminho
                    if abs(self.game_board[row, 4]) == 1:  # Se for um rato
                        path_clear = False
                    if path_clear and self.is_self_rank_higher(rank, self.game_board[target_pos[0], target_pos[1]]):
                        moves.append(target_pos)
            
            # Saltos verticais sobre o rio
            if col in (1, 4):  # Nas colunas do rio
                # Salto para cima
                if row == 5:  # Na linha 5
                    target_pos = (1, col)
                    path_clear = True
                    # Verifica se há ratos no caminho
                    for r in range(2, 5):
                        if abs(self.game_board[r, col]) == 1:  # Se for um rato
                            path_clear = False                        
                    if path_clear and self.is_self_rank_higher(rank, self.game_board[target_pos[0], target_pos[1]]):
                        moves.append(target_pos)
                
                # Salto para baixo
                if row == 1:  # Na linha 2
                    target_pos = (5, col)
                    path_clear = True
                    # Verifica se há ratos no caminho
                    for r in range(2, 5):
                        if abs(self.game_board[r, col]) == 1:  # Se for um rato
                            path_clear = False                        
                    if path_clear and self.is_self_rank_higher(rank, self.game_board[target_pos[0], target_pos[1]]):
                        moves.append(target_pos)
        
        return moves

    def get_possible_moves(self, position):
        """Retorna os movimentos possíveis de uma peça para uma posição dada

        Args:
            position (tuple(int, int)): posição dada
        """
        
        moves = None      # Gera movimentos possíveis
        current_rank = self.game_board[position[0], position[1]]    # Obtém o rank atual

        if current_rank == 0:
            return None
        
        elif abs(current_rank) == 1: # Rato
            moves = self.land_river_logic(position, current_rank)
        elif abs(current_rank) == 2: # Gato
            moves = self.land_logic(position, current_rank)
        elif abs(current_rank) == 3: # Cão
            moves = self.land_logic(position, current_rank)
        elif abs(current_rank) == 4: # Lobo
            moves = self.land_logic(position, current_rank)
        elif abs(current_rank) == 5: # Leopardo
            moves = self.land_logic(position, current_rank)
        elif abs(current_rank) == 6: # Tigre
            moves = self.land_jump_logic(position, current_rank)
        elif abs(current_rank) == 7: # Leão
            moves = self.land_jump_logic(position, current_rank)
            
        elif abs(current_rank) == 8: # Elefante
            moves = self.land_logic(position, current_rank)
        
        return moves

    def is_choosing_current_move(self, pos) -> bool:
        """Verifica se a posição selecionada está na lista de movimentos atuais

        Args:
            pos (tuple(int, int)): Posição selecionada

        Returns:
            bool: resposta da consulta
        """
        return True if pos in self.moves and self.selected_game_piece is not None else False
    
    def is_selecting_valid_game_piece(self, pos) -> bool:
        """Verifica se o jogador está a clicar numa peça válida e não nas peças do oponente ou num espaço vazio

        Args:
            pos (tuple(int, int)): posição selecionada

        Returns:
            bool: resposta da consulta
        """
        return True if (self.game_board[pos[0], pos[1]] > 0 and self.turn == 0) or (self.game_board[pos[0], pos[1]] < 0 and self.turn == 1) else False
    
    def perform_move(self, start_place, selected_move) -> None:
        """Move uma peça da posição original para a posição selecionada

        Args:
            game_piece (tuple(int, int)): posição da peça a mover
            selected_move (tuple(int, int)): posição selecionada
        """
        self.game_board[selected_move[0], selected_move[1]] = self.game_board[start_place[0], start_place[1]]
        self.game_board[start_place[0], start_place[1]] = 0
        
    def switch_turn(self) -> None:
        """Muda o turno de 0 (Azul) para 1 (Vermelho) e vice-versa
        """
        self.turn = 0 if self.turn == 1 else 1

    def is_win(self):
        """Verifica se há um vencedor, de acordo com as regras

        Returns:
            tuple(bool, str): tuplo que contém bool se houver vitória e uma str que indica qual jogador venceu
        """
        winning_player = ''
        is_win = False
        # Verifica vitória para o jogador azul
        if self.game_board[0, 3] > 0 or (self.game_board >= 0).all():
            print('blue win')
            is_win = True
            winning_player = 'Azul'
            
        
        # Verifica vitória para o jogador vermelho
        if self.game_board[6, 2] < 0 or (self.game_board <= 0).all():
            print('red win')
            is_win = True
            winning_player = 'Vermelho'
        
        return (is_win, winning_player)
    
    def reset(self) -> None:
        """Reinicia o modelo para o seu estado inicial
        """
        board = [[-7, 0, 0, 0, 0, -5],
                 [0, -4, 0, 0, -2, 0],
                 [-1, 0, 0, -3, 0, -8],
                 [0, 0, 0, 0, 0, 0],
                 [8, 0, 3, 0, 0, 1],
                 [0, 2, 0, 0, 4, 0],
                 [5, 0, 0, 0, 0, 7]]
        self.game_board = np.asarray(board, dtype=int)    # Converte a variável do tabuleiro num array numpy
        self.moves = []
        self.selected_game_piece = None
        self.turn = 0

    def is_piece_safe_in_trap(self, pos: tuple, piece: int) -> bool:
        """Verifica se uma peça está segura em uma armadilha (não pode ser capturada)

        Args:
            pos (tuple): Posição da peça
            piece (int): Valor da peça

        Returns:
            bool: True se a peça está segura, False caso contrário
        """
        # Verifica todas as peças adjacentes
        for dir in Consts.DIRECTIONS:
            new_pos = (pos[0] + dir[0], pos[1] + dir[1])
            if not (self.is_outside_r_edge(new_pos[1]) or 
                   self.is_outside_l_edge(new_pos[1]) or 
                   self.is_outside_u_edge(new_pos[0]) or 
                   self.is_outside_d_edge(new_pos[0])):
                adjacent_piece = self.game_board[new_pos[0], new_pos[1]]
                if adjacent_piece != 0:
                    # Se a peça adjacente for do oponente e puder capturar
                    if (piece < 0 and adjacent_piece > 0) or (piece > 0 and adjacent_piece < 0):
                        if self.is_self_rank_higher(adjacent_piece, piece):
                            return False
        return True


class AI:
    def __init__(self, model: Model, depth: int = 4):
        self.model = model
        self.max_depth = depth  # Profundidade configurável
        
        # Cache para avaliações de posição
        self.position_cache = {}
        
        # Valores das peças (otimizados)
        self.piece_values = {
            1: 6,   # Rato
            2: 3,   # Gato
            3: 4,   # Cão
            4: 5,   # Lobo
            5: 6,   # Leopardo
            6: 7,   # Tigre
            7: 8,   # Leão
            8: 10   # Elefante
        }
        
        # Posições das armadilhas
        self.traps = [
            (0, 2), (0, 4), (1, 3),  # Armadilhas vermelhas
            (6, 1), (6, 3), (5, 2)   # Armadilhas azuis
        ]
        
        # Posições das tocas
        self.dens = [(0, 3), (6, 2)]  # (vermelho, azul)
        
        # Limite de movimentos para poda
        self.move_limit = 20  # Limita o número de movimentos avaliados por nó
        
    def evaluate_board(self) -> float:
        """Avalia o estado atual do tabuleiro com uma função de avaliação otimizada"""
        # Verifica cache
        board_key = str(self.model.game_board)
        if board_key in self.position_cache:
            return self.position_cache[board_key]
            
        score = 0
        
        # 1. Avaliação de material (peso aumentado)
        for i in range(7):
            for j in range(6):
                piece = self.model.game_board[i, j]
                if piece != 0:
                    value = self.piece_values[abs(piece)]
                    if piece < 0:  # Peça vermelha (AI)
                        score += value * 1.2  # Aumentado o peso para peças da IA
                    else:  # Peça azul
                        score -= value
        
        # 2. Avaliação de posição (otimizada)
        for i in range(7):
            for j in range(6):
                piece = self.model.game_board[i, j]
                if piece != 0:
                    # Progresso em direção à toca adversária
                    if piece < 0:  # Peça vermelha (AI)
                        dist_to_den = abs(i - self.dens[1][0]) + abs(j - self.dens[1][1])
                        score += (8 - dist_to_den) * 0.8  # Aumentado o peso
                    else:  # Peça azul
                        dist_to_den = abs(i - self.dens[0][0]) + abs(j - self.dens[0][1])
                        score -= (8 - dist_to_den) * 0.8  # Aumentado o peso
        
        # 3. Avaliação de armadilhas (otimizada)
        for trap in self.traps:
            piece = self.model.game_board[trap[0], trap[1]]
            if piece != 0:
                if piece < 0 and trap in self.traps[:3]:  # Peça vermelha na armadilha azul
                    if self.model.is_piece_safe_in_trap(trap, piece):
                        score += 8  # Aumentado o peso
                    else:
                        score -= 30  # Aumentado a penalidade
                elif piece > 0 and trap in self.traps[3:]:  # Peça azul na armadilha vermelha
                    if self.model.is_piece_safe_in_trap(trap, piece):
                        score -= 8  # Aumentado o peso
                    else:
                        score += 30  # Aumentado a penalidade
        
        # 4. Avaliação de mobilidade (otimizada)
        red_moves = len(self.get_all_possible_moves(True))
        blue_moves = len(self.get_all_possible_moves(False))
        if red_moves + blue_moves > 0:
            mobility_score = (red_moves - blue_moves) / (red_moves + blue_moves)
            score += mobility_score * 4  # Aumentado o peso
        
        # 5. Avaliação de ameaças (otimizada)
        for i in range(7):
            for j in range(6):
                piece = self.model.game_board[i, j]
                if piece != 0:
                    moves = self.model.get_possible_moves((i, j))
                    if moves:  # Só avalia se houver movimentos possíveis
                        for move in moves:
                            target = self.model.game_board[move[0], move[1]]
                            if target != 0:
                                if piece < 0 and target > 0:  # Ameaça vermelha
                                    if abs(piece) >= abs(target):
                                        score += 3.5  # Aumentado o peso
                                elif piece > 0 and target < 0:  # Ameaça azul
                                    if abs(piece) >= abs(target):
                                        score -= 3.5  # Aumentado o peso
        
        # 6. Avaliação de controle do centro (otimizada)
        center_positions = [(3, 2), (3, 3)]
        for pos in center_positions:
            piece = self.model.game_board[pos[0], pos[1]]
            if piece != 0:
                if piece < 0:  # Peça vermelha
                    score += 4  # Aumentado o peso
                else:  # Peça azul
                    score -= 4  # Aumentado o peso
        
        # 7. Avaliação de proteção de peças valiosas (otimizada)
        for i in range(7):
            for j in range(6):
                piece = self.model.game_board[i, j]
                if piece != 0 and abs(piece) >= 7:  # Leão e Elefante
                    if piece < 0:  # Peça vermelha
                        if self.model.is_piece_safe_in_trap((i, j), piece):
                            score += 6  # Aumentado o peso
                    else:  # Peça azul
                        if self.model.is_piece_safe_in_trap((i, j), piece):
                            score -= 6  # Aumentado o peso

        # 8. Avaliação de posicionamento estratégico (nova)
        strategic_positions = [(2, 2), (2, 3), (4, 2), (4, 3)]  # Posições estratégicas
        for pos in strategic_positions:
            piece = self.model.game_board[pos[0], pos[1]]
            if piece != 0:
                if piece < 0:  # Peça vermelha
                    score += 2
                else:  # Peça azul
                    score -= 2

        # 9. Avaliação de proteção mútua (nova)
        for i in range(7):
            for j in range(6):
                piece = self.model.game_board[i, j]
                if piece != 0:
                    protected = False
                    for dir in Consts.DIRECTIONS:
                        new_pos = (i + dir[0], j + dir[1])
                        if not (self.model.is_outside_r_edge(new_pos[1]) or 
                               self.model.is_outside_l_edge(new_pos[1]) or 
                               self.model.is_outside_u_edge(new_pos[0]) or 
                               self.model.is_outside_d_edge(new_pos[0])):
                            adjacent_piece = self.model.game_board[new_pos[0], new_pos[1]]
                            if (piece < 0 and adjacent_piece < 0) or (piece > 0 and adjacent_piece > 0):
                                if self.model.is_self_rank_higher(adjacent_piece, piece):
                                    protected = True
                                    break
                    if protected:
                        if piece < 0:  # Peça vermelha
                            score += 1.5
                        else:  # Peça azul
                            score -= 1.5
        
        # Armazena no cache
        self.position_cache[board_key] = score
        return score
    
    def get_all_possible_moves(self, is_ai_turn: bool) -> list:
        """Retorna todas as possíveis jogadas para o jogador atual (otimizada)"""
        moves = []
        for i in range(7):
            for j in range(6):
                piece = self.model.game_board[i, j]
                if (is_ai_turn and piece < 0) or (not is_ai_turn and piece > 0):
                    possible_moves = self.model.get_possible_moves((i, j))
                    if possible_moves:
                        moves.extend(((i, j), move) for move in possible_moves)
        
        # Ordena e limita o número de movimentos
        moves.sort(key=lambda x: self.evaluate_move(x), reverse=is_ai_turn)
        return moves[:self.move_limit]  # Retorna apenas os melhores movimentos
    
    def negamax(self, depth: int, alpha: float, beta: float, color: int) -> tuple:
        """Implementa o algoritmo Negamax com cortes alfa-beta (otimizada)"""
        if depth == 0 or self.model.is_win()[0]:
            return color * self.evaluate_board(), None
        
        moves = self.get_all_possible_moves(color < 0)
        if not moves:  # Se não houver movimentos possíveis
            return color * self.evaluate_board(), None
            
        max_eval = float('-inf')
        best_move = moves[0]  # Usa o primeiro movimento como padrão
        
        for start, end in moves:
            # Faz a jogada
            piece_value = self.model.game_board[end[0], end[1]]
            self.model.game_board[end[0], end[1]] = self.model.game_board[start[0], start[1]]
            self.model.game_board[start[0], start[1]] = 0
            
            # Avalia a jogada
            eval, _ = self.negamax(depth - 1, -beta, -alpha, -color)
            eval = -eval  # Inverte o valor da avaliação
            
            # Desfaz a jogada
            self.model.game_board[start[0], start[1]] = self.model.game_board[end[0], end[1]]
            self.model.game_board[end[0], end[1]] = piece_value
            
            if eval > max_eval:
                max_eval = eval
                best_move = (start, end)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
                
        return max_eval, best_move

    def get_best_move(self) -> tuple:
        """Retorna a melhor jogada para a IA"""
        # Limpa o cache antes de cada nova busca
        self.position_cache.clear()
        _, best_move = self.negamax(self.max_depth, float('-inf'), float('inf'), -1)  # -1 para peças vermelhas (IA)
        return best_move
    
    def evaluate_move(self, move: tuple) -> float:
        """Avalia um movimento específico para ordenação (otimizada)"""
        start, end = move
        score = 0
        
        # Captura de peça (peso aumentado)
        if self.model.game_board[end[0], end[1]] != 0:
            captured_piece = abs(self.model.game_board[end[0], end[1]])
            score += self.piece_values[captured_piece] * 2  # Peso baseado no valor da peça capturada
        
        # Captura de peça em armadilha (peso aumentado)
        if end in self.traps:
            if self.model.game_board[end[0], end[1]] != 0:
                score += 30
        
        # Movimento para armadilha adversária (peso aumentado)
        if end in self.traps[:3] and self.model.game_board[start[0], start[1]] < 0:
            score += 5
        elif end in self.traps[3:] and self.model.game_board[start[0], start[1]] > 0:
            score += 5
        
        # Movimento em direção à toca adversária (peso aumentado)
        if self.model.game_board[start[0], start[1]] < 0:
            dist_before = abs(start[0] - self.dens[1][0]) + abs(start[1] - self.dens[1][1])
            dist_after = abs(end[0] - self.dens[1][0]) + abs(end[1] - self.dens[1][1])
            if dist_after < dist_before:
                score += 3
        else:
            dist_before = abs(start[0] - self.dens[0][0]) + abs(start[1] - self.dens[0][1])
            dist_after = abs(end[0] - self.dens[0][0]) + abs(end[1] - self.dens[0][1])
            if dist_after < dist_before:
                score += 3
        
        # Movimento para o centro (novo)
        center_positions = [(3, 2), (3, 3)]
        if end in center_positions:
            score += 2
        
        # Movimento que protege peças valiosas (novo)
        piece = self.model.game_board[start[0], start[1]]
        if abs(piece) >= 6:  # Tigre, Leão e Elefante
            if self.model.is_piece_safe_in_trap(end, piece):
                score += 3
        
        # Movimento que ameaça peças valiosas (novo)
        for dir in Consts.DIRECTIONS:
            threat_pos = (end[0] + dir[0], end[1] + dir[1])
            if (0 <= threat_pos[0] < 7 and 0 <= threat_pos[1] < 6):
                threat_piece = self.model.game_board[threat_pos[0], threat_pos[1]]
                if threat_piece != 0 and abs(threat_piece) >= 6:
                    if (piece < 0 and threat_piece > 0) or (piece > 0 and threat_piece < 0):
                        if self.model.is_self_rank_higher(piece, threat_piece):
                            score += 4
        
        return score


class RandomAI:
    def __init__(self, model: Model):
        self.model = model
        
    def get_best_move(self) -> tuple:
        """Retorna uma jogada aleatória válida"""
        # Obtém todas as jogadas possíveis para a IA (peças vermelhas)
        possible_moves = []
        for i in range(7):
            for j in range(6):
                piece = self.model.game_board[i, j]
                if piece < 0:  # Peça vermelha (IA)
                    moves = self.model.get_possible_moves((i, j))
                    if moves:
                        for move in moves:
                            possible_moves.append(((i, j), move))
        
        # Se não houver movimentos possíveis, retorna None
        if not possible_moves:
            return None
            
        # Escolhe um movimento aleatório
        return random.choice(possible_moves)  


class NegamaxAI:
    def __init__(self, model: Model, depth: int = 4):
        self.model = model
        self.max_depth = depth
        self.position_cache = {}
        
        # Valores das peças (otimizados)
        self.piece_values = {
            1: 6,   # Rato
            2: 3,   # Gato
            3: 4,   # Cão
            4: 5,   # Lobo
            5: 6,   # Leopardo
            6: 7,   # Tigre
            7: 8,   # Leão
            8: 10   # Elefante
        }
        
        # Posições das armadilhas
        self.traps = [
            (0, 2), (0, 4), (1, 3),  # Armadilhas vermelhas
            (6, 1), (6, 3), (5, 2)   # Armadilhas azuis
        ]
        
        # Posições das tocas
        self.dens = [(0, 3), (6, 2)]  # (vermelho, azul)
        
        # Limite de movimentos para poda
        self.move_limit = 20

    def evaluate_board(self) -> float:
        """Avalia o estado atual do tabuleiro"""
        board_key = str(self.model.game_board)
        if board_key in self.position_cache:
            return self.position_cache[board_key]
            
        score = 0
        
        # Avaliação de material
        for i in range(7):
            for j in range(6):
                piece = self.model.game_board[i, j]
                if piece != 0:
                    value = self.piece_values[abs(piece)]
                    if piece < 0:  # Peça vermelha (AI)
                        score += value
                    else:  # Peça azul
                        score -= value
        
        # Avaliação de posição
        for i in range(7):
            for j in range(6):
                piece = self.model.game_board[i, j]
                if piece != 0:
                    if piece < 0:  # Peça vermelha (AI)
                        dist_to_den = abs(i - self.dens[1][0]) + abs(j - self.dens[1][1])
                        score += (8 - dist_to_den) * 0.5
                    else:  # Peça azul
                        dist_to_den = abs(i - self.dens[0][0]) + abs(j - self.dens[0][1])
                        score -= (8 - dist_to_den) * 0.5
        
        # Avaliação de armadilhas
        for trap in self.traps:
            piece = self.model.game_board[trap[0], trap[1]]
            if piece != 0:
                if piece < 0 and trap in self.traps[:3]:  # Peça vermelha na armadilha azul
                    if self.model.is_piece_safe_in_trap(trap, piece):
                        score += 5
                    else:
                        score -= 25
                elif piece > 0 and trap in self.traps[3:]:  # Peça azul na armadilha vermelha
                    if self.model.is_piece_safe_in_trap(trap, piece):
                        score -= 5
                    else:
                        score += 25
        
        # Avaliação de mobilidade
        red_moves = len(self.get_all_possible_moves(True))
        blue_moves = len(self.get_all_possible_moves(False))
        if red_moves + blue_moves > 0:
            mobility_score = (red_moves - blue_moves) / (red_moves + blue_moves)
            score += mobility_score * 3
        
        # Avaliação de ameaças
        for i in range(7):
            for j in range(6):
                piece = self.model.game_board[i, j]
                if piece != 0:
                    moves = self.model.get_possible_moves((i, j))
                    if moves:
                        for move in moves:
                            target = self.model.game_board[move[0], move[1]]
                            if target != 0:
                                if piece < 0 and target > 0:  # Ameaça vermelha
                                    if abs(piece) >= abs(target):
                                        score += 2.5
                                elif piece > 0 and target < 0:  # Ameaça azul
                                    if abs(piece) >= abs(target):
                                        score -= 2.5
        
        # Avaliação de controle do centro
        center_positions = [(3, 2), (3, 3)]
        for pos in center_positions:
            piece = self.model.game_board[pos[0], pos[1]]
            if piece != 0:
                if piece < 0:  # Peça vermelha
                    score += 3
                else:  # Peça azul
                    score -= 3
        
        # Avaliação de proteção de peças valiosas
        for i in range(7):
            for j in range(6):
                piece = self.model.game_board[i, j]
                if piece != 0 and abs(piece) >= 7:  # Leão e Elefante
                    if piece < 0:  # Peça vermelha
                        if self.model.is_piece_safe_in_trap((i, j), piece):
                            score += 4
                    else:  # Peça azul
                        if self.model.is_piece_safe_in_trap((i, j), piece):
                            score -= 4
        
        self.position_cache[board_key] = score
        return score

    def get_all_possible_moves(self, is_ai_turn: bool) -> list:
        """Retorna todas as possíveis jogadas para o jogador atual"""
        moves = []
        for i in range(7):
            for j in range(6):
                piece = self.model.game_board[i, j]
                if (is_ai_turn and piece < 0) or (not is_ai_turn and piece > 0):
                    possible_moves = self.model.get_possible_moves((i, j))
                    if possible_moves:
                        moves.extend(((i, j), move) for move in possible_moves)
        
        moves.sort(key=lambda x: self.evaluate_move(x), reverse=is_ai_turn)
        return moves[:self.move_limit]

    def negamax(self, depth: int, alpha: float, beta: float, color: int) -> tuple:
        """Implementa o algoritmo Negamax com cortes alfa-beta"""
        if depth == 0 or self.model.is_win()[0]:
            return color * self.evaluate_board(), None
        
        moves = self.get_all_possible_moves(color > 0)
        if not moves:
            return color * self.evaluate_board(), None
            
        best_value = float('-inf')
        best_move = moves[0]
        
        for start, end in moves:
            # Faz a jogada
            piece_value = self.model.game_board[end[0], end[1]]
            self.model.game_board[end[0], end[1]] = self.model.game_board[start[0], start[1]]
            self.model.game_board[start[0], start[1]] = 0
            
            # Avalia a jogada
            value, _ = self.negamax(depth - 1, -beta, -alpha, -color)
            value = -value
            
            # Desfaz a jogada
            self.model.game_board[start[0], start[1]] = self.model.game_board[end[0], end[1]]
            self.model.game_board[end[0], end[1]] = piece_value
            
            if value > best_value:
                best_value = value
                best_move = (start, end)
            
            alpha = max(alpha, value)
            if alpha >= beta:
                break
                
        return best_value, best_move

    def evaluate_move(self, move: tuple) -> float:
        """Avalia um movimento específico para ordenação"""
        start, end = move
        score = 0
        
        # Captura de peça
        if self.model.game_board[end[0], end[1]] != 0:
            captured_piece = abs(self.model.game_board[end[0], end[1]])
            score += self.piece_values[captured_piece] * 2
        
        # Captura de peça em armadilha
        if end in self.traps:
            if self.model.game_board[end[0], end[1]] != 0:
                score += 30
        
        # Movimento para armadilha adversária
        if end in self.traps[:3] and self.model.game_board[start[0], start[1]] < 0:
            score += 5
        elif end in self.traps[3:] and self.model.game_board[start[0], start[1]] > 0:
            score += 5
        
        # Movimento em direção à toca adversária
        if self.model.game_board[start[0], start[1]] < 0:
            dist_before = abs(start[0] - self.dens[1][0]) + abs(start[1] - self.dens[1][1])
            dist_after = abs(end[0] - self.dens[1][0]) + abs(end[1] - self.dens[1][1])
            if dist_after < dist_before:
                score += 3
        else:
            dist_before = abs(start[0] - self.dens[0][0]) + abs(start[1] - self.dens[0][1])
            dist_after = abs(end[0] - self.dens[0][0]) + abs(end[1] - self.dens[0][1])
            if dist_after < dist_before:
                score += 3
        
        # Movimento para o centro
        center_positions = [(3, 2), (3, 3)]
        if end in center_positions:
            score += 2
        
        # Movimento que protege peças valiosas
        piece = self.model.game_board[start[0], start[1]]
        if abs(piece) >= 6:  # Tigre, Leão e Elefante
            if self.model.is_piece_safe_in_trap(end, piece):
                score += 3
        
        # Movimento que ameaça peças valiosas
        for dir in Consts.DIRECTIONS:
            threat_pos = (end[0] + dir[0], end[1] + dir[1])
            if (0 <= threat_pos[0] < 7 and 0 <= threat_pos[1] < 6):
                threat_piece = self.model.game_board[threat_pos[0], threat_pos[1]]
                if threat_piece != 0 and abs(threat_piece) >= 6:
                    if (piece < 0 and threat_piece > 0) or (piece > 0 and threat_piece < 0):
                        if self.model.is_self_rank_higher(piece, threat_piece):
                            score += 4
        
        return score

    def get_best_move(self) -> tuple:
        """Retorna a melhor jogada para a IA"""
        self.position_cache.clear()
        _, best_move = self.negamax(self.max_depth, float('-inf'), float('inf'), 1)
        return best_move


class RandomAI:
    def __init__(self, model: Model):
        self.model = model
        
    def get_best_move(self) -> tuple:
        """Retorna uma jogada aleatória válida"""
        # Obtém todas as jogadas possíveis para a IA (peças vermelhas)
        possible_moves = []
        for i in range(7):
            for j in range(6):
                piece = self.model.game_board[i, j]
                if piece < 0:  # Peça vermelha (IA)
                    moves = self.model.get_possible_moves((i, j))
                    if moves:
                        for move in moves:
                            possible_moves.append(((i, j), move))
        
        # Se não houver movimentos possíveis, retorna None
        if not possible_moves:
            return None
            
        # Escolhe um movimento aleatório
        return random.choice(possible_moves)  
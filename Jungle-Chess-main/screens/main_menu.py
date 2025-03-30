import pygame as pg
from assets.button import Button
import time
from assets.consts import Consts
from MVC.controller import Controller
import os
import sys

class MainMenu:
    def __init__(self) -> None:
        """Init main menu
        """
        pg.init()
        os.system('cls' if os.name == 'nt' else 'clear')
        # Init Clock
        self.clock = pg.time.Clock()

        # Screen Layout
        self.display = pg.display.set_mode((Consts.WINDOW_WIDTH, Consts.WINDOW_HEIGHT), 0, 32)
        
        # Botões centralizados
        button_width = 200
        button_height = 60
        button_spacing = 20
        start_y = 225
        
        self.pvp_button = Button("#4CAF50", Consts.WINDOW_WIDTH/2 - button_width/2, start_y, button_width, button_height, 
                                border_radius=15, text="Jogar PxP", font=Consts.button_font)
        self.pve_button = Button("#2196F3", Consts.WINDOW_WIDTH/2 - button_width/2, start_y + button_height + button_spacing, 
                                button_width, button_height, border_radius=15, text="Jogar PxIA", 
                                font=Consts.button_font)
        self.quit_button = Button("#f44336", Consts.WINDOW_WIDTH/2 - button_width/2, start_y + (button_height + button_spacing) * 2, 
                                 button_width, button_height, border_radius=15, text="Sair", 
                                 font=Consts.button_font)
        self.buttons = [self.pvp_button, self.pve_button, self.quit_button]
        
        # Textos centralizados
        self.texts = [
            Consts.main_title_font.render('Jungle Chess', True, Consts.TEXT_COLOR),
            Consts.sub_title_font.render('Elementos de Inteligência Artificial e Ciência de Dados', True, Consts.SUBTITLE_COLOR),
            Consts.label_font.render('por Afonso Santos, Hugo Ferreira e Xavier Teixeira', True, Consts.LABEL_COLOR)
        ]

        # Posicionamento dos textos
        title_y = 100
        self.text_rects = [
            self.texts[0].get_rect(center=(Consts.WINDOW_WIDTH/2, title_y)),
            self.texts[1].get_rect(center=(Consts.WINDOW_WIDTH/2, title_y + 40)),
            self.texts[2].get_rect(center=(Consts.WINDOW_WIDTH/2, title_y + 70))
        ]
        
        # Fundo com gradiente
        self.background_color = Consts.BACKGROUND_COLOR
        pg.display.update()
        time.sleep(0.01)
        self.display.fill(self.background_color)

        # Desenha os elementos
        for button in self.buttons:
            button.draw(self.display)

        for i in range(3):
            self.display.blit(self.texts[i], self.text_rects[i])
            
        self.main_menu_loop()
    
    def main_menu_loop(self) -> None:
        """Main Menu loop
        """
        while True:
            pg.display.update()     # Refresh display
            
            for button in self.buttons:
                button.draw(self.display)   # Draw button
            
            pos = pg.mouse.get_pos()    # Get mouse position
            
            for event in pg.event.get():
                """Handle events"""
                ev_type = event.type
                if ev_type == pg.QUIT:      # if event was quit, exit program
                    pg.quit()
                    sys.exit()
                
                elif ev_type == pg.MOUSEBUTTONDOWN:     # if event was mouse button down, handle press
                    if self.buttons[0].is_over(pos):    # Handle press on PvP Button
                        pg.display.quit()
                        time.sleep(0.2)
                        game = Controller(False)
                        
                    elif self.buttons[1].is_over(pos):  # Handle press on PvE Button
                        self.ai_selection_loop()
                    elif self.buttons[2].is_over(pos):  # Handle press on quit Button
                        pg.quit()
                        sys.exit()

    def draw_ai_selection_menu(self):
        """Desenha o menu de seleção de IA"""
        self.display.fill(Consts.BACKGROUND_COLOR)
        
        # Título
        title = Consts.main_title_font.render("Selecione o tipo de IA", True, Consts.TEXT_COLOR)
        title_rect = title.get_rect(center=(Consts.WINDOW_WIDTH/2, 100))
        self.display.blit(title, title_rect)
        
        # Botões centralizados
        button_width = 200
        button_height = 60
        button_spacing = 20
        total_buttons_height = (button_height * 3) + (button_spacing * 2)
        start_y = (Consts.WINDOW_HEIGHT - total_buttons_height) // 2
        
        self.random_button = Button("#DCDCDC", Consts.WINDOW_WIDTH/2 - button_width/2, start_y, button_width, button_height, 
                                    border_radius=15, text="Aleatório", font=Consts.button_font)
        self.minimax_button = Button("#4CAF50", Consts.WINDOW_WIDTH/2 - button_width/2, start_y + button_height + button_spacing, 
                                   button_width, button_height, border_radius=15, text="Minimax", 
                                   font=Consts.button_font)
        self.back_button = Button("#808080", Consts.WINDOW_WIDTH/2 - button_width/2, start_y + (button_height + button_spacing) * 2, 
                                 button_width, button_height, border_radius=15, text="Voltar", 
                                 font=Consts.button_font)
        
        # Desenha os botões
        self.random_button.draw(self.display)
        self.minimax_button.draw(self.display)
        self.back_button.draw(self.display)
        
        pg.display.flip()

    def draw_minimax_difficulty_menu(self):
        """Desenha o menu de seleção de dificuldade do Minimax"""
        self.display.fill(Consts.BACKGROUND_COLOR)
        
        # Título
        title = Consts.main_title_font.render("Selecione a Dificuldade", True, Consts.TEXT_COLOR)
        title_rect = title.get_rect(center=(Consts.WINDOW_WIDTH/2, 100))
        self.display.blit(title, title_rect)
        
        # Botões centralizados
        button_width = 200
        button_height = 60
        button_spacing = 20
        total_buttons_height = (button_height * 4) + (button_spacing * 3)
        start_y = (Consts.WINDOW_HEIGHT - total_buttons_height) // 2
        
        self.easy_button = Button("#4CAF50", Consts.WINDOW_WIDTH/2 - button_width/2, start_y, button_width, button_height, 
                                   border_radius=15, text="Fácil", font=Consts.button_font)
        self.medium_button = Button("#FFA500", Consts.WINDOW_WIDTH/2 - button_width/2, start_y + button_height + button_spacing, 
                                   button_width, button_height, border_radius=15, text="Médio", 
                                   font=Consts.button_font)
        self.hard_button = Button("#f44336", Consts.WINDOW_WIDTH/2 - button_width/2, start_y + (button_height + button_spacing) * 2, 
                                   button_width, button_height, border_radius=15, text="Difícil", 
                                   font=Consts.button_font)
        self.back_button = Button("#808080", Consts.WINDOW_WIDTH/2 - button_width/2, start_y + (button_height + button_spacing) * 3, 
                                 button_width, button_height, border_radius=15, text="Voltar", 
                                 font=Consts.button_font)
        
        # Desenha os botões
        self.easy_button.draw(self.display)
        self.medium_button.draw(self.display)
        self.hard_button.draw(self.display)
        self.back_button.draw(self.display)
        
        pg.display.flip()
        
    def ai_selection_loop(self):
        """Loop do menu de seleção de IA"""
        while True:
            self.draw_ai_selection_menu()
            
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
                    
                if event.type == pg.MOUSEBUTTONDOWN:
                    mouse_pos = pg.mouse.get_pos()
                    
                    # Verifica clique nos botões
                    if self.random_button.is_over(mouse_pos):
                        game = Controller(True, "random")
                        return
                    elif self.minimax_button.is_over(mouse_pos):
                        self.minimax_difficulty_loop()
                        return
                    elif self.back_button.is_over(mouse_pos):
                        # Limpa a tela e redesenha o menu principal
                        self.display.fill(Consts.BACKGROUND_COLOR)
                        for button in self.buttons:
                            button.draw(self.display)
                        for i in range(3):
                            self.display.blit(self.texts[i], self.text_rects[i])
                        pg.display.flip()
                        return
                        
            self.clock.tick(60)

    def minimax_difficulty_loop(self):
        """Loop do menu de seleção de dificuldade do Minimax"""
        while True:
            self.draw_minimax_difficulty_menu()
            
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
                    
                if event.type == pg.MOUSEBUTTONDOWN:
                    mouse_pos = pg.mouse.get_pos()
                    
                    # Verifica clique nos botões
                    if self.easy_button.is_over(mouse_pos):
                        game = Controller(True, "minimax", 2)
                        return
                    elif self.medium_button.is_over(mouse_pos):
                        game = Controller(True, "minimax", 3)
                        return
                    elif self.hard_button.is_over(mouse_pos):
                        game = Controller(True, "minimax", 4)
                        return
                    elif self.back_button.is_over(mouse_pos):
                        return  # Volta para o menu de seleção de IA
                        
            self.clock.tick(60)
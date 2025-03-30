# Dou Shou Qi (Xadrez da Selva) IA
> Por Yoav Amitai
> 

<img style="float: left" src="https://ancientchess.com/graphics-rules/dou_shou_qi_jungle_game-board.jpg">
Este projeto visa implementar o jogo tradicional chinês _Dou Shou Qi_ (鬥獸棋, ou Xadrez da Selva) usando Python, e adicionar um algoritmo minimax como base para um oponente computadorizado.

O projeto usa bibliotecas Python, tais como:
 1. numPy
 2. pygame

___

O jogo utiliza um padrão de design de software MVC:
 1. **model.py** armazena, modifica e usa as estruturas de dados do jogo - um array 2D representando o rank das peças e sua posição no tabuleiro.
 2. **view.py** implementa a representação visual do jogo, usando _pygame_ como biblioteca gráfica.
 3. **controller.py** gere o fluxo do jogo, as comunicações entre a view e o model.


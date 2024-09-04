import os
import pygame
import torch
from torch import nn
import torch.nn.functional as F
from game import Game


class CheckersAI(nn.Module):
    def __init__(self):
        super(CheckersAI, self).__init__()
        self.fc1 = nn.Linear(64, 32)
        self.fc2 = nn.Linear(32, 16)
        self.fc3 = nn.Linear(16, 8)
        self.fc4 = nn.Linear(8, 4)

    def forward(self, x):
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        x = F.relu(self.fc3(x))
        x = self.fc4(x)
        return x

    def save(self, file_name='checkersAI.pth'):
        model_folder_path = 'models'
        if not os.path.exists(model_folder_path):
            os.makedirs(model_folder_path)
        file_path = os.path.join(model_folder_path, file_name)
        torch.save(self.state_dict(), file_path)




FPS = 60
WINDOW = pygame.display.set_mode((800, 800))
pygame.display.set_caption('Checkers')

def get_row_col_from_mouse(pos):
    x, y = pos
    row = y // 100
    col = x // 100
    return row, col

def game():
    run = True
    clock = pygame.time.Clock()
    game = Game(WINDOW)
    turn = 'white'

    while run:
        clock.tick(FPS)

        if game.winner() != None:
            print(game.winner())
            run = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if game.turn == 'white':
                    pos = pygame.mouse.get_pos()
                    row, col = get_row_col_from_mouse(pos)
                    game.select(row, col)

                elif game.turn == 'black':




                    data = torch.empty(64)
                    for row in range(8):
                        for col in range(8):
                            if game.board.board[row][col] == 0:
                                data[row*8+col] = 0
                            else:
                                data[row*8+col] = game.board.board[row][col].value()
                    data = data.to(torch.float32)
                    choice = model(data)
                    print(choice)
                    game.select(choice[0], choice[1])

        game.update()

    pygame.quit()







model = CheckersAI()
optimizer = torch.optim.Adam(model.parameters(), lr=0.01)

game()
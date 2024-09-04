import pygame


class Piece:
    def __init__(self, row, col, color):
        self.row = row
        self.col = col
        self.color = color
        self.king = False
        self.x = 0
        self.y = 0
        self.radius = 40
        self.direction = 1 if self.color == 'black' else -1
    
    def calc_pos(self):
        self.x = self.col * 100 + 50
        self.y = self.row * 100 + 50

    def draw(self, window):
        pygame.draw.circle(window, (128,128,128), (self.x, self.y), self.radius + 2)

        if self.color == 'white':
            pygame.draw.circle(window, (255, 255, 255), (self.x, self.y), self.radius)
        else:
            pygame.draw.circle(window, (0, 0, 0), (self.x, self.y), self.radius)

        if self.king:
            pygame.draw.circle(window, (255, 0, 0), (self.x, self.y), self.radius - 25)

    def move(self, row, col):
        self.row = row
        self.col = col
        self.x = self.col * 100
        self.y = self.row * 100

    def make_king(self):
        self.king = True

    def value(self):
        if self.color == 'white':
            if self.king:
                return -2
            return -1
        elif self.color == 'black':
            if self.king:
                return 2
            return 1
        
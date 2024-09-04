import pygame
from board import Board

class Game:
    def __init__(self, window):
        self.reset()
        self.window = window

    def update(self):
        self.board.draw(self.window)
        self.draw_valid_moves(self.valid_moves)
        pygame.display.update()

    def winner(self):
        return self.board.winner()
    
    def reset(self):
        self.board = Board()
        self.turn = 'white'
        self.selected = None
        self.valid_moves = {}
    
    def select(self, row, col):
        if self.selected:
            result = self._move(row, col)
            if not result:
                self.selected = None
                self.select(row, col)
        
        piece = self.board.get_piece(row, col)
        if piece != 0 and piece.color == self.turn:
            self.selected = piece
            self.valid_moves = self.board.get_valid_moves(piece)
            return True
        
        return False
    
    def _move(self, row, col):
        piece = self.board.get_piece(row, col)
        if self.selected and piece == 0 and (row, col) in self.valid_moves:
            self.board.move(self.selected, row, col)
            skipped = self.valid_moves[(row, col)]
            if skipped:
                self.board.remove_pieces(skipped)
            self.change_turn()
        else:
            return False
        return True
    
    def draw_valid_moves(self, moves):
        for move in moves:
            row, col = move
            pygame.draw.circle(self.window, (0, 255, 0), (col * 100 + 50, row * 100 + 50), 45)
    
    def change_turn(self):
        self.valid_moves = {}
        if self.turn == 'white':
            self.turn = 'black'
        else:
            self.turn = 'white'


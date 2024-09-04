import pygame
from piece import Piece

class Board:
    def __init__(self):
        self.board = []
        self.white_count, self.black_count = 12, 12
        self.white_kings, self.black_kings = 0, 0
        self.create_board()
    
    def draw_squares(self, window):
        window.fill((0, 0, 0))
        for row in range(8):
            for col in range(row % 2, 8, 2):
                pygame.draw.rect(window, (255, 255, 255), (row * 100, col * 100, 100, 100))

    def move(self, piece:Piece, row, col):
        self.board[piece.row][piece.col], self.board[row][col] = self.board[row][col], self.board[piece.row][piece.col]
        piece.move(row, col)

        if row == 0 or row == 7:
            piece.make_king()
            if piece.color == 'white':
                self.white_kings += 1
            else:
                self.black_kings += 1
        
    def get_piece(self, row, col):
        return self.board[row][col]
    
    def create_board(self):
        for row in range(8):
            self.board.append([])
            for col in range(8):
                if col % 2 == ((row + 1) % 2):
                    if row < 3:
                        self.board[row].append(Piece(row, col, 'black'))
                    elif row > 4:
                        self.board[row].append(Piece(row, col, 'white'))
                    else:
                        self.board[row].append(0)
                else:
                    self.board[row].append(0)
    
    def draw(self, window):
        self.draw_squares(window)
        for row in self.board:
            for piece in row:
                if piece != 0:
                    piece.calc_pos()
                    piece.draw(window)
    
    def remove_pieces(self, pieces):
        for piece in pieces:
            self.board[piece.row][piece.col] = 0
            if piece.color == 'white':
                self.white_count -= 1
            elif piece.color == 'black':
                self.black_count -= 1
            if piece.king:
                if piece.color == 'white':
                    self.white_kings -= 1
                elif piece.color == 'black':
                    self.black_kings -= 1
    
    def winner(self):
        if self.white_count <= 0:
            return 'black'
        elif self.black_count <= 0:
            return 'white'
        else:
            return None

    def get_valid_moves(self, piece:Piece):
        moves = {}
        left = piece.col - 1
        right = piece.col + 1
        row = piece.row

        if piece.color == 'white' or piece.king:
            moves.update(self._traverse_left(row - 1, max(row - 3, -1), -1, piece.color, left))
            moves.update(self._traverse_right(row - 1, max(row - 3, -1), -1, piece.color, right))
        if piece.color == 'black' or piece.king:
            moves.update(self._traverse_left(row + 1, min(row + 3, 8), 1, piece.color, left))
            moves.update(self._traverse_right(row + 1, min(row + 3, 8), 1, piece.color, right))
        
        return moves
    
    def _traverse_left(self, start, stop, step, color, left, skipped=[]):
        moves = {}
        last = []
        for r in range(start, stop, step):
            if left < 0:
                break
            current = self.board[r][left]
            if current == 0:
                if skipped and not last:
                    break
                elif skipped:
                    moves[(r, left)] = last + skipped
                else:
                    moves[(r, left)] = last
                if last:
                    if step == -1:
                        row = max(r - 3, 0)
                    else:
                        row = min(r + 3, 8)
                    moves.update(self._traverse_left(r + step, row, step, color, left - 1, skipped=last))
                    moves.update(self._traverse_right(r + step, row, step, color, left + 1, skipped=last))
                break
            elif current.color == color:
                break
            else:
                last = [current]
            left -= 1
        return moves
    
    def _traverse_right(self, start, stop, step, color, right, skipped=[]):
        moves = {}
        last = []
        for r in range(start, stop, step):
            if right >= 8:
                break
            current = self.board[r][right]
            if current == 0:
                if skipped and not last:
                    break
                elif skipped:
                    moves[(r, right)] = last + skipped
                else:
                    moves[(r, right)] = last
                if last:
                    if step == -1:
                        row = max(r - 3, 0)
                    else:
                        row = min(r + 3, 8)
                    moves.update(self._traverse_left(r + step, row, step, color, right - 1, skipped=last))
                    moves.update(self._traverse_right(r + step, row, step, color, right + 1, skipped=last))
                break
            elif current.color == color:
                break
            else:
                last = [current]
            right += 1
        return moves
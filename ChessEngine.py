"""
Responsible for storing all the information about the current state of a chess game. it will also be
responsible for determining the valid moves at the current state. It will also keep a move log.
"""

# This program is a chess game. It is a simple chess game that is played on a chess board. The board is 8x8 squares.

# white pieces start the game. ie move first.
# Pieces are the pawn, rook, knight, bishop, queen, and king.
# Pawn: can move forward 1 or 2 squares if not already moved, can be blocked by other pieces.
# The pawn can capture diagonally 1 square in forward direction.
# the pawn can eat en passant if the enemy pawn is on the adjacent square after have moved 2 squares.
# Rook: can move any number of squares in any direction, can be blocked by other pieces.
# knight can move in an L shape:
#   - 3 squares in one direction and 2 squares in an orthogonal direction
#   - 2 squares in one direction and 3 squares in an orthogonal direction
# Bishop: can move any number of squares diagonally.
# Queen: can move any number of squares in any direction. (This is the same as the bishop + the rook.)
# King: can move only 1 square in any direction, can be blocked by other pieces.
# if the king and the rook haven't already moved, the player can castle.
# The king can not move into check. So a king can't check the other king.
# if the king is in check, the player must move the king out of check.
# if the king can't move out of check, the game is over.
# if the king can't move but without being in check, the game is a pat.
# if both players can't checkmate, the game is a draw.
# if a pattern is repeated 3 times, the game is a draw.


# TODO: Add in piece highlighting and move suggestions
# TODO: Add in AI


class GameState:
    def __init__(self):
        # Board is a 8*8 2D list, each element of the list has 2 characters.
        # The 1st character is the color of the piece, 'b' or 'w'
        # The 2nd char is the type of the piece
        # "--" is a blank square (empty space/square with no pieces on it)
        # (Can be also done with numpy arrays (for IA purposes))
        self.board = [
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bP", "bP", "bP", "bP", "bP", "bP", "bP", "bP"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["wP", "wP", "wP", "wP", "wP", "wP", "wP", "wP"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]
        ]
        self.whiteToMove = True
        self.color = "w"
        self.moveLog = []

    def make_move(self, move):  # TODO: add in castling, en passant, pawn promotion.
        self.board[move.start_row][move.start_col] = "--"
        self.board[move.end_row][move.end_col] = move.piece_moved
        self.moveLog.append(move)  # Add move to move log, so we can undo it later if needed.
        self.whiteToMove = not self.whiteToMove  # Switch to other player's turn.

    def getValidMoves(self):
        """
        All moves considering checks
        """
        # WorkInProgress
        return self.getAllpossibleMoves()  # for now, we will not worry about checks and co.

    def getAllpossibleMoves(self):
        moves = self.get_possibles_moves()
        for row in range(8):
            for col in range(8):
                turn = self.board[row][col][0]
                if (turn == "w" and self.whiteToMove) and (turn == "b" and not self.whiteToMove):
                    piece_name = self.board[row][col][1]
                    if piece_name == "P":
                        self.getPawnMoves(row, col, moves)
                    elif piece_name == "R":
                        self.getRookMoves(row, col, moves)
                    elif piece_name == "N":
                        self.getKnightMoves(row, col, moves)
                    elif piece_name == "B":
                        self.getBishopMoves(row, col, moves)
                    elif piece_name == "Q":
                        self.getQueenMoves(row, col, moves)
                    elif piece_name == "K":
                        self.getKingMoves(row, col, moves)
        return moves


    def get_possibles_moves(self):
        """
        Get all the possibles moves for the current player.
        """
        possibles_moves = []
        for row in range(8):
            for col in range(8):
                if self.board[row][col] != "--":
                    piece = self.board[row][col]
                    if piece[0] == "w" and self.whiteToMove:
                        possibles_moves += self.get_possibles_moves_for_piece(row, col)
                    elif piece[0] == "b" and not self.whiteToMove:
                        possibles_moves += self.get_possibles_moves_for_piece(row, col)
        return possibles_moves

    def is_in_check(self):
        """
        Check if the current player is in check:
        """
        if self.color == "w":
            king_row = self.find_king("wK")[0]
            king_col = self.find_king("wK")[1]
        else:
            king_row = self.find_king("wK")[0]
            king_col = self.find_king("wK")[1]
        for row in range(8):
            for col in range(8):
                if self.board[row][col][0] != self.color:
                    valid_moves = self.get_possibles_moves_for_piece(row, col)
                    for move in valid_moves:
                        if move.end_row == king_row and move.end_col == king_col:
                            return True
        return False

    def find_king(self, color):
        """
        Find the row and column of the king of a given color.
        """
        for row in range(8):
            for col in range(8):
                if self.board[row][col] == color + "K":
                    return row, col
        return Exception("No king found")

    def get_possibles_moves_for_piece(self, row, col):
        """
        Get all the possibles moves for a piece at a given row and column.
        """
        possibles_moves = []
        piece = self.board[row][col]
        if piece[1] == "P":
            possibles_moves += self.get_possibles_moves_for_pawn(row, col)
        elif piece[1] == "R":
            possibles_moves += self.get_possibles_moves_for_rook(row, col)
        elif piece[1] == "N":
            possibles_moves += self.get_possibles_moves_for_knight(row, col)
        elif piece[1] == "B":
            possibles_moves += self.get_possibles_moves_for_bishop(row, col)
        elif piece[1] == "Q":
            possibles_moves += self.get_possibles_moves_for_queen(row, col)
        elif piece[1] == "K":
            possibles_moves += self.get_possibles_moves_for_king(row, col)
        return possibles_moves

    def getPawnMoves(self, row, col, moves):
        pass

    def get_possibles_moves_for_pawn(self, row, col):
        """
        Get all the possibles moves for a pawn at a given row and column.
        """
        possibles_moves = []
        if self.whiteToMove:
            if row == 1 and self.board[row + 1][col] == "--" and self.board[row + 2][col] == "--":
                possibles_moves.append(Move(row+2, col, self.board))
            if self.board[row+1][col+1][0] == "b":
                possibles_moves.append(Move(row+1, col+1, self.board))
            if self.board[row + 1][col - 1][0] == "b":
                possibles_moves.append(Move(row + 1, col - 1, self.board))
            possibles_moves.append(Move(row+1, col, self.board))
        else:
            if row == 6:
                possibles_moves.append(Move(row, col, self.board))
            if self.board[row - 1][col + 1][0] == "w":
                possibles_moves.append(Move(row - 1, col + 1, self.board))
            if self.board[row - 1][col - 1][0] == "w":
                possibles_moves.append(Move(row - 1, col - 1, self.board))
            possibles_moves.append(Move(row, col, self.board))
        return possibles_moves

    def get_possibles_moves_for_rook(self, row, col):
        """
        Get all the possibles moves for a rook at a given row and column.
        """
        possibles_moves = []
        #prev_pos = self.board[row][col]
        for i in range(row + 1, 8):
            if self.board[i][col] == "--":
                possibles_moves.append(Move(row+i, col, self.board))
            else:
                break
        for i in range(row - 1, -1, -1):
            if self.board[i][col] == "--":
                possibles_moves.append(Move(row+i, col, self.board))
            else:
                break
        for i in range(col + 1, 8):
            if self.board[row][i] == "--":
                possibles_moves.append(Move(row, col+i, self.board))
            else:
                break
        for i in range(col - 1, -1, -1):
            if self.board[row][i] == "--":
                possibles_moves.append(Move(row, col+i, self.board))
            else:
                break
        return possibles_moves

    def getRookMoves(self, row, col, moves):
        pass

    def get_possibles_moves_for_knight(self, row, col):
        """
        Get all the possibles moves for a knight at a given row and column.
        """
        possibles_moves = []
        if row - 3 >= 0 and col - 2 >= 0:
            possibles_moves.append(Move(row-3, col-2, self.board))
        if row - 3 >= 0 and col + 2 < 8:
            possibles_moves.append(Move(row-3, col+2, self.board))
        if row - 2 >= 0 and col - 3 >= 0:
            possibles_moves.append(Move(row-2, col-3, self.board))
        if row - 2 >= 0 and col + 3 < 8:
            possibles_moves.append(Move(row-2, col+3, self.board))
        if row + 2 < 8 and col - 3 >= 0:
            possibles_moves.append(Move(row+2, col-3, self.board))
        if row + 2 < 8 and col + 3 < 8:
            possibles_moves.append(Move(row+2, col+3, self.board))
        if row + 3 < 8 and col - 2 >= 0:
            possibles_moves.append(Move(row+3, col-2, self.board))
        if row + 3 < 8 and col + 2 < 8:
            possibles_moves.append(Move(row+3, col+2, self.board))
        return possibles_moves

    def getKnightMoves(self, row, col, moves):
        pass

    def get_possibles_moves_for_bishop(self, row, col):
        """
        Get all the possibles moves for a bishop at a given row and column.
        """
        possibles_moves = []
        for i in range(row + 1, 8):
            if col + 1 < 8:
                if self.board[i][col + 1] == "--":
                    possibles_moves.append(Move(row+i, col + i, self.board))
                else:
                    break
            else:
                break
        for i in range(row - 1, -1, -1):
            if col + 1 < 8:
                if self.board[i][col + 1] == "--":
                    possibles_moves.append(Move(row+i, col + i, self.board))
                else:
                    break
            else:
                break
        for i in range(row + 1, 8):
            if col - 1 >= 0:
                if self.board[i][col - 1] == "--":
                    possibles_moves.append(Move(row+i, col - i, self.board))
                else:
                    break
            else:
                break
        for i in range(row - 1, -1, -1):
            if col - 1 >= 0:
                if self.board[i][col - 1] == "--":
                    possibles_moves.append(Move(row+i, col - i, self.board))
                else:
                    break
            else:
                break
        return possibles_moves

    def getBishopMoves(self, row, col, moves):
        pass

    def get_possibles_moves_for_queen(self, row, col):
        """
        Get all the possibles moves for a queen at a given row and column.
        """
        possibles_moves = self.get_possibles_moves_for_rook(row, col) + self.get_possibles_moves_for_bishop(row, col)
        return possibles_moves

    def getQueenMoves(self, row, col, moves):
        pass

    def get_possibles_moves_for_king(self, row, col):
        """
        Get all the possibles moves for a king at a given row and column.
        """
        possibles_moves = []
        if self.color == "w":
            if row == 7 and col == 4:
                if self.board[7][3] == "--" and self.board[7][2] == "--" and self.board[7][1] == "--" and self.board[7][0] == "wR":
                    possibles_moves.append(Move(row, col, 7, 2))
                if self.board[7][5] == "--" and self.board[7][6] == "--" and self.board[7][7] == "wR":
                    possibles_moves.append(Move(row, col, 7, 6))
        if self.color == "b":
            if row == 0 and col == 4:
                if self.board[0][3] == "--" and self.board[0][2] == "--" and self.board[0][1] == "--" and self.board[0][0] == "bR":
                    possibles_moves.append(Move(row, col, 0, 2))
                if self.board[0][5] == "--" and self.board[0][6] == "--" and self.board[0][7] == "bR":
                    possibles_moves.append(Move(row, col, 0, 6))
        # ↑ check if the king have space to castle (for now we don't check if the king has already moved) TODO: check if the king has already moved
        if row - 1 >= 0:
            if col - 1 >= 0:
                possibles_moves.append(Move(row - 1, col - 1, self.board))
            if col + 1 < 8:
                possibles_moves.append(Move(row - 1, col + 1, self.board))
            possibles_moves.append(Move(row - 1, col, self.board))
        if row + 1 < 8:
            if col - 1 >= 0:
                possibles_moves.append(Move(row + 1, col - 1, self.board))
            if col + 1 < 8:
                possibles_moves.append(Move(row + 1, col + 1, self.board))
            possibles_moves.append(Move(row + 1, col, self.board))
        if col - 1 >= 0:
            possibles_moves.append(Move(row, col - 1, self.board))
        if col + 1 < 8:
            possibles_moves.append(Move(row, col + 1, self.board))
        return possibles_moves

    def getKingMoves(self, row, col, moves):
        pass

    def switch_turn(self):
        self.whiteToMove = not self.whiteToMove
        self.color = "b" if self.whiteToMove else "w"

    def undo_move(self):
        """
        Undo the last move.
        """
        if len(self.moveLog) > 0:
            move = self.moveLog.pop()
            self.board[move.start_row][move.start_col] = move.piece_moved
            self.board[move.end_row][move.end_col] = move.piece_captured
            #TODO: undo IA suggestions (display the previous suggestions)
            GameState.switch_turn(self)


# 2 ways to visualize the pieces moves : chess notation method or "2 strings method" (I will specify later.)
class Move:  # TODO: add in castling, en passant, pawn promotion and maybe check, checkmate, stalemate and draw.
    # maps key to values.
    # key : value
    ranks_to_row = {"1": 7, "2": 6, "3": 5, "4": 4, "5": 3, "6": 2, "7": 1, "8": 0} # i'm happy you understand this my friend Github Copilot :D
    rows_to_rank = {v: k for k, v in ranks_to_row.items()}
    files_to_col = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7}
    cols_to_file = {v: k for k, v in files_to_col.items()}

    def __init__(self, start_sq, end_sq, board):
        self.start_row = start_sq[0]
        self.start_col = start_sq[1]
        self.end_row = end_sq[0]
        self.end_col = end_sq[1]
        self.board = board
        self.piece_moved = board[self.start_row][self.start_col]
        self.piece_captured = board[self.end_row][self.end_col]
        self.moveID = self.start_row * 1000 + self.start_col * 100 + self.end_row * 10 + self.end_col  # a unique ID for each move. (between 0 and 7777)
        print(self.moveID)  # for debug purpose TODO: remove this line.

    def __eq__(self, other):
        if isinstance(other, Move):
            return self.moveID == other.moveID
        return False

    def get_chess_notation(self):
        # TODO: make my own chess notation:
        #   - display the move number follow by a dot and a space (ex: "1. ")
        #   - add the piece that moved (ex: "1. wN")
        #   - add the piece location (ex: "1. wNg1")
        #   - add /O-O-O for big castle (ex: "wKe1/O-O-O") or /O-O for small castle (ex: "wKe1/O-O")
        #   - add x after the piece name if it eat another piece and write the piece ate (ex: "3. wNf3x")
        #   - add the piece that ate (ex: "3. wNf6xwP")
        #   - add + when a piece checks the other king (ex: "9. wNh5+")
        #   - add # after the name piece when the piece checkmate the other king (ex: "9. wNh5#)
        #   - add -> after the piece location or consequence (ex: "1. wNg1->" , "9. wNh5+->")
        #   - add the update location of the piece (ex: "1. wNg1->f3")
        #   - if the piece is promoted add = after update location followed by the new piece type(ex: "9. wPc7->c8=Q")
        #   - same process for black pieces(ex: "9. wNh5xbP+->f6 bBg7xwN->f6")

        # It will be like this:
        """return f"{turn}. {w_piece_moved}{w_start_sq}{w_castle}{w_eat_mark}{w_eaten}{w_check}->{w_end_sq}{w_promotion}" \
               f" {b_piece_moved}{b_start_sq}{b_castle}{b_eat_mark}{b_eaten}{w_check}->{b_end_sq}{b_promotion}" """

        return self.get_rank_file(self.start_row, self.start_col) + self.get_rank_file(self.end_row, self.end_col)

    def get_rank_file(self, r, c):
        return self.cols_to_file[c] + self.rows_to_rank[r]


# TODO: Add in piece highlighting and move suggestions
def highlight_piece(screen, gs, fromRow, fromCol):
    pass

# TODO: Add in AI
def get_ai_move(gs):
    pass
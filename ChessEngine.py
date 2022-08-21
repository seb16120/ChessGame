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

# TODO: Add in move log
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
        self.moveLog = []

    def make_move(self, move):
        self.board[move.start_row][move.start_col] = "--"
        self.board[move.end_row][move.end_col] = move.piece_moved
        self.moveLog.append(move)  # Add move to move log, so we can undo it later if needed.
        self.whiteToMove = not self.whiteToMove  # Switch to other player's turn.


# 2 ways to visualize the pieces moves : chess notation method or "2 strings method" (I will specify later.)
class Move:
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
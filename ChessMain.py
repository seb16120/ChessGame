"""
The main driver file. it will be responsible for handling user input and displaying the current GameState object.
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

# TODO: Add in move piece function  # almost done
# TODO: Add in game over screen
# TODO: Add in game reset
# TODO: Add in game save and load

import pygame as p
import ChessEngine


WIDTH = HEIGHT = 512
DIMENSION = 8
SQ_SIZE = HEIGHT // DIMENSION
MAX_FPS = 15 #for animations later on
IMAGES = {}


def load_images():
    """
    initialize a global dict of images. This will be called exactly once in the main
    """
    pieces = ['wP', 'wR', 'wN', 'wB', 'wK', 'wQ', 'bP', 'bR', 'bN', 'bB', 'bK', 'bQ']
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load("chess pieces/Chess pieces package/images/" + piece + ".png"), (SQ_SIZE, SQ_SIZE))

    #Note: We can access an image by saying 'IMAGES['wp']'





def main():
    """
    The main driver for our code. This will handle user input and updating the graphics
    """
    p.init()
    screen = p.display.set_mode((WIDTH, HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color("White"))
    gs = ChessEngine.GameState()
    load_images()  # only do this once, before the while loop
    running = True
    sq_selected = (None, None) # keep track of the last square the user clicked on. (row, col)
    player_clicks = []  # keep track of the player's clicks. (two tuples: [sq_(previously)_selected, sq_selected])
    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            elif e.type == p.MOUSEBUTTONDOWN:
                # get the mouse position:
                mouse_pos = p.mouse.get_pos()
                # get the row and column of the mouse position:
                row = mouse_pos[1] // SQ_SIZE
                col = mouse_pos[0] // SQ_SIZE
                # if the player clicked on the same square, unselect it and clear the player_clicks list:
                if sq_selected == (row, col):
                    sq_selected = (None, None)
                    player_clicks = []
                # else the player didn't click on the same square, save it to sq_selected:
                else:
                    sq_selected = (row, col)
                    player_clicks.append(sq_selected)  # append for both 1st and 2nd click.
                # if it was the second click, check if the player clicked on a valid move:
                # TODO: verify that the player clicked on a valid move
                if len(player_clicks) == 2:
                    move = ChessEngine.Move(player_clicks[0], player_clicks[1], gs.board)
                    print(move.get_chess_notation())
                    gs.make_move(move)
                    sq_selected = (None, None)  # reset the selected square
                    player_clicks = []  # reset the player_clicks list

        draw_game_state(screen, gs)
        clock.tick(MAX_FPS)
        p.display.flip()


def draw_game_state(screen, gs):
    """
    Responsible for all the graphic with a current game state.
    """
    draw_board(screen)  # draw squares on the board
    # add in piece highlighting or move suggestions (later)
    draw_pieces(screen, gs.board)  # draw pieces on top of those squares


def draw_board(screen):
    """
    Draw the board squares on the pygame screen.
    :param screen: the pygame screen to draw on
    :return: None
    """
    colors = [p.Color("White"), p.Color("Gray")]
    for r in range (DIMENSION):
        for c in range(DIMENSION):
            color = colors[((r+c) % 2)]
            p.draw.rect(screen, color, p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))


def draw_pieces(screen, board):
    """
    Draw the pieces on the board using the current GameState object (GameState.board attribute)
    :param screen: the pygame screen to draw on
    :param board: the current GameState.board attribute
    :return: None
    """
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = board[r][c]
            if piece != "--":
                screen.blit(IMAGES[piece], p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))


# TODO: Add in move piece function
def movePiece(gs, fromRow, fromCol, toRow, toCol):
    gs.board[toRow][toCol] = gs.board[fromRow][fromCol]
    gs.board[fromRow][fromCol] = "--"
    gs.whiteToMove = not gs.whiteToMove
    gs.moveLog.append((fromRow, fromCol, toRow, toCol))
    return gs

# TODO: Add in draw move suggestion
def drawMoveSuggestions(screen, gs, fromRow, fromCol):
    pass


def getValidMoves(gs, fromRow, fromCol):
    pass

# TODO: Add in game over screen
def gameOver(screen, gs):
    pass

# TODO: Add in game reset
def resetGame(screen, gs):
    pass

# TODO: Add in game save and load
def saveGame(gs):
    pass

def loadGame(gs):
    pass

# TODO: Add in move log
def updateMoveLog(screen, gs, fromRow, fromCol, toRow, toCol):
    pass



if __name__ == "__main__":
    main()



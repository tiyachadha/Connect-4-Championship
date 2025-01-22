# hey so this is the basic connect 4 logic. there are only fuctions present here


import numpy as np
import pygame
import sys
import math
import random

# global BLUE, BLACK, RED, YELLOW, ROW_COUNT, COULMN_COUNT,PLAYER,AI,AI_PIECE,PLAYER_PIECE, WINDOW_LENGTH

BLUE = (0,0,255)
LIGHT_BLUE = (178,106,215)
BLACK = (0,0,0)
RED = (255,0,0)
YELLOW =(255,255,0)


ROW_COUNT = 6
COULMN_COUNT = 7

PLAYER = 0
AI = 1

PLAYER_PIECE = 1
AI_PIECE = 2

WINDOW_LENGTH = 4

def create_board():
    board = np.zeros((ROW_COUNT,COULMN_COUNT))
    return board

def drop_piece(board, row , col, piece):
    board[row][col] = piece

def is_valid_location(board,col):
    return board[ROW_COUNT-1][col] == 0 

def get_next_open_row(board,col):
    for r in range(ROW_COUNT):
        if board[r][col] == 0:
            return r

def print_board(board):
    print(np.flip(board, 0))

def winning_move(board, piece):
    # Check all horizontal wins 
    for c in range(COULMN_COUNT-3):
        for r in range(ROW_COUNT):
            if board[r][c] == piece and board[r][c+1] == piece and board[r][c+2] == piece and board[r][c+3] == piece:
                return [(r, c), (r, c+1), (r, c+2), (r, c+3)]
            
    # Check all vertical wins
    for c in range(COULMN_COUNT):
        for r in range(ROW_COUNT-3):
            if board[r][c] == piece and board[r+1][c] == piece and board[r+2][c] == piece and board[r+3][c] == piece:
                return [(r, c), (r+1, c), (r+2, c), (r+3, c)]
            
    # Check for positively sloped diagonals
    for c in range(COULMN_COUNT-3):
        for r in range(ROW_COUNT-3):
            if board[r][c] == piece and board[r+1][c+1] == piece and board[r+2][c+2] == piece and board[r+3][c+3] == piece:
                return [(r, c), (r+1, c+1), (r+2, c+2), (r+3, c+3)] 
            
    # Check for negatively sloped Diagonals
    for c in range(COULMN_COUNT-3):
        for r in range(3,ROW_COUNT):
            if board[r][c] == piece and board[r-1][c+1] == piece and board[r-2][c+2] == piece and board[r-3][c+3] == piece:
                return [(r, c), (r-1, c+1), (r-2, c+2), (r-3, c+3)]

    return None 



#########     Scoring the Columns and Choosing Best One    ##############
#########################################################################
#########################################################################

def evaluate_window(window, piece):
    score = 0
    opp_piece = PLAYER_PIECE
    if piece == PLAYER_PIECE:
        opp_piece = AI_PIECE


    if window.count(piece) == 4:
        score += 100
    elif window.count(piece) == 3 and window.count(0) == 1:
        score += 10
    elif window.count(piece) == 2 and window.count(0) == 2:
        score += 5

    if window.count(opp_piece) == 2 and window.count(0) == 2:
        score -= 7

    if window.count(opp_piece) == 3 and window.count(0) == 1:
        score -= 40     # we prefer blocking opponents 3 in a row over making out own 3 in a row

    return score


def score_position(board,piece):

    score = 0

    ## Scoring the Centre Columns
    center_array = [int(i) for i in list(board[:,COULMN_COUNT//2])]
    center_count = center_array.count(piece)
    score += center_count * 6


    ## Score Horizontal
    for r in range(ROW_COUNT):
        row_array = [int(i) for i in list(board[r,:])]         # Create a list from 2D board. List contains element of row r
        
        for c in range(COULMN_COUNT-3):
            window = row_array[c:c+4]
            score += evaluate_window(window,piece)


    ## Score Vertical
    for c in range(COULMN_COUNT):
        column_array = [int(i) for i in list(board[:,c])] 

        for r in range(ROW_COUNT -3):
            window = column_array[r:r+4]
            score += evaluate_window(window,piece)

    ## Score Positive Slope Diagonals
    for r in range(ROW_COUNT-3):
        for c in range(COULMN_COUNT-3):
            window = [board[r+i][c+i] for i in range(WINDOW_LENGTH)]
            score += evaluate_window(window,piece)

    ## Score Negatively Slope Diagoals
    for r in range(ROW_COUNT-3):
        for c in range(COULMN_COUNT-3):
            window = [board[r+3-i][c+i] for i in range(WINDOW_LENGTH)]
            score += evaluate_window(window,piece)


    return score


def is_terminal_node(board):
    return winning_move(board, PLAYER_PIECE) or winning_move(board, AI_PIECE) or len(get_valid_locations(board)) == 0


def minimax(board, depth, alpha, beta, maximizingPlayer):
    valid_locations = get_valid_locations(board)
    is_terminal = is_terminal_node(board)
    if depth == 0 or is_terminal:
        if is_terminal:
            if winning_move(board, AI_PIECE):
                return (None,10000000)
            elif winning_move(board, PLAYER_PIECE):
                return (None,-1000000)
            else:
                return (None,0)
        else:
            return (None, score_position(board, AI_PIECE))
        
    if maximizingPlayer:
        value = -math.inf
        column = random.choice(valid_locations)
        for col in valid_locations:
            row = get_next_open_row(board,col)
            b_copy = board.copy()
            drop_piece(b_copy, row, col , AI_PIECE)
            new_score = minimax(b_copy, depth-1,alpha,beta, False)[1]
            if new_score > value:
                value = new_score
                column = col

            alpha = max(alpha, value)
            if alpha >= beta:
                break
        return column, value
        
    else: # Minimizing Player
        value = math.inf
        column = random.choice(valid_locations)
        for col in valid_locations:
            row = get_next_open_row(board, col)
            b_copy = board.copy()
            drop_piece(b_copy, row, col , PLAYER_PIECE)
            new_score = minimax(b_copy, depth-1,alpha, beta,True)[1]
            if new_score < value:
                value = new_score
                column = col

            beta = min(beta,value)
            if alpha >= beta:
                break

        return column, value



def get_valid_locations(board):
    valid_locations = []
    for col in range(COULMN_COUNT):
        if is_valid_location(board, col):
            if get_next_open_row(board,col) < ROW_COUNT-1:
                valid_locations.append(col)

    return valid_locations
        
    

def pick_best_move(board, piece):
    best_score = -1000             # to prevent screwups
    valid_locations = get_valid_locations(board)

    best_col = random.choice(valid_locations)
    for col in valid_locations:
        row = get_next_open_row(board, col)
        temp_board = board.copy()               ## create a temp board to fill in 
        drop_piece(temp_board,row,col, piece)
        score = score_position(temp_board,piece)     ## Score every possible column move in the temp board and chose the best next move
        if score > best_score:
            best_score = score
            best_col = col

    return best_col


#########################################################################
#########################################################################

         

def drawboard(board):
    for c in range(COULMN_COUNT):
        for r in range(ROW_COUNT):
            pygame.draw.rect(screen, BLUE, (c*SQUARESIZE, r*SQUARESIZE + SQUARESIZE,SQUARESIZE, SQUARESIZE))
            pygame.draw.circle(screen, BLACK,(int(c*SQUARESIZE + SQUARESIZE/2), int(r*SQUARESIZE + SQUARESIZE + SQUARESIZE/2)), RADIUS)

    for c in range(COULMN_COUNT):
        for r in range(ROW_COUNT):           
            if board[r][c] == PLAYER_PIECE:
                pygame.draw.circle(screen, RED,(int(c*SQUARESIZE + SQUARESIZE/2), height-int(r*SQUARESIZE + SQUARESIZE/2)), RADIUS)
            elif board[r][c] == AI_PIECE:
                pygame.draw.circle(screen, YELLOW,(int(c*SQUARESIZE + SQUARESIZE/2), height-int(r*SQUARESIZE + SQUARESIZE/2)), RADIUS)

    pygame.display.update()



def highlight_winning_pieces(win_coordinates, piece):
    color = (255, 255, 255)  # White for highlighting
    for _ in range(5):  # Flashing effect
        for r, c in win_coordinates:
            pygame.draw.circle(screen, color, (int(c * SQUARESIZE + SQUARESIZE / 2), height - int(r * SQUARESIZE + SQUARESIZE / 2)), RADIUS + 5)
        pygame.display.update()
        pygame.time.wait(300)
        for r, c in win_coordinates:
            pygame.draw.circle(screen, RED if piece == PLAYER_PIECE else YELLOW, (int(c * SQUARESIZE + SQUARESIZE / 2), height - int(r * SQUARESIZE + SQUARESIZE / 2)), RADIUS)
        pygame.display.update()
        pygame.time.wait(300)



def gameplay(depth_val):

    board = create_board()
    print_board(board)
    game_over = False
    turn = 0

    #Initialize pygame before game loop starts
    pygame.init(),

    global SQUARESIZE, width, height, screen, RADIUS
    SQUARESIZE = 100

    width = COULMN_COUNT * SQUARESIZE
    height = ROW_COUNT * SQUARESIZE
    size = (width,height)

    RADIUS = int(SQUARESIZE/2 - 5)

    
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("Tiya's connect 4")
    drawboard(board)
    pygame.display.update()

    myfont = pygame.font.SysFont("monospace", 75)

    turn = random.randint(PLAYER,AI)



    while not game_over:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            if event.type == pygame.MOUSEMOTION:
                pygame.draw.rect(screen, BLACK, (0,0, width, SQUARESIZE))
                posx = event.pos[0]
                if turn == PLAYER:
                    pygame.draw.circle(screen, RED, (posx, int(SQUARESIZE/2)), RADIUS)
                    #pygame.draw.rect(screen,LIGHT_BLUE, (posx, SQUARESIZE, SQUARESIZE, height)) 

            pygame.display.update()


            if event.type == pygame.MOUSEBUTTONDOWN:

                pygame.draw.rect(screen, BLACK, (0,0, width, SQUARESIZE))

                # Ask for player 1 input
                if turn == PLAYER:
                    posx = event.pos[0]
                    col = int(math.floor(posx/SQUARESIZE))  #int(input("Player 1 Make you selection (0-6):"))

                    if is_valid_location(board, col):
                        row = get_next_open_row(board, col)
                        drop_piece(board, row, col, PLAYER_PIECE)

                        if winning_move(board, PLAYER_PIECE) != None:
                            label = myfont.render("Player 1 wins!!!", 1,RED)
                            screen.blit(label, (40,10))
                            game_over = True

                        turn += 1
                        turn = turn % 2

                        print(board)
                        drawboard(board)



        # Ask for player 2 input
        if turn == AI and not game_over:
        
            #col = random.randint(0, COULMN_COUNT-1)
            #col = pick_best_move(board, AI_PIECE)
            col, minimax_score = minimax(board, depth_val ,-math.inf, math.inf, True)

            if is_valid_location(board, col):
                pygame.time.wait(500)
                row = get_next_open_row(board, col)
                drop_piece(board, row, col, AI_PIECE)

                if winning_move(board, AI_PIECE) != None:
                    list = winning_move(board, AI_PIECE)

                    label = myfont.render("Player 2 wins!!!", 1,YELLOW)
                    screen.blit(label, (40,10))
                    highlight_winning_pieces(list,AI_PIECE)
                    game_over = True

                print_board(board)
                drawboard(board)
            
                turn += 1
                turn = turn % 2

        if game_over:
            pygame.time.wait(1500)



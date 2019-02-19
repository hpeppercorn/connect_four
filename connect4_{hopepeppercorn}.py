# -*- coding: utf-8 -*-
"""
A connect four game that can be played by two people, a person vs a computer or
the computer vs itself
"""
from copy import deepcopy
import os
from random import choice

def newGame(player1, player2):
    """
    takes 2 string parameters corresponding to each player's name, and returns a 
    dictionary, game, which has 4 key - value pairs
    player1 - first player's name
    player2 - second player's name
    who - integer 1 or 2 indicating whose turn it is to play
    board - list of 6 lists, each with 7 elements representing the
        board
        """
    
    game = {
         'player one' : player1,
         'player two' : player2,
         'who' : 1,
         'board' : [[0,0,0,0,0,0,0],
                    [0,0,0,0,0,0,0],
                    [0,0,0,0,0,0,0],
                    [0,0,0,0,0,0,0],
                    [0,0,0,0,0,0,0],
                    [0,0,0,0,0,0,0]]
         }                              # game dictionary describing new game state

    return game


def printBoard(board):
    """
    takes a list of 6 lists each with 7 elements ("board") and
    prints a nicely formatted connect 4 board with "X" representing player one's
    moves and "O" representing player two's moves
    """
    
    print("| 1 | 2 | 3 | 4 | 5 | 6 | 7 |\n\
+ - + - + - + - + - + - + - +")  # prints labels for each column of the board
    toprint = deepcopy(board) 
    for row in toprint:
        
        for i in range(7):
            if row[i] == 1:
                row[i] = "X"
            elif row[i] == 2:
                row[i] = "O"
            else:
                row[i] = " "  
                    
        print("| {} | {} | {} | {} | {} | {} | {} |\n\
+ - + - + - + - + - + - + - +".format(row[0], row[1], row[2], row[3], row[4], row[5], row[6]))
        
class WrongFormatError(ValueError):
    pass
        
def loadGame():
    """
    loads a particular game state by opening file game.txt containing the names
    of player one and player two, an integer 1 or 2 depending on whose turn it 
    is to play, and a list of lists corresponding to the board in that 
    game state
    returns this data in the form of a game dictionary with keys "player one", 
    "player two", "who" and "board"
    """
    game = dict()
    
    if not os.path.exists("game.txt"):
        raise FileNotFoundError("The game file could not be loaded.")
        
    with open("game.txt", mode="rt", encoding="utf8") as f:
        
        lines = f.readlines()
        if len(lines) != 9:
            raise WrongFormatError("The game file was in the wrong format and could not be loaded.")
 
        game['player one'] = lines[0][:-1]
        game['player two'] = lines[1][:-1]
        game['who'] = int(lines[2][:-1])
        game['board'] = list()
            
        for line in lines[3:9]:
            line = line.split(",")
            if len(line) != 7:
                raise WrongFormatError("The game file was in the wrong format and could not be loaded.")
            for i in range(len(line)):
                line[i] = int(line[i])
                if line[i] > 2 or line[i] < 0:
                    raise WrongFormatError("The game file was in the wrong format and could not be loaded.")
            game['board'].append(line)
            
        for key in game:
            if game[key] == "":
                raise WrongFormatError("The game file was in the wrong format and could not be loaded.")
        
    return game


def getValidMoves(board):
    """
    takes a list of lists representing the game board and determines which 
    'columns' are completely full - returns a list of indices 0-6 indicating which
    columns are NOT full.
    """
    validmoves = list()
    
    for i in range(7):
        for row in board:
            if row[i] == 0:
                validmoves.append(i)
                break
            else:
                continue
                
    return validmoves  

def makeMove(board, move, who):
    """
    takes input of a board, the move to be made and the player making the move,
    and prints an 'X' or an 'O' (depending on the player) in the next available 
    space in the column specified by 'move'
    """
     
    for row in reversed(board):
        if row[move] == 0:
            row[move] = who
            break
    
    return board
        
def hasWon(board, who):
    """
    takes input of a list of lists representing the board in any game state, and 
    an integer 1 or 2 representing the player whose turn it is, and returns True 
    if the player has won, and false if not
    """
    for j in range(6):
        for i in range(4):

            if board[j][i] == who and board[j][i+1] == who and board[j][i+2] == who and board[j][i+3] == who:
                return True #horizontal check
                
    for j in range(3):
        for i in range(7): 
            
            if board[j][i] == who and board[j+1][i] == who and board[j+2][i] == who and board[j+3][i] == who:
                return True #vertical check
            
    for j in range(3):
        for i in range(4):
            
            if board[j][i] == who and board[j+1][i+1] == who and board[j+2][i+2] == who and board[j+3][i+3] == who:
                return True #diagonal check 1
    
    for j in range(3):
        for i in range(7):
            
            if board[j][i] == who and board[j+1][i-1] == who and board[j+2][i-2] == who and board[j+3][i-3] == who:
                return True #diagonal check 2
    return False

def suggestMove1(board, who):
    """
    first checks if any valid move will lead to the current player winning and 
    if so returns this move, then checks if any valid move will lead to the 
    opponent winning and if so returns this move, and if neither of these results 
    in a move, returns a random valid move
    """
    if who == 1:
        opponent = 2
    elif who == 2:
        opponent = 1

    print(getValidMoves(board))
    for move in getValidMoves(board):
        
        if hasWon(makeMove(deepcopy(board), move, who), who):
            return move
        
    for move in getValidMoves(board):
        
        if hasWon(makeMove(deepcopy(board), move, opponent), opponent):
            return move
    
    return choice(getValidMoves(board))

def saveGame(game):
    
    with open("game.txt", mode="wt", encoding="utf8") as f:
        f.write(game['player one'] + "\n")
        f.write(game['player two'] + "\n")
        f.write(str(game['who']) + "\n")
        for row in game['board']:
            line = "{},{},{},{},{},{},{}\n".format(row[0], row[1], row[2], row[3], row[4], row[5], row[6])
            f.write(line)
    
        
def play():
    """
    the main function of the game, prints a welcome message, prints the board 
    turn, asks for the move the next player wishes to make, makes that move 
    and then reprints the board until someone has won the game at which point 
    prints a congratulations message and the game ends
    """
    print("*"*55)
    print("***"+" "*9+"WELCOME TO HOPE'S CONNECT FOUR!"+" "*9+"***")
    print("*"*55,"\n")
    print("Enter the players' names, or type 'C' or 'L'.\n")
    
    player1 = input("Player one: ")
    
    if player1 == "L":
        game = loadGame()
        printBoard(game['board'])
    else:    
        player2 = input("Player two: ")
        game = newGame(player1, player2)
        printBoard(game['board'])
        
    who = int(game['who'])
    board = game['board']
    
    print("To make a move please enter the number of the column you wish to place your counter in.")
    
    while True:
        
        if who == 1:
            activeplayer = game['player one']
        elif who == 2:
            activeplayer = game['player two']
         
        if activeplayer != "C":
            move = input(str(activeplayer) + ", please make a move: ")
            if move == "S":
                saveGame(game)
                break
            
            move = int(move) - 1
                      
            if not move in getValidMoves(board):
                print("\nThe move you tried to make wasn't in the board!\n")
                move = int(input("Make a valid move: ")) - 1
                          
            printBoard(makeMove(board, move, who))
            
            if hasWon(board, who):
                print("\nCongratulations {}! You've won!".format(activeplayer))
                break
            
        elif activeplayer == "C":
            
            move = suggestMove2(board, who)
            print("\nComputer plays: {}\n".format(move+1))
            printBoard(makeMove(board, move, who))
            
            if hasWon(board, who):
                print("\nComputer wins!".format(activeplayer))
                break
        
        if who == 1:
            who = 2
        elif who == 2:
            who = 1
    
def suggestMove2(board, who):
    """function taking inputs board and whowhich makes a slightly better 
    suggestion for the next move for a computer opponent by adding a few extra 
    conditions to check"""
    
    if who == 1:
        if board == [[0,0,0,0,0,0,0],
                     [0,0,0,0,0,0,0],
                     [0,0,0,0,0,0,0],
                     [0,0,0,0,0,0,0],
                     [0,0,0,0,0,0,0],
                     [0,0,0,0,0,0,0]]:
            return 3
    
    if who == 1:
        opponent = 2
    elif who == 2:
        opponent = 1
        
    valid = getValidMoves(board)

    for move in valid:
        
        if hasWon(makeMove(deepcopy(board), move, who), who):
            return move
        
    for move in valid:
        
        if hasWon(makeMove(deepcopy(board), move, opponent), opponent):
            return move
        
        if hasWon(makeMove(makeMove(deepcopy(board), move, who), move, opponent), opponent):
            valid.remove(move)
            
    for row in board:
        for i in range(1, 6):
            if row[i] == opponent and row[i+1]:
                return i-1
    print(valid)        
    
    return choice(valid)

if __name__ == '__main__' or __name__ == 'builtins':
    play()


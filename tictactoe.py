import random #import random to use randint() later

def drawBoard(board): #cannot use images like hangman, because of the x's and o's
    print(board[7] + '|' + board[8] + '|' + board[9]) # ascii art
    print('-+-+-')  # strings are either X, O, or blanks ' '
    print(board[4] + '|' + board[5] + '|' + board[6])
    print('-+-+-') #example drawBoard([' ', ' ', ' ', ' ', 'X', 'O', ' ', 'X', ' ', 'O'])
    print(board[1] + '|' + board[2] + '|' + board[3])

def inputPlayerLetter(): 
    letter = ''  
    while not (letter == 'X' or letter == 'O'): #if letter is x, bypasses while loop
        print('Do you want to be X or O?')
        letter = input().upper() #lets player choose which letter

    if letter == 'X': #used later on 
        return ['X','O'] #first element is player's
    else: 
        return['O','X'] #second element is computer's

def whoGoesFirst(): #randomly choose who goes first, a virtual coinflip
    if random.randint(0,1) == 0:
        return 'computer'
    else:
        return 'player'

def makeMove(board, letter, move):
    #3 parameters
    #board - the list with 10 strings, used to know where to place the move
    #letter - the player's letter, knows what to put on the board
    #move - the move the player makes (a integer from 1 to 9, which places something on the board)
    board[move] = letter  #decides whether to place X or O
    #changes made to board will affect the actual list

def isWinner(bo, le): #checks if there is a winner
    # bo - board, le - letter
    # checks every winning combination
    return ((bo[7] == le and bo[8] == le and bo[9] == le) or
            (bo[4] == le and bo[5] == le and bo[6] == le) or
            (bo[1] == le and bo[2] == le and bo[3] == le) or
            (bo[7] == le and bo[4] == le and bo[1] == le) or
            (bo[8] == le and bo[5] == le and bo[2] == le) or
            (bo[9] == le and bo[6] == le and bo[3] == le) or
            (bo[7] == le and bo[5] == le and bo[3] == le) or
            (bo[1] == le and bo[5] == le and bo[9] == le))

def getBoardCopy(board): #makes a copy of the board and returns it
    boardCopy = []          #for computer move algorithm, 
    for i in board:         #to make modifications on the board without changing the actual one
        boardCopy.append(i)
    return boardCopy

def isSpaceFree(board,move):
    #returns True if there is no letter in selected move, if there is ' ' in the space
    return board[move] == ' '

def getPlayerMove(board):
    move = ' ' #empty value, checks to make sure that move is valid and not chosen yet
    while move not in '1 2 3 4 5 6 7 8 9'.split() or not isSpaceFree(board,int(move)): 
        print('What is your move?')
        move = input() #gets player input
    return int(move) #returns move as an integer
    # when entering a non-integer, doesnt have an error because it short-circuits
    #i.e. during the while loop, once the first half evaluates as true, it skips everything else
    #so the isSpaceFree and int(move) aren't called -> no error message

def chooseRandomMoveFromList(board, movesList):
    #returns a valid move from the passed list on the passed board
    #returns none if there is no valid move
    possibleMoves = [] #checks if there are any possible moves
    for i in movesList: #iterates over movesList
        if isSpaceFree(board,i): #if isSpaceFree is True
            possibleMoves.append(i) #appends it to the list of possible moves

    if len(possibleMoves) != 0: #checks if list is empty
        return random.choice(possibleMoves) #if not, returns a random move
    else: #if no moves, returns None
        return None # None returns no value

def getComputerMove(board, computerLetter):
    #given board and computerLetter, determine moves to do
    if computerLetter == 'X': #first determines the letter of the computer and player
        playerLetter = 'O'
    else:
        playerLetter = 'X'

    #checks if next move will win
    for i in range(1,10):
        boardCopy = getBoardCopy(board)
        if isSpaceFree(board, i): #checks open spaces
            makeMove(boardCopy, computerLetter, i) #makes a move
            if isWinner(boardCopy, computerLetter): #checks if the move results in a win
                return i #if win, returns the move

    #checks if the player will win and blocks them
    for i in range(1,10):
        boardCopy = getBoardCopy(board)
        if isSpaceFree(boardCopy, i): #similar to above
            makeMove(boardCopy, playerLetter, i) #but checks if the player's letter will win
            if isWinner(boardCopy, playerLetter): #and returns that move to block it
                  return i

    #takes the corners
    move = chooseRandomMoveFromList(board, [1,3,7,9]) #chooses a random corner move
    if move != None: #checks if the spaces are free
        return move #returns the move if they are
        
    #try to take the center if free
    if isSpaceFree(board, 5): #checks if center space is free
        return 5

    #try the remaining moves, the sides
    return chooseRandomMoveFromList(board, [2,4,6,8])

def isBoardFull(board):
    #returns true if every space has been taken
    for i in range(1,10): #checks every spot on the board
        if isSpaceFree(board,i): #if there is a ' ', then this will be True and will return False
            return False
    return False

print('Welcome to Tic-Tac-Toe!') #introduction

while True: #keeps looping until a break statement
    theBoard = [' '] * 10 # creates a list of 10 blanks, which is used to create a blank board
    playerLetter, computerLetter = inputPlayerLetter() #player is first letter, computer is second
    turn = whoGoesFirst() #chooses who goes first
    print('The ' + turn + ' will go first.') #tells player who goes first
    gameIsPlaying = True #keeps track if game is still being played, or  if game ended
 
    while gameIsPlaying:
        if turn == 'player':  #player's turn, if false - jumps ahead to down below
            drawBoard(theBoard) # draws the board; theBoard - board is blank
            move = getPlayerMove(theBoard) #gets the player's move
            makeMove(theBoard, playerLetter, move) #places the move on the board

            if isWinner(theBoard, playerLetter): #checks if player won
                drawBoard(theBoard) #displays board
                print('You win!')
                gameIsPlaying = False # ends the game, so that it doesn't continue with the computer;'s turn

            else:
                if isBoardFull(theBoard):
                    drawBoard(theBoard)
                    print('The game is a tie')
                    break #breaks out of the while loop, skips to bottom
                else:
                    turn = 'computer' #if game doesnt end, becomes computer's turn
        
        else:
            #computer's turn
            move = getComputerMove(theBoard, computerLetter) #similar to how the player's move works
            makeMove(theBoard, computerLetter,move)

            if isWinner(theBoard, computerLetter): #repeats the same code as above
                drawBoard(theBoard)
                print('You lost to the computer. You SUCK')
                gameIsPlaying = False
            else:
                if isBoardFull(theBoard): 
                    drawBoard(theBoard)
                    print('The game is a tie')
                    break
                else:
                    turn = 'player'
                
    print('Do you want to play again?') #asks if player wants to play again
    if not input().lower().startswith('y'):#accepts any iterations of yes
        break
        

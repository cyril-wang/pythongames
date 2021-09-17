import random

HANGMAN_PICS = ['''
     +--+
        |
        |
        |
       ===''', '''
    +---+
    O   |
        |
        |
       ===''', '''
    +---+
    O   |
    |   |
        |
       ===''', '''
    +---+
    O   |
   /|   |
        |
       ===''', '''
    +---+
    O   |
   /|\  |
        |
       ===''', '''
    +---+
    O   |
   /|\  |
   /    |
       ===''', '''
    +---+
    O   |
   /|\  |
   / \  |
       ==='''] 

listowords = '''ant baboon badger bat bear beaver camel cat clam cobra cougar
       coyote crow deer dog donkey duck eagle ferret fox frog goat goose hawk
       lion lizard llama mole monkey moose mouse mule newt otter owl panda
       parrot pigeon python rabbit ram rat raven rhino salmon seal shark sheep
       skunk sloth snake spider stork swan tiger toad trout turkey turtle
       weasel whale wolf wombat zebra'''.split() #splits the list into individual strings

def getRandomWord(wordList): #calls function later with list above
    wordIndex = random.randint(0, len(wordList)-1) #returns random string from list
    return wordList[wordIndex] #returns randomly selected word

def displayBoard(missedLetters, correctLetters, secretWord): #parameters defined later
    print(HANGMAN_PICS[len(missedLetters)]) #prints corresponding pictures
    print()

    print('Missed letters:', end=' ') #displays missing letters label
    for letter in missedLetters:
        print(letter, end= ' ') #prints each missing letter
    print()

    blanks = '_' * len(secretWord) #creates blanks with the length of the word

    for i in range(len(secretWord)): #checks each letter if any were correctly guessed
        if secretWord[i] in correctLetters: #and replaces the blanks with the correct letter
            blanks = blanks[0:i]+ secretWord[i]+blanks[i+1:] 

    for letter in blanks:
        print(letter, end = ' ') #prints out the blanks and letters
    print()

def getGuess(alreadyGuessed):
    while True: #loops until a proper guess is made
        print('Guess a letter')
        guess = input() #guess is the input
        guess = guess.lower()  #makes the guess lowercase
        if len(guess) != 1: #makes sure the guess is one character
            print('Enter a letter dumbo')
        elif guess in alreadyGuessed: #makes sure no repeated guesses
            print('You already guessed that letter dumbo. Choose another')
        elif guess not in 'abcdefghijklmnopqrstuvwxyz': #makes sure it is a letter
            print('PLEASE ENTER A FLUBBING LETTER')
        else:
            return guess #returns the guessed letter

def playAgain(): #ask to play again
    print('Do you want to play again?')
    return input().lower().startswith('y') #accepts any form of yes

print('H A N G M A N') #running the actual game using the above functions
missedLetters = '' #blank list to be filled in later
correctLetters = ''
secretWord = getRandomWord(listowords) #calls function to get a word
gameIsDone = False #used later, see below

while True: #repeats until a condition is fulfilled
    displayBoard(missedLetters, correctLetters, secretWord) #displays the board

    guess = getGuess(missedLetters + correctLetters) #uses above function to get guess and make sure its a proper guess
    #missedLetters + correctLetters -> alreadyGuessed, makes sure of no repeats
    if guess in secretWord: #if guess is correct
        correctLetters += guess #adds the guess to correctLetters
        
        foundAllLetters = True #checks if player guessed the word
        for i in range(len(secretWord)): #checks if each letter has been guessed
            if secretWord[i] not in correctLetters: #if correctLetters doesnt have every letter,
                foundAllLetters = False  #then program breaks out of this loop and moves on,until it comes back around
                break
        if foundAllLetters == True: #if true, then all letters were guessed
            print('YES! You win a bag of Lays air edition')
            gameIsDone = True

    else: #if guess was wrong, adds it to missedLetters
        missedLetters += guess

        if len(missedLetters) == len(HANGMAN_PICS)-1: #if number of missed letters = number of pics (python list starts at 0)
            displayBoard(missedLetters, correctLetters, secretWord) #displays final board
            print("You ran out of guesses loser") 
            print("The word was " + secretWord) #displays the secretWord
            gameIsDone = True #ends the game

    if gameIsDone: #normally while lopping, gameIsDone is false, so it skips over this, unless foundAllLetters or ran out of guesses
        if playAgain(): #resets the board
            missedLetters = ''
            correctLetters = ''
            secretWord = getRandomWord(listofwords) #generates new word
            gameIsDone = False #leaves this loop and starts the loop over 
        else:
            print("You suck")
            break #ends the program
        









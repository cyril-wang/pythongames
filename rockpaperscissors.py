from random import randint
import time

# list of play options
moves = ["rock", "paper", "scissors"]

# computer's move
computer = moves[randint(0,2)]

while True:
    player = input("Rock, Paper, Scissors? ").lower()
    if player == computer:
        print("You tied")
        continue
    elif player == "rock":
        if computer == "paper":
            print("You lose! " + computer + " > " + player)
        else:
            print("You win! " + player + " > " + computer)
    elif player == "paper":
        if computer == "scissors":
            print("You lose! " + computer + " > " + player)
        else:
            print("You win! " + player + " > " + computer)
    elif player == "scissors":
        if computer == "rock":
            print("You lose! " + computer + " > " + player)
        else:
            print("You win! " + player + " > " + computer)
    else:
        print("Please enter a valid move")
        continue

    computer = moves[randint(0,2)]
    time.sleep(1)

    if input("Play again? ").lower() != "yes":
        break




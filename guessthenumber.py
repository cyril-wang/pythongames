import random
guesses = 0

print("Hello! What is your name?")
myName = input()

number = random.randint(1,20)

print("Well, " + myName + " ,I am thinking of a number between 1 and 20")

for guesses in range(6):
    print("Take a guess.")
    guess = input()
    guess = int(guess)
    guesses += 1

    if guess < number:
        print("Your guess is too low.")

    if  guess > number :
        print("Your  guess it too high.")

    if guess  == number:
        number  = str(number)
        guesses = str(guesses)
        print("Good joob, " + myName + "! You guessed my number in" + guesses + " guesses!")
        
else:
    number  =  str(number)
    print("Nope. The  number I was  thinking of was " + number)

     


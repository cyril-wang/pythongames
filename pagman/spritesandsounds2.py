# using sounds and images

# adding images with sprites
# sprites - single two-dimensional image
# sprites are drawn on top of the background

# sprites are stored in image files on computer
# pygame supports bmp, png, jpg, gif for images
# and supports MIDI, WAV, MP3 for sound file

# similar to collision detection game, except will use sprites
# and will play backgorund music and add sound effects

import pygame, sys, time, random # import modules
from pygame.locals import *

# set up pygame
pygame.init() # initialize pygame
mainClock = pygame.time.Clock() # similar use as time.sleep()

# set up the window
WINDOWWIDTH = 1200 # width and height of window
WINDOWHEIGHT = 675
windowSurface = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT),
                                         0, 32) # set up window
pygame.display.set_caption('Sprites and Sounds')

# set up the colors
WHITE = (255,255,255) # only need white for the background

# set up the block data structure
player = pygame.Rect(300,100,40,40) # creates player rectangle
playerImage = pygame.image.load('OMEGALUL.png')
playerStretchedImage = pygame.transform.scale(playerImage, (40,40))

BackGround = pygame.image.load('FinalDestination.jpg')
# stretches the image the more food you eat
foodImage = pygame.image.load('khal.png')
foods = []
for i in range(20): # creates 20 food squares randomly splaced
    foods.append(pygame.Rect(random.randint(0, WINDOWWIDTH - 56),
                             random.randint(0, WINDOWHEIGHT - 56),
                             56, 56))

foodCounter = 0
NEWFOOD = 40

# set up keyboard variables
moveLeft = False # keeps track of which arrow key is being pressed
moveRight = False # when key is pressed, variable is set to TRUE
moveUp = False # i.e. if up arrow is pressed, moveUp = True
moveDown = False

MOVESPEED = 6

# set up the music
pickUpSound = pygame.mixer.Sound('coin.wav')
pygame.mixer.music.load('inferno.mp3') # loads the music
pygame.mixer.music.set_volume(0.1)
pygame.mixer.music.play(-1, 0.0) # plays the music
# first paramter is how many times to play it, -1 means play forever
# second parameter is the point in the sound file to start playing, 0.0 = beginning
musicPlaying = True

# Run the game loop
while True: # runs until QUIT event type
    for event in pygame.event.get(): # check each event
        if event.type == QUIT: # if quit event
            pygame.quit() # quits pygame
            sys.exit() # terminates program
        # handling events - user inputs from mouse and keyboards
        # pygame.event.get():
        # quit, keydown, keyup, mousemotion, mousebuttondown, mousebuttonup
        if event.type == KEYDOWN: # if keydown event type, or pressing the key
            # changing the keyboard variables
            if event.key == K_LEFT or event.key == K_a:
                # if pressed key is left arrow or a
                moveRight = False
                moveLeft = True
            if event.key == K_RIGHT or event.key == K_d:
                # if pressed key is right arrow or d
                moveLeft = False # moveLeft first so that both arent true
                moveRight = True  
            if event.key == K_UP or event.key == K_w:
                # if key is up arrow or w
                moveDown = False
                moveUp = True
            if event.key == K_DOWN or event.key == K_s:
                # if key is down arrow or s
                moveUp = False
                moveDown = True

        if event.type == KEYUP: # if KEYUP event type, or releasing the key
            if event.key == K_ESCAPE: # if escape key
                pygame.quit()
                sys.exit() # terminates the program
            if event.key == K_LEFT or event.key == K_a:
                moveLeft = False # if releasing left key, stops moving left
            if event.key == K_RIGHT or event.key == K_d:
                moveRight = False # if releasing right, stops moving right
            if event.key == K_UP or event.key == K_w:
                moveUp = False # if released up, stops moving up
            if event.key == K_DOWN or event.key == K_s:
                moveDown = False # if released down, stops moving down
            # teleporting the player
            if event.key == K_x: # if releasing x, teleports player
                player.top = random.randint(0, WINDOWHEIGHT - player.height)
                player.left = random.randint(0, WINDOWWIDTH - player.width)
                # generates random coordinates for the top-left corner
                # - player.height so that it does not go off the screen
            if event.key == K_m: # pressing m 
                if musicPlaying: # if music is playing, 
                    pygame.mixer.music.stop()# stops the music
                else: # but if no music
                    pygame.mixer.music.play(-1, 0.0) # plays the music
                musicPlaying = not musicPlaying # toggles the value in musicPlaying

        if event.type == MOUSEBUTTONUP: # if clicking the mouse/releases the mouse
            foods.append(pygame.Rect(event.pos[0], event.pos[1], 28, 28))
            # appends more food squares
            # based on the position of the mouse event, or where mouse is clicked

    # adding food automatically
    foodCounter += 1  # foodCounter increases by 1 each iteration
    if foodCounter >= NEWFOOD: # once foodCounter passes NEWFOOD (i.e. after 40 iterations)
        # adds new food
        foodCounter = 0 # resets foodCounter
        foods.append(pygame.Rect(random.randint(0, WINDOWWIDTH - 56),
                                 random.randint(0, WINDOWHEIGHT - 56),
                                 56, 56))
        # and adds a new food square, similar to the ones created before

    # draw the white background onto the surface
    windowSurface.fill(WHITE) # fills the surface with white, like a reset
    windowSurface.blit(BackGround, (0,0))

    # move the player
    if moveDown and player.bottom < WINDOWHEIGHT:
        # if moveDown is True and player's box isn't past the bottom
        player.top += MOVESPEED # moves player down
    if moveUp and player.top > 0: # moveUP == True and box isn't past the top
        player.top -= MOVESPEED # moves player up
    if moveLeft and player.left > 0: 
        player.left -= MOVESPEED # moves player left
    if moveRight and player.right < WINDOWWIDTH:
        player.right += MOVESPEED # moves player right

    # draw the block onto the surface
    windowSurface.blit(playerStretchedImage, player)
    # draws the stretched image where the player's position is

    # check whether the block has interesected with any food
    for food in foods[:]:
        if player.colliderect(food):
            foods.remove(food)
            player = pygame.Rect(player.left, player.top,
                                 player.width + 2, player.height +2)
            playerStretchedImage = pygame.transform.scale(playerImage,
                                                          (player.width, player.height))
            if musicPlaying:
                pickUpSound.play()

    # draw the food
    for food in foods:
        windowSurface.blit(foodImage, food)

    # draw the window onto the screen
    pygame.display.update()
    mainClock.tick(40)


    



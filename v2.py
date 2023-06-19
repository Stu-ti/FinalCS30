###############################################################################
#Space_Invaders
#CS 30
#Stuti Sapru
#Version 002
###############################################################################
'''
This is a basic game of space invaders designed for one player. In
this game, the players moves through the space with a 'battleship' character,
and has to avoid the incoming 'rocks'. The game runs for a total of 1 minute,
and the score of the player is stored. Both the timer and the score are stored
in the upper right corner of the console. Additionally, the game has 3 modes:
Easy, Medium, and Hard.
'''
import pygame
import random

#The length and width of the screen are set below
screen_w = 800
screen_l = 600

#The colours of the screen, battleship, and rocks are set below
BLUE = (4, 12, 36)
RED = (164, 0, 0)
YELLOW = (248, 188, 4)


class Rock(pygame.sprite.Sprite):
    '''
    The Rock class is a child class of pygame.sprite.Sprite, which allows
    it to be in sync with the other sprites. It is responsible for the rocks
    that fly around in space.
    '''

    def __init__(self, speed):
        #Initializes the attributes and methods of the parent class
        super().__init__()
        #Sets the size of the rock
        self.image = pygame.Surface([25, 25])
        #Sets the size of the rock
        self.image.fill(YELLOW)
        #Determines the shape of the rock
        self.rect = self.image.get_rect()
        #Sets the horizontal position of the rock
        self.rect.x = random.randint(0, screen_w - 20)
        #Sets the vertical position of the rock
        self.rect.y = random.randint(0, screen_l - 400)
        #Sets the vertical speed of the rocks as a variable so that it can
        #change
        self.dy = speed

    #Updates the position of the rock and makes it appear at a random
    #position on the top of the screen every loop
    def update(self):
        self.rect.y += self.dy
        if self.rect.y > screen_l:
            self.rect.y = random.randint(-400, -20)
            self.rect.x = random.randint(0, screen_w - 20)


class Battleship(pygame.sprite.Sprite):
    '''
    The Battleship class is also a child class of pygame.sprite.Sprite, which
    allows it to be in sync with the other sprites. It is responsible for the
    user's battleship.
    '''

    def __init__(self):
        #Initializes the attributes and methods of the parent class
        super().__init__()
        #Sets the size of the user's battleship
        self.image = pygame.Surface([30, 30])
        #Sets the size of the battleship
        self.image.fill(RED)
        #Determines the shape of the user's battleship
        self.rect = self.image.get_rect()
        #Sets the horizontal position of the user's battleship
        self.rect.x = 390
        #Sets the vertical position of the user's battleship
        self.rect.y = 400
        #Sets the horizontal speed of the battleship
        self.dx = 5

    #Updates the position of the user's battleship
    def update(self):
        #Syncs the movement of the user's battleship with keys on their keyboard
        keys = pygame.key.get_pressed()
        #If the user types the letter a, the battleship moves left
        if keys[pygame.K_a]:
            self.rect.x -= self.dx
        #If the user types the letter d, the battleship moves right
        elif keys[pygame.K_d]:
            self.rect.x += self.dx
        #If the user types the letter w, the battleship moves up
        elif keys[pygame.K_w]:
            self.rect.y -= self.dx
        #If the user types the letter s, the battleship moves down
        elif keys[pygame.K_s]:
            self.rect.y += self.dx
        self.loop_position()

    #The battleship moves to the other end of the screen when it reaches the screen boundary
    def loop_position(self):
        if self.rect.x < 0:
            self.rect.x = screen_w - 20
        elif self.rect.x > screen_w - 20:
            self.rect.x = 0
        if self.rect.y < 0:
            self.rect.y = screen_l - 20
        elif self.rect.y > screen_l - 20:
            self.rect.y = 0


#Sets the clock of the game
clock = pygame.time.Clock()


class TheGame:
    '''
    TheGame class represents the game itself. It creates the groups for the
    sprites and creates instances for the other classes as well. It is
    responsible for running the overall program.
    '''

    def __init__(self):
        #Initalizes pygame
        pygame.init()
        #Sets the screen and header of the game
        self.screen = pygame.display.set_mode((screen_w, screen_l))
        pygame.display.set_caption("Alien Invasion Game")
        #Creates groups for the sprites
        self.all_sprites = pygame.sprite.Group()
        self.rocks = pygame.sprite.Group()
        #Initalizes the Battleship class
        self.battleship = Battleship()
        self.all_sprites.add(self.battleship)
        #Initializes mode
        self.mode = ""
        #Initializes time
        self.timer = 0
        #Initializes the font(object)
        self.font = pygame.font.Font(None, 36)
        #A boolean value to use when the player loses or the game is over
        self.game_over = False

    #Creates rocks at either a slow, medium, or fast speed according to the
    #difficulty of the mode the user chooses
    def make_rocks(self, num_rocks):
        if self.mode == "Easy":
            speed = 5
        elif self.mode == "Medium":
            speed = 5
        elif self.mode == "Hard":
            speed = 7
        #Creates rocks and adds them to the group of all sprites
        for _ in range(num_rocks):
            rock = Rock(speed)
            self.rocks.add(rock)
            self.all_sprites.add(rock)

    #Checks for a collision between the rock and the battleship
    def collide(self):
        if pygame.sprite.spritecollide(self.battleship, self.rocks, True):
            #Boolean value set to true. Thus, game over if there is a collision
            self.game_over = True

    #Updates the timer by 1 on every update
    def update_timer(self):
        self.timer += 1

    #Displays the timer in the game
    def display_timer(self):
        timer_text = self.font.render("Timer: {}".format(self.timer), True,
                                      RED)
        self.screen.blit(timer_text, (12, 40))

    #Displays the game over message
    def gameover(self):
        game_over_text = self.font.render("Game Over", True, YELLOW)
        self.screen.blit(game_over_text,
                         (screen_w // 2 - 70, screen_l // 2 - 20))

    #Main game loop
    def play(self):
        running = True
        #While the game is running
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            #If there are no collisions, score of 1 is added and all the
            #sprites are updated
            if not self.game_over:
                self.update_timer()
                self.all_sprites.update()
                self.collide()
                #Updates the screen color
                self.screen.fill(BLUE)
                #Updates the sprites, score, timer, and the highscore
                self.all_sprites.draw(self.screen)
                self.display_timer()
                #Keeps the game running at 60 frames per second
                pygame.display.flip()
                clock.tick(60)
            #If the game is over
            else:
                self.gameover()
                pygame.display.flip()
        #Stops the game
        pygame.quit()


#Creates an instance of the game
game = TheGame()

#Starts the game loop (of the instance)
while True:
    #Prints the welcome message and asks the user to choose what mode they
    #want to play
    print("\nWelcome to Space Invaders! \n\nYou can play this game in three "
          "modes: Easy, Medium or Hard.To choose a mode, simply type 'Easy'"
          ", 'Medium' or 'Hard' when prompted below.\nHope you enjoy the "
          "game!")
    #Accepts user input to choose what mode the game should be on
    mode_choice = input("\nSelect a mode: ")
    #If easy mode is chosen, 3 rocks are created every frame
    if mode_choice == "Easy":
        game.mode = "Easy"
        game.make_rocks(5)
        break
    #If medium mode is chosen, 5 rocks are created every frame
    elif mode_choice == "Medium":
        game.mode = "Medium"
        game.make_rocks(5)
        break
    #If hard mode is chosen, 7 rocks are created every frame
    elif mode_choice == "Hard":
        game.mode = "Hard"
        game.make_rocks(5)
        break
    else:
        #If anything other than the three choices are typed out, the statement
        #below prints
        print(
            "\nInvalid choice. Please type your choice exactly as prompted in"
            " the welcome message!")

#Runs the game
game.play()

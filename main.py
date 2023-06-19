###############################################################################
#Space_Invaders
#CS 30
#June 19, 2023
#Stuti Sapru
#Version 003
###############################################################################
'''
This is a basic game of space invaders designed for one player. In
this game, the players moves through the space with a 'battleship' character,
and has to avoid the incoming 'rocks'. The game runs for a total of 1 minute,
and the score of the player is stored. Both the timer and the score are stored
in the upper right corner of the console. Additionally, the game has 3 modes:
Easy, Medium and Fast.
'''
#pygame library handles the graphics of the game and the random library helps
#generate random numbers
import pygame, random

#The length and width of the screen are set below
screen_w = 800
screen_l = 600

#The colours of the screen, battleship and rocks are set below
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
        #initializes the attributes and methods of the parent class
        super().__init__()
        #sets the size of the rock
        self.image = pygame.Surface([25, 25])
        #sets the size of the rock
        self.image.fill(YELLOW)
        #determines the shape of the rock
        self.rect = self.image.get_rect()
        #sets the horizontal position of the rock
        self.rect.x = random.randint(0, screen_w - 20)
        #sets the vertical position of the rock
        self.rect.y = random.randint(0, screen_l - 400)
        #sets the vertical speed of the rocks as a variable so that it can
        #change
        self.dy = speed

    #updates the position of the rock, and makes it appear at random a random
    #position on the top of the screen every loop
    def update(self):
        self.rect.y += self.dy
        if self.rect.y > screen_l:
            self.rect.y = random.randint(-400, -20)
            self.rect.x = random.randint(0, screen_w - 20)


class Battleship(pygame.sprite.Sprite):
    '''
    The Battleship class is also child class of pygame.sprite.Sprite, which 
    allows it to be in sync with the other sprites. It is responsible for the 
    user's battleship.
    '''

    def __init__(self):
        #initializes the attributes and methods of the parent class
        super().__init__()
        #sets the size of the user's battleship
        self.image = pygame.Surface([30, 30])
        #sets the size of the battleship
        self.image.fill(RED)
        #determines the shape of the user's battleship
        self.rect = self.image.get_rect()
        #sets the horizontal position of the user's battleship
        self.rect.x = 390
        #sets the vertical position of the user's battleship
        self.rect.y = 400
        #sets the horizontal speed of the battleship
        self.dx = 5

    #updates the position of the user's battleship
    def update(self):
        #syncs the movment of the user's battleship with key's on their keyboard
        keys = pygame.key.get_pressed()
        #if the user types the letter a, the battleship moves left
        if keys[pygame.K_a]:
            self.rect.x -= self.dx
        #if the user types the letter d, the battleship moves right
        elif keys[pygame.K_d]:
            self.rect.x += self.dx
        #if the user types the letter w, the battleship moves up
        elif keys[pygame.K_w]:
            self.rect.y -= self.dx
        #if the user types the letter s, the battleship moves down
        elif keys[pygame.K_s]:
            self.rect.y += self.dx
        self.loop_position()

    #the battleship moves to the other end of the screen when it reaches the screen boundary (can change?)
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
    responsible for the running of the overall program.
    '''

    def __init__(self):
        #initalizes pygame
        pygame.init()
        #sets the screen and header of the game
        self.screen = pygame.display.set_mode((screen_w, screen_l))
        pygame.display.set_caption("Alien Invasion Game")
        #creates groups for the sprites
        self.all_sprites = pygame.sprite.Group()
        self.rocks = pygame.sprite.Group()
        #initalizes the Battleship class
        self.battleship = Battleship()
        self.all_sprites.add(self.battleship)
        #initializes score
        self.score = 0
        #initializes mode
        self.mode = ""
        #initializes time
        self.timer = 0
        #initializes highscore
        self.highscore = 0
        #initializes the font(object)
        self.font = pygame.font.Font(None, 36)
        #a boolean value to use when the player loses or the game is over
        self.game_over = False

    #creates a rock at either a slow, medium or fast speed according to the
    #difficulty of the mode the user chooses
    def make_rocks(self, num_rocks):
        if self.mode == "Easy":
            speed = 5
        elif self.mode == "Medium":
            speed = 5
        elif self.mode == "Hard":
            speed = 7
        #creates rocks and adds them to the group of all sprites
        for _ in range(num_rocks):
            rock = Rock(speed)
            self.rocks.add(rock)
            self.all_sprites.add(rock)

    #checks for a collision between the rock and the battleship
    def collide(self):
        if pygame.sprite.spritecollide(self.battleship, self.rocks, True):
            #boolean value set to true. Thus, game over if there is a collision
            self.game_over = True

    #updates the timer by 1 on every update
    def update_timer(self):
        self.timer += 1

    #displays the timer in a single game
    def display_timer(self):
        timer_text = self.font.render("Timer: {}".format(self.timer), True,
                                      RED)
        self.screen.blit(timer_text, (12, 40))

    #displays the highscore
    def show_highscore(self):
        highscore_text = self.font.render(
            "Highscore: {}".format(self.highscore), True, RED)
        self.screen.blit(highscore_text, (15, 75))

    #displays the score of the game
    def show_score(self):
        score_text = self.font.render("Score: {}".format(self.score), True,
                                      RED)
        self.screen.blit(score_text, (12, 12))

    #displays the game over message
    def gameover(self):
        game_over_text = self.font.render("Game Over", True, YELLOW)
        self.screen.blit(game_over_text,
                         (screen_w // 2 - 70, screen_l // 2 - 20))

    #main game loop
    def play(self):
        running = True
        #while the game is running
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            #if there are no collisions, score of 1 is added and all the
            #sprites are updated
            if not self.game_over:
                highscore_text = self.font.render(
                    "Highscore: {}".format(self.highscore), True, RED)
                self.screen.blit(highscore_text, (15, 75))
                self.update_timer()
                self.all_sprites.update()
                self.collide()
                self.score += 1
                #updates the screen colour
                self.screen.fill(BLUE)
                #updates the sprites, score, timer, and the highscore
                self.all_sprites.draw(self.screen)
                self.show_score()
                self.display_timer()
                self.show_highscore()
                #keeps the game running at 60 frames per second
                pygame.display.flip()
                clock.tick(60)
            #if the game is over
            else:
                #displays the game over message and updates the highscore if
                #needed
                if self.score > self.highscore:
                    self.highscore = self.score
                self.gameover()
                pygame.display.flip()
        #stops the game
        pygame.quit()


#creates an instance of the game
game = TheGame()

#starts the game loop (of the instance)
while True:
    #prints the welcome message and asks the user to choose what mode they
    #want to play
    print("\nWelcome to Space Invaders! \n\nYou can play this game in three "
          "modes: Easy, Medium or Hard.\nTo choose a mode, simply type 'Easy'"
          ", 'Medium' or 'Hard' when prompted below.\n\nThe program ends when "
          " you colide with a rock\n\nHope you Enjoy the game!")
    #accepts a user input to choose what mode the game should be on
    mode_choice = input("\nSelect a mode: ")
    #if easy mode is chosen, 5 rocks are created every frame
    if mode_choice == "Easy":
        game.mode = "Easy"
        game.make_rocks(3)
        break
    #if easy mode is chosen, 10 rocks are created every frame
    elif mode_choice == "Medium":
        game.mode = "Medium"
        game.make_rocks(5)
        break
    #if easy mode is chosen, 17 rocks are created every frame
    elif mode_choice == "Hard":
        game.mode = "Hard"
        game.make_rocks(7)
        break
    else:
        #if anything other than the three choices are typed out, the statement
        #below prints
        print(
            "\nInvalid choice. Please type your choice exactly as prompted in"
            " the welcome message!")

#runs the game
game.play()

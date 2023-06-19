###############################################################################
#Space_Invaders
#CS 30
#Stuti Sapru
#Version 001
###############################################################################
import pygame
import random

screen_w = 800
screen_l = 600

WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)


class Rock(pygame.sprite.Sprite):

    def __init__(self, speed):
        super().__init__()
        self.image = pygame.Surface([25, 25])
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, screen_w - self.rect.width)
        self.rect.y = random.randint(-100, -40)
        self.speed = speed

    def update(self):
        self.rect.y += self.speed
        if self.rect.y > screen_l:
            self.rect.x = random.randint(0, screen_w - self.rect.width)
            self.rect.y = random.randint(-100, -40)


class Battleship(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()
        self.image = pygame.Surface([30, 30])
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x = screen_w // 2
        self.rect.y = screen_l - self.rect.height
        self.dx = 5

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            self.rect.x -= self.dx
        elif keys[pygame.K_d]:
            self.rect.x += self.dx
        elif keys[pygame.K_w]:
            self.rect.y -= self.dx
        elif keys[pygame.K_s]:
            self.rect.y += self.dx
        self.loop_position()

    def loop_position(self):
        if self.rect.x < 0:
            self.rect.x = screen_w - 20
        elif self.rect.x > screen_w - 20:
            self.rect.x = 0
        if self.rect.y < 0:
            self.rect.y = screen_l - 20
        elif self.rect.y > screen_l - 20:
            self.rect.y = 0


clock = pygame.time.Clock()


class TheGame:

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((screen_w, screen_l))
        pygame.display.set_caption("Alien Invasion Game")
        self.all_sprites = pygame.sprite.Group()
        self.rocks = pygame.sprite.Group()
        self.battleship = Battleship()
        self.all_sprites.add(self.battleship)
        self.game_over = False

    def make_rocks(self, num_rocks):
        speed = 5
        for _ in range(num_rocks):
            rock = Rock(speed)
            self.rocks.add(rock)
            self.all_sprites.add(rock)

    def collide(self):
        if pygame.sprite.spritecollide(self.battleship, self.rocks, True):
            self.game_over = True

    def gameover(self):
        font = pygame.font.Font(None, 36)
        game_over_text = font.render("Game Over", True, YELLOW)
        self.screen.blit(game_over_text,
                         (screen_w // 2 - 70, screen_l // 2 - 20))

    def play(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            if not self.game_over:
                self.all_sprites.update()
                self.collide()
                self.screen.fill(BLUE)
                self.all_sprites.draw(self.screen)
                self.show_score()
                pygame.display.flip()
                clock.tick(60)
            else:
                self.gameover()
                pygame.display.flip()
        pygame.quit()


game = TheGame()

while True:
    print("\nWelcome to Space Invaders!")
    mode_choice = input("\nSelect a mode: ")
    if mode_choice == "Easy":
        game.make_rocks(5)
        break
    elif mode_choice == "Medium":
        game.make_rocks(5)
        break
    elif mode_choice == "Hard":
        game.make_rocks(5)
        break
    else:
        print("\nInvalid choice. Please select 'Easy', 'Medium', or 'Hard'.")

game.play()

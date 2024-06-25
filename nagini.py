import pygame
import pygame.color
import pygame.display
import pygame.draw
import pygame.event
import sys
import random
import pygame.image
import pygame.rect
import pygame.surface
import pygame.time
from pygame.math import Vector2
"""nagini game"""


class SNAKE:
    def __init__(self):
        self.body = [Vector2(5, 10), Vector2(4, 10), Vector2(3, 10)]
        self.direction = Vector2(1, 0)
        self.new_block = False

    def draw_snake(self):
        for block in self.body:
            # create rect
            x_position = int(block.x * cell_size)
            y_position = int(block.y * cell_size)
            snake_rectngle = pygame.Rect(
                x_position, y_position, cell_size, cell_size)
            # draw rect
            pygame.draw.rect(screen, (183, 111, 122), snake_rectngle)

    def snake_move(self):
        if self.new_block == True:
            body_copy = self.body[:]
            body_copy.insert(0, body_copy[0] + self.direction)
            self.body = body_copy
            self.new_block = False
        else:
            body_copy = self.body[:-1]
            body_copy.insert(0, body_copy[0] + self.direction)
            self.body = body_copy

    def eat_fruit(self):
        self.new_block = True


class FRUIT:
    def __init__(self):
        self.new_fruit()

    def draw_fruit(self):
        # create rectangle
        fruit_rectangle = pygame.Rect(
            int(self.position.x * cell_size), int(self.position.y * cell_size), cell_size, cell_size)
        # draw rectangle
        # pygame.draw.rect(screen, (126, 166, 114), fruit_rectangle)
        screen.blit(bait, fruit_rectangle)

    def new_fruit(self):
        self.x = random.randint(0, cell_number - 1)
        self.y = random.randint(0, cell_number - 1)
        self.position = Vector2(self.x, self.y)


class MAIN:
    def __init__(self):
        self.snake = SNAKE()
        self.fruit = FRUIT()

    def update(self):
        self.snake.snake_move()
        self.check_collision()
        self.check_fail()

    def draw_elements(self):
        self.fruit.draw_fruit()
        self.snake.draw_snake()

    def check_collision(self):
        if self.fruit.position == self.snake.body[0]:
            # reposition the fruit
            self.fruit.new_fruit()
            # add another block to the snake
            self.snake.eat_fruit()

    def check_fail(self):
        # check if snake is outside of the screen
        if not 0 <= self.snake.body[0].x < cell_number or not 0 <= self.snake.body[0].y < cell_number:
            self.game_over()

        # check if the snake hits itself
        for block in self.snake.body[1:]:
            if block == self.snake.body[0]:
                self.game_over()

    def game_over(self):
        pygame.quit()
        sys.exit()


pygame.init()
cell_size = 35
cell_number = 17
screen = pygame.display.set_mode(
    (cell_size * cell_number, cell_size * cell_number))

clock = pygame.time.Clock()

bait = pygame.image.load('Graphics/bait.png').convert_alpha()
main_game = MAIN()

# create timer to update snake movement
SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE, 150)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == SCREEN_UPDATE:
            main_game.update()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                if main_game.snake.direction.y != 1:
                    main_game.snake.direction = Vector2(0, -1)
            if event.key == pygame.K_DOWN:
                if main_game.snake.direction.y != -1:
                    main_game.snake.direction = Vector2(0, 1)
            if event.key == pygame.K_RIGHT:
                if main_game.snake.direction.x != -1:
                    main_game.snake.direction = Vector2(1, 0)
            if event.key == pygame.K_LEFT:
                if main_game.snake.direction.x != 1:
                    main_game.snake.direction = Vector2(-1, 0)

    screen.fill((175, 215, 70))
    main_game.draw_elements()
    pygame.display.update()
    clock.tick(60)

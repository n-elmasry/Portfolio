import pygame
import pygame.color
import pygame.display
import pygame.draw
import pygame.event
import sys
import random
import pygame.font
import pygame.image
import pygame.mixer
import pygame.rect
import pygame.surface
import pygame.time
from pygame.math import Vector2
"""nagini game"""


class SNAKE:
    def __init__(self):
        self.body = [Vector2(5, 10), Vector2(4, 10), Vector2(3, 10)]
        self.direction = Vector2(0, 0)
        self.new_block = False

        self.head_up = pygame.image.load(
            'Graphics/head_up.png').convert_alpha()
        self.head_down = pygame.image.load(
            'Graphics/head_down.png').convert_alpha()
        self.head_right = pygame.image.load(
            'Graphics/head_right.png').convert_alpha()
        self.head_left = pygame.image.load(
            'Graphics/head_left.png').convert_alpha()

        self.tail_up = pygame.image.load(
            'Graphics/tail_up.png').convert_alpha()
        self.tail_down = pygame.image.load(
            'Graphics/tail_down.png').convert_alpha()
        self.tail_right = pygame.image.load(
            'Graphics/tail_right.png').convert_alpha()
        self.tail_left = pygame.image.load(
            'Graphics/tail_left.png').convert_alpha()

        self.body_vertical = pygame.image.load(
            'Graphics/body_vertical.png').convert_alpha()
        self.body_horizontal = pygame.image.load(
            'Graphics/body_horizontal.png').convert_alpha()

        self.body_tr = pygame.image.load(
            'Graphics/body_tr.png').convert_alpha()
        self.body_tl = pygame.image.load(
            'Graphics/body_tl.png').convert_alpha()
        self.body_br = pygame.image.load(
            'Graphics/body_br.png').convert_alpha()
        self.body_bl = pygame.image.load(
            'Graphics/body_bl.png').convert_alpha()
        self.crunch_sound = pygame.mixer.Sound('Sound/crunch.wav')

    def draw_snake(self):
        self.updating_snake_head()
        self.updating_tail()

        for index, block in enumerate(self.body):
            # create rect
            x_position = int(block.x * cell_size)
            y_position = int(block.y * cell_size)
            snake_rectngle = pygame.Rect(
                x_position, y_position, cell_size, cell_size)
            # draw rect
            # pygame.draw.rect(screen, (183, 111, 122), snake_rectngle)
            # direction of the head
            if index == 0:
                screen.blit(self.head, snake_rectngle)
            elif index == len(self.body) - 1:
                screen.blit(self.tail, snake_rectngle)
            else:
                pre_block = self.body[index + 1] - block
                next_block = self.body[index - 1] - block
                if pre_block.x == next_block.x:
                    screen.blit(self.body_vertical, snake_rectngle)
                elif pre_block.y == next_block.y:
                    screen.blit(self.body_horizontal, snake_rectngle)
                else:
                    if pre_block.x == -1 and next_block.y == -1 or pre_block.y == -1 and next_block.x == -1:
                        screen.blit(self.body_tl, snake_rectngle)
                    elif pre_block.x == -1 and next_block.y == 1 or pre_block.y == 1 and next_block.x == -1:
                        screen.blit(self.body_bl, snake_rectngle)
                    elif pre_block.x == 1 and next_block.y == -1 or pre_block.y == -1 and next_block.x == 1:
                        screen.blit(self.body_tr, snake_rectngle)
                    elif pre_block.x == 1 and next_block.y == 1 or pre_block.y == 1 and next_block.x == 1:
                        screen.blit(self.body_br, snake_rectngle)

    def updating_snake_head(self):
        head_relation = self.body[1] - self.body[0]
        if head_relation == Vector2(1, 0):
            self.head = self.head_left
        if head_relation == Vector2(-1, 0):
            self.head = self.head_right
        if head_relation == Vector2(0, 1):
            self.head = self.head_up
        if head_relation == Vector2(0, -1):
            self.head = self.head_down

    def updating_tail(self):
        tail_relation = self.body[-2] - self.body[-1]
        if tail_relation == Vector2(1, 0):
            self.tail = self.tail_left
        elif tail_relation == Vector2(-1, 0):
            self.tail = self.tail_right
        elif tail_relation == Vector2(0, 1):
            self.tail = self.tail_up
        elif tail_relation == Vector2(0, -1):
            self.tail = self.tail_down

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

    def play_crunch_sound(self):
        self.crunch_sound.play()

    def restart(self):
        self.body = [Vector2(5, 10), Vector2(4, 10), Vector2(3, 10)]
        self.direction = Vector2(0, 0)


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
        self.draw_background()
        self.fruit.draw_fruit()
        self.snake.draw_snake()
        self.draw_score()

    def check_collision(self):
        if self.fruit.position == self.snake.body[0]:
            # reposition the fruit
            self.fruit.new_fruit()
            # add another block to the snake
            self.snake.eat_fruit()
            self.snake.play_crunch_sound()

            for block in self.snake.body[1:]:
                if block == self.fruit.position:
                    self.fruit.new_fruit()

    def check_fail(self):
        # check if snake is outside of the screen
        if not 0 <= self.snake.body[0].x < cell_number or not 0 <= self.snake.body[0].y < cell_number:
            self.game_over()

        # check if the snake hits itself
        for block in self.snake.body[1:]:
            if block == self.snake.body[0]:
                self.game_over()

    def game_over(self):
        self.snake.restart()
        # pygame.quit()
        # sys.exit()

    def draw_background(self):
        background_color = (200, 200, 230)
        for row in range(cell_number):
            if row % 2 == 0:
                for col in range(cell_number):
                    if col % 2 == 0:
                        background_rect = pygame.Rect(
                            col * cell_size, row * cell_size, cell_size, cell_size)
                        pygame.draw.rect(
                            screen, background_color, background_rect)
            else:
                for col in range(cell_number):
                    if col % 2 != 0:
                        background_rect = pygame.Rect(
                            col * cell_size, row * cell_size, cell_size, cell_size)
                        pygame.draw.rect(
                            screen, background_color, background_rect)

    def draw_score(self):
        score_text = str(len(self.snake.body) - 3)
        score_surface = game_font.render(score_text, True, (56, 74, 12))
        score_x = int(cell_size * cell_number - 60)
        score_y = int(cell_size * cell_number - 40)
        score_rectangle = score_surface.get_rect(center=(score_x, score_y))
        bait_rectangle = scaled_bait.get_rect(midright=(
            score_rectangle.left - 10, score_rectangle.centery))
        # background_rect = pygame.Rect(bait_rectangle.left, bait_rectangle.top,bait_rectangle.width + score_rectangle.width, bait_rectangle.height)

        # pygame.draw.rect(screen, (167, 100, 20), background_rect)
        screen.blit(score_surface, score_rectangle)
        screen.blit(scaled_bait, bait_rectangle)


pygame.init()

pygame.mixer.pre_init(44100, -16, 2, 512)

cell_size = 35
cell_number = 17
screen = pygame.display.set_mode(
    (cell_size * cell_number, cell_size * cell_number))

clock = pygame.time.Clock()

bait = pygame.image.load('Graphics/bait.png').convert_alpha()
scaled_bait = pygame.transform.scale(bait, (20, 20))
game_font = pygame.font.Font('Fonts/HarryP.ttf', 25)
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

    screen.fill((169, 169, 169))
    main_game.draw_elements()
    pygame.display.update()
    clock.tick(60)

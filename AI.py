import pygame
import random
from enum import Enum
from collections import namedtuple
import numpy as np

import threading

def task():
    # This code runs within the thread and can interact with Python's interpreter
    pass

# Make sure to handle the thread carefully without releasing the GIL
thread = threading.Thread(target=task)
thread.start()
thread.join()

pygame.init()

class Direction(Enum):
    right = 1
    left = 2
    up = 3
    down = 4

Point = namedtuple('Point', 'x, y')

background_color = (255, 255, 255)
snake_color = (0, 255, 0)
food_color = (255, 0, 0)
text_color = (0, 0, 0)

block_size = 20
game_speed = 50


class SnakeGameAI:
    def __init__(self, width=640, height=480):
        self.width = width
        self.height = height
        self.display = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption('AI Snake Game')
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont(None, 30)
        self.initialize_game()

    def initialize_game(self):
        self.direction = Direction.right
        self.head = Point(self.width // 2, self.height // 2)
        self.snake = [self.head,
                      Point(self.head.x - block_size, self.head.y),
                      Point(self.head.x - 2 * block_size, self.head.y)]
        self.score = 0
        self.food = None
        self._generate_food()
        self.frame_count = 0

    def _generate_food(self):
        x = random.randint(0, (self.width - block_size) // block_size) * block_size
        y = random.randint(0, (self.height - block_size) // block_size) * block_size
        self.food = Point(x, y)
        if self.food in self.snake:
            self._generate_food()

    def step(self, action):
        self.frame_count += 1
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        self._update_direction(action)
        self.snake.insert(0, self.head)

        reward = 0
        game_over = False
        if self.detect_collision() or self.frame_count > 100 * len(self.snake):
            game_over = True
            reward = -10
            return reward, game_over, self.score

        if self.head == self.food:
            self.score += 1
            reward = 10
            self._generate_food()
        else:
            self.snake.pop()

        self._refresh_display()
        self.clock.tick(game_speed)
        return reward, game_over, self.score

    def detect_collision(self, point=None):
        if point is None:
            point = self.head
        if point.x >= self.width or point.x < 0 or point.y >= self.height or point.y < 0:
            return True
        if point in self.snake[1:]:
            return True
        return False

    def _refresh_display(self):
        self.display.fill(background_color)
        for segment in self.snake:
            pygame.draw.rect(self.display, snake_color, pygame.Rect(segment.x, segment.y, block_size, block_size))
        pygame.draw.rect(self.display, food_color, pygame.Rect(self.food.x, self.food.y, block_size, block_size))
        score_text = self.font.render("Score: " + str(self.score), True, text_color)
        self.display.blit(score_text, [0, 0])
        pygame.display.flip()

    def _update_direction(self, action):
        directions = [Direction.right, Direction.down, Direction.left, Direction.up]
        idx = directions.index(self.direction)

        if np.array_equal(action, [1, 0, 0]):  
            new_direction = directions[idx]
        elif np.array_equal(action, [0, 1, 0]):  
            new_direction = directions[(idx + 1) % 4]
        else:  
            new_direction = directions[(idx - 1) % 4]

        self.direction = new_direction
        x, y = self.head.x, self.head.y
        if self.direction == Direction.right:
            x += block_size
        elif self.direction == Direction.left:
            x -= block_size
        elif self.direction == Direction.down:
            y += block_size
        elif self.direction == Direction.up:
            y -= block_size

        self.head = Point(x, y)

import pygame
import random
import numpy as np
pygame.init()

SCREEN_DIMENSIONS = [800, 600]
CELL_SIZE = 25
SCREEN_WIDTH = round(SCREEN_DIMENSIONS[0] // CELL_SIZE) * CELL_SIZE
SCREEN_HEIGHT = round(SCREEN_DIMENSIONS[1] // CELL_SIZE) * CELL_SIZE
FPS = 60
MOVE_DELAY = 100

RED = (255, 0, 0)
GREEN =(0, 255, 0)
BLUE = (0, 0, 255)
WHITE =(255, 255, 255)
BLACK = (0, 0, 0)

class SnakeGame:
    def __init__(self):
        self.win = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        pygame.display.set_caption('Snake ML')
        self.last_moved = pygame.time.get_ticks()
        self.font = pygame.font.SysFont('Arial', 24)
        self.run = True
        self.player = {
            'x': 100,
            'y': 100,
            'width': CELL_SIZE,
            'height': CELL_SIZE,
            'speed': CELL_SIZE,
            'isheading': 'right',
            'length': 1,
            'tail': []
        }
        self.food = {
            'exist': False,
            'x': 0,
            'y': 0,
            'width': CELL_SIZE,
            'height': CELL_SIZE
        }

    def reset(self):
        self.last_moved = pygame.time.get_ticks()
        self.player = {
            'x': 100,
            'y': 100,
            'width': CELL_SIZE,
            'height': CELL_SIZE,
            'speed': CELL_SIZE,
            'isheading': 'right',
            'length': 1,
            'tail': []
            }
        self.food = {
            'exist': False,
            'x': 0,
            'y': 0,
            'width': CELL_SIZE,
            'height': CELL_SIZE
            }

    def refreshDisplay(self):
        self.win.fill(BLACK)
        score = self.font.render(f"Score: {self.player['length'] - 1}", True, WHITE)
        if self.food['exist']:
            pygame.draw.rect(self.win, RED, (self.food['x'], self.food['y'], self.food['width'], self.food['height']))

        pygame.draw.rect(self.win, BLUE, (self.player['x'], self.player['y'], self.player['width'], self.player['height']))

        for segment in self.player['tail']:
            pygame.draw.rect(self.win, BLUE, (segment[0], segment[1], self.player['width'], self.player['height']))

        self.win.blit(score, (10, 10))
        pygame.display.update()

    def spawnFood(self):
        if not self.food['exist']:
            while True:
                x = round(random.randint(0, SCREEN_WIDTH - CELL_SIZE) // CELL_SIZE) * CELL_SIZE
                y = round(random.randint(0, SCREEN_HEIGHT - CELL_SIZE) // CELL_SIZE) * CELL_SIZE
                occupied = [(self.player['x'], self.player['y'])] + self.player['tail']

                if (x, y) not in occupied:
                    self.food['x'] = x
                    self.food['y'] = y
                    self.food['exist'] = True
                    break

    def checkFoodCollision(self):
        if self.player['x'] == self.food['x'] and self.player['y'] == self.food['y']:
            self.player['length'] += 1
            self.food['exist'] = False

    def getDirection(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            if self.player['length'] == 1:
                self.player['isheading'] = 'right'
            elif self.player['isheading'] != 'left':
                self.player['isheading'] = 'right'

        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            if self.player['length'] == 1:
                self.player['isheading'] = 'left'
            elif self.player['isheading'] != 'right':
                self.player['isheading'] = 'left'

        if keys[pygame.K_UP] or keys[pygame.K_w]:
            if self.player['length'] == 1:
                self.player['isheading'] = 'up'
            elif self.player['isheading'] != 'down':
                self.player['isheading'] = 'up'

        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            if self.player['length'] == 1:
                self.player['isheading'] = 'down'
            elif self.player['isheading'] != 'up':
                self.player['isheading'] = 'down'

    def moveEventHandler(self):
        previous_position = [self.player['x'], self.player['y']]
        now = pygame.time.get_ticks()

        if now >= self.last_moved + MOVE_DELAY:
            if self.player['isheading'] == 'right':
                self.player['x'] += self.player['speed']

            if self.player['isheading'] == 'left':
                self.player['x'] -= self.player['speed']

            if self.player['isheading'] == 'up':
                self.player['y'] -= self.player['speed']

            if self.player['isheading'] == 'down':
                self.player['y'] += self.player['speed']

            self.player['tail'].append(previous_position)
            if len(self.player['tail']) > self.player['length'] - 1:
                self.player['tail'].pop(0)

            self.last_moved = now

    def is_Collision(self, x, y):
        for segment in self.player['tail']:
            if x == segment[0] and y == segment[1]:
                return True
    
        if x < 0 or y < 0 or x > SCREEN_WIDTH - CELL_SIZE or y > SCREEN_HEIGHT - CELL_SIZE:
            return True
        
        return False

    def getLoseCondition(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.run = False

        if self.is_Collision(self.player['x'], self.player['y']):
            self.reset()

game = SnakeGame()

while game.run:
    game.clock.tick(FPS)
    game.spawnFood()
    game.checkFoodCollision()
    game.getDirection()
    game.moveEventHandler()
    game.getLoseCondition()
    game.refreshDisplay()

pygame.quit()

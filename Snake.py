import pygame
import random
pygame.init()

SCREEN_DIMENSIONS = [800, 600]
CELL_SIZE = 25
SCREEN_WIDTH = round(SCREEN_DIMENSIONS[0] // CELL_SIZE) * CELL_SIZE
SCREEN_HEIGHT = round(SCREEN_DIMENSIONS[1] // CELL_SIZE) * CELL_SIZE
FPS = 10

win = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

clock = pygame.time.Clock()

pygame.display.set_caption('Snake ML')

RED = (255, 0, 0)
GREEN =(0, 255, 0)
BLUE = (0, 0, 255)
WHITE =(255, 255, 255)
BLACK = (0, 0, 0)

player = {
    'x': 100,
    'y': 100,
    'width': CELL_SIZE,
    'height': CELL_SIZE,
    'speed': CELL_SIZE,
    'isheading': 'right',
    'length': 1,
    'tail': []
}

food = {
    'exist': False,
    'x': 0,
    'y': 0,
    'width': CELL_SIZE,
    'height': CELL_SIZE
}

def refreshDisplay():
    win.fill(BLACK)
    if food['exist']:
        pygame.draw.rect(win, RED, (food['x'], food['y'], food['width'], food['height']))

    pygame.draw.rect(win, BLUE, (player['x'], player['y'], player['width'], player['height']))

    for segment in player['tail']:
        pygame.draw.rect(win, BLUE, (segment[0], segment[1], player['width'], player['height']))

    pygame.display.update()

run = True

while run:
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    
    if not food['exist']:
        food['x'] = round(random.randint(0, SCREEN_WIDTH - CELL_SIZE) // CELL_SIZE) * CELL_SIZE
        food['y'] = round(random.randint(0, SCREEN_HEIGHT - CELL_SIZE) // CELL_SIZE) * CELL_SIZE
        food['exist'] = True

    if player['x'] == food['x'] and player['y'] == food['y']:
        player['length'] += 1
        food['exist'] = False

    keys = pygame.key.get_pressed()

    if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        if player['length'] == 1:
            player['isheading'] = 'right'
        elif player['isheading'] != 'left':
            player['isheading'] = 'right'

    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
        if player['length'] == 1:
            player['isheading'] = 'left'
        elif player['isheading'] != 'right':
            player['isheading'] = 'left'

    if keys[pygame.K_UP] or keys[pygame.K_w]:
        if player['length'] == 1:
            player['isheading'] = 'up'
        elif player['isheading'] != 'down':
            player['isheading'] = 'up'

    if keys[pygame.K_DOWN] or keys[pygame.K_s]:
        if player['length'] == 1:
            player['isheading'] = 'down'
        elif player['isheading'] != 'up':
            player['isheading'] = 'down'

    previous_position = [player['x'], player['y']]

    if player['isheading'] == 'right':
        player['x'] += player['speed']

    if player['isheading'] == 'left':
        player['x'] -= player['speed']

    if player['isheading'] == 'up':
        player['y'] -= player['speed']

    if player['isheading'] == 'down':
        player['y'] += player['speed']

    player['tail'].append(previous_position)
    if len(player['tail']) > player['length'] - 1:
        player['tail'].pop(0)

    for segment in player['tail']:
        if player['x'] == segment[0] and player['y'] == segment[1]:
            run = False

    if player['x'] < 0 or player['x'] > SCREEN_WIDTH - CELL_SIZE or player['y'] < 0 or player['y'] > SCREEN_HEIGHT - CELL_SIZE:
        run = False

    refreshDisplay()

pygame.quit()

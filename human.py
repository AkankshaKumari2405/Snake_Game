import pygame
import random

pygame.init()
width = 750
height = 750
window = pygame.display.set_mode((width, height))
pygame.display.set_caption("Human Snake Game")

background = (255, 255, 255)
snake_color = (0, 255, 0)
food_color = (255, 0, 0)
score_color = (0, 0, 0)
text_color = (0, 0 , 0)
block_size = 20
font = pygame.font.SysFont(None, 30)

snake = [[100, 50], [100 - block_size, 50], [100 - (2 * block_size), 50]]
food = [random.randrange(1, width // block_size) * block_size, random.randrange(1, height // block_size) * block_size]
direction = 'right'
next_direction = direction
score = 0
high_score = 0

def show_score(score):
    score_text = font.render(f"Score: {score}", True, score_color)
    window.blit(score_text, [10, 10])

def start_screen():
    window.fill(background)
    start_text = font.render("Click to Start the Game", True, text_color)
    text_rect = start_text.get_rect(center=(width // 2, height // 2))
    window.blit(start_text, text_rect)
    pygame.display.flip()
    wait_for_click()

def game_over(score):
    window.fill(background)
    game_over_text = font.render(f"Game Over! Final Score: {score}", True, text_color)
    play_again_text = font.render("Click to Play Again or Press Q to Quit", True, text_color)
    window.blit(game_over_text, game_over_text.get_rect(center=(width // 2, height // 2 - 30)))
    window.blit(play_again_text, play_again_text.get_rect(center=(width // 2, height // 2 + 30)))
    pygame.display.flip()
    print(f"Final Score: {score}")
    global high_score
    if score > high_score:
        high_score = score
    return wait_for_click_or_quit()

def wait_for_click():
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                waiting = False

def wait_for_click_or_quit():
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_q:
                return False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                return True
    return False

start_screen()

while True:
    snake = [[120, 60], [80, 40], [60, 40]]
    food = [random.randrange(0, width // block_size) * block_size, random.randrange(0, height // block_size) * block_size]
    direction = 'right'
    next_direction = direction
    score = 0
    playing = True

    while playing:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and direction != 'down':
                    next_direction = 'up'
                elif event.key == pygame.K_DOWN and direction != 'up':
                    next_direction = 'down'
                elif event.key == pygame.K_LEFT and direction != 'right':
                    next_direction = 'left'
                elif event.key == pygame.K_RIGHT and direction != 'left':
                    next_direction = 'right'
        direction = next_direction
        head_x, head_y = snake[0]
        if direction == 'up':
            head_y -= block_size
        elif direction == 'down':
            head_y += block_size
        elif direction == 'left':
            head_x -= block_size
        elif direction == 'right':
            head_x += block_size
        new_head = [head_x, head_y]
        snake.insert(0, new_head)
        if snake[0] == food:
            food = [random.randrange(0, width // block_size) * block_size, random.randrange(0, height // block_size) * block_size]
            score += 1
        else:
            snake.pop()
        if(head_x < 0 or head_x >= width or head_y < 0 or head_y >= height or new_head in snake[1:]):
            playing = False
        window.fill(background)
        for segment in snake:
            pygame.draw.rect(window, snake_color, pygame.Rect(segment[0], segment[1], block_size, block_size))
        pygame.draw.rect(window, food_color, pygame.Rect(food[0], food[1], block_size, block_size))
        show_score(score)
        pygame.display.flip()
        pygame.time.Clock().tick(10)
    if not game_over(score):
        break
print(f"High Score: {high_score}")
pygame.quit()
    

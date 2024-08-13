import pygame
import random

pygame.init()

WIDTH = 288
HEIGHT = 512
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird")

SKY_BLUE = (78, 192, 202)
GREEN = (0, 216, 0)
WHITE = (255, 255, 255)
ORANGE = (255, 140, 0)
BLACK = (0, 0, 0)

bird_x = 50
bird_y = HEIGHT // 2
bird_width = 34
bird_height = 24
bird_velocity = 0
gravity = 0.3
jump_strength = -6

pipe_width = 52
pipe_gap = 150
pipe_x = WIDTH
pipe_velocity = -1
pipes = []

score = 0
font = pygame.font.Font(None, 36)

def draw_bird(x, y):
    pygame.draw.ellipse(screen, (255, 255, 255), (x, y, 34, 24))
    pygame.draw.ellipse(screen, (255, 165, 0), (x, y, 34, 24), 2)
    pygame.draw.circle(screen, (255, 255, 255), (x + 24, y + 10), 4)
    pygame.draw.circle(screen, (0, 0, 0), (x + 24, y + 10), 2)
    pygame.draw.circle(screen, (0, 0, 0), (x + 24, y + 10), 1)
    pygame.draw.polygon(screen, (255, 165, 0), [(x + 28, y + 12), (x + 32, y + 10), (x + 28, y + 8)])
    pygame.draw.polygon(screen, (0, 0, 0), [(x + 28, y + 12), (x + 32, y + 10), (x + 28, y + 8)], 1)
    wing_y = y + 15 if pygame.time.get_ticks() % 500 < 250 else y + 10
    pygame.draw.polygon(screen, (255, 165, 0), [(x + 5, wing_y), (x + 20, wing_y), (x + 5, wing_y + 10)])
    pygame.draw.polygon(screen, (0, 0, 0), [(x + 5, wing_y), (x + 20, wing_y), (x + 5, wing_y + 10)], 1)
    pygame.draw.line(screen, (0, 0, 0), (x + 16, y + 24), (x + 20, y + 28), 2)
    pygame.draw.line(screen, (0, 0, 0), (x + 20, y + 24), (x + 24, y + 28), 2)

def draw_pipe(x, height, is_top=False):
    if is_top:
        pygame.draw.rect(screen, GREEN, (x, 0, pipe_width, height))
        pygame.draw.rect(screen, (0, 150, 0), (x, height - 20, pipe_width, 20))
    else:
        pygame.draw.rect(screen, GREEN, (x, height, pipe_width, HEIGHT - height))
        pygame.draw.rect(screen, (0, 150, 0), (x, height, pipe_width, 20))

def create_pipe():
    pipe_height = random.randint(100, HEIGHT - 100 - pipe_gap)
    return pipe_height

clock = pygame.time.Clock()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bird_velocity = jump_strength

    bird_velocity += gravity
    bird_y += bird_velocity

    if len(pipes) == 0 or pipes[-1][0] < WIDTH - 200:
        pipes.append([WIDTH, create_pipe()])

    for pipe in pipes:
        pipe[0] += pipe_velocity

    if pipes and pipes[0][0] < -pipe_width:
        pipes.pop(0)
        score += 1

    for pipe in pipes:
        if (pipe[0] - bird_width < bird_x < pipe[0] + pipe_width and
            (bird_y < pipe[1] or bird_y + bird_height > pipe[1] + pipe_gap)):
            running = False

    if bird_y + bird_height > HEIGHT or bird_y < 0:
        running = False

    screen.fill(SKY_BLUE)
    for pipe in pipes:
        draw_pipe(pipe[0], pipe[1], True)
        draw_pipe(pipe[0], pipe[1] + pipe_gap, False)
    
    draw_bird(bird_x, int(bird_y))

    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()

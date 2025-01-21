import pygame
import sys
import random

pygame.init()

WIDTH, HEIGHT = 1000, 800

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Block Physics Game")

clock = pygame.time.Clock()

block_size = 50
ball_radius = 25

block_color = BLUE
ball_color = RED

block_mass = 15
ball_mass = 5

gravitational_force = 0.5
friction = 0.8
jump_force = -10
dash_speed = 15
movement_speed = 5
push_force = 5
ground_height = HEIGHT - 50
roof_height = 50

default_block_pos = (WIDTH // 2, HEIGHT // 2)
default_ball_pos = (WIDTH // 2, HEIGHT // 4)

block_x, block_y = default_block_pos
ball_x, ball_y = default_ball_pos

velocity_x = 0
velocity_y = 0
ball_velocity_x = 0
ball_velocity_y = 0

on_ground = False
ball_on_ground = False

last_move_time = 0
move_cooldown = 250

max_air_speed = 10

game_mode = "start"  # Modes: "start", "player", "ai"
game_start_time = None


def reset_game():
    global block_x, block_y, ball_x, ball_y, velocity_x, velocity_y, ball_velocity_x, ball_velocity_y
    block_x, block_y = default_block_pos
    ball_x, ball_y = default_ball_pos
    velocity_x = 0
    velocity_y = 0
    ball_velocity_x = 0
    ball_velocity_y = 0


def draw_start_screen():
    """Draws the start screen with Player and AI buttons."""
    screen.fill(WHITE)
    font = pygame.font.Font(None, 72)
    player_button = pygame.draw.rect(screen, GREEN, (WIDTH // 4 - 100, HEIGHT // 2 - 50, 200, 100))
    ai_button = pygame.draw.rect(screen, GREEN, (3 * WIDTH // 4 - 100, HEIGHT // 2 - 50, 200, 100))
    text_player = font.render("Player", True, BLACK)
    text_ai = font.render("AI", True, BLACK)
    screen.blit(text_player, (WIDTH // 4 - 50, HEIGHT // 2 - 25))
    screen.blit(text_ai, (3 * WIDTH // 4 - 50, HEIGHT // 2 - 25))
    pygame.display.flip()
    return player_button, ai_button


def ai_simulate_movement():
    """Simulate movement for AI by selecting random keys."""
    keys = [pygame.K_a, pygame.K_d, pygame.K_w, pygame.K_q, pygame.K_e, pygame.K_z, pygame.K_x, pygame.K_c]
    return random.choice(keys)


def resolve_collision(ball_velocity, block_velocity, ball_mass, block_mass):
    """Resolves collision between the ball and the block."""
    ball_velocity_new = (ball_velocity * (ball_mass - block_mass) + 2 * block_mass * block_velocity) / (ball_mass + block_mass)
    block_velocity_new = (block_velocity * (block_mass - ball_mass) + 2 * ball_mass * ball_velocity) / (ball_mass + block_mass)
    return ball_velocity_new, block_velocity_new


def draw_timer(elapsed_time):
    """Draws the countdown timer at the top of the screen."""
    font = pygame.font.Font(None, 48)
    time_left = max(0, 10 - int(elapsed_time))
    timer_text = font.render(f"Time Left: {time_left}s", True, GREEN)
    screen.blit(timer_text, (WIDTH // 2 - 100, 10))


def main():
    global game_mode, game_start_time, last_move_time
    global block_x, block_y, velocity_x, velocity_y, ball_x, ball_y, ball_velocity_x, ball_velocity_y
    global on_ground, ball_on_ground

    running = True

    while running:
        if game_mode == "start":
            player_button, ai_button = draw_start_screen()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    if player_button.collidepoint(mouse_x, mouse_y):
                        game_mode = "player"
                        reset_game()
                        game_start_time = pygame.time.get_ticks()
                    elif ai_button.collidepoint(mouse_x, mouse_y):
                        game_mode = "ai"
                        reset_game()
                        game_start_time = pygame.time.get_ticks()

        else:
            elapsed_time = (pygame.time.get_ticks() - game_start_time) / 1000
            if elapsed_time > 10:
                game_mode = "start"
                continue

            keys = pygame.key.get_pressed() if game_mode == "player" else None
            if game_mode == "ai":
                ai_key = ai_simulate_movement()
                keys = pygame.key.get_pressed()
                pygame.event.post(pygame.event.Event(pygame.KEYDOWN, key=ai_key))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    if restart_button.collidepoint(mouse_x, mouse_y):
                        reset_game()
                        game_mode = "start"

                elif event.type == pygame.KEYDOWN:
                    current_time = pygame.time.get_ticks()
                    if current_time - last_move_time >= move_cooldown:
                        if event.key == pygame.K_a:
                            velocity_x -= dash_speed if on_ground else dash_speed / 2
                        elif event.key == pygame.K_q:
                            velocity_x -= dash_speed if on_ground else dash_speed / 2
                            velocity_y += jump_force
                        elif event.key == pygame.K_w:
                            velocity_y += jump_force
                        elif event.key == pygame.K_e:
                            velocity_x += dash_speed if on_ground else dash_speed / 2
                            velocity_y += jump_force
                        elif event.key == pygame.K_d:
                            velocity_x += dash_speed if on_ground else dash_speed / 2
                        elif event.key == pygame.K_c:
                            velocity_x += dash_speed if on_ground else dash_speed / 2
                            velocity_y -= jump_force
                        elif event.key == pygame.K_x:
                            velocity_y += dash_speed if on_ground else dash_speed / 2
                        elif event.key == pygame.K_z:
                            velocity_x -= dash_speed if on_ground else dash_speed / 2
                            velocity_y -= jump_force

                        last_move_time = current_time

            velocity_y += gravitational_force
            if on_ground:
                velocity_x *= friction

            ball_velocity_y += gravitational_force
            if ball_on_ground:
                ball_velocity_x *= friction

            block_x += velocity_x
            block_y += velocity_y

            if not on_ground:
                velocity_x = max(-max_air_speed, min(velocity_x, max_air_speed))

            if block_y + block_size > ground_height:
                block_y = ground_height - block_size
                velocity_y = 0
                on_ground = True
            else:
                on_ground = False

            if block_y < roof_height:
                block_y = roof_height
                velocity_y = 0

            if block_x < 0:
                block_x = 0
                velocity_x = 0
            if block_x + block_size > WIDTH:
                block_x = WIDTH - block_size
                velocity_x = 0

            ball_x += ball_velocity_x
            ball_y += ball_velocity_y

            if ball_y + ball_radius > ground_height:
                ball_y = ground_height - ball_radius
                ball_velocity_y = -ball_velocity_y * 0.8
                ball_on_ground = True
            else:
                ball_on_ground = False

            if ball_y - ball_radius < roof_height:
                ball_y = roof_height + ball_radius
                ball_velocity_y = -ball_velocity_y * 0.8

            if ball_x - ball_radius < 0:
                ball_x = ball_radius
                ball_velocity_x = -ball_velocity_x
            if ball_x + ball_radius > WIDTH:
                ball_x = WIDTH - ball_radius
                ball_velocity_x = -ball_velocity_x

            if (
                block_x < ball_x + ball_radius
                and block_x + block_size > ball_x - ball_radius
                and block_y < ball_y + ball_radius
                and block_y + block_size > ball_y - ball_radius
            ):
                if ball_x < block_x:  # Left collision
                    ball_x = block_x - ball_radius
                    ball_velocity_x, velocity_x = resolve_collision(ball_velocity_x, velocity_x, ball_mass, block_mass)
                elif ball_x > block_x + block_size:  # Right collision
                    ball_x = block_x + block_size + ball_radius
                    ball_velocity_x, velocity_x = resolve_collision(ball_velocity_x, velocity_x, ball_mass, block_mass)

                if ball_y < block_y:  # Top collision
                    ball_y = block_y - ball_radius
                    ball_velocity_y, velocity_y = resolve_collision(ball_velocity_y, velocity_y, ball_mass, block_mass)
                elif ball_y > block_y + block_size:  # Bottom collision
                    ball_y = block_y + block_size + ball_radius
                    ball_velocity_y, velocity_y = resolve_collision(ball_velocity_y, velocity_y, ball_mass, block_mass)

            screen.fill(WHITE)

            pygame.draw.rect(screen, BLACK, (0, ground_height, WIDTH, HEIGHT - ground_height))
            pygame.draw.rect(screen, BLACK, (0, 0, WIDTH, roof_height))
            pygame.draw.rect(screen, BLUE, (block_x, block_y, block_size, block_size))
            pygame.draw.circle(screen, RED, (ball_x, ball_y), ball_radius)

            restart_button = pygame.draw.rect(screen, GREEN, (WIDTH - 150, 10, 140, 50))
            font = pygame.font.Font(None, 36)
            text = font.render("Restart", True, BLACK)
            screen.blit(text, (WIDTH - 130, 20))

            draw_timer(elapsed_time)

            pygame.display.flip()
            clock.tick(60)


if __name__ == "__main__":
    main()

import pygame
from pygame.color import THECOLORS
import sys
import random
import functions

pygame.init()

WIDTH, HEIGHT = 1000, 800

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("AI Spike")

clock = pygame.time.Clock()
timer = 5

block_size = 50
ball_radius = 25

block_color = BLUE
ball_color = RED
wall_color = THECOLORS['grey']

block_mass = 15
ball_mass = 5
wall_mass = 50

wall_width = 30
wall_height = 300
wall_x = (WIDTH - wall_width) // 2
wall_y = HEIGHT // 2 + 200

gravitational_force = 0.5
friction = 0.8
jump_force = -10
dash_speed = 15
movement_speed = 5
push_force = 5
ground_height = HEIGHT - 50
roof_height = 50

default_block_pos = (WIDTH // 2 + 200, HEIGHT // 2 + 300)
default_ball_pos = (WIDTH // 2 + 50, HEIGHT // 4 + 350)

block_x, block_y = default_block_pos
ball_x, ball_y = default_ball_pos

velocity_x = 0
velocity_y = 0
ball_velocity_x = 0
ball_velocity_y = 0

on_ground = False
ball_on_ground = False

ai_last_move_time = 0  
ai_move_interval = 100  

last_move_time = 0
move_cooldown = 100

max_air_speed = 10

game_mode = "start"  # modes: "start", "player", "ai"
game_start_time = None

ai_move_log = [] 
ai_events_log = [] 

db = functions.DB(0.1, 10, 5, 0.1, 5)

# INITIALSSSSS
def reset_game():
    global block_x, block_y, ball_x, ball_y, velocity_x, velocity_y, ball_velocity_x, ball_velocity_y
    block_x, block_y = default_block_pos
    ball_x, ball_y = default_ball_pos
    velocity_x = 0
    velocity_y = 0
    ball_velocity_x = 0
    ball_velocity_y = -25

    ai_move_log.clear()
    ai_events_log.clear()


def draw_start_screen():
    """Draws the start screen with Player and AI buttons."""
    screen.fill(WHITE)
    font = pygame.font.Font(None, 72)
    player_button = pygame.draw.rect(screen, GREEN, (WIDTH // 4 - 100, HEIGHT // 2 - 50, 200, 100))
    ai_button = pygame.draw.rect(screen, GREEN, (3 * WIDTH // 4 - 100, HEIGHT // 2 - 50, 200, 100))
    text_player = font.render("Player", True, BLACK)
    text_ai = font.render("AI", True, BLACK)
    screen.blit(text_player, (WIDTH // 4 - 78, HEIGHT // 2 - 25))
    screen.blit(text_ai, (3 * WIDTH // 4 - 30, HEIGHT // 2 - 25))
    pygame.display.flip()
    return player_button, ai_button

def ai_simulate_movement():
    """Simulate movement for AI by selecting random keys at controlled intervals."""
    global ai_last_move_time, ai_move_log

    current_time = pygame.time.get_ticks() 
    if current_time - ai_last_move_time < ai_move_interval:
        return None 

    ai_last_move_time = current_time  

    keys = {
        pygame.K_a: "Left",
        pygame.K_d: "Right",
        pygame.K_w: "Jump",
        pygame.K_q: "Up Left",
        pygame.K_e: "Up Right",
        pygame.K_z: "Down Left",
        pygame.K_x: "Straight Down",
        pygame.K_c: "Down Right",
        pygame.K_0: "Idle"
    }

    selected_key = random.choice(list(keys.keys()))
    ai_move_log.append(keys[selected_key])

    if len(ai_move_log) > 10:
        ai_move_log.pop(0)

    return selected_key

def draw_ai_moves():
    font = pygame.font.Font(None, 28)
    x, y = 10, 100 

    box_width = 150
    box_height = 220
    pygame.draw.rect(screen, (200, 200, 200), (x - 5, y - 5, box_width, box_height)) 

    for move in ai_move_log[:10]:  
        move_text = font.render(move, True, BLACK)
        screen.blit(move_text, (x, y))
        y += 20  
    
def draw_ai_events():
    """AI probability"""
    font = pygame.font.Font(None, 28)
    x, y = 200, 100 

    box_width = 150
    box_height = 220
    pygame.draw.rect(screen, (180, 180, 180), (x - 5, y - 5, box_width, box_height)) 

    for move in ai_events_log[:10]:  
        move_text = font.render(move, True, BLACK)
        screen.blit(move_text, (x, y))
        y += 20  

def addEvent(event):
    ai_events_log.append(event)

    if len(ai_events_log) > 10:
        ai_events_log.pop(0)

def resolve_collision(ball_velocity, block_velocity, ball_mass, block_mass):
    ball_velocity_new = (ball_velocity * (ball_mass - block_mass) + 2 * block_mass * block_velocity) / (ball_mass + block_mass)
    block_velocity_new = (block_velocity * (block_mass - ball_mass) + 2 * ball_mass * ball_velocity) / (ball_mass + block_mass)
    return ball_velocity_new, block_velocity_new


def draw_timer(elapsed_time):
    font = pygame.font.Font(None, 48)
    time_left = max(0, timer - int(elapsed_time))
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
            if elapsed_time > timer and game_mode == "ai":
                game_mode = "ai"
                reset_game()
                game_start_time = pygame.time.get_ticks()
                continue

            if elapsed_time > timer:
                game_mode = "start"
                continue

            if game_mode == "ai":
                ai_key = ai_simulate_movement()
                if ai_key:  # Only post the event if a move was actually made
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

            # Touch ground
            if block_y + block_size > ground_height:
                block_y = ground_height - block_size
                velocity_y = 0
                on_ground = True

                if block_x < wall_x: 
                    addEvent("wrong court")

                    reset_game()
                    elapsed_time = timer
            else:
                on_ground = False

            # Touch roof
            if block_y < roof_height:
                block_y = roof_height
                velocity_y = 0

            # Touch left boundary of screen
            if block_x < 0:
                block_x = 0
                velocity_x = 0

            # Touch right boundary of screen
            if block_x + block_size > WIDTH:
                block_x = WIDTH - block_size
                velocity_x = 0

            # Update ball position
            ball_x += ball_velocity_x
            ball_y += ball_velocity_y

            # Ball touches ground
            if ball_y + ball_radius > ground_height:
                ball_y = ground_height - ball_radius
                ball_velocity_y = -ball_velocity_y * 0.8  
                ball_on_ground = True

                if ball_x < wall_x: 
                    addEvent("spike")

                if ai_events_log.count("ball ground") != 0 and ai_events_log.count("spike") == 0:
                    reset_game()
                    game_start_time = pygame.time.get_ticks()
                else:
                    addEvent("ball ground")
            else:
                ball_on_ground = False

            # Ball touches roof
            if ball_y - ball_radius < roof_height:
                ball_y = roof_height + ball_radius
                ball_velocity_y = -ball_velocity_y * 0.8 

            # Ball touches left boundary
            if ball_x - ball_radius < 0:
                ball_x = ball_radius
                ball_velocity_x = -ball_velocity_x  
                
                if ai_events_log.count("spike") == 0:
                    addEvent("out")
                    reset_game()
                    game_start_time = pygame.time.get_ticks()
                else:
                    addEvent("legal out")

            # Ball touches right boundary
            if ball_x + ball_radius > WIDTH:
                ball_x = WIDTH - ball_radius
                ball_velocity_x = -ball_velocity_x 

            # Ball collides with block
            if (block_x < ball_x + ball_radius and block_x + block_size > ball_x - ball_radius and block_y < ball_y + ball_radius and block_y + block_size > ball_y - ball_radius):
                # Ball hits block from left side
                if ball_x < block_x:  
                    ball_x = block_x - ball_radius
                    ball_velocity_x, velocity_x = resolve_collision(ball_velocity_x, velocity_x, ball_mass, block_mass)
                
                # Ball hits block from right side
                elif ball_x > block_x + block_size:  
                    ball_x = block_x + block_size + ball_radius
                    ball_velocity_x, velocity_x = resolve_collision(ball_velocity_x, velocity_x, ball_mass, block_mass)

                # Ball hits block from top
                if ball_y < block_y:  
                    ball_y = block_y - ball_radius
                    ball_velocity_y, velocity_y = resolve_collision(ball_velocity_y, velocity_y, ball_mass, block_mass)
                
                # Ball hits block from bottom
                elif ball_y > block_y + block_size:  
                    ball_y = block_y + block_size + ball_radius
                    ball_velocity_y, velocity_y = resolve_collision(ball_velocity_y, velocity_y, ball_mass, block_mass)
                
                if ai_events_log.count("block ball") != 0:
                    reset_game()
                    game_start_time = pygame.time.get_ticks()
                else:
                    addEvent("block ball")

            screen.fill(WHITE)

            # Ball collides with wall
            if (
                ball_x + ball_radius > wall_x
                and ball_x - ball_radius < wall_x + wall_width
                and ball_y + ball_radius > wall_y
                and ball_y - ball_radius < wall_y + wall_height
            ):
                # Ball hits wall from top
                if ball_y < wall_y:  
                    ball_y = wall_y - ball_radius
                    ball_velocity_y = -ball_velocity_y * 0.8   

                # Ball hits wall from bottom
                elif ball_y > wall_y + wall_height:  
                    ball_y = wall_y + wall_height + ball_radius
                    ball_velocity_y = -ball_velocity_y * 0.8  

                # Ball hits wall from left
                elif ball_x < wall_x:  
                    ball_x = wall_x - ball_radius
                    ball_velocity_x = -ball_velocity_x * 0.8  

                # Ball hits wall from right
                elif ball_x > wall_x + wall_width:  
                    ball_x = wall_x + wall_width + ball_radius
                    ball_velocity_x = -ball_velocity_x * 0.8  

            # Block collides with wall
            if (
                block_x + block_size > wall_x
                and block_x < wall_x + wall_width
                and block_y + block_size > wall_y
                and block_y < wall_y + wall_height
            ):
                # Block hits wall from top
                if block_y + block_size > wall_y and block_y < wall_y:
                    block_y = wall_y - block_size
                    velocity_y = 0

                # Block hits wall from bottom
                elif block_y < wall_y + wall_height and block_y + block_size > wall_y + wall_height:
                    block_y = wall_y + wall_height
                    velocity_y = 0

                # Block hits wall from left
                elif block_x + block_size > wall_x and block_x < wall_x:
                    block_x = wall_x - block_size
                    velocity_x = 0

                # Block hits wall from right
                elif block_x < wall_x + wall_width and block_x + block_size > wall_x + wall_width:
                    block_x = wall_x + wall_width
                    velocity_x = 0
                
                reset_game()
                game_start_time = pygame.time.get_ticks()

            pygame.draw.rect(screen, wall_color, (wall_x, wall_y, wall_width, wall_height))
            pygame.draw.rect(screen, BLACK, (0, ground_height, WIDTH, HEIGHT - ground_height))
            pygame.draw.rect(screen, BLACK, (0, 0, WIDTH, roof_height))
            pygame.draw.rect(screen, block_color, (block_x, block_y, block_size, block_size))
            pygame.draw.circle(screen, ball_color, (ball_x, ball_y), ball_radius)

            restart_button = pygame.draw.rect(screen, GREEN, (WIDTH - 150, 10, 140, 50))
            font = pygame.font.Font(None, 36)
            text = font.render("Restart", True, BLACK)
            screen.blit(text, (WIDTH - 130, 20))

            draw_timer(elapsed_time)
            draw_ai_moves()
            draw_ai_events()
            pygame.display.flip()
            clock.tick(60)


if __name__ == "__main__":
    main()

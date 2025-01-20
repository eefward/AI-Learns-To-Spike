import pygame
import sys

pygame.init()

WIDTH, HEIGHT = 1000, 800

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Block Physics Game")

clock = pygame.time.Clock()

# CUSTOMIZE

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

def main():
    global block_x, block_y, velocity_x, velocity_y, on_ground, last_move_time
    global ball_x, ball_y, ball_velocity_x, ball_velocity_y, ball_on_ground

    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
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

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1: 
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    if restart_button.collidepoint(mouse_x, mouse_y):
                        reset_game()

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

        if (block_x < ball_x + ball_radius and
            block_x + block_size > ball_x - ball_radius and
            block_y < ball_y + ball_radius and
            block_y + block_size > ball_y - ball_radius):

            if ball_x < block_x:  
                ball_x = block_x - ball_radius  
                ball_velocity_x, velocity_x = resolve_collision(ball_velocity_x, velocity_x, ball_mass, block_mass)
            elif ball_x > block_x + block_size: 
                ball_x = block_x + block_size + ball_radius  
                ball_velocity_x, velocity_x = resolve_collision(ball_velocity_x, velocity_x, ball_mass, block_mass)

            if ball_y < block_y: 
                ball_y = block_y - ball_radius 
                ball_velocity_y, velocity_y = resolve_collision(ball_velocity_y, velocity_y, ball_mass, block_mass)
            elif ball_y > block_y + block_size:
                ball_y = block_y + block_size + ball_radius 
                ball_velocity_y, velocity_y = resolve_collision(ball_velocity_y, velocity_y, ball_mass, block_mass)

        screen.fill(WHITE)

        pygame.draw.rect(screen, BLACK, (0, ground_height, WIDTH, HEIGHT - ground_height))
        pygame.draw.rect(screen, BLACK, (0, 0, WIDTH, roof_height))

        pygame.draw.rect(screen, BLUE, (block_x, block_y, block_size, block_size))

        pygame.draw.circle(screen, RED, (ball_x, ball_y), ball_radius)

        restart_button = pygame.draw.rect(screen, (0, 255, 0), (WIDTH - 100, HEIGHT - 50, 80, 40))
        font = pygame.font.Font(None, 36)
        text = font.render("Restart", True, (0, 0, 0))
        screen.blit(text, (WIDTH - 90, HEIGHT - 40))

        pygame.display.flip()

        clock.tick(60)

    pygame.quit()
    sys.exit()

def resolve_collision(ball_velocity, block_velocity, ball_mass, block_mass):
    ball_velocity_new = (ball_velocity * (ball_mass - block_mass) + 2 * block_mass * block_velocity) / (ball_mass + block_mass)
    block_velocity_new = (block_velocity * (block_mass - ball_mass) + 2 * ball_mass * ball_velocity) / (ball_mass + block_mass)

    return ball_velocity_new, block_velocity_new

def reset_game():
    global block_x, block_y, ball_x, ball_y, velocity_x, velocity_y, ball_velocity_x, ball_velocity_y
    block_x, block_y = default_block_pos
    ball_x, ball_y = default_ball_pos
    velocity_x = 0
    velocity_y = 0
    ball_velocity_x = 0
    ball_velocity_y = 0

if __name__ == "__main__":
    main()

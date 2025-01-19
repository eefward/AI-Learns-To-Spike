import pygame
import sys

pygame.init()

WIDTH, HEIGHT = 800, 600

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Block Physics Game")

clock = pygame.time.Clock()

block_size = 50
block_x = WIDTH // 2
block_y = HEIGHT // 2
block_color = BLUE

velocity_x = 0
velocity_y = 0
gravitational_force = 0.5
friction = 0.8
jump_force = -10
dash_speed = 10
angular_dash_speed = 15
movement_speed = 5
push_force = 5
ground_height = HEIGHT - 50
on_ground = False

dash_duration = 5
dash_timer = 0
is_dashing = False

def main():
    global block_x, block_y, velocity_x, velocity_y, on_ground, dash_timer, is_dashing

    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w and on_ground:
                    velocity_y = jump_force
                elif event.key == pygame.K_q and not is_dashing:
                    velocity_x -= angular_dash_speed * 0.7
                    velocity_y -= angular_dash_speed
                    is_dashing = True
                    dash_timer = dash_duration
                elif event.key == pygame.K_w and not is_dashing:
                    velocity_y -= dash_speed
                    is_dashing = True
                    dash_timer = dash_duration
                elif event.key == pygame.K_e and not is_dashing:
                    velocity_x += angular_dash_speed * 0.7
                    velocity_y -= angular_dash_speed
                    is_dashing = True
                    dash_timer = dash_duration
                elif event.key == pygame.K_d and not is_dashing:
                    velocity_x += dash_speed
                    is_dashing = True
                    dash_timer = dash_duration
                elif event.key == pygame.K_c and not is_dashing:
                    velocity_x += angular_dash_speed
                    velocity_y += angular_dash_speed * 0.7
                    is_dashing = True
                    dash_timer = dash_duration
                elif event.key == pygame.K_x and not is_dashing:
                    velocity_y += dash_speed
                    is_dashing = True
                    dash_timer = dash_duration
                elif event.key == pygame.K_z and not is_dashing:
                    velocity_x -= angular_dash_speed
                    velocity_y += angular_dash_speed * 0.7
                    is_dashing = True
                    dash_timer = dash_duration
                elif event.key == pygame.K_a:
                    velocity_x -= movement_speed
                elif event.key == pygame.K_d:
                    velocity_x += movement_speed
                elif event.key == pygame.K_s:
                    velocity_y += movement_speed

        if is_dashing:
            dash_timer -= 1
            if dash_timer <= 0:
                is_dashing = False

        velocity_y += gravitational_force
        velocity_x *= friction

        block_x += velocity_x
        block_y += velocity_y

        if block_y + block_size > ground_height:
            block_y = ground_height - block_size
            velocity_y = 0
            on_ground = True
        else:
            on_ground = False

        if block_x < 0:
            block_x = 0
            velocity_x = 0
        if block_x + block_size > WIDTH:
            block_x = WIDTH - block_size
            velocity_x = 0

        screen.fill(WHITE)
        pygame.draw.rect(screen, BLACK, (0, ground_height, WIDTH, HEIGHT - ground_height))
        pygame.draw.rect(screen, block_color, (block_x, block_y, block_size, block_size))

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()

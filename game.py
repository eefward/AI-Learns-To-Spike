import pygame
import sys

pygame.init()

WIDTH, HEIGHT = 1600, 900

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
NET_COLOR = (255, 0, 0)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Block Physics Game")

clock = pygame.time.Clock()

block_size = 50
block_x = WIDTH - 200
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
roof_height = 50
on_ground = False

dash_duration = 5
dash_timer = 0
is_dashing = False

net_width = 10
net_height = 200
net_x = (WIDTH - net_width) // 2
net_y = ground_height - net_height

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
                    velocity_x -= movement_speed * 1.5
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
        elif block_y < roof_height:
            block_y = roof_height
            velocity_y = 0
        else:
            on_ground = False

        if block_x < 0:
            block_x = 0
            velocity_x = 0
        if block_x + block_size > WIDTH:
            block_x = WIDTH - block_size
            velocity_x = 0

        if net_x < block_x + block_size and block_x < net_x + net_width and net_y < block_y + block_size and block_y < net_y + net_height:
            if velocity_x > 0:
                velocity_x = -velocity_x * 0.5
                block_x = net_x - block_size
            elif velocity_x < 0:
                velocity_x = -velocity_x * 0.5
                block_x = net_x + net_width

        screen.fill(WHITE)
        pygame.draw.rect(screen, BLACK, (0, ground_height, WIDTH, HEIGHT - ground_height))
        pygame.draw.rect(screen, BLACK, (0, 0, WIDTH, roof_height))
        pygame.draw.rect(screen, NET_COLOR, (net_x, net_y, net_width, net_height))
        pygame.draw.rect(screen, block_color, (block_x, block_y, block_size, block_size))

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()

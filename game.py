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
dash_speed = 15
movement_speed = 5

ground_height = HEIGHT - 50
on_ground = False

def main():
    global block_x, block_y, velocity_x, velocity_y, on_ground

    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            velocity_x = -movement_speed
        elif keys[pygame.K_RIGHT]:
            velocity_x = movement_speed
        else:
            velocity_x *= friction

        if keys[pygame.K_SPACE] and on_ground:
            velocity_y = jump_force

        if keys[pygame.K_a]:
            block_x -= dash_speed
        if keys[pygame.K_q]:
            block_x -= dash_speed
            block_y -= dash_speed
        if keys[pygame.K_w]:
            block_y -= dash_speed
        if keys[pygame.K_e]:
            block_x += dash_speed
            block_y -= dash_speed
        if keys[pygame.K_d]:
            block_x += dash_speed
        if keys[pygame.K_c]:
            block_x += dash_speed
            block_y += dash_speed
        if keys[pygame.K_x]:
            block_y += dash_speed
        if keys[pygame.K_z]:
            block_x -= dash_speed
            block_y += dash_speed

        velocity_y += gravitational_force

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
        if block_x + block_size > WIDTH:
            block_x = WIDTH - block_size

        screen.fill(WHITE)

        pygame.draw.rect(screen, BLACK, (0, ground_height, WIDTH, HEIGHT - ground_height))

        pygame.draw.rect(screen, block_color, (block_x, block_y, block_size, block_size))

        pygame.display.flip()

        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()

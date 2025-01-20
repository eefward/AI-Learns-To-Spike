import pygame
import sys

pygame.init()

WIDTH, HEIGHT = 1000, 800 

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
push_force = 5
ground_height = HEIGHT - 50
roof_height = 50
on_ground = False

def main():
    global block_x, block_y, velocity_x, velocity_y, on_ground

    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    velocity_x -= dash_speed
                elif event.key == pygame.K_q:
                    velocity_x -= dash_speed
                    velocity_y += jump_force
                elif event.key == pygame.K_w:
                    velocity_y += jump_force
                elif event.key == pygame.K_e:
                    velocity_x += dash_speed
                    velocity_y += jump_force
                elif event.key == pygame.K_d:
                    velocity_x += dash_speed
                elif event.key == pygame.K_c:
                    velocity_x += dash_speed
                    velocity_y -= jump_force
                elif event.key == pygame.K_x:
                    velocity_y += dash_speed
                elif event.key == pygame.K_z:
                    velocity_x -= dash_speed
                    velocity_y -= jump_force

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

        if block_y < roof_height:
            block_y = roof_height
            velocity_y = 0

        if block_x < 0:
            block_x = 0
            velocity_x = 0
        if block_x + block_size > WIDTH:
            block_x = WIDTH - block_size
            velocity_x = 0

        screen.fill(WHITE)

        pygame.draw.rect(screen, BLACK, (0, ground_height, WIDTH, HEIGHT - ground_height)) 
        pygame.draw.rect(screen, BLACK, (0, 0, WIDTH, roof_height)) 

        pygame.draw.rect(screen, block_color, (block_x, block_y, block_size, block_size))

        pygame.display.flip()

        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()

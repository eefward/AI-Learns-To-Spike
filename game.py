import pygame
import sys

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)

# Initialize screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Block Physics Game")

# Clock for controlling frame rate
clock = pygame.time.Clock()

# Block properties
block_size = 50
block_x = WIDTH // 2
block_y = HEIGHT // 2
block_color = BLUE

# Physics properties
velocity_x = 0
velocity_y = 0
gravitational_force = 0.5
friction = 0.8
jump_force = -10
movement_speed = 5

ground_height = HEIGHT - 50
on_ground = False

def main():
    global block_x, block_y, velocity_x, velocity_y, on_ground

    running = True

    while running:
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Key state handling
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            velocity_x = -movement_speed
        elif keys[pygame.K_RIGHT]:
            velocity_x = movement_speed
        else:
            velocity_x *= friction

        if keys[pygame.K_SPACE] and on_ground:
            velocity_y = jump_force

        # Apply gravity
        velocity_y += gravitational_force

        # Update block position
        block_x += velocity_x
        block_y += velocity_y

        # Collision with ground
        if block_y + block_size > ground_height:
            block_y = ground_height - block_size
            velocity_y = 0
            on_ground = True
        else:
            on_ground = False

        # Collision with walls
        if block_x < 0:
            block_x = 0
        if block_x + block_size > WIDTH:
            block_x = WIDTH - block_size

        # Drawing
        screen.fill(WHITE)  # Clear screen

        # Draw ground
        pygame.draw.rect(screen, BLACK, (0, ground_height, WIDTH, HEIGHT - ground_height))

        # Draw block
        pygame.draw.rect(screen, block_color, (block_x, block_y, block_size, block_size))

        pygame.display.flip()

        # Cap the frame rate
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()

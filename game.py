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
angular_dash_speed = 15  # Base speed for more powerful angular dashes
movement_speed = 5
push_force = 5
ground_height = HEIGHT - 50
on_ground = False

dash_duration = 5  # Duration of the dash burst in frames
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
                if event.key == pygame.K_LEFT:
                    velocity_x -= push_force
                elif event.key == pygame.K_RIGHT:
                    velocity_x += push_force
                elif event.key == pygame.K_w and on_ground:
                    velocity_y = jump_force
                elif event.key == pygame.K_a and not is_dashing:  # Start dash left
                    velocity_x -= dash_speed
                    is_dashing = True
                    dash_timer = dash_duration
                elif event.key == pygame.K_q and not is_dashing:  # Start diagonal dash up-left (more powerful and angled)
                    velocity_x -= angular_dash_speed * 0.7  # Less horizontal movement
                    velocity_y -= angular_dash_speed  # More vertical movement
                    is_dashing = True
                    dash_timer = dash_duration
                elif event.key == pygame.K_w and not is_dashing:  # Start dash up
                    velocity_y -= dash_speed
                    is_dashing = True
                    dash_timer = dash_duration
                elif event.key == pygame.K_e and not is_dashing:  # Start diagonal dash up-right (more powerful and angled)
                    velocity_x += angular_dash_speed * 0.7  # Less horizontal movement
                    velocity_y -= angular_dash_speed  # More vertical movement
                    is_dashing = True
                    dash_timer = dash_duration
                elif event.key == pygame.K_d and not is_dashing:  # Start dash right
                    velocity_x += dash_speed
                    is_dashing = True
                    dash_timer = dash_duration
                elif event.key == pygame.K_c and not is_dashing:  # Start diagonal dash down-right (more powerful and angled)
                    velocity_x += angular_dash_speed  # More horizontal movement
                    velocity_y += angular_dash_speed * 0.7  # Less vertical movement
                    is_dashing = True
                    dash_timer = dash_duration
                elif event.key == pygame.K_x and not is_dashing:  # Start dash down
                    velocity_y += dash_speed
                    is_dashing = True
                    dash_timer = dash_duration
                elif event.key == pygame.K_z and not is_dashing:  # Start diagonal dash down-left (more powerful and angled)
                    velocity_x -= angular_dash_speed  # More horizontal movement
                    velocity_y += angular_dash_speed * 0.7  # Less vertical movement
                    is_dashing = True
                    dash_timer = dash_duration

        # Dash effect (burst)
        if is_dashing:
            dash_timer -= 1
            if dash_timer <= 0:  # Dash effect ends, normalize velocity
                is_dashing = False

        # Apply gravity and friction
        velocity_y += gravitational_force
        velocity_x *= friction

        block_x += velocity_x
        block_y += velocity_y

        # Collision with the ground
        if block_y + block_size > ground_height:
            block_y = ground_height - block_size
            velocity_y = 0
            on_ground = True
        else:
            on_ground = False

        # Prevent the block from going off the screen
        if block_x < 0:
            block_x = 0
            velocity_x = 0
        if block_x + block_size > WIDTH:
            block_x = WIDTH - block_size
            velocity_x = 0

        # Clear the screen
        screen.fill(WHITE)

        # Draw the ground
        pygame.draw.rect(screen, BLACK, (0, ground_height, WIDTH, HEIGHT - ground_height))

        # Draw the block
        pygame.draw.rect(screen, block_color, (block_x, block_y, block_size, block_size))

        # Update the display
        pygame.display.flip()

        # Cap the frame rate
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()

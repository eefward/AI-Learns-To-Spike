import pygame
import sys
import time

pygame.init()

WIDTH, HEIGHT = 1600, 900

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
NET_COLOR = (255, 0, 0)
BALL_COLOR = (255, 255, 0)
BUTTON_COLOR = (0, 255, 0)
BUTTON_TEXT_COLOR = (0, 0, 0)

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

initial_dash_change = 10
current_dash_change = initial_dash_change
max_air_dashes = 3
air_dashes_left = max_air_dashes

dash_divide_factor = 2

# Ball properties
ball_radius = 25
ball_x = net_x + net_width + 100  # Right of the net
ball_y = ground_height - ball_radius  # Ball starts on the ground
ball_velocity_x = 0
ball_velocity_y = 5  # Start with downward velocity
ball_bounce_factor = 0.7  # How much velocity is retained after bouncing
ball_launch_timer = 0  # Timer for 1.5 seconds delay
ball_boosted = False  # Flag to track if boost has happened

# Game timer
game_time = 6  # Game lasts 6 seconds
start_time = None
game_running = False
game_paused = False

# Start button
button_x = WIDTH // 2 - 100
button_y = HEIGHT // 2 - 50
button_width = 200
button_height = 100
button_text = "Start Game"

def draw_text(text, font, color, x, y):
    label = font.render(text, True, color)
    screen.blit(label, (x, y))

def main():
    global block_x, block_y, velocity_x, velocity_y, on_ground, dash_timer, is_dashing, current_dash_change, air_dashes_left, ball_x, ball_y, ball_velocity_x, ball_velocity_y
    global ball_launch_timer, ball_boosted, start_time, game_running, game_paused

    running = True
    while running:
        screen.fill(WHITE)

        if not game_running:
            font = pygame.font.Font(None, 74)
            draw_text(button_text, font, BUTTON_TEXT_COLOR, button_x + 30, button_y + 30)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = event.pos
                    if button_x <= mouse_x <= button_x + button_width and button_y <= mouse_y <= button_y + button_height:
                        game_running = True
                        start_time = time.time()

        if game_running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_w and not is_dashing and air_dashes_left > 0:
                        velocity_y -= dash_speed
                        is_dashing = True
                        dash_timer = dash_duration
                        air_dashes_left -= 1
                        current_dash_change = current_dash_change / dash_divide_factor

                    elif event.key == pygame.K_q and not is_dashing and air_dashes_left > 0:
                        velocity_x -= angular_dash_speed * 0.7
                        velocity_y -= angular_dash_speed
                        is_dashing = True
                        dash_timer = dash_duration
                        air_dashes_left -= 1
                        current_dash_change = current_dash_change / dash_divide_factor

                    elif event.key == pygame.K_e and not is_dashing and air_dashes_left > 0:
                        velocity_x += angular_dash_speed * 0.7
                        velocity_y -= angular_dash_speed
                        is_dashing = True
                        dash_timer = dash_duration
                        air_dashes_left -= 1
                        current_dash_change = current_dash_change / dash_divide_factor

                    elif event.key == pygame.K_d and not is_dashing and air_dashes_left > 0:
                        velocity_x += dash_speed
                        is_dashing = True
                        dash_timer = dash_duration
                        air_dashes_left -= 1
                        current_dash_change = current_dash_change / dash_divide_factor

                    elif event.key == pygame.K_a and not is_dashing and air_dashes_left > 0:
                        velocity_x -= dash_speed
                        is_dashing = True
                        dash_timer = dash_duration
                        air_dashes_left -= 1
                        current_dash_change = current_dash_change / dash_divide_factor

                    elif event.key == pygame.K_z and not is_dashing:
                        velocity_x -= angular_dash_speed
                        velocity_y += angular_dash_speed * 0.7
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

            # Ball physics: gravity and bouncing
            ball_velocity_y += gravitational_force
            ball_x += ball_velocity_x
            ball_y += ball_velocity_y

            if ball_launch_timer > 90 and not ball_boosted:  # 1.5 seconds passed (assuming 60 FPS)
                ball_velocity_y = -80  # Make the ball go higher
                ball_boosted = True  # Set flag to true so it doesn't boost again
                ball_launch_timer = -1  # Reset the timer to stop launching further

            ball_launch_timer += 1  # Increment the timer every frame

            if ball_y + ball_radius > ground_height:
                ball_y = ground_height - ball_radius
                ball_velocity_y = -ball_velocity_y * ball_bounce_factor

            if ball_y - ball_radius < roof_height:
                ball_y = roof_height + ball_radius
                ball_velocity_y = -ball_velocity_y * ball_bounce_factor

            if block_y + block_size > ground_height:
                block_y = ground_height - block_size
                velocity_y = 0
                on_ground = True
                air_dashes_left = max_air_dashes
                current_dash_change = initial_dash_change
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

            # Draw the ball
            pygame.draw.circle(screen, BALL_COLOR, (ball_x, ball_y), ball_radius)

            # Timer display
            elapsed_time = time.time() - start_time
            remaining_time = max(0, game_time - elapsed_time)
            font = pygame.font.Font(None, 36)
            draw_text(f"Time: {int(remaining_time)}s", font, BLACK, 10, 10)

            if remaining_time == 0:
                game_running = False
                game_paused = True
                draw_text("Game Over! Press r to Restart", font, BLACK, WIDTH // 2 - 150, HEIGHT // 2)

            pygame.display.flip()

        if game_paused:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                    game_running = False
                    game_paused = False
                    ball_boosted = False
                    ball_x = net_x + net_width + 100
                    ball_y = ground_height - ball_radius
                    ball_velocity_y = 5
                    velocity_x = 0
                    velocity_y = 0
                    block_x = WIDTH - 200
                    block_y = HEIGHT // 2
                    start_time = None
                    air_dashes_left = max_air_dashes
                    ball_launch_timer = 0

        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()

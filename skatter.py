import pygame
import random

# Constants
WIDTH, HEIGHT = 800, 600
PADDLE_WIDTH, PADDLE_HEIGHT = 10, 100
BALL_SIZE = 15
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)

# Power-up class
class PowerUp:
    def __init__(self):
        self.rect = pygame.Rect(random.randint(100, WIDTH - 100), random.randint(100, HEIGHT - 100), 20, 20)
        self.active = False

    def draw(self, screen):
        if self.active:
            pygame.draw.rect(screen, GREEN, self.rect)

# Paddle class
class Paddle:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, PADDLE_WIDTH, PADDLE_HEIGHT)
        self.speed = 10

    def move(self, up=True):
        if up:
            self.rect.y -= self.speed
        else:
            self.rect.y += self.speed

        # Keep paddle on screen
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT

# Ball class
class Ball:
    def __init__(self):
        self.rect = pygame.Rect(WIDTH // 2, HEIGHT // 2, BALL_SIZE, BALL_SIZE)
        self.vx = random.choice([-5, 5])
        self.vy = random.choice([-5, 5])

    def move(self):
        self.rect.x += self.vx
        self.rect.y += self.vy

        # Bounce off top and bottom walls
        if self.rect.top <= 0 or self.rect.bottom >= HEIGHT:
            self.vy *= -1

    def reset(self):
        self.rect.center = (WIDTH // 2, HEIGHT // 2)
        self.vx = random.choice([-5, 5])
        self.vy = random.choice([-5, 5])

# Game class
class PongGame:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Skatters")
        self.clock = pygame.time.Clock()

        # Initialize paddles and ball
        self.left_paddle = Paddle(10, HEIGHT // 2 - PADDLE_HEIGHT // 2)
        self.right_paddle = Paddle(WIDTH - 20, HEIGHT // 2 - PADDLE_HEIGHT // 2)
        self.ball = Ball()

        # Score
        self.left_score = 0
        self.right_score = 0

        # Power-up
        self.power_up = PowerUp()
        self.spawn_power_up()

        self.running = True
        self.winner = None

        # Display welcome message
        self.display_welcome_message()

    def spawn_power_up(self):
        self.power_up.active = True

    def display_welcome_message(self):
        font = pygame.font.Font(None, 36)
        text = font.render("Welcome To Skatters - Play with no worries", True, WHITE)
        text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        self.screen.fill(BLACK)
        self.screen.blit(text, text_rect)
        pygame.display.flip()
        pygame.time.wait(3000)  # Display message for 3 seconds

    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(60)

        pygame.quit()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.left_paddle.move(up=True)
        if keys[pygame.K_s]:
            self.left_paddle.move(up=False)
        if keys[pygame.K_UP]:
            self.right_paddle.move(up=True)
        if keys[pygame.K_DOWN]:
            self.right_paddle.move(up=False)

        self.ball.move()

        # Ball and paddle collision
        if self.ball.rect.colliderect(self.left_paddle.rect):
            self.ball.vx *= -1
        if self.ball.rect.colliderect(self.right_paddle.rect):
            self.ball.vx *= -1

        # Check for scoring
        if self.ball.rect.left <= 0:
            self.right_score += 1
            self.ball.reset()
        if self.ball.rect.right >= WIDTH:
            self.left_score += 1
            self.ball.reset()

        # Power-up collision
        if self.power_up.active and self.ball.rect.colliderect(self.power_up.rect):
            self.ball.vx *= 1.5  # Increase ball speed
            self.power_up.active = False  # Deactivate power-up

        # Respawn power-up
        if not self.power_up.active:
            self.spawn_power_up()

        # Check for win condition
        if self.left_score >= 10:
            self.winner = "Left Player Wins!"
            self.running = False
        if self.right_score >= 10:
            self.winner = "Right Player Wins!"
            self.running = False

    def draw(self):
        self.screen.fill(BLACK)
        pygame.draw.rect(self.screen, WHITE, self.left_paddle.rect)
        pygame.draw.rect(self.screen, WHITE, self.right_paddle.rect)
        pygame.draw.ellipse(self.screen, WHITE, self.ball.rect)
        pygame.draw.aaline(self.screen, WHITE, (WIDTH // 2, 0), (WIDTH // 2, HEIGHT))

        # Draw power-up
        self.power_up.draw(self.screen)

        # Draw scores
        font = pygame.font.Font(None, 74)
        left_text = font.render(str(self.left_score), True, WHITE)
        right_text = font.render(str(self.right_score), True, WHITE)
        self.screen.blit(left_text, (WIDTH // 4, 10))
        self.screen.blit(right_text, (WIDTH * 3 // 4, 10))

        # Draw winner message
        if self.winner:
            font = pygame.font.Font(None, 50)
            winner_text = font.render(self.winner, True, WHITE)
            winner_rect = winner_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
            self.screen.blit(winner_text, winner_rect)

        pygame.display.flip()

# Start the game
if __name__ == "__main__":
    game = PongGame()
    game.run()

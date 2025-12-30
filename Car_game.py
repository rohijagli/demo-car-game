import pygame
import random
import sys

# ================= INIT =================
pygame.init()

WIDTH, HEIGHT = 400, 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Car Racing Game Demo")

CLOCK = pygame.time.Clock()
FPS = 60

# ================= COLORS =================
WHITE = (255, 255, 255)
GRAY = (40, 40, 40)
RED = (200, 50, 50)
BLUE = (50, 150, 255)
DARK_BLUE = (0, 0, 100)
DARK_RED = (100, 0, 0)
ROAD_COLOR = (100, 100, 100)
BLACK = (0, 0, 0)

# ================= FONTS =================
font = pygame.font.SysFont(None, 30)
big_font = pygame.font.SysFont(None, 48)

# ================= CLASSES =================
class Player:
    def __init__(self):
        self.width = 50
        self.height = 90
        self.x = WIDTH // 2 - self.width // 2
        self.y = HEIGHT - self.height - 20
        self.speed = 6
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def move(self, keys):
        if keys[pygame.K_LEFT] and self.x > 50:
            self.x -= self.speed
        if keys[pygame.K_RIGHT] and self.x < WIDTH - 100:
            self.x += self.speed
        self.rect.topleft = (self.x, self.y)

    def draw(self):
        # Demo player car: blue rectangle with black wheels
        pygame.draw.rect(WIN, BLUE, self.rect)
        # Wheels
        pygame.draw.rect(WIN, BLACK, (self.x + 5, self.y + 10, 10, 20))
        pygame.draw.rect(WIN, BLACK, (self.x + 35, self.y + 10, 10, 20))
        pygame.draw.rect(WIN, BLACK, (self.x + 5, self.y + 60, 10, 20))
        pygame.draw.rect(WIN, BLACK, (self.x + 35, self.y + 60, 10, 20))
        # Roof
        pygame.draw.rect(WIN, DARK_BLUE, (self.x + 10, self.y + 20, 30, 50))

class Enemy:
    def __init__(self):
        self.width = 50
        self.height = 90
        self.reset()
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def reset(self):
        self.x = random.randint(50, WIDTH - 100)
        self.y = random.randint(-600, -100)
        self.speed = random.uniform(4, 7)
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def move(self):
        self.y += self.speed
        self.rect.topleft = (self.x, self.y)
        if self.y > HEIGHT:
            self.reset()
            return True
        return False

    def draw(self):
        # Demo enemy car: red rectangle with black wheels
        pygame.draw.rect(WIN, RED, self.rect)
        # Wheels
        pygame.draw.rect(WIN, BLACK, (self.x + 5, self.y + 10, 10, 20))
        pygame.draw.rect(WIN, BLACK, (self.x + 35, self.y + 10, 10, 20))
        pygame.draw.rect(WIN, BLACK, (self.x + 5, self.y + 60, 10, 20))
        pygame.draw.rect(WIN, BLACK, (self.x + 35, self.y + 60, 10, 20))
        # Roof
        pygame.draw.rect(WIN, DARK_RED, (self.x + 10, self.y + 20, 30, 50))

# ================= GAME =================
class Game:
    def __init__(self):
        self.reset()

    def reset(self):
        self.player = Player()
        self.enemies = [Enemy() for _ in range(3)]
        self.score = 0
        self.highscore = 0
        self.game_over = False
        self.road_y = 0

    def draw_road(self):
        self.road_y += 6
        if self.road_y > 40:
            self.road_y = 0
        # Road
        pygame.draw.rect(WIN, ROAD_COLOR, (50, 0, WIDTH - 100, HEIGHT))
        # Center dashed line
        for i in range(0, HEIGHT, 40):
            pygame.draw.rect(WIN, WHITE, (WIDTH//2 - 5, i + self.road_y, 10, 30))
        # Boundaries
        pygame.draw.line(WIN, WHITE, (50, 0), (50, HEIGHT), 5)
        pygame.draw.line(WIN, WHITE, (WIDTH - 50, 0), (WIDTH - 50, HEIGHT), 5)

    def update(self):
        keys = pygame.key.get_pressed()
        self.player.move(keys)

        for enemy in self.enemies:
            if enemy.move():
                self.score += 1

        # Gradual speed increase
        for enemy in self.enemies:
            enemy.speed += 0.002

        # Collision detection
        for enemy in self.enemies:
            if self.player.rect.colliderect(enemy.rect):
                self.game_over = True
                if self.score > self.highscore:
                    self.highscore = self.score

    def draw_ui(self):
        WIN.blit(font.render(f"Score: {self.score}", True, WHITE), (10, 10))
        WIN.blit(font.render(f"High Score: {self.highscore}", True, WHITE), (10, 40))

    def draw_game_over(self):
        WIN.blit(big_font.render("GAME OVER", True, RED),
                 (WIDTH//2 - 120, HEIGHT//2 - 40))
        WIN.blit(font.render("Press R to Restart", True, WHITE),
                 (WIDTH//2 - 110, HEIGHT//2 + 10))

    def draw(self):
        WIN.fill(GRAY)
        self.draw_road()
        self.player.draw()
        for enemy in self.enemies:
            enemy.draw()
        self.draw_ui()
        if self.game_over:
            self.draw_game_over()

# ================= MAIN LOOP =================
def main():
    game = Game()
    running = True

    while running:
        CLOCK.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        if not game.game_over:
            game.update()
        else:
            if pygame.key.get_pressed()[pygame.K_r]:
                game.reset()

        game.draw()
        pygame.display.update()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()

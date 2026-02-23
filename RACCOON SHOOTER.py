import pygame
import random

pygame.init()

WIDTH, HEIGHT = 1280, 720
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Raccoon Cookie Dodger")

clock = pygame.time.Clock()

# -------- IMAGES --------
menu_bg = pygame.transform.scale(pygame.image.load("Premium Vector _ Cartoon style of space with gas clouds.jpeg"), (WIDTH, HEIGHT))
button_img = pygame.image.load("Button.png").convert_alpha()

bg = pygame.transform.scale(pygame.image.load("fondo.jpg"), (WIDTH, HEIGHT))
gameover_bg = pygame.transform.scale(pygame.image.load("gameOVER.jpeg"), (WIDTH, HEIGHT))

player_img = pygame.transform.scale(pygame.image.load("raccoon.png").convert_alpha(), (130, 130))
cookie_img = pygame.transform.scale(pygame.image.load("galleta.png").convert_alpha(), (70, 70))

# -------- BUTTON --------
button_rect = button_img.get_rect(center=(WIDTH//2, HEIGHT//2 + 120))  # botón más abajo

# -------- PLAYER --------
player_rect = player_img.get_rect(midbottom=(WIDTH//2, HEIGHT-20))
player_speed = 8

# -------- SCORE SYSTEM --------
def load_scores():
    try:
        with open("high_scores.txt", "r") as f:
            return [int(x) for x in f.read().split(",") if x]
    except:
        return []

def save_scores(scores):
    with open("high_scores.txt", "w") as f:
        f.write(",".join(map(str, scores)))

scores = load_scores()

font_big = pygame.font.SysFont(None, 80)
font_small = pygame.font.SysFont(None, 40)
menu_font = pygame.font.SysFont(None, 110)  # font grande del menú

# -------- STATES --------
menu = True
game_over = False
score = 0

def reset_game():
    global cookies, lasers, score, game_over

    player_rect.midbottom = (WIDTH//2, HEIGHT-20)
    score = 0
    game_over = False

    cookies.clear()
    lasers.clear()

    for i in range(5):
        rect = cookie_img.get_rect(center=(random.randint(0, WIDTH), random.randint(-500, 0)))
        cookies.append(rect)

    for i in range(6):
        lasers.append(pygame.Rect(random.randint(0, WIDTH), random.randint(-600, 0), 6, 40))

cookies = []
lasers = []
reset_game()

cookie_speed = 4
laser_speed = 6

# -------- LOOP --------
running = True
while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # ---- MENU CLICK ----
        if menu and event.type == pygame.MOUSEBUTTONDOWN:
            if button_rect.collidepoint(event.pos):
                menu = False
                reset_game()

        # ---- RESTART ----
        if game_over and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                reset_game()

    # -------- MENU --------
    if menu:
        screen.blit(menu_bg, (0, 0))

        title_text = menu_font.render("Press to Start", True, "white")
        screen.blit(title_text, title_text.get_rect(center=(WIDTH//2, HEIGHT//2 - 40)))

        screen.blit(button_img, button_rect)

    # -------- GAME --------
    elif not game_over:
        screen.blit(bg, (0, 0))

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player_rect.left > 0:
            player_rect.x -= player_speed
        if keys[pygame.K_RIGHT] and player_rect.right < WIDTH:
            player_rect.x += player_speed

        # COOKIES
        for rect in cookies:
            rect.y += cookie_speed
            screen.blit(cookie_img, rect)

            if rect.colliderect(player_rect):
                rect.y = random.randint(-500, 0)
                rect.x = random.randint(0, WIDTH)
                score += 1

            if rect.y > HEIGHT:
                rect.y = random.randint(-500, 0)
                rect.x = random.randint(0, WIDTH)

        # LASERS
        for laser in lasers:
            laser.y += laser_speed
            pygame.draw.rect(screen, "red", laser, border_radius=3)

            if player_rect.colliderect(laser):
                game_over = True
                scores.append(score)
                scores.sort(reverse=True)
                scores[:] = scores[:3]
                save_scores(scores)

            if laser.y > HEIGHT:
                laser.y = random.randint(-600, 0)
                laser.x = random.randint(0, WIDTH)

        screen.blit(player_img, player_rect)

        high = scores[0] if scores else 0
        text = font_small.render(f"Cookies: {score}  Highscore: {high}", True, "white")
        screen.blit(text, (20, 20))

    # -------- GAME OVER --------
    else:
        screen.blit(gameover_bg, (0, 0))

        over_text = font_big.render("GAME OVER", True, "white")
        screen.blit(over_text, over_text.get_rect(center=(WIDTH//2, HEIGHT//2 - 120)))

        score_text = font_small.render(f"Score: {score}", True, "white")
        screen.blit(score_text, score_text.get_rect(center=(WIDTH//2, HEIGHT//2 - 40)))

        for i, s in enumerate(scores):
            hs = font_small.render(f"Top {i+1}: {s}", True, "white")
            screen.blit(hs, hs.get_rect(center=(WIDTH//2, HEIGHT//2 + i*40)))

        restart_text = font_small.render("Press R to play again", True, "white")
        screen.blit(restart_text, restart_text.get_rect(center=(WIDTH//2, HEIGHT//2 + 140)))

    pygame.display.update()
    clock.tick(60)

pygame.quit()
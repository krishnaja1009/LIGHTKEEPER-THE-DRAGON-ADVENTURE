import pygame
import random

pygame.init()

# SCREEN
WIDTH, HEIGHT = 900, 650
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("LIGHTKEEPER - Dragon Adventure")
clock = pygame.time.Clock()

# FONTS
font = pygame.font.SysFont("arial", 24, bold=True)
big = pygame.font.SysFont("arial", 52, bold=True)
small = pygame.font.SysFont("arial", 17)

# COLORS
WHITE = (255, 255, 255)
BLACK = (10, 10, 30)
GOLD = (255, 210, 40)
RED = (255, 60, 60)
BLUE = (60, 180, 255)
PURPLE = (160, 60, 255)
GREEN = (50, 230, 120)
ORANGE = (255, 130, 20)
CYAN = (80, 240, 255)

# DIFFICULTY
DIFFICULTIES = {
    "Easy": 4,
    "Medium": 6,
    "Hard": 8
}
difficulty = "Easy"

# GAME VARIABLES
state = "MENU"
pause_from = "PLAY"

score = 0
coins = 0
lives = 3
level = 1

# DRAGON SKINS
skins = [
    ("Fire Dragon", ORANGE, 0),
    ("Ice Dragon", CYAN, 50),
    ("Shadow Dragon", PURPLE, 100),
    ("Golden Dragon", GOLD, 200)
]

unlocked = [0]
selected_skin = 0

# PLAYER
player = pygame.Rect(100, 300, 60, 50)
player_speed = 5

# OBJECTS
feathers = []
clouds = []
coin_items = []
powerups = []
fireballs = []
boss_shots = []

# BACKGROUND
stars = [
    [random.randint(0, WIDTH),
     random.randint(0, HEIGHT),
     random.randint(1, 3)]
    for _ in range(70)
]

houses = [
    [i * 160, random.randint(430, 480)]
    for i in range(7)
]

# TIMERS
feather_timer = 0
cloud_timer = 0
coin_timer = 0
power_timer = 0
fire_timer = 0
shield_timer = 0

# PORTAL
portal = pygame.Rect(850, 200, 70, 110)
portal_active = False
portal_wait = 0
bonus_timer = 0

# BOSS
boss = pygame.Rect(680, 230, 130, 130)
boss_hp = 100
boss_direction = 1
boss_timer = 0


# ==================================
# TEXT FUNCTION
# ==================================

def draw_text(message, font_type, color, x, y):
    image = font_type.render(str(message), True, color)
    rect = image.get_rect(center=(x, y))
    screen.blit(image, rect)


# ==================================
# BACKGROUND
# ==================================

def draw_background():
    screen.fill((8, 12, 40))

    for star in stars:
        pygame.draw.circle(
            screen, WHITE,
            (int(star[0]), int(star[1])),
            star[2]
        )

        star[0] -= 2

        if star[0] < 0:
            star[0] = WIDTH
            star[1] = random.randint(0, 450)

    for house in houses:
        x, y = house

        pygame.draw.rect(
            screen, (40, 45, 90),
            (x, y, 75, 100)
        )

        pygame.draw.polygon(
            screen, PURPLE,
            [(x - 10, y), (x + 35, y - 40),
             (x + 85, y)]
        )

        pygame.draw.rect(
            screen, GOLD,
            (x + 15, y + 25, 15, 20)
        )

        pygame.draw.rect(
            screen, GOLD,
            (x + 45, y + 25, 15, 20)
        )

        house[0] -= 2

        if house[0] < -100:
            house[0] = WIDTH + random.randint(0, 100)

    pygame.draw.rect(
        screen, (20, 25, 55),
        (0, 520, WIDTH, 130)
    )


# ==================================
# DRAGON CHARACTER
# ==================================

def draw_dragon():
    color = skins[selected_skin][1]
    x, y = player.x, player.y

    # Wings
    pygame.draw.polygon(
        screen, color,
        [(x + 20, y + 20),
         (x - 10, y - 20),
         (x + 40, y + 10)]
    )

    pygame.draw.polygon(
        screen, color,
        [(x + 35, y + 20),
         (x + 65, y - 20),
         (x + 50, y + 40)]
    )

    # Body
    pygame.draw.ellipse(
        screen, color,
        (x + 5, y + 15, 45, 30)
    )

    # Head
    pygame.draw.circle(
        screen, color,
        (x + 50, y + 15), 20
    )

    # Horn
    pygame.draw.polygon(
        screen, GOLD,
        [(x + 40, y + 2),
         (x + 38, y - 15),
         (x + 50, y + 3)]
    )

    # Eye
    pygame.draw.circle(
        screen, WHITE,
        (x + 57, y + 10), 5
    )

    pygame.draw.circle(
        screen, BLACK,
        (x + 58, y + 10), 2
    )

    # Tail
    pygame.draw.polygon(
        screen, color,
        [(x + 10, y + 30),
         (x - 15, y + 15),
         (x + 5, y + 40)]
    )

    # Shield
    if shield_timer > 0:
        pygame.draw.circle(
            screen, CYAN,
            player.center, 43, 3
        )


# ==================================
# OBJECT DRAWING
# ==================================

def draw_cloud(rect):
    pygame.draw.circle(
        screen, (90, 100, 130),
        (rect.x + 15, rect.y + 20), 20
    )

    pygame.draw.circle(
        screen, (100, 110, 140),
        (rect.x + 35, rect.y + 10), 24
    )

    pygame.draw.circle(
        screen, (90, 100, 130),
        (rect.x + 55, rect.y + 20), 20
    )


def draw_feather(rect):
    pygame.draw.ellipse(screen, GOLD, rect)

    pygame.draw.line(
        screen, WHITE,
        rect.topleft, rect.bottomright, 2
    )


def draw_coin(rect):
    pygame.draw.circle(
        screen, GOLD, rect.center, 13
    )

    pygame.draw.circle(
        screen, ORANGE, rect.center, 9, 2
    )

    draw_text(
        "$", small, WHITE,
        rect.centerx, rect.centery
    )


def draw_portal():
    pygame.draw.ellipse(
        screen, PURPLE, portal, 6
    )

    pygame.draw.ellipse(
        screen, CYAN,
        portal.inflate(-20, -20), 3
    )

    draw_text(
        "PORTAL", small, WHITE,
        portal.centerx, portal.bottom + 15
    )


# ==================================
# RESET GAME
# ==================================

def reset_game():
    global score, lives, level, state
    global shield_timer, fire_timer
    global feather_timer, cloud_timer
    global coin_timer, power_timer
    global portal_active, portal_wait
    global boss_hp, boss_timer
    global bonus_timer, boss_direction

    score = 0
    lives = 3
    level = 1

    player.x = 100
    player.y = 300

    shield_timer = 0
    fire_timer = 0

    feather_timer = 0
    cloud_timer = 0
    coin_timer = 0
    power_timer = 0

    feathers.clear()
    clouds.clear()
    coin_items.clear()
    powerups.clear()
    fireballs.clear()
    boss_shots.clear()

    portal_active = False
    portal_wait = 0
    bonus_timer = 0

    boss_hp = 100
    boss_timer = 0
    boss_direction = 1

    state = "PLAY"


# ==================================
# SPAWN OBJECTS
# ==================================

def spawn_objects():
    global feather_timer, cloud_timer
    global coin_timer, power_timer

    feather_timer += 1
    cloud_timer += 1
    coin_timer += 1
    power_timer += 1

    if feather_timer > 65:
        feathers.append(
            pygame.Rect(
                WIDTH,
                random.randint(70, 470),
                30, 30
            )
        )
        feather_timer = 0

    if cloud_timer > 100:
        clouds.append(
            pygame.Rect(
                WIDTH,
                random.randint(80, 470),
                65, 40
            )
        )
        cloud_timer = 0

    if coin_timer > 55:
        coin_items.append(
            pygame.Rect(
                WIDTH,
                random.randint(80, 470),
                25, 25
            )
        )
        coin_timer = 0

    if power_timer > 350:
        powerups.append(
            pygame.Rect(
                WIDTH,
                random.randint(80, 450),
                30, 30
            )
        )
        power_timer = 0


# ==================================
# FIRE BREATH
# ==================================

def shoot_fire():
    global fire_timer

    if fire_timer <= 0:
        fireballs.append(
            pygame.Rect(
                player.right,
                player.y + 15,
                35, 18
            )
        )

        fire_timer = 35


def update_fire():
    for fire in fireballs[:]:
        fire.x += 12

        pygame.draw.ellipse(
            screen, ORANGE, fire
        )

        pygame.draw.ellipse(
            screen, GOLD,
            (fire.x + 5, fire.y + 4, 20, 10)
        )

        if fire.x > WIDTH:
            fireballs.remove(fire)


# ==================================
# BOSS DRAWING
# ==================================

def draw_boss():
    pygame.draw.circle(
        screen, (100, 20, 100),
        boss.center, 65
    )

    pygame.draw.circle(
        screen, (160, 35, 70),
        boss.center, 50
    )

    # Eyes
    pygame.draw.circle(
        screen, RED,
        (boss.x + 40, boss.y + 45), 12
    )

    pygame.draw.circle(
        screen, RED,
        (boss.x + 90, boss.y + 45), 12
    )

    # Horns
    pygame.draw.polygon(
        screen, WHITE,
        [(boss.x + 20, boss.y + 15),
         (boss.x + 5, boss.y - 25),
         (boss.x + 45, boss.y + 15)]
    )

    pygame.draw.polygon(
        screen, WHITE,
        [(boss.x + 85, boss.y + 15),
         (boss.x + 115, boss.y - 25),
         (boss.x + 105, boss.y + 20)]
    )

    pygame.draw.line(
        screen, BLACK,
        (boss.x + 35, boss.y + 90),
        (boss.x + 95, boss.y + 90), 5
    )


# ==================================
# BOSS UPDATE
# ==================================

def update_boss():
    global boss_hp, boss_direction
    global boss_timer, lives, state

    boss.y += boss_direction * 3

    if boss.y < 80 or boss.y > 410:
        boss_direction *= -1

    boss_timer += 1

    if boss_timer > 85:
        boss_shots.append(
            pygame.Rect(
                boss.x, boss.centery, 25, 18
            )
        )

        boss_timer = 0

    for shot in boss_shots[:]:
        shot.x -= 8

        if player.colliderect(shot):
            boss_shots.remove(shot)

            if shield_timer <= 0:
                lives -= 1

        elif shot.right < 0:
            boss_shots.remove(shot)

    for fire in fireballs[:]:
        if fire.colliderect(boss):
            fireballs.remove(fire)
            boss_hp -= 10

    if boss_hp <= 0:
        state = "WIN"

    if lives <= 0:
        state = "GAMEOVER"


# ==================================
# MAIN GAME LOOP
# ==================================

running = True

while running:

    clock.tick(60)

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:

            # MENU
            if state == "MENU":

                if event.key == pygame.K_1:
                    difficulty = "Easy"

                if event.key == pygame.K_2:
                    difficulty = "Medium"

                if event.key == pygame.K_3:
                    difficulty = "Hard"

                if event.key == pygame.K_RETURN:
                    reset_game()

                if event.key == pygame.K_c:
                    state = "SHOP"

            # SHOP
            elif state == "SHOP":

                if event.key in (
                    pygame.K_1, pygame.K_2,
                    pygame.K_3, pygame.K_4
                ):

                    index = int(event.unicode) - 1
                    price = skins[index][2]

                    if index in unlocked:
                        selected_skin = index

                    elif coins >= price:
                        coins -= price
                        unlocked.append(index)
                        selected_skin = index

                if event.key == pygame.K_ESCAPE:
                    state = "MENU"

            # GAME
            elif state in ("PLAY", "BONUS", "BOSS"):

                if event.key == pygame.K_SPACE:
                    shoot_fire()

                if event.key == pygame.K_p:
                    pause_from = state
                    state = "PAUSE"

                if event.key == pygame.K_r:
                    reset_game()

            # PAUSE
            elif state == "PAUSE":

                if event.key == pygame.K_p:
                    state = pause_from

                if event.key == pygame.K_r:
                    reset_game()

                if event.key == pygame.K_m:
                    state = "MENU"

            # GAME OVER / WIN
            elif state in ("WIN", "GAMEOVER"):

                if event.key == pygame.K_r:
                    reset_game()

                if event.key == pygame.K_RETURN:
                    state = "MENU"

    keys = pygame.key.get_pressed()

    # ==================================
    # MENU SCREEN
    # ==================================

    if state == "MENU":

        draw_background()

        draw_text(
            "LIGHTKEEPER", big, GOLD, 450, 110
        )

        draw_text(
            "DRAGON ADVENTURE", font, CYAN, 450, 170
        )

        draw_text(
            "1 - EASY", font, WHITE, 450, 245
        )

        draw_text(
            "2 - MEDIUM", font, WHITE, 450, 290
        )

        draw_text(
            "3 - HARD", font, WHITE, 450, 335
        )

        draw_text(
            "Selected: " + difficulty,
            font, GREEN, 450, 390
        )

        draw_text(
            "ENTER - START GAME",
            font, GOLD, 450, 450
        )

        draw_text(
            "C - DRAGON SHOP",
            font, CYAN, 450, 500
        )

        draw_text(
            "Coins: " + str(coins),
            font, GOLD, 450, 550
        )

    # ==================================
    # SHOP SCREEN
    # ==================================

    elif state == "SHOP":

        draw_background()

        draw_text(
            "DRAGON SKIN SHOP",
            big, GOLD, 450, 90
        )

        draw_text(
            "Coins: " + str(coins),
            font, WHITE, 450, 155
        )

        for i, skin in enumerate(skins):

            y = 230 + i * 75

            pygame.draw.circle(
                screen, skin[1], (220, y), 22
            )

            status = (
                "UNLOCKED" if i in unlocked
                else str(skin[2]) + " coins"
            )

            if selected_skin == i:
                status += " - SELECTED"

            draw_text(
                str(i + 1) + " - " + skin[0] +
                " : " + status,
                small, WHITE, 510, y
            )

        draw_text(
            "Press 1, 2, 3 or 4 to buy/select",
            small, CYAN, 450, 565
        )

        draw_text(
            "ESC - BACK", font, GOLD, 450, 615
        )

    # ==================================
    # GAMEPLAY
    # ==================================

    elif state in ("PLAY", "BONUS", "BOSS"):

        draw_background()

        # Player movement
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            player.x -= player_speed

        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            player.x += player_speed

        if keys[pygame.K_UP] or keys[pygame.K_w]:
            player.y -= player_speed

        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            player.y += player_speed

        player.clamp_ip(screen.get_rect())

        if fire_timer > 0:
            fire_timer -= 1

        if shield_timer > 0:
            shield_timer -= 1

        # NORMAL GAME
        if state == "PLAY":

            spawn_objects()

            speed = DIFFICULTIES[difficulty]

            # Feathers
            for item in feathers[:]:

                item.x -= speed

                if player.colliderect(item):
                    feathers.remove(item)
                    score += 25

                elif item.right < 0:
                    feathers.remove(item)

            # Storm clouds
            for cloud in clouds[:]:

                cloud.x -= speed

                if player.colliderect(cloud):

                    clouds.remove(cloud)

                    if shield_timer <= 0:
                        lives -= 1

                elif cloud.right < 0:
                    clouds.remove(cloud)

            # Coins
            for coin in coin_items[:]:

                coin.x -= speed

                if player.colliderect(coin):
                    coin_items.remove(coin)
                    coins += 10
                    score += 10

                elif coin.right < 0:
                    coin_items.remove(coin)

            # Shield power-ups
            for power in powerups[:]:

                power.x -= speed

                if player.colliderect(power):
                    powerups.remove(power)
                    shield_timer = 300

                elif power.right < 0:
                    powerups.remove(power)

            # Draw objects
            for item in feathers:
                draw_feather(item)

            for cloud in clouds:
                draw_cloud(cloud)

            for coin in coin_items:
                draw_coin(coin)

            for power in powerups:
                pygame.draw.circle(
                    screen, CYAN, power.center, 15
                )

            # Level
            level = min(5, score // 100 + 1)

            # Magic portal
            if portal_wait > 0:
                portal_wait -= 1

            if score >= 100 and not portal_active and portal_wait == 0:
                portal_active = True
                portal.x = WIDTH
                portal.y = random.randint(150, 350)

            if portal_active:

                portal.x -= speed
                draw_portal()

                if player.colliderect(portal):
                    portal_active = False
                    portal_wait = 1200
                    bonus_timer = 600
                    coin_items.clear()
                    state = "BONUS"

                elif portal.right < 0:
                    portal_active = False
                    portal_wait = 500

            # Boss starts at 500 points
            if score >= 500:
                state = "BOSS"

        # ==================================
        # BONUS WORLD
        # ==================================

        elif state == "BONUS":

            screen.fill((35, 10, 75))

            draw_text(
                "MAGIC BONUS WORLD",
                big, GOLD, 450, 70
            )

            draw_text(
                "Collect extra coins!",
                font, WHITE, 450, 125
            )

            bonus_timer -= 1

            if random.randint(1, 18) == 1:
                coin_items.append(
                    pygame.Rect(
                        WIDTH,
                        random.randint(80, 470),
                        25, 25
                    )
                )

            for coin in coin_items[:]:

                coin.x -= 7

                if player.colliderect(coin):
                    coin_items.remove(coin)
                    coins += 20
                    score += 20

                elif coin.right < 0:
                    coin_items.remove(coin)

            for coin in coin_items:
                draw_coin(coin)

            draw_text(
                "Time: " + str(max(0, bonus_timer // 60)),
                font, CYAN, 450, 170
            )

            if bonus_timer <= 0:
                coin_items.clear()
                state = "PLAY"

        # ==================================
        # BOSS BATTLE
        # ==================================

        elif state == "BOSS":

            draw_text(
                "FINAL BOSS BATTLE!",
                big, RED, 450, 65
            )

            draw_boss()
            update_boss()

            for shot in boss_shots:
                pygame.draw.ellipse(
                    screen, RED, shot
                )

            # Health bar
            pygame.draw.rect(
                screen, RED,
                (250, 125, 400, 22)
            )

            pygame.draw.rect(
                screen, GREEN,
                (250, 125,
                 max(0, 400 * boss_hp / 100), 22)
            )

            pygame.draw.rect(
                screen, WHITE,
                (250, 125, 400, 22), 2
            )

            draw_text(
                "BOSS HP: " + str(max(0, boss_hp)),
                small, WHITE, 450, 165
            )

        # Fireballs and dragon
        update_fire()
        draw_dragon()
        # HUD
        draw_text(
            "Score: " + str(score),
            font, WHITE, 85, 20
        )

        draw_text(
            "Coins: " + str(coins),
            font, GOLD, 85, 55
        )

        draw_text(
            "Lives: " + str(lives),
            font, RED, 85, 90
        )

        draw_text(
            "Level: " + str(level),
            font, CYAN, 85, 125
        )

        if shield_timer > 0:
            draw_text(
                "SHIELD ACTIVE",
                small, CYAN, 770, 25
            )

        draw_text(
            "SPACE: FIRE | P: PAUSE | R: RESTART",
            small, WHITE, 450, 625
        )

        if lives <= 0:
            state = "GAMEOVER"

    # ==================================
    # PAUSE SCREEN
    # ==================================
    elif state == "PAUSE":

        draw_background()

        draw_text(
            "GAME PAUSED",
            big, GOLD, 450, 230
        )

        draw_text(
            "P - CONTINUE",
            font, WHITE, 450, 310
        )

        draw_text(
            "R - RESTART",
            font, CYAN, 450, 360
        )

        draw_text(
            "M - MAIN MENU",
            font, WHITE, 450, 410
        )

    # ==================================
    # GAME OVER
    # ==================================

    elif state == "GAMEOVER":

        draw_background()

        draw_text(
            "GAME OVER",
            big, RED, 450, 230
        )

        draw_text(
            "Final Score: " + str(score),
            font, WHITE, 450, 310
        )

        draw_text(
            "R - RESTART",
            font, GOLD, 450, 375
        )

        draw_text(
            "ENTER - MAIN MENU",
            font, CYAN, 450, 425
        )
        # ==================================
    # VICTORY
    # ==================================

    elif state == "WIN":

        draw_background()

        draw_text(
            "VICTORY!",
            big, GOLD, 450, 200
        )

        draw_text(
            "YOU DEFEATED THE BOSS!",
            font, CYAN, 450, 280
        )

        draw_text(
            "Final Score: " + str(score),
            font, WHITE, 450, 340
        )

        draw_text(
            "Coins: " + str(coins),
            font, GOLD, 450, 390
        )

        draw_text(
            "R - PLAY AGAIN",
            font, WHITE, 450, 460
        )

        draw_text(
            "ENTER - MAIN MENU",
            font, CYAN, 450, 510
        )

    pygame.display.flip()

pygame.quit()
import random
from pygame import *
from pyautogui import leftClick

init()
mixer.init()

# ---------------- НАСТРОЙКИ ----------------
WIDTH = 1366
HEIGHT = 768
FPS = 120

# ---------------- ОКНО ----------------
screen = display.set_mode((WIDTH, HEIGHT))
display.set_caption("Jump Physics Demo")

# ---------------- ФОН ----------------
background = image.load("assets/background selo.png").convert()
background = transform.scale(background, (WIDTH, HEIGHT))

clock = time.Clock()
running = True

# ---------------- КЛАССЫ ----------------
class Hero:
    def __init__(self, x, y, image_path, speed):
        self.original_image = image.load(image_path).convert_alpha()
        self.original_image = transform.scale(self.original_image, (200, 200))
        self.image = self.original_image
        self.rect = self.image.get_rect(midbottom=(x, y))
        self.speed = speed
        self.hp = 100

    def draw(self, surface):
        surface.blit(self.image, self.rect)


class Player(Hero):
    def __init__(self, x, y):
        super().__init__(x, y, "assets/mellstroi.png", 8)
        self.damage = 50
        self.delay = 60
        self.cooldown = 0

        # ФИЗИКА
        self.vel_y = 0
        self.gravity = 1
        self.jump_power = -18
        self.on_ground = False

        self.facing_right = True

    def strike(self, enemy):
        udar = mouse.get_pressed()

        if self.cooldown > 0:
            self.cooldown -= 1

        if udar[0] and self.cooldown == 0:
            attack_img = image.load("assets/udar mellstroy.png").convert_alpha()
            attack_img = transform.scale(attack_img, (200, 200))

            if not self.facing_right:
                attack_img = transform.flip(attack_img, True, False)

            self.image = attack_img

            if self.rect.colliderect(enemy.rect):
                enemy.hp -= self.damage
                print("Enemy HP:", enemy.hp)

            self.cooldown = self.delay

        if self.cooldown == 1:
            self.image = self.original_image
            if not self.facing_right:
                self.image = transform.flip(self.original_image, True, False)

    def move(self):
        keys = key.get_pressed()

        if keys[K_a]:
            self.rect.x -= self.speed
            self.facing_right = False

        if keys[K_d]:
            self.rect.x += self.speed
            self.facing_right = True

        self.image = self.original_image
        if not self.facing_right:
            self.image = transform.flip(self.original_image, True, False)

        if keys[K_w] and self.on_ground:
            self.vel_y = self.jump_power
            self.on_ground = False

        self.vel_y += self.gravity
        self.rect.y += self.vel_y

        ground = HEIGHT
        if self.rect.bottom >= ground:
            self.rect.bottom = ground
            self.vel_y = 0
            self.on_ground = True

        self.rect.clamp_ip(screen.get_rect())


class Enemy(Hero):
    def __init__(self, x, y):
        super().__init__(x, y, "assets/enemy.png", 4)
        self.hp = 100

    def move(self):
        self.rect.x -= self.speed


# ---------------- ИГРОК ----------------
player = Player(WIDTH // 2, HEIGHT)

# ---------------- СПАВНЕР ----------------
enemies = []
spawn_delay = 240      # каждые 2 секунды при 120 FPS
spawn_timer = 0

# ---------------- ЦИКЛ ИГРЫ ----------------
while running:
    for e in event.get():
        if e.type == QUIT:
            running = False

    screen.blit(background, (0, 0))

    # ---------- СПАВН ----------
    spawn_timer += 1
    if spawn_timer >= spawn_delay:
        spawn_x = WIDTH + random.randint(50, 200)
        enemies.append(Enemy(spawn_x, HEIGHT))
        spawn_timer = 0

    # ---------- ВРАГИ ----------
    for enemy in enemies[:]:
        if enemy.hp <= 0:
            enemies.remove(enemy)
            continue

        enemy.move()
        enemy.draw(screen)
        player.strike(enemy)

    # ---------- ИГРОК ----------
    player.move()
    player.draw(screen)

    display.update()
    clock.tick(FPS)

quit()
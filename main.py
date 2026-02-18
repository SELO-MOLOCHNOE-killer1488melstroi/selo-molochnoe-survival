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

# ---------------- МУЗИКА ----------------

mixer.music.load("assets/bg.mp3")
mixer.music.set_volume(1)
mixer.music.play(-1)


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

        # Картинка удара (загружается один раз)
        self.attack_image = image.load("assets/udar mellstroy.png").convert_alpha()
        self.attack_image = transform.scale(self.attack_image, (200, 200))

        # Физика
        self.vel_y = 0
        self.gravity = 1
        self.jump_power = -18
        self.on_ground = False

        self.facing_right = True
        self.is_attacking = False

    def strike(self, enemy):
        mouse_buttons = mouse.get_pressed()

        if self.cooldown > 0:
            self.cooldown -= 1

        if mouse_buttons[0] and self.cooldown == 0:
            self.is_attacking = True

            if self.rect.colliderect(enemy.rect):
                enemy.hp -= self.damage
                print("Enemy HP:", enemy.hp)

            self.cooldown = self.delay

        if self.cooldown == 0:
            self.is_attacking = False

    def move(self):
        keys = key.get_pressed()

        if keys[K_a]:
            self.rect.x -= self.speed
            self.facing_right = False

        if keys[K_d]:
            self.rect.x += self.speed
            self.facing_right = True

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

        if self.is_attacking:
            current_image = self.attack_image
        else:
            current_image = self.original_image

        if not self.facing_right:
            current_image = transform.flip(current_image, True, False)

        self.image = current_image


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
from pygame import *

init()

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
        self.image = image.load(image_path).convert_alpha()
        self.image = transform.scale(self.image, (200, 200))
        self.rect = self.image.get_rect(midbottom=(x, y))
        self.speed = speed
        self.hp = 100

    def draw(self, surface):
        surface.blit(self.image, self.rect)


class Player(Hero):
    def __init__(self, x, y):
        super().__init__(x, y, "assets/mellstroi.png", 8)

        # ФИЗИКА
        self.vel_y = 0
        self.gravity = 1
        self.jump_power = -18
        self.on_ground = False

    def move(self):
        keys = key.get_pressed()

        # движение в стороны
        if keys[K_a]:
            self.rect.x -= self.speed
        if keys[K_d]:
            self.rect.x += self.speed

        # прыжок
        if keys[K_w] and self.on_ground:
            self.vel_y = self.jump_power
            self.on_ground = False

        # гравитация
        self.vel_y += self.gravity
        self.rect.y += self.vel_y

        # земля
        ground = HEIGHT
        if self.rect.bottom >= ground:
            self.rect.bottom = ground
            self.vel_y = 0
            self.on_ground = True

        # границы экрана
        self.rect.clamp_ip(screen.get_rect())


class Enemy(Hero):
    def __init__(self, x, y):
        super().__init__(x, y, "assets/enemy.png", 8)

        # ФИЗИКА
        self.vel_y = 0
        self.gravity = 1
        self.jump_power = -18
        self.on_ground = False

    def move(self):
        self.rect.x -= 1

    def strike(self):
        ...


# ---------------- ИГРОК ----------------
player = Player(WIDTH // 2, HEIGHT)

enemy = Enemy(WIDTH // 2, HEIGHT)

# ---------------- ЦИКЛ ИГРЫ ----------------
while running:
    for e in event.get():
        if e.type == QUIT:
            running = False

    screen.blit(background, (0, 0))

    enemy.move()
    enemy.draw(screen)

    player.move()
    player.draw(screen)

    display.update()
    clock.tick(FPS)

quit()
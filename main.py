from pygame import *

init()

screen = display.set_mode((100,100))

clock = time.Clock()

running = True

class Hero():
    def __init__(self,x,y,image_path, speed):
        self.image = image.load(image_path).convert_alpha()
        self.speed = speed
        self.hp = 100
        self.rect = self.image.get_rect(center=(x, y))

    def draw(self, surface):
        surface.blit(self.image, self.rect)


class Player(Hero):
    def __init__(self, x, y):
        super().__init__(x, y, "assets/mellstroi.png", 10)

    def move(self):
        keys = key.get_pressed()

        if keys[K_a]:
            self.rect.x -= self.speed

        if keys[K_d]:
            self.rect.x += self.speed

        if keys[K_w]:
            self.rect.y += self.speed

class Enemy(Hero):
    def __init__(self, x, y):
        super().__init__(x, y, "assets/pesok.jng", 10)

player = Player(100,100)

while running:
    for e in event.get():
        if e.type == QUIT:
            quit()

    player.move()
    player.draw(screen)

    display.update()
    clock.tick(60)

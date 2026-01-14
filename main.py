from pygame import *

init()

screen = display.set_mode((100,100))

clock = time.Clock()

running = True

while running:
    for e in event.get():
        if e.type == QUIT:
            quit()
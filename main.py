import random
import pgzrun
import os
import time
from pgzhelper import *

# окно
WIDTH = 640
HEIGHT = 480
TITLE = 'Flappy Bird'

# фон
bg = 0
bg_list = ['bg', 'bg-night']
last_bg_delay = 0
bg_delay = 0.2

# земля
ground = Actor('ground')
ground.x = 320
ground.y = 465

# птичка
bird = Actor('bird1')
bird.x = 75
bird.y = 100
bird.images = ['bird1', 'bird2', 'bird3', 'bird4']
bird.fps = 10

# надпись в конце игры
gameover = Actor('gameover')
gameover.x = 320
gameover.y = 150
gameover.scale = 0.6

# трубы
top_pipe = Actor('top')
bottom_pipe = Actor('bottom')
top_pipe.x = WIDTH
top_pipe.y = -00
gap = 150
bottom_pipe.x = WIDTH
bottom_pipe.y = top_pipe.height + gap

# физика
gravity = 0.3
bird.speed = 1
bird.alive = True
pipe_speed = -4
score = 0
maxscore = 0

# начальный экран
def start_screen():
    screen.blit(bg_list[bg], (0, 0))
    screen.blit('start', (226, 30))
    ground.draw()
start = True

# управление
def on_mouse_down():
    global score, start
    start = False
    if bird.alive:
        bird.speed = -6.5
        sounds.wing.play() # звук взмаха крыльев
    else:
        score = 0
        bird.alive = True
        bird.x = 75
        bird.y = 100

# отрисовка
def update():
    global score, maxscore, start, bg, last_bg_delay, bg_delay
    if start:
        return
    # смена фона на пробел
    if bird.alive == False:
        if keyboard.space:
            current_time = time.time()
            if current_time - last_bg_delay > bg_delay:
                bg = (bg + 1) % len(bg_list)
                screen.blit(bg_list[bg], (0,0))
                last_bg_delay = current_time

    # птичка
    bird.animate()
    bird.y += bird.speed
    bird.speed += gravity
    if bird.y > HEIGHT-40 or bird.y < -150:
        bird.alive = False
        sounds.die.play()
        bird.x = 75
        bird.y = 440
        if maxscore<score:
            maxscore=score

    # движение труб
    top_pipe.x += pipe_speed
    bottom_pipe.x += pipe_speed
    if top_pipe.x < -50:
        move = random.uniform(-100, -200)
        gap = 150
        top_pipe.midleft = (WIDTH, move)
        bottom_pipe.midleft = (WIDTH, move+top_pipe.height+gap)
        score += 1 # + очко
        sounds.point.play()

    # столкновение
    if bird.colliderect(top_pipe) or bird.colliderect(bottom_pipe):
        bird.alive = False
        sounds.hit.play()
        if maxscore < score:
            maxscore = score


# img
def draw():
    global start
    if start:
        start_screen()
        return
    screen.blit(bg_list[bg], (0, 0))
    if bird.alive:
        bird.draw()
        top_pipe.draw()
        bottom_pipe.draw()
        ground.draw()
    # когда умирает
    else:
        screen.draw.text("НАЖМИ ЧТОБЫ ИГРАТЬ ЕЩЕ РАЗ", color =(252,160,72), center=(320, 240), shadow=(0.5,0.5), scolor=(230,111,46), fontsize=27)
        gameover.draw()
        ground.draw()
        bird.image = 'birddead'
        bird.speed = 0
        top_pipe.x = WIDTH
        bottom_pipe.x = WIDTH
        bird.draw()
    screen.draw.text("Счет: " + str(score), color=(176,224,218), midtop=(55, 10), shadow=(0.5,0.5), scolor='black', fontsize=30)
    screen.draw.text("Рекорд: " + str(maxscore), color=(196,181,111), midtop=(65, 455), shadow=(0.5,0.5), scolor='black', fontsize=30)

os.environ['SDL_VIDEO_CENTERED'] = '1'
pgzrun.go()
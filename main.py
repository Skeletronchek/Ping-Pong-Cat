from pygame import *
from random import *
from time import time as timer
font.init()
font2 = font.SysFont('Arial', 40)
cd = False
starttime = 0
curtime = 0
img_hero = 'IsacTennis.png'
img_ball = 'Ball.png'
img_enemy = 'CatTennis.jpg'
img_back = 'basement.png'

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, speedx, speedy):
        sprite.Sprite.__init__(self)

        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speedx = speedx
        self.speedy = speedy

        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))
bullets = sprite.Group()

class Player(GameSprite):
    def update(self):
        global cd
        global starttime
        keys = key.get_pressed() 
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speedx
        if keys[K_RIGHT] and self.rect.x < win_width - 80:
            self.rect.x += self.speedx


class Ball(GameSprite):
    def update(self):
        global cd
        global starttime
        if self.rect.x <5 or self.rect.x > win_width - 80:
            self.speedx *= -1
        collision = sprite.spritecollide(
            self, Players, False
        )
        if collision and cd == False:
            self.speedy *= -1
            starttime = timer()
            cd = True
        self.rect.x += self.speedx
        self.rect.y += self.speedy

class Enemy(GameSprite):
    def update(self):
        global cd
        global starttime
        if Ball.rect.x < self.rect.x:
            self.rect.x -= self.speedx
        if Ball.rect.x > self.rect.x:
            self.rect.x += self.speedx





      



#Игровая сцена:
win_width = 700
win_height = 500
window = display.set_mode((win_width, win_height))
background = transform.scale(image.load(img_back), (win_width, win_height))

display.set_caption("Cat Tennis")

Players = sprite.Group()

isac = Player(img_hero, win_width /2, win_height - 80, 60, 60, 4,0)
cat = Enemy(img_enemy, win_width /2, 0, 60, 60, 4,0)
Ball = Ball(img_ball, win_width /2, win_height /2, 60, 60, 5.4,5.4)
Players.add(isac)
Players.add(cat)







run = True
finish = False
clock = time.Clock()
FPS = 60


#музыка
mixer.init()
mixer.music.load('TennisTheme.ogg')
mixer.music.play()


starttime = 0
curtime = 0
while run:
    for e in event.get():
        if e.type == QUIT:
            run = False
                
    window.blit(background,(0,0))
    if not finish:
        if cd == True:
            curtime = timer()
            delay = curtime - starttime
            print(delay)
            if delay > 0.7:
                cd = False
                delay = 0
                starttime = 0
                curtime = 0
        if Ball.rect.y > win_height - 100 or Ball.rect.y < -5:
            finish = True
        isac.update()
        cat.update()
        Ball.update()
        isac.reset()
        Ball.reset()
        cat.reset()
        display.update()   
           
    time.delay(30)


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
        global lost
        global finish
        keys = key.get_pressed() 
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speedx
        if keys[K_RIGHT] and self.rect.x < win_width - 80:
            self.rect.x += self.speedx
        if keys[K_1] and lost == 'nigla':            
            finish = False
            lost = False
        if keys[K_2] and lost == 'nigla':            
            finish = False
            lost = 'ninga'


class Ball(GameSprite):
    def update(self):
        global cd
        global starttime
        if self.rect.x <5 or self.rect.x > win_width - 80:
            if self.speedx < 1:
                self.speedx -= 0.3
                self.speedy -= 0.3
                isac.speedx += 0.2
                cat.speedx += 0.2
            else:
                self.speedx += 0.3
                self.speedy += 0.3
                isac.speedx += 0.2
                cat.speedx += 0.2
            self.speedx *= -1
        collision = sprite.spritecollide(
            self, Players, False
        )
        if collision and cd == False:
            if self.speedy < 1:
                self.speedy -= 0.3
                self.speedx -= 0.3
                isac.speedx += 0.2
                cat.speedx += 0.2
            else:
                self.speedy += 0.3
                self.speedx += 0.3
                isac.speedx += 0.2
                cat.speedx += 0.2
            self.speedy *= -1
            starttime = timer()
            cd = True
        self.rect.x += self.speedx
        self.rect.y += self.speedy

class Enemy(GameSprite):
    def update(self):
        global cd
        global starttime
        global lost
        if lost == 'ninga':
            keys = key.get_pressed() 
            if keys[K_a] and self.rect.x > 5:
                self.rect.x -= self.speedx
            if keys[K_d] and self.rect.x < win_width - 80:
                self.rect.x += self.speedx
        elif lost == False:
            if ball.rect.x < self.rect.x:
                self.rect.x -= self.speedx
            if ball.rect.x > self.rect.x:
                self.rect.x += self.speedx






      



#Игровая сцена:
win_width = 700
win_height = 500
window = display.set_mode((win_width, win_height))
background = transform.scale(image.load(img_back), (win_width, win_height))

display.set_caption("Cat Tennis")

Players = sprite.Group()
isac = Player(img_hero, win_width /2, win_height - 80, 60, 60, 6,0)
cat = Enemy(img_enemy, win_width /2, 0, 60, 60, 6,0)
Players.add(isac)
Players.add(cat)
ball = Ball(img_ball, win_width /2, win_height /2, 60, 60, 5.4,5.4)










run = True
finish = True
clock = time.Clock()
FPS = 60
lost = 'nigla'

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
    textlost = font2.render('CAT WIN!', 1, (0, 255, 0))
    textwin = font2.render('ISAC WIN!', 1, (0, 255, 0))
    textname = font2.render('Racist Cat Ping Pong', 1, (255, 255, 255))
    textlol = font2.render('Press 1 to PvE', 1, (255, 255, 255))
    textlol2 = font2.render('Press 2 to PvP', 1, (255, 255, 255))
    isac.update()
    isac.reset()
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
        if ball.rect.y > win_height - 70 or ball.rect.y < -5:
            finish = True
            if ball.rect.y < -5:
                lost = False
            elif ball.rect.y > win_height - 70:
                lost = True

        cat.update()
        ball.update()
        ball.reset()
        cat.reset()
    else:
        if lost == True:
            window.blit(textlost, (win_height/2, win_width/3))
        elif lost == False:
            window.blit(textwin, (win_height/2, win_width/3))
        else:
            window.blit(textname, (win_height/3, win_width/4.5))
            window.blit(textlol, (win_height/3, win_width/2))
            window.blit(textlol2, (win_height/3, win_width/3))

          
    display.update()      
    time.delay(30)


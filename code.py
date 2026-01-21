from pygame import *
from random import randint
from time import time as timer

mixer.init()
font.init()

sparta = transform.scale(image.load('csk.png'), (200, 200))

font1 = font.Font(None, 50)

wonbat = font1.render('Рабочий день окончен! Победа!', 1, (0, 0, 0))

loosebat = font1.render('Огоузок подобрался к плите и приготовил....', 1, (0, 0, 0))

relo = font1.render('ЛЁВА, НЕСИ СКОВОРОДКИ!', 1, (0, 0, 0))

lifc = 3

love = mixer.Sound('chef_love.mp3')

love.set_volume(0.4)

wonb = transform.scale(image.load('morgenchief.jpg'), (1880, 990))

class GameSprite(sprite.Sprite):
    def __init__(self, pl_image, pl_x, pl_y, pl_speed):
        super().__init__()
        self.image = transform.scale(image.load(pl_image), (90, 90))
        self.speed = pl_speed
        self.rect = self.image.get_rect()
        self.rect.x = pl_x
        self.rect.y = pl_y

    def reset(self):
        win.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()

        if keys[K_w] and self.rect.y > 5:
            self.rect.y -= self.speed

        if keys[K_s] and self.rect.y < 890:
            self.rect.y += self.speed

        if keys[K_a] and self.rect.x > 5:
            self.rect.x -= self.speed

        if keys[K_d] and self.rect.x < 1800:
            self.rect.x += self.speed

    def fire(self):
        bullet = Bullet('patron.jpg', self.rect.centerx, self.rect.top, 15)
        bull.add(bullet)

num_fire = 0
rel_time = False

lost = 0

class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > 1350:
            self.rect.y = 0
            self.rect.x = randint(5, 1800)
            lost += 1

downed = 0

bull = sprite.Group()

class Bullet(GameSprite):

    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < 5:
            self.kill()

class Egg(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y > 890:
            self.rect.y = 0
            self.rect.x = randint(5, 1750) 

eggs = sprite.Group()

for i in range(3):
    eggsd = Egg('bossnaga.png', randint(5, 1750), -20, randint(1, 3))
    eggs.add(eggsd)

 
oguzki = sprite.Group()

for i in range(5):
    og1 = Enemy('maksik.png', randint(5, 1750), -20, randint(1, 2))
    oguzki.add(og1)


vitya = Player('chief.png', 400, 200, 7)

screamer = transform.scale(image.load('bossnaga.png'), (1880, 990))

win = display.set_mode((1880, 990))
back = transform.scale(image.load('kitchen.png'), (1880, 990))
display.set_caption('shooter')

clock = time.Clock()

FPS = 144

game = True

font2 = font.Font(None, 100)

font3 = font.Font(None, 100)

finish = False

killed = 0

num_fire = 0

rel_time = 0

paw = mixer.Sound('oluhi.mp3')
mixer.music.load('sound.mp3')
mixer.music.play()

sos = mixer.Sound('nyam.mp3')

while game:
    for e in event.get():
        if e.type == QUIT:
            game = False

        if e.type == KEYDOWN:
            if e.key == K_SPACE:
                if num_fire < 5 and rel_time == False:
                    vitya.fire()
                    num_fire += 1
                    paw.play()

                if rel_time == False and num_fire >= 5:
                    rel_time = True
                    start = timer()                

    if finish != True:
        life = font1.render('Надежда посмотреть футбол:' + str(lifc), 1, (132, 125, 31))
        text_lose = font2.render('Пропущенно: ' + str(lost), 1, (255, 255, 17))
        text_downed = font3.render('подавлено огузков:' + str(killed), 1, (255, 255, 10) )
        win.blit(back, (0, 0))
        win.blit(text_lose, (200, 150))
        win.blit(text_downed, (200, 50))
        win.blit(sparta, (1700, 790))
        win.blit(life, (1300, 950))

        vitya.reset()
        vitya.update()
        oguzki.update()
        oguzki.draw(win)
        bull.update()
        bull.draw(win)
        coll = sprite.groupcollide(oguzki, bull, True, True)
        for _ in coll:
            killed += 1
            og = Enemy('maksik.png', randint(5, 1750), -20, randint(1, 2))
            oguzki.add(og)
        

        if sprite.spritecollide(vitya, eggs, True) or sprite.spritecollide(vitya, oguzki, True):
            lifc -= 1
    
        eggs.update()
        eggs.draw(win)

        if rel_time == True:
            end = timer()
            total = end - start

            if total >= 3:
                num_fire = 0 
                rel_time = False
            else:
                win.blit(relo, (450, 500))
        
        if killed >= 15:
            mixer.music.stop()
            love.play()
            win.blit(wonbat, (495, 580))
            win.blit(wonb, (0, 0))
            finish = True
 
        if lost >= 2:
            mixer.music.stop()
            win.blit(loosebat, (490, 500))
            los = mixer.Sound('chefder.ogg')
            los.play()
            finish = True

        if lifc <= 0:
            finish = True
            win.blit(screamer, (0, 0))
            sos.play()
            



    clock.tick(FPS)
    display.update()

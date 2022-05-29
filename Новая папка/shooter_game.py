from random import randint
from pygame import *
from time import time as timer

goal = 10
win_width = 700
win_height = 500
window = display.set_mode((win_width, win_height))
display.set_caption('冰淇淋')
bkgr = image.load('galaxy.jpg')
bkgr = transform.scale(bkgr,(win_width,win_height ))

mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
mixer.music.set_volume(0.3)
fire_sound = mixer.Sound('fire.ogg')

font.init()
font1 = font.SysFont('Arial', 36)
font2 = font.SysFont('Arial', 80)
win = font2.render('好!', True, (0, 255, 0))
lose = font2.render('Ti kakashka', True, (255, 0, 0))

max_lost = 4
score = 0
lost = 0

class GameSprite(sprite.Sprite):
    def __init__(self, img, width, height, x, y, speed):
        super().__init__()
        self.width = width
        self.height = height
        self.image = transform.scale(image.load(img),(self.width,self.height))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = speed
    def reset(self):
        window.blit(self.image,(self.rect.x, self.rect.y))

class Player(GameSprite):
    
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 0:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x+self.width < win_height:
            self.rect.x += self.speed
    def fire(self):
        bullet = Bullet('bullet.png', 15, 20, self.rect.centerx, self.rect.top, -15)
        bullets.add(bullet)


class UFO(GameSprite):
    
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > win_height:
            self.rect.y = 0
            self.rect.x = randint(0,win_height-self.width)
            lost += 1

class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()

class Asteroid(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y > win_height:
            self.rect.y = 0
            self.rect.x = randint(0, win_height - 80)

life = 3

asteroids = sprite.Group()
for i in range(1,3):
    asteroid = Asteroid('asteroid.png', 80, 50, randint(0,win_height-50), -40, randint(1,7))
    asteroids.add(asteroid)

rel_time = False
num_fire = 0

Enemies = sprite.Group()
for i in range(5):
    ufo = UFO(img='ufo.png', width=50, height = 50, x=randint(0,win_height-50), y=0, speed = 1)
    Enemies.add(ufo)

rocket = Player(img='rocket.png', width = 50, height = 50, x = win_width/2, y = 450,speed = 2)

bullets = sprite.Group()

finish = False
run = True

while run:
    for i in event.get():
        if i.type == QUIT:
            run = False
        elif i.type == KEYDOWN:
            if i.key == K_SPACE:
                if num_fire < 5 and rel_time == False:
                    num_fire += 1
                    fire_sound.play()
                    rocket.fire()
                if num_fire >= 5 and rel_time == False:
                    last_time = timer()
                    rel_time = True


    if not finish:
        

        window.blit(bkgr,(0,0))

        Enemies.draw(window)
        Enemies.update()

        rocket.reset()
        rocket.update()

        ufo.reset()
        ufo.update()

        bullets.update()
        bullets.draw(window)

        asteroids.update()
        asteroids.draw(window)
        if rel_time == True:
            now_time = timer()

            if now_time - last_time < 3:
                reloads = font2.render('等一下', 1, (150, 0, 0))
                window.blit(reloads, (260, 460))
            else:
                num_fire = 0
                rel_time = False

        collides = sprite.groupcollide(Enemies, bullets, True, True)
        for c in collides:
            score += 1
            ufo = UFO(img='ufo.png', width=50, height = 50, x=randint(0,win_height-50), y=0, speed = 1)
            Enemies.add(ufo)

        if sprite.spritecollide(rocket, Enemies, False) or sprite.spritecollide(rocket, asteroids, False):
            sprite.spritecollide (rocket, Enemies, True)
            sprite.spritecollide(rocket, asteroids, True)
            life -= 1

        if life == 0 or lost >= max_lost:
            finish = True
            window.blit(lose,(200,800))

        if score >= goal:
            finish = True
            window.blit(win,(200,200))

        text_score = font1.render('Счет:' + str(score), 1, (255,255,255))
        window.blit(text_score, (10,50))
        text_lose = font1.render('Пропущено:' + str(lost), 1, (255,255,255))
        window.blit(text_lose, (10,20))
        
        if life == 3:
            life_color = (0, 255, 0)
        if life == 2:
            life_color = (150, 150, 0)
        if life == 1:
            life_color = (255, 0, 0)
            

        text_life = font1.render(str(life), 1, life_color)
        window.blit(text_life, (650, 10))
            

        display.update()
    else:
        finish = False
        score = 0
        lost = 0
        num_fire = 0
        life = 3
        for b in bullets:
            b.kill()
        for e in Enemies:
            e.kill()
        for a in asteroids:
            a.kill()
        time.delay(3000)
        for i in range(5):
            ufo = UFO(img='ufo.png', width=50, height = 50, x=randint(0,win_height-50), y=0, speed = 1)
            Enemies.add(ufo)
        for i in range(1,3):
            asteroid = Asteroid('asteroid.png', 80, 50, randint(0,win_height-50), -40, randint(1,7))
            asteroids.add(asteroid)

    time.delay(50)
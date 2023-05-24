from pygame import *
from random import *
from time import time as timer
mixer.init()
font.init()
window = display.set_mode((700, 500))
display.set_caption('pygame window')
background = transform.scale(image.load('galaxy.jpg'), (700, 500))
class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_speed, size_x, size_y, type):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed
        self.size_x = size_x
        self.size_y =size_y
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
        self.type = type
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))
class Player(GameSprite):
    def update(self):
        keys_pressed = key.get_pressed()
        if keys_pressed[K_RIGHT] and self.rect.x < 630:
            self.rect.x+=self.speed
        if keys_pressed[K_LEFT] and self.rect.x > 0:
            self.rect.x-=self.speed
    def strike(self):
        global r_b
        keys_pressed = key.get_pressed()
        if keys_pressed[K_SPACE]:
            fire.play()
            bullets.add(Bullet('bullet.png', self.rect.centerx-15/2, self.rect.top, 8, 15, 20, 0))
            r_b-=1
class Enemy(GameSprite):
    def update(self):
        global num2
        self.rect.y+=self.speed
        if self.rect.y > 435:
            self.rect.y = 0
            self.rect.x = randint(0, 700 - self.size_x)
            self.speed = randint(1, 5)
            if self.type == 1:
                num2+=1
class Bullet(GameSprite):
    def update(self):
        self.rect.y-=self.speed    
bullets = sprite.Group()
mixer.music.load('space.ogg')
mixer.music.play()
fire = mixer.Sound('fire.ogg')
rocket = Player('rocket.png', 318, 435, 15, 65, 65, 0)
monster1 = Enemy('ufo.png', randint(0, 635), 0, randint(1, 5), 65, 65, 1)
monster2 = Enemy('ufo.png', randint(0, 635), 0, randint(1, 5), 65, 65, 1)
monster3 = Enemy('ufo.png', randint(0, 635), 0, randint(1, 5), 65, 65, 1)
monster4 = Enemy('ufo.png', randint(0, 635), 0, randint(1, 5), 65, 65, 1)
monster5 = Enemy('ufo.png', randint(0, 635), 0, randint(1, 5), 65, 65, 1)
monsters = sprite.Group()
monsters.add(monster1)
monsters.add(monster2)
monsters.add(monster3)
monsters.add(monster4)
monsters.add(monster5)
asteroid1 = Enemy('asteroid.png', randint(0, 635), 0, randint(5, 10), 55, 55, 0)
asteroid2 = Enemy('asteroid.png', randint(0, 635), 0, randint(5, 10), 55, 55, 0)
asteroid3 = Enemy('asteroid.png', randint(0, 635), 0, randint(5, 10), 55, 55, 0)
asteroids = sprite.Group()
asteroids.add(asteroid1)
asteroids.add(asteroid2)
asteroids.add(asteroid3)
font1 = font.SysFont('Arial', 35)
font2 = font.SysFont('Arial', 120)
win = font2.render('YOU WIN!', True, (255, 215, 0))
lose = font2.render('YOU LOSE!', True, (255, 0, 0))
num1 = 0
num2 = 0
FPS = 20
r_b = 5
sec1 = 0
sec2 = 0
bm = list()
clock = time.Clock()
game = True
run = True
while game:
    if run == True:
        clock.tick(FPS)
        window.blit(background, (0, 0))
        rocket.reset()
        rocket.update()
        monsters.draw(window)
        asteroids.draw(window)
        bullets.draw(window)
        monsters.update()
        asteroids.update()
        for bullet in bullets:
            if bullet.rect.y < 0:
                bullet.kill()
        bullets.update()
        bul = font1.render('Осталось патронов:' + str(r_b), True, (255, 255, 255))
        window.blit(bul, (340, 10))    
        if r_b > 0:
            rocket.strike()
            sec1 = timer()
        else:
            reloading = font1.render('Идёт перезарядка:' + str(int(4-sec2+sec1)), True, (255, 255, 255))
            window.blit(reloading, (435, 40))
            sec2 = timer()
            if sec2 > sec1 + 3:
                r_b = 5
        counter1 = font1.render('Счет:' + str(num1), True, (255, 255, 255))
        counter2 = font1.render('Пропущено:' + str(num2), True, (255, 255, 255))
        if len(sprite.spritecollide(rocket, monsters, False)) > 0 or len(sprite.spritecollide(rocket, asteroids, False)) or num2 > 2:
            window.blit(lose, (130, 250))
            run = False
        if num1 > 9:
            window.blit(win, (130, 250))
            run = False
        bm = sprite.groupcollide(monsters, bullets, False, True)
        if len(bm) > 0:
            for m in bm:
                m.rect.y = 1000
                num2-=1
                num1+=1
        window.blit(counter1, (10, 10))
        window.blit(counter2, (10, 40))
        display.update()
    for e in event.get():
        if e.type == QUIT:
            game = False

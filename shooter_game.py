#Создай собственный Шутер!
from random import *
from pygame import *
from time import time as timer
window = display.set_mode((700,500))
mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
back = transform.scale(image.load('galaxy.jpg'), (700,500))
clock = time.Clock()

class GameSprite(sprite.Sprite):
    def __init__(self,player_image,player_x,player_y,size_x,size_y,player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (size_x,size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image,(self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_a] and self.rect.x > 0:
            self.rect.x -= self.speed
        if keys[K_d] and self.rect.x < 700:
            self.rect.x += self.speed
        if keys[K_w] and self.rect.y > 0:
            self.rect.y -= self.speed
        if keys[K_s] and self.rect.y < 500:
            self.rect.y += self.speed
    def fire(self):
        bullet = Bullet('bullet.png',self.rect.centerx,self.rect.top,15,20,5)
        Bullets.add(bullet)
        
lost = 0
seti = 0
font.init()
font1 = font.SysFont('Arial',36)
font3 = font.SysFont('Arial',36)
class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y >= 500:
            self.rect.y = 0
            self.rect.x = randint(0,700)

            lost = lost + 1
class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y <= 0:
            self.kill()

Bullets = sprite.Group()



font2 = font.SysFont('Arial', 130)
monsters = sprite.Group()
for i in range(1,6):
    monster = Enemy('ufo.png', randint(0,700), -40, 80, 50, randint(2,5))
    monsters.add(monster)

asteroids = sprite.Group()
for i in range(1,3):
    asteroid = Enemy('asteroid.png', randint(0,700), -40, 80, 50, randint(2,5))
    asteroids.add(asteroid)
firee = 0
rel_time = False
life2 = 3
score = 0
GH = Player('rocket.png',500,400, 80, 100, 5)
game = True
finish = False
font = font.SysFont('Arial',130)
while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                
                if firee < 5 and rel_time == False:
                    firee = firee + 1
                    GH.fire()
                if firee >= 5 and rel_time == False:
                    last_time = timer()
                    rel_time = True 
    if not finish:
        window.blit(back, (0,0))
        text_lose = font1.render('Пропущено:' + str(lost), 1, (255,255,255))
        text_seti = font3.render('Счет:' + str(score), 1, (255 ,240,255))
        window.blit(text_lose,(0,0))
        window.blit(text_seti,(20,40))
        GH.reset()
        GH.update()
        monsters.draw(window)
        monsters.update()
        Bullets.update()
        Bullets.draw(window)
        asteroids.update()
        asteroids.draw(window)
        if rel_time == True:
            now_time = timer()
            if now_time - last_time < 1:
                reload = font2.render('Wait,reload...', 1, (150,0,0))
                window.blit(reload, (200,400))
            else:
                firee = 0
                rel_time = False
        if lost >= 3 or sprite.spritecollide(GH,monsters,False):
            finish = True
            you_lose = font2.render('YOU LOSE!',True,(235,0,0))
            window.blit(you_lose, (100,200))
        collides = sprite.groupcollide(monsters, Bullets, True, True)
        for c in collides:
            score += 1
            monster = Enemy('ufo.png', randint(0,700), -40, 80, 50, randint(2,5))
            monsters.add(monster)
        if score >= 10:
            finish = True
            you_win = font.render('YOU WIN!', True, (0,250,0))
            window.blit(you_win, (130,200))
        if sprite.spritecollide(GH,asteroids,False):
            finish =True
            you_lose = font2.render('YOU LOSE!', True, (235,0,0))
            window.blit(you_lose, (100,200))
        collides = sprite.groupcollide(asteroids, Bullets, False, True)

    display.update()
    clock.tick(60)



da
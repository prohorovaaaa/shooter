#Создай собственный Шутер!
from random import randint 
from pygame import *
from time import time as timer

font.init()
font1 = font.Font(None, 80)
win = font1.render('YOU WIN!', True, (255, 255, 255))
lose = font1.render('YOU LOSE!', True, (180, 0, 0))

    
win_width = 700
win_height = 500
window = display.set_mode((win_width, win_height))
display.set_caption("Maze")
background = transform.scale(image.load("galaxy.jpg"), (win_width, win_height))

img_back = "galaxy.jpg"
img_hero = "rocket.png"
img_enemy = 'ufo.png'
img_bullet = 'bullet.png'
img_asteroid = "asteroid.png"
score = 0
lost = 0
goal = 10
max_lost = 3


    
class GameSprite(sprite.Sprite):
  
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))
 
class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_width - 80:
            self.rect.x += self.speed
        if keys[K_UP] and self.rect.y > 5:
            self.rect.y -= self.speed
        if keys[K_DOWN] and self.rect.y < win_height - 80:
            self.rect.y += self.speed



    def fire(self):
        bullet = Bullet(img_bullet, self.rect.centerx, self.rect.top, 15, 20, -15)
        bullets.add(bullet)
class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > win_height:
            self.rect.x = randint(80, win_width - 80)
            self.rect.y = 0
            lost = lost + 1

ship = Enemy(img_enemy, 5, win_height -  100, 80, 100, 10)
monsters = sprite.Group()
for i in range(1, 6):
    monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
    monsters.add(monster)


asteroids = sprite.Group()
for i in range(1, 3):
    asteroid = Enemy(img_asteroid, randint(30, win_width - 30), -40, 80, 50, randint(1, 7))
    asteroids.add(asteroid)
game = True 
finish = False
clock = time.Clock()
FPS = 60



    


bullets = sprite.Group()

finish = False

rel_time = False
num_fire = 0

class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y < 0:
            self.kill()


ship = Player("rocket.png", 5, win_height - 100, 80, 100, 10)
mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
fire_sound = mixer.Sound('fire.ogg')

font.init()
font2 = font.Font(None, 36)

while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                    if num_fire < 5 and rel_time == False:
                        num_Fire = num_fire + 1
                        fire_sound.play()
                        ship.fire()
            fire_sound.play()
            ship.fire() 
            
            if num_Fire >= 5 and rel_time == False :

                last_time = timer()
                rel_time = True
                
    if rel_time == True:
        now_time = timer()

        if now_time - last_time < 3:

            reload = font2.render('Wait, reload...', 1, (150, 0, 0))
            window.blit(reload, (260, 460))
        else:
            num_fire = 0
            rel_time = False



            if life == 3:
                life_color = (0, 150, 0)
            if life == 2:
                life_color = (150, 150, 0)
            if life == 1:
                life_color = (150, 150, 150)


            if life == 0 or lost >= max_lost:
                finish = True
                window.blit(lose, (200, 200))

            if score >= goal:
                finish = True
                window.blit(win, (200, 200))




    if not finish:

        window.blit(background, (0,0))
        
        text = font2.render("Счёт: " + str(score), 1, (255, 255, 255))
        window.blit(text, (10, 20))

        text_lose = font2.render("Пропущено: " + str(lost), 1, (255, 255, 255))
        window.blit(text_lose, (10, 50))
        ship.update()
        ship.reset()

        monsters.draw(window)
        monsters.update()
        bullets.update()
        bullets.draw(window)
        asteroids.draw(window)
        asteroids.update(window)

        collides = sprite.groupcollide(monsters, bullets, True, True)
        for c in collides:

            score = score + 1
            monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
            monsters.add(monster)
        if sprite.spritecollide(ship, monsters, False) or sprite.spritecollide(ship, asteroids, False):
            sprite.spritecollide(ship, monsters, True)
            sprite.spritecollide(ship, asteroids, True)
            life = life -1


            finish = True
            window.blit(lose, (200, 200))
        if score >= goal:
            finish = True
            window.blit(win, (200, 200))


    display.update()
    clock.tick(FPS)

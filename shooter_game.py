#Создай собственный Шутер!
from pygame import *
from random import randint
from time import time as timer
win_width = 700
win_height = 500
window = display.set_mode((win_width, win_height))
display.set_caption("The Shooter")
bulets = sprite.Group()
lost = 0
score = 0
num_fire = 0
rel_time = timer()
rel_time = False
last_time = timer()
font.init()
fonte = font.SysFont("Arial", 75)
background = transform.scale(image.load("galaxy.jpg"), (win_width, win_height))
class GameSprite(sprite.Sprite):
    def _＿init＿_(self, player_image, player_x, player_y, player_speed):
        super()._＿init＿_()
        self.image = transform.scale(image.load(player_image), (65, 65))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))
class Player(GameSprite):
    def update(self):
        keys_pressed = key.get_pressed()
        if keys_pressed[K_a] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys_pressed[K_d] and self.rect.x < 630:
            self.rect.x += self.speed
    def fire(self):
        keys_pressed = key.get_pressed()
        if keys_pressed[K_SPACE]:
            bulet = Bulet("bullet.png", self.rect.centerx, self.rect.top, -9)
            bulets.add(bulet)
class Enemy(GameSprite):
    def update(self):
            self.rect.y += self.speed
            global lost
            if self.rect.y > win_height:
                self.rect.x = randint(80, win_width - 80)
                self.rect.y = 0
                lost += 1
class Bulet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y <0:
            self.kill()
class Asterio(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y > win_height:
            self.rect.x = randint(80, win_width - 80)
            self.rect.y = 0


            
game = True
finish = False
speed_monsters = randint(1, 5)
clock = time.Clock()
FPS = 60
player = Player('rocket.png', 350, 425, 4)
asterios = sprite.Group()
monsters = sprite.Group()
bulets = sprite.Group()
for i in range(5):
    monster = Enemy("ufo.png", randint(80, win_width - 80), 0, 1.5)
    monsters.add(monster)
for i in range(2):
    asterio = Asterio("asteroid.png", randint(80, win_width - 80), 0, 1.8)
    asterios.add(asterio)
mixer.init()
mixer.music.load("space.ogg")
mixer.music.play()
while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                if num_fire < 5 and rel_time == False:
                    player.fire()
                    num_fire += 1
                    kick = mixer.Sound("fire.ogg")
                    kick.play()
                if num_fire >= 5 and rel_time == False:
                    last_time = timer()
                    rel_time = True
    if not finish:
        font.init()
        font1 = font.SysFont("Arial", 36)
        text1 = font1.render("Счёт: " + str(score), 1, (255, 255, 255))
        window.blit(text1, (10, 20))
        text2 = font1.render("Пропущено: " + str(lost), 1, (255, 255, 255))
        window.blit(text2, (10, 50))
        player.update()
        player.reset()
        monsters.update()
        monsters.draw(window)
        asterios.update()
        asterios.draw(window)
        bulets.update()
        bulets.draw(window)
        display.update()
        window.blit(background, (0, 0))

        
        if rel_time == True:
            now_time = timer()
            if now_time - last_time < 2:
                font.init()
                font2 = font.SysFont("Arial", 36)
                reloa = font2.render("Wait, reload...", 1, (155, 0, 0))
                window.blit(reloa, (260, 450))
            else:
                num_fire = 0
                rel_time = False

        if lost > 5 or sprite.spritecollide(player, monsters, False):
            finish = True
            win = fonte.render("GAME OVER", True, (255, 255, 255))
            window.blit(win, (175, 220))
        if sprite.spritecollide(player, asterios, False):
            finish = True
            win = fonte.render("GAME OVER", True, (255, 255, 255))
            window.blit(win, (175, 220))
        if sprite.groupcollide(monsters, bulets, True, True):
            monster = Enemy("ufo.png", randint(80, win_width - 80), 0, 1.8)
            monsters.add(monster)
            score += 1
        if score == 7:
            finish = True
            win1 = fonte.render("YOU WIN!", True, (255, 255, 0))
            window.blit(win1, (220, 220))
    clock.tick(FPS)
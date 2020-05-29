import pygame
import random
import math
from pygame.locals import (
    RLEACCEL,
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
    K_SPACE,
    K_p,
)


SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60
LASERPOWER=1
DIFFICULTY=1
MOB_MAX_NUM=5
MOB_MIN_SPEED=1
MOB_MAX_SPEED=3
ENEMY_SPEED=1
ENEMY_MAX_NUM=3
bgX1 = 0
bgX2 = -SCREEN_HEIGHT
BACKGROUND_SCROLL_SPEED=0.5
PLAY_HP=20
POWUP_TIME=5000
TREAT_HP=2

background = pygame.image.load('./images/blue.png')
background_rect = background.get_rect()
player_img = pygame.transform.scale(pygame.image.load('./images/playerShip1_orange.png'),(61,41))
laser_bullet_img = pygame.image.load('./images/laserRed16.png')
super_laser_bullet_img = pygame.image.load('./images/laser.png')
meteor_img = pygame.image.load('./images/meteor.png')
enemy_img = pygame.image.load('./images/EnemyShip_Small.png')
powup_img = pygame.image.load('./images/bolt_gold.png')
treat_img = pygame.image.load('./images/shield_gold.png')
enemy_bullet_img=pygame.image.load('./images/missile.png')

meteor_img_list = []
meteor_img_list.append(pygame.image.load('./images/meteorBrown_big1.png'))
meteor_img_list.append(pygame.image.load('./images/meteorBrown_big2.png'))
meteor_img_list.append(pygame.image.load('./images/meteorBrown_med1.png'))
meteor_img_list.append(pygame.image.load('./images/meteorBrown_med3.png'))
meteor_img_list.append(pygame.image.load('./images/meteorBrown_small1.png'))
meteor_img_list.append(pygame.image.load('./images/meteorBrown_small2.png'))
meteor_img_list.append(pygame.image.load('./images/meteorBrown_tiny1.png'))

enemy_explosion_anim = {}
enemy_explosion_anim['lg'] = []
enemy_explosion_anim['sm'] = []
for i in range(9):
    filename = './images/sonicExplosion0{}.png'.format(i)
    img = pygame.image.load(filename)
    enemy_explosion_anim['lg'].append(img)
    img_sm = pygame.transform.scale(img, (75, 75))
    enemy_explosion_anim['sm'].append(img_sm)

play_explosion_anim = {}
play_explosion_anim['lg'] = []
play_explosion_anim['sm'] = []
for i in range(9):
    filename = './images/regularExplosion0{}.png'.format(i)
    img = pygame.image.load(filename)
    play_explosion_anim['lg'].append(img)
    img_sm = pygame.transform.scale(img, (75, 75))
    play_explosion_anim['sm'].append(img_sm)


WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

class PlayerBullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = laser_bullet_img
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = -10
        self.damage=1

    def update(self):
        self. rect.y += self.speedy
        if self.rect.bottom < 0:
            self.kill()

class SuperPlayerBullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = super_laser_bullet_img
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = -10
        self.damage=2

    def update(self):
        self. rect.y += self.speedy
        if self.rect.bottom < 0:
            self.kill()

class EnemyBullet(pygame.sprite.Sprite):
    def __init__(self, x, y, enemy):
        pygame.sprite.Sprite.__init__(self)
        self.image = enemy_bullet_img
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = 3
        self.enemy=enemy
        self.damage=2

    def update(self):
        self. rect.y += self.speedy
        if self.rect.top > SCREEN_HEIGHT + 10:
            self.destory()

    def destory(self):
        self.enemy.bulletNum-=1
        self.kill()

class PowUp(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = powup_img
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(SCREEN_WIDTH - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self.speedx = ENEMY_SPEED
        self.speedy = ENEMY_SPEED
        self.enterMainScreen=False

    def update(self):
        self.rect.move_ip(self.speedx,0)
        self.rect.move_ip(0, self.speedy)
        if self.rect.y>0 and self.rect.x>0 and self.rect.x<SCREEN_WIDTH-self.rect.width and self.enterMainScreen is False:
            self.enterMainScreen=True
        if self.enterMainScreen is True and (self.rect.x<=0 or self.rect.x>=SCREEN_WIDTH-self.rect.width):
            self.speedx=-self.speedx

class Treat(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = treat_img
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(SCREEN_WIDTH - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self.speedx = ENEMY_SPEED
        self.speedy = ENEMY_SPEED
        self.enterMainScreen=False

    def update(self):
        self.rect.move_ip(self.speedx,0)
        self.rect.move_ip(0, self.speedy)
        if self.rect.y>0 and self.rect.x>0 and self.rect.x<SCREEN_WIDTH-self.rect.width and self.enterMainScreen is False:
            self.enterMainScreen=True
        if self.enterMainScreen is True and (self.rect.x<=0 or self.rect.x>=SCREEN_WIDTH-self.rect.width):
            self.speedx=-self.speedx


class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = player_img
        self.rect = self.image.get_rect()
        self.rect.centerx = int(SCREEN_WIDTH/2)
        self.rect.bottom = SCREEN_HEIGHT
        self.speedx = 0
        self.hp=PLAY_HP
        self.powup=False
        self.last_powup_update = pygame.time.get_ticks()

    def update(self, pressed_keys):
        if pressed_keys[K_UP]:
            self.rect.move_ip(0, -5)
        if pressed_keys[K_DOWN]:
            self.rect.move_ip(0, 5)
        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-5, 0)
        if pressed_keys[K_RIGHT]:
            self.rect.move_ip(5, 0)
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT
        if pressed_keys[K_SPACE]:
            self.shoot()
        if self.powup is True:
            now = pygame.time.get_ticks()
            if now - self.last_powup_update > POWUP_TIME:
                self.last_powup_update = now
                self.powup=False
        

    def shoot(self):
        if self.powup is False:
            if len(player_bullets)>=LASERPOWER:
                return
            laserBullet = PlayerBullet(self.rect.centerx, self.rect.top)
            all_sprites.add(laserBullet)
            player_bullets.add(laserBullet)
        else:
            superLaserBullet = SuperPlayerBullet(self.rect.centerx, self.rect.top)
            all_sprites.add(superLaserBullet)
            player_bullets.add(superLaserBullet)
        
    def beHit(self, damage):
        global End
        self.hp-=damage
        if self.hp<=0:
            End=True
            expl = PlayExplosion(self.rect.center,'lg')
            all_sprites.add(expl)
            self.kill()

    def powUp(self):
        self.powup=True
        self.last_powup_update=pygame.time.get_ticks()

    def beTreat(self, addHp):
        if addHp>PLAY_HP-self.hp:
            addHp=PLAY_HP-self.hp
        self.hp+=addHp


class Mob(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.selectIndex=random.randrange(0,len(meteor_img_list))
        self.image_orig = meteor_img_list[self.selectIndex]
        self.image = self.image_orig.copy()
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(SCREEN_WIDTH - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self.speedx = math.ceil((self.selectIndex+1)*MOB_MAX_SPEED/(len(meteor_img_list))*random.choice([-1,1]))
        self.speedy = math.ceil((self.selectIndex+1)*MOB_MAX_SPEED/(len(meteor_img_list)))
        self.hp=math.ceil((1-self.selectIndex/len(meteor_img_list))*10)
        self.damage=self.hp
        self.rot = 0
        self.rot_speed = random.randrange(-8, 8)
        self.last_update = pygame.time.get_ticks()

    def update(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        self.rotate()
        if self.rect.top > SCREEN_HEIGHT + 10 or self.rect.left < -25 or self.rect.right > SCREEN_WIDTH + 20:
            self.kill()

    def rotate(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > 50:
            self.last_update = now
            self.rot = (self.rot + self.rot_speed) % 360
            new_image = pygame.transform.rotate(self.image_orig, self.rot)
            old_center = self.rect.center
            self.image = new_image
            self.rect = self.image.get_rect()
            self.rect.center = old_center

    def beHit(self, damage):
        self.hp-=damage
        if self.hp<=0:
            if self.selectIndex<len(meteor_img_list)*2/3:
                expl = EnemyExplosion(self.rect.center,'lg')
                all_sprites.add(expl)
            else:
                expl = EnemyExplosion(self.rect.center,'sm')
                all_sprites.add(expl)
            self.kill()

        

class PlayExplosion(pygame.sprite.Sprite,):
    def __init__(self, center, size):
        pygame.sprite.Sprite.__init__(self)
        self.size = size
        self.image = play_explosion_anim[self.size][0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 40

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len(play_explosion_anim[self.size]):
                self.kill()
            else:
                center = self.rect.center
                self.image = play_explosion_anim[self.size][self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center

class EnemyExplosion(pygame.sprite.Sprite,):
    def __init__(self, center, size):
        pygame.sprite.Sprite.__init__(self)
        self.size = size
        self.image = enemy_explosion_anim[self.size][0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 40

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len(enemy_explosion_anim[self.size]):
                self.kill()
            else:
                center = self.rect.center
                self.image = enemy_explosion_anim[self.size][self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = enemy_img
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(SCREEN_WIDTH - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self.speedx = ENEMY_SPEED
        self.speedy = ENEMY_SPEED
        self.bulletNum=0
        self.hp=1
        self.enterMainScreen=False

    def update(self):
        self.rect.move_ip(self.speedx,0)
        self.rect.move_ip(0, self.speedy)
        if self.rect.y>0 and self.rect.x>0 and self.rect.x<SCREEN_WIDTH-self.rect.width and self.enterMainScreen is False:
            self.enterMainScreen=True
        if self.enterMainScreen is True and (self.rect.y<=0 or self.rect.y>=SCREEN_HEIGHT-self.rect.height):
            self.speedy=-self.speedy
        if self.enterMainScreen is True and (self.rect.x<=0 or self.rect.x>=SCREEN_WIDTH-self.rect.width):
            self.speedx=-self.speedx

        self.shoot()
    
    def shoot(self):
        if self.bulletNum>=1:
            return
        enemyBullet = EnemyBullet(self.rect.centerx, self.rect.bottom+5, self)
        all_sprites.add(enemyBullet)
        enemy_bullets.add(enemyBullet)
        self.bulletNum+=1

    def beHit(self, damage):
        self.hp-=damage
        if self.hp<=0:
            expl = EnemyExplosion(self.rect.center,'sm')
            all_sprites.add(expl)
            self.kill()

font_name = pygame.font.match_font('arial')
def draw_text(surf, text, size, x, y, color):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)

def draw_hp_bar(surf, x, y, hp):
    if hp < 0:
        hp = 0
    BAR_LENGTH = 100
    BAR_HEIGHT = 10
    fill = (hp / PLAY_HP) * BAR_LENGTH
    outline_rect = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pygame.Rect(x, y, fill, BAR_HEIGHT)
    draw_text(surf, "Life", 20, x-20, y-10, GREEN)
    pygame.draw.rect(surf, GREEN, fill_rect)
    pygame.draw.rect(surf, WHITE, outline_rect, 2)

pygame.init()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

player = Player()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)
player_bullets = pygame.sprite.Group()
enemy_bullets = pygame.sprite.Group()
mobs = pygame.sprite.Group()
powups=pygame.sprite.Group()
treats=pygame.sprite.Group()
for i in range(MOB_MAX_NUM):
    m = Mob()
    mobs.add(m)
enemies = pygame.sprite.Group()
for i in range(ENEMY_MAX_NUM):
    e=Enemy()
    enemies.add(e)



all_sprites.add(mobs)
all_sprites.add(enemies)

ADDENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(ADDENEMY, 250)
ADDMOB = pygame.USEREVENT + 2
pygame.time.set_timer(ADDMOB, 250)
ADDPOWER = pygame.USEREVENT + 3
pygame.time.set_timer(ADDPOWER, 5000)
ADDTREAT = pygame.USEREVENT + 4
pygame.time.set_timer(ADDTREAT, 10000)

running = True
pause = False
End=False
score=0
clock = pygame.time.Clock()

pygame.joystick.init()
joystick_count = pygame.joystick.get_count()
print("joystick_count : "+str(joystick_count))

while running:

    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False
            elif event.key==K_p:
                pause = True
        elif event.type == QUIT:
            running = False
        elif event.type == ADDENEMY:
            if len(enemies) < ENEMY_MAX_NUM:
                new_enemy = Enemy()
                enemies.add(new_enemy)
                all_sprites.add(new_enemy)
        elif event.type == ADDMOB:
            if len(mobs) < MOB_MAX_NUM:
                new_mob = Mob()
                mobs.add(new_mob)
                all_sprites.add(new_mob)
        elif event.type==ADDPOWER:
            if len(powups)<1:
                powup=PowUp()
                powups.add(powup)
                all_sprites.add(powups)
        elif event.type==ADDTREAT:
            if len(treats)<1:
                treat=Treat()
                treats.add(treat)
                all_sprites.add(treats)

    while pause :
        for event in pygame.event.get():
            if event.type==KEYDOWN:
                if event.key==K_p:
                    pause = False
    
    pressed_keys = pygame.key.get_pressed()
    player.update(pressed_keys)

    hits_mob_bullets = pygame.sprite.groupcollide(mobs, player_bullets, False, False)
    for mob,bullets in hits_mob_bullets.items():
        for bullet in bullets:
            mob.beHit(bullet.damage)
            bullet.kill()
        score+=5
    hits_mob_player = pygame.sprite.spritecollide(player, mobs, False)
    if hits_mob_player:
        player.beHit(hits_mob_player[0].damage)
        hits_mob_player[0].kill()
        m = Mob()
        all_sprites.add(m)
        mobs.add(m)
        

    hits_enemy_player = pygame.sprite.spritecollide(player, enemy_bullets, False)
    if hits_enemy_player:
        hits_enemy_player[0].destory()
        player.beHit(hits_enemy_player[0].damage)
    hits_enemy_player = pygame.sprite.spritecollide(player, enemies, False)
    if hits_enemy_player:
        player.beHit(hits_enemy_player[0].hp*5)
        hits_enemy_player[0].kill()
        
    hits_enemy_bullets = pygame.sprite.groupcollide(enemies, player_bullets, True, True)
    for enemy,bullets in hits_enemy_bullets.items():
        for bullet in bullets:
            enemy.beHit(bullet.damage)
            score+=10

    hits_play_powups=pygame.sprite.spritecollide(player,powups,False)
    if hits_play_powups:
        player.powUp()
        hits_play_powups[0].kill()

    hits_play_treats=pygame.sprite.spritecollide(player,treats,False)
    if hits_play_treats:
        player.beTreat(TREAT_HP)
        hits_play_treats[0].kill()
        

    for sprite in all_sprites:
        if isinstance(sprite,Player) is False:
            sprite.update()


    
    screen.blit(background, (0, bgX1))  
    screen.blit(background, (0, bgX2)) 
    
    bgX1 += BACKGROUND_SCROLL_SPEED
    bgX2 += BACKGROUND_SCROLL_SPEED
    if bgX1 > SCREEN_HEIGHT:
        bgX1 = -SCREEN_HEIGHT
    if bgX2 > SCREEN_HEIGHT:
        bgX2 = -SCREEN_HEIGHT

    all_sprites.draw(screen)
    draw_text(screen, "Your Score : "+str(score), 28, SCREEN_WIDTH/2, 30, WHITE)
    draw_hp_bar(screen, 50, SCREEN_HEIGHT - 40, player.hp)
    if End:
        draw_text(screen, "Game Over", 28, SCREEN_WIDTH/2, SCREEN_HEIGHT/2, RED)
    pygame.display.flip()
    clock.tick(FPS)


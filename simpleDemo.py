import pygame
import random
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
    JOYAXISMOTION,
    JOYBALLMOTION,
    JOYBUTTONDOWN,
    JOYBUTTONUP,
    JOYHATMOTION,
)

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60
bgY1 = 0 
bgY2 = -SCREEN_HEIGHT
BACKGROUND_SCROLL_SPEED=0.5



background = pygame.image.load('./images/blue.png')
background_rect = background.get_rect()
player_img = pygame.transform.scale(pygame.image.load('./images/playerShip1_orange.png'),(61,41)) 
enemy_img = pygame.image.load('./images/EnemyShip_Small.png') 

class Player(pygame.sprite.Sprite): 
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = player_img
        self.rect = self.image.get_rect()
        self.rect.centerx = int(SCREEN_WIDTH/2)
        self.rect.bottom = SCREEN_HEIGHT

    def up(self):
        self.rect.move_ip(0, -5)
    def down(self):
        self.rect.move_ip(0, 5)
    def left(self):
        self.rect.move_ip(-5, 0)
    def right(self):
        self.rect.move_ip(5, 0)

    def update(self, pressed_keys): 
        if pressed_keys[K_UP]:
            self.up()
        if pressed_keys[K_DOWN]:
            self.down()
        if pressed_keys[K_LEFT]:
            self.left()
        if pressed_keys[K_RIGHT]:
            self.right()
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT

class Enemy(pygame.sprite.Sprite): 
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = enemy_img
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(SCREEN_WIDTH - self.rect.width) 
        self.rect.y = random.randrange(-100, -40)
        self.speedx = 1
        self.speedy = 1 
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

font_name = pygame.font.match_font('arial')
def draw_text(surf, text, size, x, y, color): 
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)

pygame.init()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
player = Player() 
enemies = pygame.sprite.Group() 
for i in range(3):
    e=Enemy()
    enemies.add(e)
all_sprites = pygame.sprite.Group() 
all_sprites.add(player)
all_sprites.add(enemies) 

clock = pygame.time.Clock()

pygame.joystick.init()
joystick_count = pygame.joystick.get_count()
print("joystick_count : "+str(joystick_count))
if joystick_count>0:
    joystick=pygame.joystick.Joystick(0)
    joystick.init()

    name=joystick.get_name()
    print("name : "+name)

running = True
End=False

while running:
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False
        elif event.type == QUIT:
            running = False


    #axes[0]: x-axis, axes[1]: y-axis 
    if joystick_count>0:
        axes=joystick.get_numaxes()
        xAxis=joystick.get_axis(0)
        yAxis=joystick.get_axis(1)
        if xAxis>0.5:
            player.right()
        if xAxis<-0.5:
            player.left()
        if yAxis<-0.5:
            player.up()
        if yAxis>0.5:
            player.down()

    pressed_keys = pygame.key.get_pressed() 
    player.update(pressed_keys) 

    for enemy in enemies:
        enemy.update()

    hits_enemy_player = pygame.sprite.spritecollide(player, enemies, False)
    if hits_enemy_player:
        player.kill()
        End=True 

    screen.blit(background, (0, bgY1))  
    screen.blit(background, (0, bgY2)) 
    
    bgY1 += BACKGROUND_SCROLL_SPEED
    bgY2 += BACKGROUND_SCROLL_SPEED
    if bgY1 > SCREEN_HEIGHT:
        bgY1 = -SCREEN_HEIGHT
    if bgY2 > SCREEN_HEIGHT:
        bgY2 = -SCREEN_HEIGHT
    
    all_sprites.draw(screen) 
    if End: 
        draw_text(screen, "Game Over", 28, SCREEN_WIDTH/2, SCREEN_HEIGHT/2, (255, 0, 0))
    pygame.display.flip()
    clock.tick(FPS)
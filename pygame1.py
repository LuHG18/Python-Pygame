import pygame
from pygame.locals import *
import random
import threading

pygame.mixer.pre_init(44200, 16, 2, 4096)
pygame.init()



    
poweruptest = False
#powerupShield = 0    
lightningPowerup = 1

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.image = pygame.image.load('supermanhero3.PNG').convert_alpha()
        self.image.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.image.get_rect()
        self.speed = lightningPowerup

    def update(self, pressed_keys):
        if pressed_keys[K_w]:
            self.rect.move_ip(0, -self.speed)
        if pressed_keys[K_s]:
            self.rect.move_ip(0, self.speed)
        if pressed_keys[K_a]:
            self.rect.move_ip(-self.speed, 0)
        if pressed_keys[K_d]:
            self.rect.move_ip(self.speed, 0)
            

        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > 1300:
            self.rect.right = 1300
        if self.rect.top <= 0:
            self.rect.top = 0
        elif self.rect.bottom >= 600:
            self.rect.bottom = 600

class Opponent(pygame.sprite.Sprite):
    def __init__(self, level):
        super(Opponent, self).__init__()
        self.image = pygame.image.load('kryptoniteenemy.png').convert_alpha()
        self.image.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.image.get_rect(
            center=(1350, random.randint(0,600))
        )
        self.speed = random.randint(0, level)

    def update(self):
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right < 0:
            self.kill()

class Powerup(pygame.sprite.Sprite):
    def __init__(self):
        super(Powerup, self).__init__()
        self.image = pygame.image.load('powerup-lightning2.png').convert_alpha()
        self.image.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.image.get_rect(
            center=(1350, random.randint(0,600))
        )
        self.speed = random.randint(0, 2)

    def update(self):
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right < 0:
            self.kill()
        global poweruptest
        if poweruptest == True:
            self.kill()
            poweruptest = False

#class Powerup2(pygame.sprite.Sprite):
    #def __init__(self):
        #super(Powerup2, self).__init__()
        #self.image = pygame.image.load('shield-image2.png').convert_alpha()
        #self.image.set_colorkey((255, 255, 255), RLEACCEL)
        #self.rect = self.image.get_rect(
            #center=(1350, random.randint(0,600))
        #)
        #self.speed = random.randint(0, 2)

    #def update(self):
        #self.rect.move_ip(-self.speed, 0)
        #if self.rect.right < 0:
            #self.kill()

            
pygame.init()

level = 1

lightning2 = False
screen = pygame.display.set_mode((1300,600), HWSURFACE|DOUBLEBUF|RESIZABLE)

pygame.mixer.music.load("superman-theme-song.mp3")
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1)

player = Player()
opponent = Opponent(level)
powerup = Powerup()
#powerup2 = Powerup2()

def lightning():
    player.speed = 3
    player.update(pressed_keys)
    player.speed = 1

#def shield():
    #powerupShield = 100

welcome = True
while welcome:
    
    background = pygame.Surface(screen.get_size())
    background.fill((144, 180, 237))
    screen.blit(background, (0,0))
    
    basicfont1 = pygame.font.SysFont('AzureoN', 64)
    text1 = basicfont1.render('Welcome to Kryptonite Attack!', True, (0, 0, 0))
    textrect1 = text1.get_rect()
    textrect1.centerx = screen.get_rect().centerx
    textrect1.centery = screen.get_rect().centery - 115
    screen.blit(text1, textrect1)

    basicfont2 = pygame.font.SysFont('Quango', 64)
    text2 = basicfont2.render('(Press any Key to Begin)', True, (0, 0, 0))
    textrect2 = text2.get_rect()
    textrect2.centerx = screen.get_rect().centerx
    textrect2.centery = screen.get_rect().centery + 115
    screen.blit(text2, textrect2)
    

    basicfont3 = pygame.font.SysFont('Quango', 64)
    text3 = basicfont3.render('Use Superman and Avoid the Kryptonite!', True, (0, 0, 0))
    textrect3 = text3.get_rect()
    textrect3.centerx = screen.get_rect().centerx
    textrect3.centery = screen.get_rect().centery - 20
    screen.blit(text3, textrect3)
       

    basicfont4 = pygame.font.SysFont('Quango', 64)
    text4 = basicfont4.render('Use WSAD to Control, Q is quit', True, (0, 0, 0))
    textrect4 = text4.get_rect()
    textrect4.centerx = screen.get_rect().centerx
    textrect4.centery = screen.get_rect().centery + 50
    screen.blit(text4, textrect4)
    pygame.display.flip()
    
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            welcome = False
    

background = pygame.Surface(screen.get_size())
background.fill((144, 180, 237))

players = pygame.sprite.Group()
opponents = pygame.sprite.Group()
powerups = pygame.sprite.Group()
powerup2s = pygame.sprite.Group()

all_sprites = pygame.sprite.Group()
all_sprites.add(player)
all_sprites.add(powerup)

all_sprites.add(player)
#all_sprites.add(powerup2)


ADDOPPONENT = pygame.USEREVENT + 1
pygame.time.set_timer(ADDOPPONENT, 260 - (level * 10))

ADDLEVEL = pygame.USEREVENT + 2
pygame.time.set_timer(ADDLEVEL, 20000)

ADDPOWERUP = pygame.USEREVENT + 3
pygame.time.set_timer(ADDPOWERUP, 15000)

#ADDPOWERUP2 = pygame.USEREVENT + 4
#pygame.time.set_timer(ADDPOWERUP2, 4000)

health = 100
killed = False

running = True
while running:
    time = pygame.time.get_ticks()

    for event in pygame.event.get():
        if event.type == KEYDOWN and event.key == K_q:
             running = False
             print("Escape")

        elif event.type == QUIT:
            running == False
            print("QUIT")

        elif event.type == ADDOPPONENT:
            new_opponent = Opponent(level)
            opponents.add(new_opponent)
            all_sprites.add(new_opponent)

        elif event.type == ADDLEVEL:
            level += 1

        elif event.type == ADDPOWERUP:
            new_powerup = Powerup()
            powerups.add(new_powerup)
            all_sprites.add(new_powerup)

        #elif event.type == ADDPOWERUP2:
            #new_powerup2 = Powerup2()
            #powerup2s.add(new_powerup2)
            #all_sprites.add(new_powerup2)

        
        
    
    screen.blit(background, (0, 0))
    pressed_keys = pygame.key.get_pressed()
    player.update(pressed_keys)

    opponents.update()
    powerups.update()
    powerup2s.update()
    pygame.display.set_caption("Health: " + str(health))

    basicfont = pygame.font.SysFont(None, 48)
    text = basicfont.render(str(health), True, (0, 0, 0))
    screen.blit(text, (50, 50))
    
    basicfont1 = pygame.font.SysFont(None, 48)
    text1 = basicfont1.render("Level " + str(level), True, (0, 0, 0))
    screen.blit(text1, (25, 25))

    
    if (time % 10000) - 1 < 0:
        level = level + 1
        

    if health < 50:
        background.fill((209, 18, 18))
    if health < 25:
        background.fill((255, 0, 0))

    for entity in all_sprites:
        screen.blit(entity.image, entity.rect)
        
    if pygame.sprite.spritecollideany(player, opponents):
        if health > 0:
            health -= .5
    elif health <= 0:
        killed = True

    if pygame.sprite.spritecollideany(player, powerups):
        lightningPowerup = 3
        player.speed = lightningPowerup
        lightning2 = True
    if pygame.sprite.spritecollideany(player, opponents) and lightning2 == True:
        lightningPowerup = 1
        lightning2 = False
        poweruptest = True
    #if pygame.sprite.spritecollideany(player, powerup2s):
        #powerupShield()
    if poweruptest == True:
        lightning()
        powerups.update()
        
            
    pygame.display.flip()

    while killed:
        background = pygame.Surface(screen.get_size())
        background.fill((144, 180, 237))
        screen.blit(background, (0,0))
        
        basicfont5 = pygame.font.SysFont('AzureoN', 64)
        text5 = basicfont5.render('You have been Killed', True, (0, 0, 0))
        textrect5 = text5.get_rect()
        textrect5.centerx = screen.get_rect().centerx
        textrect5.centery = screen.get_rect().centery - 115
        screen.blit(text5, textrect5)

        basicfont6 = pygame.font.SysFont('AzureoN', 64)
        text6 = basicfont6.render('Press Q to Quit', True, (0, 0, 0))
        textrect6 = text6.get_rect()
        textrect6.centerx = screen.get_rect().centerx
        textrect6.centery = screen.get_rect().centery + 80
        screen.blit(text6, textrect6)
        

        basicfont7 = pygame.font.SysFont('AzureoN', 64)
        text7 = basicfont7.render("You Finished on Level: " + str(level), True, (0, 0, 0))
        textrect7 = text7.get_rect()
        textrect7.centerx = screen.get_rect().centerx
        textrect7.centery = screen.get_rect().centery + 5
        screen.blit(text7, textrect7)
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == KEYDOWN and event.key == K_q:
                killed = False
                running = False

pygame.quit() 

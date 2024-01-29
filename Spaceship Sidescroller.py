import pygame
import random
import os
import threading

#global variables defined
WIDTH = 480
HEIGHT = 720
CONTROLS = 0
COUNT = 0
DURATION = 5000

#colours defined
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
CYAN = (0,255,255)

#game, image and sound folder defined using os module
game_folder = os.path.dirname(__file__)
img_folder = os.path.join(game_folder, 'img')
sound_folder = os.path.join(game_folder, 'wav')

class Player(pygame.sprite.Sprite):
    global playerdmg
    def __init__(self, hp, maxhp, speed, spritenum):
        pygame.sprite.Sprite.__init__(self)
        if spritenum == 1:
            self.image = pygame.transform.scale(player1_img, (50, 50))
        elif spritenum == 2:
            self.image = pygame.transform.scale(player2_img, (50, 50))
        elif spritenum == 3:
            self.image = pygame.transform.scale(player3_img, (50, 50))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH / 2
        self.rect.centery = HEIGHT / 1.25
        self.speedx = 0
        self.speedy = 0
        self.last = pygame.time.get_ticks()
        self.cooldown = 75
        self.hp = hp
        self.maxhp = maxhp
        self.speed = speed
        self.lives = 3
        self.bulletdmg = playerdmg
        self.power = 1
        self.power_time = pygame.time.get_ticks()

    def update(self):
        self.speedx = 0
        self.speedy = 0
        keystate = pygame.key.get_pressed()
        if CONTROLS == 0:
            if keystate[pygame.K_LEFT]:
                self.speedx = -self.speed
            if keystate[pygame.K_RIGHT]:
                self.speedx = self.speed
            if keystate[pygame.K_UP]:
                self.speedy = -self.speed
            if keystate[pygame.K_DOWN]:
                self.speedy = self.speed
            if keystate[pygame.K_LSHIFT]:
                self.speedx = (self.speedx / 2)
                self.speedy = (self.speedy / 2)
            if keystate[pygame.K_z]:
                now = pygame.time.get_ticks()
                if now - self.last >= self.cooldown:
                    self.last = now
                    player.shoot()
        elif CONTROLS == 1:
            if keystate[pygame.K_a]:
                self.speedx = -10
            if keystate[pygame.K_d]:
                self.speedx = 10
            if keystate[pygame.K_w]:
                self.speedy = -10
            if keystate[pygame.K_s]:
                self.speedy = 10
            if keystate[pygame.K_RSHIFT]:
                self.speedx = (self.speedx / 2)
                self.speedy = (self.speedy / 2)
            if keystate[pygame.K_SLASH]:
                now = pygame.time.get_ticks()
                if now - self.last >= self.cooldown:
                    self.last = now
                    player.shoot()
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT
        if self.power >= 2 and pygame.time.get_ticks() - self.power_time > DURATION:
            self.power -= 1
            self.power_time = pygame.time.get_ticks()
        hits = pygame.sprite.spritecollide(player, mobs, True)
        if hits:
            player.lives = player.lives - 1
            player.hp = player.maxhp
            pygame.mixer.Sound.play(explosionSound)
            player.respawn()
        hits2 = pygame.sprite.spritecollide(player, powerups, True)
        for hit in hits2:
            if hit.type == 'shield':
                pygame.mixer.Sound.play(powerSound)
                player.hp += random.randint(20,40)
                if player.hp > player.maxhp:
                    player.hp = player.maxhp
            if hit.type == 'gun':
                self.powerup()
                pygame.mixer.Sound.play(powerSound)

    def useSpec(self):
        self.speedx = 0
        self.speedy = 0
        player.spec()
    
    def shoot(self):
        now = pygame.time.get_ticks()
        if now - self.last > self.cooldown:
            self.last = now
        if self.power == 1:
            bullet = Bullet(self.rect.centerx, self.rect.top)
            all_sprites.add(bullet)
            bullets.add(bullet)
        if self.power >= 2:
            bullet1 = Bullet(self.rect.left, self.rect.centery)
            bullet2 = Bullet(self.rect.right, self.rect.centery)
            all_sprites.add(bullet1)
            all_sprites.add(bullet2)
            bullets.add(bullet1)
            bullets.add(bullet2)
        keystate = pygame.key.get_pressed()
        if (CONTROLS == 0 and keystate[pygame.K_LSHIFT]) or (CONTROLS == 1 and keystate[pygame.K_RSHIFT]):
            pygame.mixer.Sound.play(focusSound)
        else:
            pygame.mixer.Sound.play(shootSound)

    def spec(self):
        special = Special(self.rect.centerx, self.rect.top)
        all_sprites.add(special)
        specials.add(special)
        
    def powerup(self):
        self.power += 1
        self.power_time = pygame.time.get_ticks()

    def respawn(self):
        self.rect.centerx = WIDTH / 2
        self.rect.centery = HEIGHT / 1.25

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(bullet_img, (10, 20))
        self.rect = self.image.get_rect()
        self.image.set_colorkey(BLACK)
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = -30
        keystate = pygame.key.get_pressed()
        if (CONTROLS == 0 and keystate[pygame.K_LSHIFT] and keystate[pygame.K_z]) or (CONTROLS == 1 and keystate[pygame.K_RSHIFT] and keystate[pygame.K_SLASH]):
            self.image = pygame.transform.scale(fbullet_img, (15, 30))
            self.speedy = -50
            self.rect = self.image.get_rect()
            self.rect.bottom = y
            self.rect.centerx = x

    def update(self):
        self.rect.y += self.speedy
        if self.rect.bottom < 0:
            self.kill()

class Special(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(spec_img, (WIDTH*2, 100))
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = -20

    def update(self):
        self.rect.y += self.speedy
        if self.rect.bottom < 0:
            self.kill()

class Mob(pygame.sprite.Sprite):
    def __init__(self):
        global difficulty
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(mobImg, (40,40))
        self.rect = self.image.get_rect()
        self.image.set_colorkey(BLACK)
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(-100, -60)
        self.speedy = random.randrange(4, 8)
        self.speedx = random.randrange(-3, 3)
        self.hp = 50

    def update(self):
        global score, COUNT
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT + 10 or self.rect.left < -25 or self.rect.right > WIDTH + 20:
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(8, 16)
        if self.hp <= 0:
            self.kill()
            addMob()
            COUNT += 1
            if random.random() > 0.9:
                power = Powerup(self.rect.center)
                all_sprites.add(power)
                powerups.add(power)
        hits = pygame.sprite.groupcollide(mobs, bullets, False, True)
        for hit in hits:
            if difficulty == 0:
                score += 50
            elif difficulty == 1:
                score += 65
            elif difficulty == 2:
                score += 80
            self.hp -= player.bulletdmg

        hits2 = pygame.sprite.groupcollide(mobs, specials, True, False)
        for hit in hits2:
            addMob()
            score += 15
    
    def shoot(self):
        mobbullet = mobBullet(self.rect.centerx, self.rect.bottom)
        all_sprites.add(mobbullet)
        mobBullets.add(mobbullet)

class mobBullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((10, 10))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(-100, -60)
        self.speedy = random.randrange(4, 8)
        self.speedx = random.randrange(-3, 3)

    def update(self):
        self.rect.y += self.speedy
        self.rect.x += self.speedx

class Powerup(pygame.sprite.Sprite):
    def __init__(self, center):
        pygame.sprite.Sprite.__init__(self)
        self.type = random.choice(['shield', 'gun'])
        self.image = powerup_images[self.type]
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.speedy = 2

    def update(self):
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT:
            self.kill()

#Variables
cooldown_tracker_mob = 0
score = 0
difficulty = 0
if difficulty == 0:
    cooldown_tracker = 1800
    playerdmg = 15
elif difficulty == 1:
    cooldown_tracker = 3600
    playerdmg = 10
elif difficulty == 2:
    cooldown_tracker = 5400
    playerdmg = 5

#Start Pygame
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Galactic Shootout")
clock = pygame.time.Clock()
clickSound = pygame.mixer.Sound(os.path.join(sound_folder, 'Blip_Select.wav'))
shootSound = pygame.mixer.Sound(os.path.join(sound_folder, 'Regular_Laser.wav'))
focusSound = pygame.mixer.Sound(os.path.join(sound_folder, 'Focus_Laser.wav'))
explosionSound = pygame.mixer.Sound(os.path.join(sound_folder, 'Explosion.wav'))
dmgSound = pygame.mixer.Sound(os.path.join(sound_folder, 'Hit_Hurt.wav'))
specSound = pygame.mixer.Sound(os.path.join(sound_folder, 'Spec.wav'))
powerSound = pygame.mixer.Sound(os.path.join(sound_folder, 'PowerUp.wav'))
bgMusic = pygame.mixer.music.load(os.path.join(sound_folder, 'BGM.ogg'))

#Load all sprite images:
player1_img = pygame.image.load(os.path.join(img_folder, 'playerShip1_yellow.png')).convert()
player1_rect = player1_img.get_rect()
player2_img = pygame.image.load(os.path.join(img_folder, 'playerShip1_turq.png')).convert()
player2_rect = player1_img.get_rect()
player3_img = pygame.image.load(os.path.join(img_folder, 'playerShip1_blue.png')).convert()
player3_rect = player1_img.get_rect()
background = pygame.image.load(os.path.join(img_folder, 'starfieldnew.png')).convert()
background_rect = background.get_rect()
background2 = pygame.image.load(os.path.join(img_folder, 'starfieldnew2.png')).convert()
background2_rect = background2.get_rect()
background3 = pygame.image.load(os.path.join(img_folder, 'starfieldnew3.png')).convert()
background3_rect = background3.get_rect()
bullet_img = pygame.image.load(os.path.join(img_folder, "laserRed.png")).convert()
bullet_rect = bullet_img.get_rect()
spec_img = pygame.image.load(os.path.join(img_folder, "specBlue.png")).convert()
spec_rect = spec_img.get_rect()
fbullet_img = pygame.image.load(os.path.join(img_folder, "laserGreen.png")).convert()
fbullet_rect = fbullet_img.get_rect()
mobImg = pygame.image.load(os.path.join(img_folder, "angryRedEnemy.png")).convert()
mobImg_rect = mobImg.get_rect()

#dictionary to store two images for Powerup class since it has a chance of showing either one in the game
powerup_images = {}
powerup_images['shield'] = pygame.image.load(os.path.join(img_folder, 'shield_gold.png')).convert()
powerup_images['gun'] = pygame.image.load(os.path.join(img_folder, 'bolt_gold.png')).convert()

#define mob as class, group up other sprites
mob = Mob()
all_sprites = pygame.sprite.Group()
bullets = pygame.sprite.Group()
mobBullets = pygame.sprite.Group()
specials = pygame.sprite.Group()
mobs = pygame.sprite.Group()
powerups = pygame.sprite.Group()

#procedure for adding another mob after one has been defeated
def addMob():
  if COUNT < 40:
    m = Mob()
    all_sprites.add(m)
    mobs.add(m)

#fonts
font_menu = pygame.font.SysFont(None, 20)
font_name = pygame.font.match_font('arial')

#function for drawing text on menu buttons
def menu_text(text, font, color, surface, x, y):
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)

#functions for drawing text on the playing screen in Arial font
def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)

def draw_textGreen(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, GREEN)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)

def draw_textCyan(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, CYAN)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)

class Start():
    def menu(self):
        menu = True
        while menu == True:
            screen.fill((0,0,0))
            menu_text('main menu', font_menu, (255, 255, 255), screen, 20, 20)
            button1text = pygame.font.SysFont(None, 25).render('Play', True, (255,255,255))
            button2text = pygame.font.SysFont(None, 25).render('Settings', True, (255,255,255))
            button3text = pygame.font.SysFont(None, 25).render('Leaderboard', True, (255,255,255))
            button4text = pygame.font.SysFont(None, 25).render('Quit', True, (255,255,255))
 
            mx, my = pygame.mouse.get_pos()
 
            button_1 = pygame.Rect(50, 100, 200, 50)
            button_2 = pygame.Rect(50, 200, 200, 50)
            button_3 = pygame.Rect(50, 300, 200, 50)
            button_4 = pygame.Rect(50, 400, 200, 50)
            b1_text_rect = button1text.get_rect(center=button_1.center)
            b2_text_rect = button2text.get_rect(center=button_2.center)
            b3_text_rect = button3text.get_rect(center=button_3.center)
            b4_text_rect = button4text.get_rect(center=button_4.center)

            click = False
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        click = True
            
            if button_1.collidepoint((mx, my)):
                if click:
                    pygame.mixer.Sound.play(clickSound)
                    self.selectDiff()
                    menu = False
            if button_2.collidepoint((mx, my)):
                if click:
                    pygame.mixer.Sound.play(clickSound)
                    self.options()
                    menu = False
            if button_3.collidepoint((mx, my)):
                if click:
                  pygame.mixer.Sound.play(clickSound)
                  file = open("score.txt","r")
                  readFile = file.readlines()
                  n = 10
                  sort = sorted(readFile, reverse=True)
                  print ("Top 10:")
                  print("")
                  print ("Pos\t| Points | Name")
                  print("")
                  try:
                    for line in range (n):
                      print (str(line+1)+"\t"+str(sort[line]))
                    file.close()
                    menu = False
                    self.menu()
                  except:
                    menu = False
                    self.menu()
            if button_4.collidepoint((mx, my)):
                if click:
                    pygame.mixer.Sound.play(clickSound)
                    pygame.quit()
            
            pygame.draw.rect(screen, (255, 0, 0), button_1)
            pygame.draw.rect(screen, (0, 255, 0), button_2)
            pygame.draw.rect(screen, (0, 0, 255), button_3)
            pygame.draw.rect(screen, (0, 255, 255), button_4)
            screen.blit(button1text, b1_text_rect)
            screen.blit(button2text, b2_text_rect)
            screen.blit(button3text, b3_text_rect)
            screen.blit(button4text, b4_text_rect)
            
            pygame.display.update()
            clock.tick(60)

    def selectDiff(self):
        global difficulty
        diffSelect = True
        while diffSelect == True:
            screen.fill((0,0,0))
            menu_text('difficulty select', font_menu, (255, 255, 255), screen, 20, 20)
            button1text = pygame.font.SysFont(None, 25).render('Easy', True, (255,255,255))
            button2text = pygame.font.SysFont(None, 25).render('Normal', True, (0,0,0))
            button3text = pygame.font.SysFont(None, 25).render('Hard', True, (255,255,255))
 
            mx, my = pygame.mouse.get_pos()
 
            button_1 = pygame.Rect(50, 100, 200, 50)
            button_2 = pygame.Rect(50, 200, 200, 50)
            button_3 = pygame.Rect(50, 300, 200, 50)
            b1_text_rect = button1text.get_rect(center=button_1.center)
            b2_text_rect = button2text.get_rect(center=button_2.center)
            b3_text_rect = button3text.get_rect(center=button_3.center)

            click = False
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        click = True
            
            if button_1.collidepoint((mx, my)):
                if click:
                    difficulty = 0
                    print ("Selected Difficulty: Easy")
                    diffSelect = False
                    pygame.mixer.Sound.play(clickSound)
                    self.charSelect()
            if button_2.collidepoint((mx, my)):
                if click:
                    difficulty = 1
                    print ("Selected Difficulty: Normal")
                    diffSelect = False
                    pygame.mixer.Sound.play(clickSound)
                    self.charSelect()
            if button_3.collidepoint((mx, my)):
                if click:
                    difficulty = 2
                    print ("Selected Difficulty: Hard")
                    diffSelect = False
                    pygame.mixer.Sound.play(clickSound)
                    self.charSelect()
            
            pygame.draw.rect(screen, (255, 0, 0), button_1)
            pygame.draw.rect(screen, (255,255,51), button_2)
            pygame.draw.rect(screen, (0, 255, 0), button_3)
            screen.blit(button1text, b1_text_rect)
            screen.blit(button2text, b2_text_rect)
            screen.blit(button3text, b3_text_rect)
            
            pygame.display.update()
            clock.tick(60)

    def charSelect(self):
        global player
        global playerType
        chrSelect = True
        while chrSelect == True:
            screen.fill((0,0,0))
            menu_text('Character Select', font_menu, (255, 255, 255), screen, 20, 20)
            button1text = pygame.font.SysFont(None, 25).render('Yellow (High HP, Low Speed)', True, (0,0,0))
            button2text = pygame.font.SysFont(None, 25).render('Turq (Balanced)', True, (255, 255, 255))
            button3text = pygame.font.SysFont(None, 25).render('Blue (Low HP, High Speed)', True, (255,255,255))
 
            mx, my = pygame.mouse.get_pos()
 
            button_1 = pygame.Rect(50, 100, 300, 50)
            button_2 = pygame.Rect(50, 200, 300, 50)
            button_3 = pygame.Rect(50, 300, 300, 50)
            b1_text_rect = button1text.get_rect(center=button_1.center)
            b2_text_rect = button2text.get_rect(center=button_2.center)
            b3_text_rect = button3text.get_rect(center=button_3.center)
            pygame.draw.rect(screen, (255, 255, 0), button_1)
            pygame.draw.rect(screen, (64, 224, 208), button_2)
            pygame.draw.rect(screen, (160, 32, 240), button_3)
            screen.blit(button1text, b1_text_rect)
            screen.blit(button2text, b2_text_rect)
            screen.blit(button3text, b3_text_rect)

            click = False
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        click = True
            
            if button_1.collidepoint((mx, my)):
                if click:
                    player = Player(170, 170, 7, 1)
                    print ("Selected Character: Yellow")
                    playerType = 1
                    pygame.mixer.Sound.play(clickSound)
                    chrSelect = False
            if button_2.collidepoint((mx, my)):
                if click:
                    player = Player(100, 100, 10, 2)
                    print ("Selected Character: Turq")
                    playerType = 2
                    pygame.mixer.Sound.play(clickSound)
                    chrSelect = False
            if button_3.collidepoint((mx, my)):
                if click:
                    print ("Selected Character: Blue")
                    playerType = 3
                    player = Player(60, 60, 15, 3)
                    pygame.mixer.Sound.play(clickSound)
                    chrSelect = False
            
            pygame.display.update()
            clock.tick(60)
        
    def options(self):
        global CONTROLS
        option = True
        click = False
        while option == True:
            screen.fill((0,0,0))
            menu_text('Options:', font_menu, (255, 255, 255), screen, 20, 20)
            button1text = pygame.font.SysFont(None, 25).render('Back To Menu', True, (0,0,0))
            button2text = pygame.font.SysFont(None, 25).render('Controls 0 (Arrow Keys, Z, X, LSHIFT)', True, (255, 255, 255))
            button3text = pygame.font.SysFont(None, 25).render('Controls 1 (WASD, "/", ".", RSHIFT)', True, (255,255,255))
            
            mx, my = pygame.mouse.get_pos()

            button_1 = pygame.Rect(150, 100, 200, 50)
            button_2 = pygame.Rect(100, 200, 325, 50)
            button_3 = pygame.Rect(100, 300, 325, 50)
            b1_text_rect = button1text.get_rect(center=button_1.center)
            b2_text_rect = button2text.get_rect(center=button_2.center)
            b3_text_rect = button3text.get_rect(center=button_3.center)
            pygame.draw.rect(screen, (255, 0, 0), button_1)
            pygame.draw.rect(screen, (0, 255, 0), button_2)
            pygame.draw.rect(screen, (0, 0, 255), button_3)
            screen.blit(button1text, b1_text_rect)
            screen.blit(button2text, b2_text_rect)
            screen.blit(button3text, b3_text_rect)

            click = False
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        option = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        click = True

            if button_1.collidepoint((mx, my)):
                if click:
                    pygame.mixer.Sound.play(clickSound)
                    self.menu()
                    option = False
            if button_2.collidepoint((mx, my)):
                if click:
                    CONTROLS = 0
                    pygame.mixer.Sound.play(clickSound)
                    print ("Control scheme set to 0.")
            if button_3.collidepoint((mx, my)):
                if click:
                    CONTROLS = 1
                    pygame.mixer.Sound.play(clickSound)
                    print ("Control scheme set to 1.")
            
            pygame.display.update()
            clock.tick(60)

class Game():
    def gameLoop(self):
        running1 = True
        running2 = False
        running3 = False
        pygame.mixer.music.play(-1)
        global WIDTH, HEIGHT, CONTROLS, cooldown_tracker, cooldown_tracker_mob, score, difficulty, player, COUNT
        all_sprites.add(player)
        for i in range(4):
          addMob()
        while running1 == True:
            clock.tick(60)
            cooldown_tracker += clock.get_time()
            cooldown_tracker_mob += clock.get_time()
            if cooldown_tracker_mob >= 250:
                cooldown_tracker_mob = random.randint(0,100)
                mob.shoot()
            # Process input (events)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running1 = False
                if event.type == pygame.KEYDOWN:
                    if (CONTROLS == 0 and event.key == pygame.K_x) or (CONTROLS == 1 and event.key == pygame.K_PERIOD):
                        if difficulty == 0 and cooldown_tracker >= 1800:
                                cooldown_tracker = 0
                                player.useSpec()
                                pygame.mixer.Sound.play(specSound)
                        elif difficulty == 1 and cooldown_tracker >= 3600:
                                cooldown_tracker = 0
                                player.useSpec()
                                pygame.mixer.Sound.play(specSound)
                        elif difficulty == 2 and cooldown_tracker >= 5400:
                                cooldown_tracker = 0
                                player.useSpec()
                                pygame.mixer.Sound.play(specSound)

            #update all sprites in group
            all_sprites.update()

            if player.lives == 0:
                print("Game Over!")
                print("Your score was: ",score)
                running1 = False

            if COUNT == 20:
                COUNT = 0
                running1 = False
                running2 = True

            hits = pygame.sprite.spritecollide(player, mobBullets, True)
            if hits:
                player.hp = player.hp - 10
                pygame.mixer.Sound.play(dmgSound)
                if player.hp == 0:
                    player.lives = player.lives - 1
                    pygame.mixer.Sound.play(explosionSound)
                    player.respawn()
                    player.hp = player.maxhp
                    if player.lives == 0:
                        pygame.mixer.Sound.play(explosionSound)
                        print("Game Over!")
                        print("Your score was: ",score)
                        running1 = False

            hits = pygame.sprite.groupcollide(mobBullets, specials, True, False)

            # Draw / render
            screen.fill(BLACK)
            screen.blit(background, background_rect)
            all_sprites.draw(screen)
            draw_text(screen, 'Score: '+str(score), 18, WIDTH / 2, 10)
            draw_text(screen, 'Enemies Shot: '+str(COUNT)+'/20', 18, (WIDTH / 6)*5, 690)
            draw_textGreen(screen, 'Lives: '+str(player.lives)+'/3', 18, (WIDTH / 6)*5, 30)
            draw_text(screen, 'Stage 1', 18, WIDTH / 9, 690)
            if player.maxhp == 170:
                draw_textGreen(screen, 'HP: '+str(player.hp)+'/170', 18, (WIDTH / 6)*5, 10)
            elif player.maxhp == 100:
                draw_textGreen(screen, 'HP: '+str(player.hp)+'/100', 18, (WIDTH / 6)*5, 10)
            elif player.maxhp == 60:
                draw_textGreen(screen, 'HP: '+str(player.hp)+'/60', 18, (WIDTH / 6)*5, 10)
            if difficulty == 0:
                if cooldown_tracker > 1800:
                    draw_textCyan(screen, 'Special Ready', 18, WIDTH / 6, 10)
                else:
                    draw_textCyan(screen, 'Charge: '+str(cooldown_tracker)+'/1800', 18, WIDTH / 6, 10)
            elif difficulty == 1:
                if cooldown_tracker > 3600:
                    draw_textCyan(screen, 'Special Ready', 18, WIDTH / 6, 10)
                else:
                    draw_textCyan(screen, 'Charge: '+str(cooldown_tracker)+'/3600', 18, WIDTH / 6, 10)
            elif difficulty == 2:
                if cooldown_tracker > 5400:
                    draw_textCyan(screen, 'Special Ready', 18, WIDTH / 6, 10)
                else:
                    draw_textCyan(screen, 'Charge: '+str(cooldown_tracker)+'/5400', 18, WIDTH / 6, 10)
                
            #After drawing everything, flip the display to update the contents of the screen
            pygame.display.flip()

        while running2 == True:
            clock.tick(60)
            cooldown_tracker += clock.get_time()
            cooldown_tracker_mob += clock.get_time()
            if cooldown_tracker_mob >= 250:
                cooldown_tracker_mob = random.randint(0,100)
                mob.shoot()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running2 = False
                if event.type == pygame.KEYDOWN:
                    if (CONTROLS == 0 and event.key == pygame.K_x) or (CONTROLS == 1 and event.key == pygame.K_PERIOD):
                        if difficulty == 0 and cooldown_tracker >= 1800:
                                cooldown_tracker = 0
                                player.useSpec()
                                pygame.mixer.Sound.play(specSound)
                        elif difficulty == 1 and cooldown_tracker >= 3600:
                                cooldown_tracker = 0
                                player.useSpec()
                                pygame.mixer.Sound.play(specSound)
                        elif difficulty == 2 and cooldown_tracker >= 5400:
                                cooldown_tracker = 0
                                player.useSpec()
                                pygame.mixer.Sound.play(specSound)
            
            all_sprites.update()

            if player.lives == 0:
                print("Game Over!")
                print("Your score was: ",score)
                running2 = False

            if COUNT == 30:
                COUNT = 0
                running2 = False
                running3 = True

            hits = pygame.sprite.spritecollide(player, mobBullets, True)
            if hits:
                player.hp = player.hp - 10
                pygame.mixer.Sound.play(dmgSound)
                if player.hp == 0:
                    player.lives = player.lives - 1
                    pygame.mixer.Sound.play(explosionSound)
                    player.respawn()
                    player.hp = player.maxhp
                    if player.lives == 0:
                        pygame.mixer.Sound.play(explosionSound)
                        print("Game Over!")
                        print("Your score was: ",score)
                        running2 = False

            hits = pygame.sprite.groupcollide(mobBullets, specials, True, False)

            screen.fill(BLACK)
            screen.blit(background2, background2_rect)
            all_sprites.draw(screen)
            draw_text(screen, 'Score: '+str(score), 18, WIDTH / 2, 10)
            draw_text(screen, 'Enemies Shot: '+str(COUNT)+'/30', 18, (WIDTH / 6)*5, 690)
            draw_text(screen, 'Stage 2', 18, WIDTH / 9, 690)
            draw_textGreen(screen, 'Lives: '+str(player.lives)+'/3', 18, (WIDTH / 6)*5, 30)
            if player.maxhp == 170:
                draw_textGreen(screen, 'HP: '+str(player.hp)+'/170', 18, (WIDTH / 6)*5, 10)
            elif player.maxhp == 100:
                draw_textGreen(screen, 'HP: '+str(player.hp)+'/100', 18, (WIDTH / 6)*5, 10)
            elif player.maxhp == 60:
                draw_textGreen(screen, 'HP: '+str(player.hp)+'/60', 18, (WIDTH / 6)*5, 10)
            if difficulty == 0:
                if cooldown_tracker > 1800:
                    draw_textCyan(screen, 'Special Ready', 18, WIDTH / 6, 10)
                else:
                    draw_textCyan(screen, 'Charge: '+str(cooldown_tracker)+'/1800', 18, WIDTH / 6, 10)
            elif difficulty == 1:
                if cooldown_tracker > 3600:
                    draw_textCyan(screen, 'Special Ready', 18, WIDTH / 6, 10)
                else:
                    draw_textCyan(screen, 'Charge: '+str(cooldown_tracker)+'/3600', 18, WIDTH / 6, 10)
            elif difficulty == 2:
                if cooldown_tracker > 5400:
                    draw_textCyan(screen, 'Special Ready', 18, WIDTH / 6, 10)
                else:
                    draw_textCyan(screen, 'Charge: '+str(cooldown_tracker)+'/5400', 18, WIDTH / 6, 10)
            pygame.display.flip()
            
        while running3 == True:
            clock.tick(60)
            cooldown_tracker += clock.get_time()
            cooldown_tracker_mob += clock.get_time()
            if cooldown_tracker_mob >= 250:
                cooldown_tracker_mob = random.randint(0,100)
                mob.shoot()
                
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running3 = False
                if event.type == pygame.KEYDOWN:
                    if (CONTROLS == 0 and event.key == pygame.K_x) or (CONTROLS == 1 and event.key == pygame.K_PERIOD):
                        if difficulty == 0 and cooldown_tracker >= 1800:
                                cooldown_tracker = 0
                                player.useSpec()
                                pygame.mixer.Sound.play(specSound)
                        elif difficulty == 1 and cooldown_tracker >= 3600:
                                cooldown_tracker = 0
                                player.useSpec()
                                pygame.mixer.Sound.play(specSound)
                        elif difficulty == 2 and cooldown_tracker >= 5400:
                                cooldown_tracker = 0
                                player.useSpec()
                                pygame.mixer.Sound.play(specSound)
            
            all_sprites.update()

            if player.lives == 0:
                print("Game Over!")
                print("Your score was: ",score)
                running3 = False

            if COUNT == 40:
              running3 = False
              print ("Congratulations, you beat the game!")
              print("Your final score is:",score)

            hits = pygame.sprite.spritecollide(player, mobBullets, True)
            if hits:
                player.hp = player.hp - 10
                pygame.mixer.Sound.play(dmgSound)
                if player.hp == 0:
                    player.lives = player.lives - 1
                    pygame.mixer.Sound.play(explosionSound)
                    player.respawn()
                    player.hp = player.maxhp
                    if player.lives == 0:
                        pygame.mixer.Sound.play(explosionSound)
                        print("Game Over!")
                        print("Your score was: ",score)
                        running3 = False

            hits = pygame.sprite.groupcollide(mobBullets, specials, True, False)

            screen.fill(BLACK)
            screen.blit(background3, background3_rect)
            all_sprites.draw(screen)
            draw_text(screen, 'Score: '+str(score), 18, WIDTH / 2, 10)
            draw_text(screen, 'Enemies Shot: '+str(COUNT)+'/40', 18, (WIDTH / 6)*5, 690)
            draw_text(screen, 'Stage 3', 18, WIDTH / 9, 690)
            draw_textGreen(screen, 'Lives: '+str(player.lives)+'/3', 18, (WIDTH / 6)*5, 30)
            if player.maxhp == 170:
                draw_textGreen(screen, 'HP: '+str(player.hp)+'/170', 18, (WIDTH / 6)*5, 10)
            elif player.maxhp == 100:
                draw_textGreen(screen, 'HP: '+str(player.hp)+'/100', 18, (WIDTH / 6)*5, 10)
            elif player.maxhp == 60:
                draw_textGreen(screen, 'HP: '+str(player.hp)+'/60', 18, (WIDTH / 6)*5, 10)
            if difficulty == 0:
                if cooldown_tracker > 1800:
                    draw_textCyan(screen, 'Special Ready', 18, WIDTH / 6, 10)
                else:
                    draw_textCyan(screen, 'Charge: '+str(cooldown_tracker)+'/1800', 18, WIDTH / 6, 10)
            elif difficulty == 1:
                if cooldown_tracker > 3600:
                    draw_textCyan(screen, 'Special Ready', 18, WIDTH / 6, 10)
                else:
                    draw_textCyan(screen, 'Charge: '+str(cooldown_tracker)+'/3600', 18, WIDTH / 6, 10)
            elif difficulty == 2:
                if cooldown_tracker > 5400:
                    draw_textCyan(screen, 'Special Ready', 18, WIDTH / 6, 10)
                else:
                    draw_textCyan(screen, 'Charge: '+str(cooldown_tracker)+'/5400', 18, WIDTH / 6, 10)
                
            pygame.display.flip()

    def saveScore(self):
      saving = True
      while saving == True:
          name = input("Enter a nickname longer than 2 characters if you wish to save this score: ")
          if len(name) < 3:
            print ("Too short, try again.")
            saving = True
          else:
            file = open("score.txt","a")
            file.write("| "+str(score)+" | "+name+"\n")
            print("Score saved.")
            file.close()
            saving = False

#assigning Start and Game classes to variables and calling methods to begin the game
start = Start()
game = Game()

start.menu()
game.gameLoop()
pygame.quit()
game.saveScore()

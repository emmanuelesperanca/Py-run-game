import pygame
from sys import exit
from random import randint, choice

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        player_walk1 = pygame.image.load('graphics/Player/player_walk_1.png').convert_alpha()
        player_walk2 = pygame.image.load('graphics/Player/player_walk_2.png').convert_alpha()
        self.player_walk = [player_walk1, player_walk2]
        self.player_index = 0
        self.player_jump = pygame.image.load('graphics/Player/jump.png').convert_alpha()
        self.image = self.player_walk[self.player_index]
        self.rect = self.image.get_rect(midbottom = (80,300))
        self.gravity = 0
        self.jump_sound = pygame.mixer.Sound('audio/jump.mp3')
        self.jump_sound.set_volume(0.01)

    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom == 300:
            self.gravity = -8
            self.jump_sound.play()
        elif keys[pygame.K_SPACE] and self.rect.bottom < 100:
            self.gravity = 5
    
    def apply_gravity(self):
        self.gravity += 0.15
        self.rect.y += self.gravity
        if self.rect.bottom >= 300:
            self.rect.bottom = 300
    
    def player_animation(self):
        if self.rect.bottom < 300:
            self.image = self.player_jump
        else:
            self.player_index += 0.1
            if self.player_index >= len(self.player_walk):
                self.player_index = 0
            self.image = self.player_walk[int(self.player_index)]

    def update(self):
        self.player_input()
        self.apply_gravity()
        self.player_animation()

class Obstacle(pygame.sprite.Sprite):
    def __init__(self, type):
        super().__init__()
        
        if type == 'fly':
            fly1_surface = pygame.image.load('graphics/Fly/fly1.png').convert_alpha()
            fly2_surface = pygame.image.load('graphics/Fly/fly2.png').convert_alpha()
            self.frames = [fly1_surface, fly2_surface]
            y_pos = 200

        else:
            snail1_surface = pygame.image.load('graphics/snail/snail1.png').convert_alpha()
            snail2_surface = pygame.image.load('graphics/snail/snail2.png').convert_alpha()
            self.frames = [snail1_surface, snail2_surface]
            y_pos = 300

        self.animation_index = 0    
        self.image = self.frames[self.animation_index]
        self.rect = self.image.get_rect(midbottom = (randint(900,1200), y_pos))
    
    def obstacle_animation(self):
        self.animation_index += 0.1
        if self.animation_index >= len(self.frames):
            self.animation_index = 0
        self.image = self.frames[int(self.animation_index)]

    def destroy(self):
        if self.rect.x <= -100:
            self.kill()    

    def update(self):
        self.obstacle_animation()
        self.rect.x -= 5
        self.destroy

def display_score():
    current_time = int(pygame.time.get_ticks()/1000) - start_time
    score_surface = text_font.render(f'Score: {current_time}', False, (50,50,50))
    score_rectangle = score_surface.get_rect(center = (400,50))
    screen.blit(score_surface,score_rectangle)
    return current_time

def collision_sprite():
    if pygame.sprite.spritecollide(player.sprite, obstacles, False):
        obstacles.empty()
        return False
    return True       

# Settings
pygame.init()
screen = pygame.display.set_mode((800, 400))
pygame.display.set_caption('Py Run!')
clock = pygame.time.Clock()
game_active = False
start_time = 0
text_font = pygame.font.Font('font/Pixeltype.ttf',  50)
text_font2 = pygame.font.Font('font/Pixeltype.ttf',  20)
score = 0
bg_music = pygame.mixer.Sound('audio/music.wav')
bg_music.set_volume(0.01)
bg_music.play(loops = -1)

# Scenario
sky_surface = pygame.image.load('graphics/Sky.png').convert()
ground_surface = pygame.image.load('graphics/ground.png').convert()

# Obstacles
obstacles = pygame.sprite.Group()

# Player
player = pygame.sprite.GroupSingle()
player.add(Player())

# Menu
player_stand = pygame.image.load('graphics/Player/player_stand.png').convert_alpha()
player_stand = pygame.transform.rotozoom(player_stand,0,2)
player_stand_rectangle = player_stand.get_rect(center = (400,200))
title_surface = text_font.render('Welcome to Py Run!', False, (111,196,169))
title_rectangle = title_surface.get_rect(center=(400,330))
credits_surface = text_font2.render('A pygame by Emmanuel Esperanca', False, (50,50,50))
credits_rectangle = credits_surface.get_rect(center=(400,380))
menu_surface = text_font.render('Press SPACE to play', False, (50,50,50))
menu_rectangle = menu_surface.get_rect(center=(400,50))

# Timer
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 1500)
snail_animation_timer = pygame.USEREVENT +2
pygame.time.set_timer(snail_animation_timer, 300)
fly_animation_timer = pygame.USEREVENT +3
pygame.time.set_timer(fly_animation_timer, 100)

while True:
    # Events    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.KEYDOWN and game_active == False:
            if event.key == pygame.K_SPACE:
                game_active = True
                start_time = int(pygame.time.get_ticks()/1000)
        if event.type == obstacle_timer and game_active:
            obstacles.add(Obstacle(choice(['fly','snail','snail','snail'])))

    if game_active:     
        # Scenario  
        screen.blit(sky_surface,(0,0))
        screen.blit(ground_surface,(0,300))  

        # Score  
        score = display_score() 
        
        # Obstacles
        obstacles.draw(screen)
        obstacles.update()
  
        # Player
        player.draw(screen)
        player.update()
        
        # Collision
        game_active = collision_sprite()

    else:
        screen.fill((94,129,162))
        screen.blit(player_stand,player_stand_rectangle) 
        player_gravity = 0
        #player_rectangle.midbottom = (80,300)
 
        score_message = text_font.render(f'Your final score: {score}', 'false',(111,196,169)) 
        score_message_rectangle = score_message.get_rect(center = (400,330))
        if score == 0:
            screen.blit(menu_surface,menu_rectangle) 
            screen.blit(title_surface,title_rectangle) 
            screen.blit(credits_surface,credits_rectangle)
        else:
            screen.blit(menu_surface,menu_rectangle)
            screen.blit(score_message,score_message_rectangle)                
            screen.blit(credits_surface,credits_rectangle)

    pygame.display.update()
    clock.tick(120)

import pygame
from menu import *
from player import *
from asteroid import Asteroid
from enemies import Enemies
import random
import time

class Game():
    def __init__(self):
        pygame.init()
        pygame.mouse.set_visible(False)
        self.running, self.playing, self.paused = True, False, False
        self.UP_KEY, self.DOWN_KEY, self.START_KEY, self.BACK_KEY = False, False, False, False
        self.DISPLAY_W, self.DISPLAY_H = 800, 480
        self.display = pygame.Surface((self.DISPLAY_W, self.DISPLAY_H))
        
        if rpi:
            from gpiozero import Button, MCP3008

            self.chanY = MCP3008(channel=0)
            self.chanX = MCP3008(channel=1)

            self.start_btn = Button(23)
            self.back_btn = Button(24)
            self.pause_btn = Button(17)

            self.window = pygame.display.set_mode(((self.DISPLAY_W, self.DISPLAY_H)), pygame.FULLSCREEN)
            self.start_btn_press = pygame.USEREVENT + 0
            self.back_btn_press = pygame.USEREVENT + 1
            self.pause_btn_press = pygame.USEREVENT + 2
            self.start_event = pygame.event.Event(self.start_btn_press)
            self.back_event = pygame.event.Event(self.back_btn_press)
            self.pause_event = pygame.event.Event(self.pause_btn_press)
            self.start_btn.when_pressed = self.start_pressed
            self.back_btn.when_pressed = self.back_pressed
            self.pause_btn.when_pressed = self.pause_pressed

            self.font_name = 'Font/8-BIT_WONDER.TTF'
            self.bg_game_scroll = pygame.image.load('Images/bg_game_scroll.png').convert()
        else:
            self.window = pygame.display.set_mode(((self.DISPLAY_W, self.DISPLAY_H)))
            self.bg_game_scroll = pygame.image.load('Space-side-scroller/Images/bg_game_scroll.png').convert()
            self.font_name = 'Space-side-scroller/Font/8-BIT_WONDER.TTF'
    
        pygame.display.set_caption("Space Sider Scroller")
        self.BLACK, self.WHITE = (0, 0, 0), (255, 255, 255)
        self.main_menu = MainMenu(self)
        self.highscore = HighscoreMenu(self)
        self.credits = CreditsMenu(self)
        self.quit = QuitMenu(self)
        self.curr_menu = self.main_menu
        self.bg_game_scroll_width = self.bg_game_scroll.get_width()
        self.scroll = 0
        self.tiles = 3
        self.clock = pygame.time.Clock()
        self.FPS = 80
        self.start_time = 0
        
    def game_loop(self):
        self.score = 0
        self.health = 3
        self.player_sprite = Player(self, (0, self.DISPLAY_H / 2), self.DISPLAY_W, self.DISPLAY_H)
        self.player = pygame.sprite.GroupSingle(self.player_sprite)
        self.bullet_group = pygame.sprite.Group()
        self.enemy_group = pygame.sprite.Group()
        self.enemy_bullet = pygame.sprite.Group()
        self.obstacle = pygame.sprite.Group()
        
        
        while self.playing:
            self.current_time = int(pygame.time.get_ticks() / 1000) - self.start_time
            #Check the event handler for events
            self.check_events()

            # Get random numbers for spawn position and when to spawn
            pos = random.randint(0, 480)
            spawn_asteroid = random.randrange(150)
            spawn_enemy = random.randrange(350)
            which_asteroid = random.randint(1,2)
            random_speed = random.randint(3, 6) 

            # Spawn enemeis
            if spawn_enemy == 10:
                self.enemy_sprite = Enemies(self, (900, pos), self.DISPLAY_W, self.DISPLAY_H, random_speed)
                self.enemy_group.add(self.enemy_sprite)
                spawn_col_pos_enemy = Enemies.return_pos(self.enemy_sprite)
                enemy_spawn_col = pygame.sprite.spritecollide(self.enemy_sprite, self.enemy_group, True)
                if spawn_col_pos_enemy > 850 and enemy_spawn_col:
                    self.enemy_sprite = Enemies(self, (900, pos), self.DISPLAY_W, self.DISPLAY_H, random_speed)
                    self.enemy_group.add(self.enemy_sprite)

            # If spawn_obstacles is five, we create and spawn one
            if spawn_asteroid == 5:
                self.asteroid_sprite = Asteroid(self, (900, pos), self.DISPLAY_W, self.DISPLAY_H, which_asteroid, random_speed)
                self.obstacle.add(self.asteroid_sprite)
                spawn_col_pos_asteroid = Asteroid.return_pos(self.asteroid_sprite)
                asteroid_spawn_col = pygame.sprite.spritecollide(self.asteroid_sprite, self.obstacle, True)
                if spawn_col_pos_asteroid > 850 and asteroid_spawn_col:
                    self.asteroid_sprite = Asteroid(self, (900, pos), self.DISPLAY_W, self.DISPLAY_H, which_asteroid, random_speed)
                    self.obstacle.add(self.asteroid_sprite)

            # When we reach 0 in healt, pause and exit
            if self.health == 0:
                self.stats()
                self.draw_text('GAME OVER', 40, self.DISPLAY_W / 2, self.DISPLAY_H / 2 - 100)
                self.window.blit(self.display, (0,0))
                pygame.display.update()
                time.sleep(3)
                self.playing = False
                scores.append(self.score)
 
            #Exit game loop with back key
            if self.BACK_KEY:
                self.playing = False
                scores.append(self.score)
            
            #Scrolling Background
            for i in range(0, self.tiles):
                self.display.blit(self.bg_game_scroll, (i * self.bg_game_scroll_width + self.scroll, 0))
            self.scroll -= 4
            if abs(self.scroll) > self.bg_game_scroll_width:
                self.scroll = 0

            #Updates
            self.score += self.current_time
            self.bullet_group.update()
            self.bullet_group.draw(self.display)
            self.enemy_bullet.update()
            self.enemy_bullet.draw(self.display)
            self.player.update()
            self.player.draw(self.display)
            self.obstacle.update()
            self.obstacle.draw(self.display)
            self.enemy_group.update()
            self.enemy_group.draw(self.display)
            self.stats()
            body_hit = pygame.sprite.spritecollide(self.player_sprite, self.obstacle, True)
            player_enemy_collide =pygame.sprite.spritecollide(self.player_sprite, self.enemy_group, True)
            enemy_fire_hit = pygame.sprite.spritecollide(self.player_sprite, self.enemy_bullet, True)
            if body_hit or enemy_fire_hit or player_enemy_collide:
                self.health -= 1
            bullet_hit_asteroid = pygame.sprite.groupcollide(self.obstacle, self.bullet_group, True, True)
            bullet_hit_enemy = pygame.sprite.groupcollide(self.enemy_group, self.bullet_group, True, True)
            if bullet_hit_asteroid or bullet_hit_enemy:
                self.score += 100
            self.window.blit(self.display, (0,0))
            pygame.display.update()
            self.reset_keys()
            self.clock.tick(self.FPS)

            #Loop to pause the game
            while self.paused:
                self.draw_text('PAUSED', 40, self.DISPLAY_W / 2, self.DISPLAY_H / 2 - 100)
                self.check_events()
                self.window.blit(self.display, (0,0))
                pygame.display.update()

    def start_pressed(self):
        pygame.event.post(self.start_event)
    def back_pressed(self):
        pygame.event.post(self.back_event)
    def pause_pressed(self):
        pygame.event.post(self.pause_event)
        
    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                pygame.display.quit()
                pygame.quit()
                exit()
            if rpi:
                if event.type == self.start_btn_press:
                        self.START_KEY = True
                if event.type == self.back_btn_press:
                        self.BACK_KEY = True
                if event.type == self.pause_btn_press:
                    if not self.main_menu.run_display:
                        if self.paused == True:
                            self.paused = False
                        else:
                            self.paused = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.START_KEY = True
                if event.key == pygame.K_BACKSPACE:
                    if self.paused:
                        self.BACK_KEY = False
                    else:
                        self.BACK_KEY = True
                if event.key == pygame.K_DOWN:
                    self.DOWN_KEY = True
                if event.key == pygame.K_UP:
                    self.UP_KEY = True
                if event.key == pygame.K_LEFT:
                    self.LEFT_KEY = True
                if event.key == pygame.K_RIGHT:
                    self.RIGHT_KEY = True
                if event.key == pygame.K_SPACE:
                    if not self.main_menu.run_display:
                        if self.paused == True:
                            self.paused = False
                        else:
                            self.paused = True
        if rpi:
            if (self.main_menu.joystick_timer >= 0.5) and ((self.chanY.value * 480) < 220): # Y DOWN
                self.DOWN_KEY = True
                self.main_menu.joystick_timer = 0
            elif (self.main_menu.joystick_timer >= 0.5) and ((self.chanY.value * 480) > 260): # Y UP
                self.UP_KEY = True
                self.main_menu.joystick_timer = 0 
            elif (self.main_menu.joystick_timer >= 0.5) and ((self.chanX.value * 800) > 420): # X RIGHT
                self.RIGHT_KEY = True
                self.main_menu.joystick_timer = 0
            elif (self.main_menu.joystick_timer >= 0.5) and ((self.chanX.value * 800) < 380): # X LEFT
                self.LEFT_KEY = True
                self.main_menu.joystick_timer = 0
            else:
                self.main_menu.joystick_timer += self.main_menu.dt

    def reset_keys(self):
        self.UP_KEY, self.DOWN_KEY, self.START_KEY, self.BACK_KEY = False, False, False, False

    
    ### Function to draw text on the screen
    ### Take 4 Arguments, "String" or integer, Size of the text, x coordinate, y coordinate
    def draw_text(self, text, size, x, y):
        font = pygame.font.Font(self.font_name, size)
        text_surface = font.render(str(text), True, self.WHITE)
        text_rect = text_surface.get_rect()
        text_rect.centerx = x
        text_rect.centery = y
        self.display.blit(text_surface, text_rect)
    
    ### Function to draw score on the screen
    ### Take 4 Arguments, "String" or integer, Size of the text, x coordinate, y coordinate
    def draw_score(self, text, size, x, y):
        font = pygame.font.Font(self.font_name, size)
        text_surface = font.render(str(text), True, self.WHITE)
        text_rect = text_surface.get_rect()
        text_rect.x = x
        text_rect.y = y
        self.display.blit(text_surface, text_rect)

    def stats(self):
        self.scorex, self.scorey = 4, 4
        self.hpx, self.hpy = 4, 35
        self.draw_score("Score " + str(self.score), 30, self.scorex, self.scorey)
        self.draw_score("Health " + str(self.health), 30, self.hpx, self.hpy)

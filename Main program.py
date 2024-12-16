import os
from random import randint
from sys import argv
from time import sleep
script_directory = os.path.dirname(os.path.abspath(argv[0]))
os.chdir(script_directory)
import pygame
pygame.init()

clock = pygame.time.Clock()
FPS = 60


Screen_W = 1200
Screen_H = 650

screen = pygame.display.set_mode((dimension_w, dimension_h))
pygame.display.set_caption("Game")

def draw_text(text, font, color, x, y):
    img = font.rander(text, True, color)
    screen.blit(x,y)


screen = pygame.display.set_mode((Screen_W, Screen_H))
pygame.display.set_caption("Turn-based RPG")

#background
background = pygame.image.load("Background.png").convert_alpha()
def draw_background():
    screen.blit(background, (0,0))

#text
font = pygame.font.SysFont("Consolas", 64)
font_color = (255,255,255)
def draw_text(text, font, font_color, x, y):
    text_img = font.render(text, True, font_color)
    screen.blit(text_img, (x, y))

#button
class button:
    def __init__(self, x, y, image, scale):
       width = image.get_width()
       height = image.get_height()
       self.image = pygame.transform.scale(image, (width*scale//1, height*scale//1))
       self.rect = self.image.get_rect()
       self.rect.topleft = (x,y)
       self.clicked = False
    def draw(self):
       action = False
       mouse_coor = pygame.mouse.get_pos()
       if self.rect.collidepoint(mouse_coor):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                action = True
            if pygame.mouse.get_pressed()[0] == 0:
                self.clicked = False      
       screen.blit(self.image, (self.rect.x, self.rect.y))
       return action

start_button_img = pygame.image.load("button_start.png")
start_button = button(16, 450+16, start_button_img, 1)
exit_button_img = pygame.image.load("button_exit.png")
exit_button = button(16, 650-16-68, exit_button_img, 1)

#character class
class character:

    def __init__(self, name, max_hp, base_atk, base_def, max_mp, base_spd, crit, x_coor, y_coor):
        self.name = name
        self.role = ""
        self.max_hp = max_hp
        self.current_hp = max_hp
        self.base_atk = base_atk
        self.base_def = base_def
        self.max_mp = max_mp
        self.current_mp = max_mp
        self.base_spd = base_spd
        self.crit = crit
        self.crit_dmg_multiplier = 1.5
        self.dmg_reduction = 1
        self.ult_cost = 10
        self.ult_energy = 0
        self.skill_dmg = 0
        self.skill_hit = 1
        self.atk_buff_multiplier = 1  #stat increase
        self.def_buff_multiplier = 1
        self.spd_buff_multiplier = 1
        self.buff_duration = 0
        self.current_atk = base_atk * self.atk_buff_multiplier
        self.current_def = base_def * self.def_buff_multiplier
        self.current_spd = base_spd * self.spd_buff_multiplier
        self.timer = 1000 / self.current_spd
        self.status = "\t"
        self.statwindow = ""
        self.alive = True
        self.blocking = False
        self.attack = False
        self.charging = False
        self.counter_stance = False
        self.stat_up_bonus = ""
        self.skill_multiplier = 0
        self.mp_cost = 0
        image = pygame.image.load("Warrior_BasicATK.png")
        self.image = pygame.transform.scale(image, (image.get_width()*0.75, image.get_height()*0.75))
        self.rect = self.image.get_rect()
        self.rect.center = (x_coor,y_coor)

    def draw(self):
        screen.blit(self.image, self.rect)

player = character("Name", 10, 3, 3, 10, 2, 5, 42, 604)

#game loop
game_is_running = True
while game_is_running:
    clock.tick(FPS)
    draw_background()
    draw_text("Turn-based game v0.0", font, font_color, 120, 100)
    if start_button.draw():
        print("Start")
    if exit_button.draw():
        game_is_running = False 

    for event in pygame.event.get():
        if event.type == pygame.QUIT:

            game_is_running = False

    pygame.display.update()


           run = False
    pass

pygame.quit()

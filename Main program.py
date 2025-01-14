
import os
from random import randint
from sys import argv
from time import sleep
script_directory = os.path.dirname(os.path.abspath(argv[0])) #change file path to current file so don't have to use file path
os.chdir(script_directory)
import pygame
pygame.init()

Screen_W = 1200 #width
Screen_H = 650 #height

screen = pygame.display.set_mode((Screen_W, Screen_H)) #create screen
pygame.display.set_caption("Main Menu")

clock = pygame.time.Clock()
FPS = 60 #refresh rate

#background
background = pygame.image.load("Misc/Background.png").convert_alpha()
def draw_background():
    screen.blit(background, (0,0)) #draw background at the origin

#text
#set font
title_font = pygame.font.SysFont("Consolas", 64) 
normal_font = pygame.font.SysFont("Consolas", 32)
small_font = pygame.font.SysFont("Consolas", 16)
#set color
black = (0,0,0)
red = (255,0,0)
green = (0,255,0)
blue = (0,0,255)
gold = (255,217,0)

def draw_text(text, font, font_color, x, y): #function to draw text on screen as an image
    text_img = font.render(text, True, font_color)
    screen.blit(text_img, (x, y))

#button 
class button:
    def __init__(self, x, y, image, scale):
        width = image.get_width()
        height = image.get_height()
        self.image = pygame.transform.scale(image, (width*scale//1, height*scale//1)) #scale up button
        self.rect = self.image.get_rect()
        self.rect.topleft = (x,y) #coordinate to draw button at
        self.clicked = False 
    def draw(self):
        screen.blit(self.image, (self.rect.x, self.rect.y))
    def click_check(self):
        action = False #action commited by button varies but they can operate based on a common flag
        mouse_coor = pygame.mouse.get_pos() #finds position of mouse
        if self.rect.collidepoint(mouse_coor): #check if mouse is on the button
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False: #checks if left mouse (indicated by [0]) is clicked (==1)
                self.clicked = True
                action = True
            if pygame.mouse.get_pressed()[0] == 0: #or not clicked(== 0)
                self.clicked = False
        return action #returns result of check to tell the game if button has been clicked

exit_button_img = pygame.image.load("Misc/button_exit.png")
exit_button = button(16, 566, exit_button_img, 1) #exit button
new_game_button_img = pygame.image.load("Misc/button_newg.png")
new_game_button = button(16, 466, new_game_button_img, 1) #start button
#character selection screen buttons:
warrior_icon = button(100, 120, pygame.image.load("Knight sprites/Icon.png"), 1.75)
confirm_button = button(990, 470, pygame.image.load("Misc/button_confirm.png"), 1)
return_to_menu_b = button(990, 560, pygame.image.load("Misc/button_return_menu.png"), 1)

class character:
    def __init__(self, name, max_hp, max_mp, base_atk, base_def, base_spd):
        self.name = name
        self.role = ""
        self.max_hp = max_hp
        self.current_hp = max_hp
        self.max_mp = max_mp
        self.current_mp = max_mp
        self.base_atk = base_atk
        self.base_def = base_def
        self.base_spd = base_spd
        self.crit_multiplier = 1.5
        self.dmg_reduction = 1
        self.sp_cost = 10
        self.current_sp = 0
        self.atk_buff_multiplier = 1  #stat increase
        self.def_buff_multiplier = 1
        self.spd_buff_multiplier = 1
        self.current_atk = base_atk * self.atk_buff_multiplier
        self.current_def = base_def * self.def_buff_multiplier
        self.current_spd = base_spd * self.spd_buff_multiplier
        self.timer = 1000 / self.current_spd
        self.alive = True
        self.blocking = False
        self.img = pygame.image.load("Misc/Border.png") #placeholder image
        self.rect = self.img.get_rect()
    def draw(self, x_pos, y_pos):
        screen.blit(self.img, self.rect)
        self.rect.center = (x_pos,y_pos)
        screen.blit(self.img, (self.rect.x, self.rect.y))

game_is_running = True
class_option = ""
screen_state = "Menu" # what screen should be displayed
while game_is_running: #main game loop
    if screen_state == "Menu": #checks if game is currently on main menu
        draw_background()
        draw_text("Turn-based game v0.0", title_font, black, 120, 100)
        new_game_button.draw()
        exit_button.draw()
        if exit_button.click_check():
            game_is_running = False  
        if new_game_button.click_check():
            screen_state = "Char select"
            pygame.display.set_caption("Character Selection")
    elif screen_state == "Char select": #check if game is currently on character selection
        draw_background()
        draw_text("Character selection", title_font, black, 25, 25)
        warrior_icon.draw()
        confirm_button.draw()
        return_to_menu_b.draw()
        if warrior_icon.click_check():
            class_option = "Warrior" #used to later initialise corresponding class
        if class_option == "Warrior":
            draw_text("Selected: Warrior", normal_font, black, 25, 475)
        if confirm_button.click_check() and class_option != "": #ensures player can't confirm class selection without having selected a class
            screen_state = "Tutorial" #allow change screen to tutorial
            pygame.display.set_caption("Tutorial") #change screen caption to "Tutorial"
        if return_to_menu_b.click_check(): #allow return button to change screen to main menu
            screen_state = "Menu"
            pygame.display.set_caption("Main Menu")
            class_option = "" #reset class option since the player exits the class selection
    else:   
        pass

    for event in pygame.event.get(): #checks input
        if event.type == pygame.QUIT: #click X corner closes the program
            game_is_running = False
    
    pygame.display.update()

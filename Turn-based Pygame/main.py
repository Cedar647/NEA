import os
from random import randint, choice
from sys import argv
from time import sleep
script_directory = os.path.dirname(os.path.abspath(argv[0])) #change file path to current file so don't have to use file path
os.chdir(script_directory)
import pygame
import dice_lib as dc
pygame.init()


Screen_W = 1200 #width
Screen_H = 650 #height

screen = pygame.display.set_mode((Screen_W, Screen_H)) #create screen
pygame.display.set_caption("Main Menu")

clock = pygame.time.Clock()
FPS = 60 #refresh rate

#background
def draw_background():
    screen.blit(pygame.image.load(f"Background/bg_{screen_state}.png").convert_alpha(), (0,0)) #draw background at the origin

#text
#set font
title_font = pygame.font.SysFont("Consolas", 64) 
normal_font = pygame.font.SysFont("Consolas", 24)
small_font = pygame.font.SysFont("Consolas", 16)
#set color
black = (0,0,0)
red = (255,0,0)
green = (0,255,0)
blue = (0,0,255)
gold = (255,217,0)
white = (255,255,255)

def draw_text(text, font, font_color, x, y): #function to draw text on screen as an image
    text_img = font.render(text, True, font_color)
    screen.blit(text_img, (x, y))

def char_select_draw_attributes(): #func to display char attributes during character selection
    draw_text(f"HP:{player. max_hp}", small_font, red, 25, 500)
    draw_text(f"MP:{player.max_mp}", small_font, blue, 125, 500)
    draw_text(f"ATK:{player.base_atk}", small_font, red, 225, 500)
    draw_text(f"DEF:{player.base_def}", small_font, blue, 325, 500)
    draw_text(f"SPD:{player.base_spd}", small_font, green, 425, 500)

dice_display = ""
def char_select_draw_dices(): #display dices during character selection
    global dice_display
    dice1button = dice_button(50,550, player.dicebag[0], 1)
    dice2button = dice_button(160,550, player.dicebag[1], 1)
    dice3button = dice_button(280,550, player.dicebag[2], 1)
    spdicebutton = dice_button(450, 550, player.SPdice, 1)
    dice1button.draw()
    dice2button.draw()
    dice3button.draw()
    spdicebutton.draw()
    if dice1button.click_check():
        dice_display = player.dicebag[0]
    if dice2button.click_check():
        dice_display = player.dicebag[1]
    if dice3button.click_check():
        dice_display = player.dicebag[2]
    if spdicebutton.click_check():
        dice_display = player.SPdice
    if dice_display != "":
        desc_lines = dice_display.desc.split(". ") #split string into list of lines
        draw_text(f"{dice_display.name}", normal_font, black, 625, 465)
        draw_text(f"Type: {dice_display.type}", small_font, black, 625, 500)
        draw_text(f"Cost: {dice_display.cost}", small_font, black, 625, 520)
        for x in range (len(desc_lines)): #display the desc lines one by one
            draw_text(f"{desc_lines[x]}", small_font, black, 625, 550+20*x) #line display goes down by 25px per line
    

#button 
class button:
    def __init__(self, x, y, image, scale):
        width = image.get_width()
        height = image.get_height()
        self.image = pygame.transform.scale(image, (width*scale//1, height*scale//1)) #scale up button if needed
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

class dice_button(button):
    def __init__(self,x, y, dice, scale): #replace attribute image with dice to allow accessing both dice image and type attribute
        self.cost = str(dice.cost)
        image = dice.image #take image of dice 
        super().__init__(x, y, image, scale) #initialize as button
        self.type_icon = pygame.image.load(f"Type_Icons/{dice.type}.png")
        if "SP" in dice.type:
            self.cost_icon = pygame.image.load("Misc/cost_bgSP.png")
        else:
            self.cost_icon = pygame.image.load("Misc/cost_bg.png")
    def draw(self): #overwrites button draw method
        screen.blit(self.image, (self.rect.x, self.rect.y))
        screen.blit(self.type_icon, (self.rect.x - 8, self.rect.y + 64)) #add icon to bottom left corner of dice image
        screen.blit(self.cost_icon, (self.rect.x + 72, self.rect.y + 64)) #add icon to bottom right corner
        if self.cost != 0: #display cost only if there's a cost
            draw_text(self.cost, small_font, black, self.rect.x + 76, self.rect.y + 65)

exit_button = button(16, 566, pygame.image.load("Misc/button_exit.png"), 1) #exit button
new_game_button = button(16, 466, pygame.image.load("Misc/button_newg.png"), 1) #start button
#character selection screen buttons:
warrior_icon = button(100, 120, pygame.image.load("Knight sprites/Icon.png"), 2)
confirm_button = button(990, 470, pygame.image.load("Misc/button_confirm.png"), 1)
return_to_menu_b = button(990, 560, pygame.image.load("Misc/button_return_menu.png"), 1)

class character:
    def __init__(self, max_hp, max_mp, base_atk, base_def, base_spd):
        self.max_hp = max_hp
        self.max_mp = max_mp
        self.base_atk = base_atk
        self.base_def = base_def
        self.base_spd = base_spd

class warrior(character):
    def __init__(self):
        character.__init__(self, 20, 10, 10, 10, 10)
        dice1 = dc.baseATKd6()
        dice2 = dc.baseDEFd6()
        dice3 = dc.baseATKd8()
        self.SPdice = dc.warriorSP()
        self.dicebag = [dice1, dice2, dice3] #starting ability for Warrior

class enemy(character):
    def __init__(self):
        character.__init__(self, 20, 10, 10, 10, 10)
        dice1 = dc.baseATKd6()
        dice2 = dc.baseDEFd6()
        dice3 = dc.baseATKd8()
        self.dicebag = [dice1, dice2, dice3]

game_is_running = True
class_option = ""
screen_state = "Menu" # what screen should be displayed
level = 1
while game_is_running: #main game loop
    if screen_state == "Menu": #checks if game is currently on main menu
        draw_background()
        draw_text("Turn-based game v0.0", title_font, black, 120, 100)
        new_game_button.draw()
        exit_button.draw()
        if exit_button.click_check():
            game_is_running = False  
        if new_game_button.click_check():
            screen_state = "char_select"
            pygame.display.set_caption("Character Selection")
    elif screen_state == "char_select": #check if game is currently on character selection
        draw_background()
        draw_text("Character Selection", title_font, black, 25, 25)
        warrior_icon.draw()
        confirm_button.draw()
        return_to_menu_b.draw()
        if warrior_icon.click_check():
            class_option = "warrior" #used to later initialise corresponding class
        if class_option == "warrior":
            draw_text("Selected: Warrior", normal_font, black, 25, 465)
            draw_text("Abilities:", small_font, black, 25, 525)
            player = warrior()
            char_select_draw_attributes()
            char_select_draw_dices()
        if confirm_button.click_check() and class_option != "": #ensures player can't confirm class selection without having selected a class
            screen_state = "Tutorial" #allow change screen to tutorial
            pygame.display.set_caption("Tutorial") #change screen caption to "Tutorial"
            screen_state = "level"
            pygame.display.set_caption(f"Level {level}")
            sleep(1)
        if return_to_menu_b.click_check(): #allow return button to change screen to main menu
            screen_state = "Menu"
            pygame.display.set_caption("Main Menu")
            class_option = "" #reset class option since the player exits the class selection
    elif screen_state == "level":
        draw_background()
        pass

    for event in pygame.event.get(): #checks input
        if event.type == pygame.QUIT: #click X corner closes the program
            game_is_running = False
    
    pygame.display.update()


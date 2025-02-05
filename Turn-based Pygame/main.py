import os
from random import randint, choice
from math import floor
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

level_msg = []
def level_msg_display():
    for line in range(len(level_msg)):
        draw_text(level_msg[line], small_font, black, 850, 465+20*line)


def char_select_draw_attributes(): #func to display char attributes during character selection
    draw_text(f"HP:{player. max_hp}", small_font, red, 25, 500)
    draw_text(f"MP:{player.max_mp}", small_font, blue, 125, 500)
    draw_text(f"ATK:{player.base_atk}", small_font, red, 225, 500)
    draw_text(f"DEF:{player.base_def}", small_font, blue, 325, 500)
    draw_text(f"SPD:{player.base_spd}", small_font, green, 425, 500)

dice_display = ""
def char_select_draw_dices(): #display dices during character selection
    global dice_display
    dice_list = [dice_button(50,550, player.dicebag[0], 1), dice_button(160,550, player.dicebag[1], 1), dice_button(270,550, player.dicebag[2], 1), dice_button(450, 550, player.SPdice, 1)]
    for x in dice_list:
        x.draw()
        if x.click_check():
            dice_display = x
    if dice_display != "":
        dice_display.info(625, 465) #display dice info when clicked
    
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
        global mouse_coor #mouse coor is global to allow other checks to not use extra mouse coor search
        mouse_coor = pygame.mouse.get_pos() #finds position of mouse
        if self.rect.collidepoint(mouse_coor): #check if mouse is on the button
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False: #checks if left mouse (indicated by [0]) is clicked (==1)
                self.clicked = True
                action = True
            if pygame.mouse.get_pressed()[0] == 0: #or not clicked(== 0)
                self.clicked = False
        return action #returns result of check to tell the game if button has been clicked
    def coor_mod(self,x,y): #allow changing coordinates of the button
        self.rect.topleft = (x,y)

class dice_button(button):
    def __init__(self,x, y, dice, scale): #replace attribute image with dice to allow accessing both dice image and type attribute
        self.dice = dice
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
    def info(self,x,y):
        desc_lines = self.dice.desc.split(". ") #split string into list of lines
        draw_text(f"{self.dice.name}", normal_font, black, x, y)
        draw_text(f"Type: {self.dice.type}", small_font, black, x, y+35)
        draw_text(f"Cost: {self.dice.cost}", small_font, black, x, y+35+20)
        for line in range (len(desc_lines)): #display the desc lines one by one
            draw_text(f"{desc_lines[line]}", small_font, black, x, 550+20*line) #line display goes down by 20px per line

class bar:
    def __init__(self, x, y, attr, current, max):
        self.x = x #coordinates
        self.y = y
        self.name = f"{attr}"
        self.current = current
        self.max = max
        match attr: #color based on attribute type
            case "HP": self.color = red
            case "MP": self.color = blue
            case "SP": self.color = gold
    def draw(self):
        draw_text(self.name, small_font, self.color, self.x, self.y - 5) 
        pygame.draw.rect(screen, black, (self.x+29, self.y-3, 152, 12)) #creates the bar border
        pygame.draw.rect(screen, white, (self.x+30, self.y-2, 150, 10)) #makes the bar appear hollow if it's not fully colored
        pygame.draw.rect(screen, self.color, (self.x+30, self.y-2, round(150*self.current/self.max,0), 10)) #adjust bar to show proportions
        draw_text(f"{self.current}/{self.max}", small_font, self.color,self.x + 188, self.y - 5) #number representation
        

exit_button = button(16, 566, pygame.image.load("Misc/button_exit.png"), 1) #exit button
new_game_button = button(16, 466, pygame.image.load("Misc/button_newg.png"), 1) #start button
#character selection screen buttons:
warrior_icon = button(100, 120, pygame.image.load("Warrior/Icon.png"), 2)
confirm_button = button(990, 470, pygame.image.load("Misc/button_confirm.png"), 1)
return_to_menu_b = button(990, 560, pygame.image.load("Misc/button_return_menu.png"), 1)
use_button = button(0, 590, pygame.image.load("Misc/button_use.png"),1)
absorb_button = button(0, 615, pygame.image.load("Misc/button_absorb.png"),1)
SPuse_button = button(700, 590, pygame.image.load("Misc/button_use.png"),1)

class character:
    def __init__(self, max_hp, max_mp, base_atk, base_def, base_spd,attr_x):
#base attributes
        self.attr_x = attr_x
        self.max_hp = max_hp
        self.current_hp = max_hp - 1
        self.max_mp = max_mp
        self.current_mp = 3
        self.max_sp = max_mp
        self.current_sp = 0
        self.base_atk = base_atk
        self.base_def = base_def
        self.shield = 0
        self.base_spd = base_spd
        self.discard_bag = []
        self.char_class = "Warrior"
        self.name = "Warrior"
        self.alive = True
        self.action = "Idle"
        self.anim_spd = 0.1
#animation
        self.anim_list = []
        for frame in range(7): #idle frames
            image = pygame.image.load(f"{self.char_class}/{self.action}/{frame}.png")
            image = pygame.transform.scale(image, (3*image.get_width(), 3*image.get_height()))
            self.anim_list.append(image)
        self.frame = 0
        self.max_frame = 7
        self.image = self.anim_list[self.frame]
        self.rect = self.image.get_rect()
        self.rect.center = (400,300)
#for dice menu
        self.indexL = 0 #range of dice display. At start always display first 4 dices
        self.indexR = 4
        self.displayinfo = False
        self.selected_diceB = ""
#display attributes on level screen
    def attr_draw(self): 
        for x in [bar(self.attr_x,25,"HP",self.current_hp, self.max_hp),bar(self.attr_x,40,"MP",self.current_mp, self.max_mp),bar(self.attr_x,55,"SP",self.current_sp, self.max_sp)]:
            x.draw()
        draw_text(f"ATK: {self.base_atk}", small_font, red,self.attr_x,75)
        draw_text(f"DEF: {self.base_def}", small_font, blue,self.attr_x,90)
        draw_text(f"SPD: {self.base_spd}", small_font, green,self.attr_x,105)
        draw_text(f"Shield: {self.shield}", small_font, (0,255,255),self.attr_x,125)
#display character sprites
    def animate(self):
        self.image = self.anim_list[floor(self.frame)] #ensures an integer is used for index
        self.frame += self.anim_spd #update new frame once per x ticks. 0.1 => per 10 ticks and 0.2 => per 5 ticks
        if self.frame >= self.max_frame: #loop animation
            self.frame = 0
            if self.action != "Idle":
                self.action = "Idle"
                self.anim_update(7,0.1)
                self.frame = 0
        screen.blit(self.image, self.rect)  
#update animation when action is changed
    def anim_update(self,new_max_frame, new_spd): 
        self.anim_list = []
        self.max_frame = new_max_frame #update new number of frames in action
        self.anim_spd = new_spd
        self.frame = 0
        for frame in range(self.max_frame): #idle frames
            image = pygame.image.load(f"{self.char_class}/{self.action}/{frame}.png")
            image = pygame.transform.scale(image, (3*image.get_width(), 3*image.get_height()))
            self.anim_list.append(image)
#chain any 2 animations together, used for multi-hit ATK
    def anim_chain(self, action_list, new_spd): 
        self.anim_list = []
        for x in action_list: #for every action, adds all of its frame to the list
            self.action = x
            for frame in range(6): #every animation for chaining is 6 frames. will update to be dynamic
                image = pygame.image.load(f"{self.char_class}/{self.action}/{frame}.png")
                image = pygame.transform.scale(image, (3*image.get_width(), 3*image.get_height()))
                self.anim_list.append(image)
        self.max_frame = len(self.anim_list) #number of frames
        self.anim_spd = new_spd #set new anim spd
        self.frame = 0 #reset frames to 0
#absorb dice
    def absorb(self):
        msg = [] #messages to be displayed
        dice = self.selected_diceB.dice #get the selected dice (actual dice instead of the button)
        self.current_mp += dice.cost #increase MP by dice cost
        msg.append(f"{dice.name} absorbed for {dice.cost} MP") #add line to list for display
        if self.current_mp > self.max_mp: #extra MP is converted into SP
            overflow = self.current_mp - self.max_mp
            self.current_sp += overflow
            self.current_mp = self.max_mp
            msg.append(f"{overflow} overflowed MP converted into SP")
            if self.current_sp > self.max_sp: #extra SP is lost
                level_msg.append(f"{self.current_sp - self.max_sp} SP lost")
                self.current_sp = self.max_sp
        self.discard_bag.append(dice) #remove absorbed dice from list of available dice and put it in discard zone/pile/list whatever
        self.dicebag.remove(dice)
        return msg #return the lines for display
#use DEF dice 
    def gain_shield(self):
        msg = [] #messages to be displayed
        dice = self.selected_diceB.dice #get the selected dice (actual dice instead of the button)
        res = dice.roll() 
        gain_shield = res[0]*(self.base_def*5/100) #every 1 def increase efficiency of shield gain by 5%
        self.shield += gain_shield #adds shield
        msg.append(f"{dice.name} rolled a {res}") #messages
        msg.append(f"{gain_shield} shields gained")
        self.discard_bag.append(dice) #remove used dice from list of available dice and put it in discard zone/pile/list whatever
        self.dicebag.remove(dice)
        return msg #return the lines for display
    def regen(self):
        msg = [] #messages to be displayed
        dice = self.selected_diceB.dice #get the selected dice (actual dice instead of the button)
        res = dice.roll() 
        self.current_hp += res[0] #increase HP by roll result
        msg.append(f"{dice.name} rolled a {res}") #messages
        if self.current_hp > self.max_hp: #extra HP is lost
            overflow = self.current_hp - self.max_hp
            healed = res[0] - overflow
            self.current_hp = self.max_hp
            msg.append(f"{healed} HP regenerated")
            msg.append(f"{overflow} overflowed HP lost")
        else:
            msg.append(f"{res} HP regenerated")
        self.discard_bag.append(dice) #remove absorbed dice from list of available dice and put it in discard zone/pile/list whatever
        self.dicebag.remove(dice)
        return msg #return the lines for display
#attack dice
    def attack(self, target):
        msg = [] #messages to be displayed
        target_response = []
        dice = self.selected_diceB.dice #get the selected dice (actual dice instead of the button)
        res = dice.roll() #roll dice
        for baseDMG in res: #multi hit requires recalculation of damage
            target_response.append(target.take_dmg())
            msg.append(f"{dice.name} rolled a {baseDMG}")
            DMG = baseDMG*(self.base_atk*5/100) #every 1 ATK increases DMG dealt by 5%
            if baseDMG in dice.crit_val:
                DMG *= 1.5 #crit hits increases DMG dealt by 1.5x
                msg.append("Critical Hit dealt")
            if target.shield > 0: #if target has shield then apply shield reduction before HP reduction
                if DMG > target.shield: #if DMG dealt is more than shield then deal the remaining to current HP
                    reduced = target.shield #all shield reduces corresponding DMG
                    target.shield = 0 #all shield is lost since it's less than DMG dealt
                else: #if DMG dealt is <= shield then reduce shield by DMG dealt
                    reduced = DMG #all DMG clocked by shield and reduced by corresponding amount
                    target.shield -= DMG
                DMG -= reduced #DMG is reduced
                msg.append(f"{reduced} DMG blocked by {target.name}'s Shield") #message
            target.current_hp -= DMG #reduce target's HP by DMG dealt
            msg.append(f"{self.name} deals {DMG} DMG to {target.name}")
            msg.append(" ")
        target.anim_chain(target_response, 0.1)
        self.discard_bag.append(dice) #remove used dice from list of available dice and put it in discard zone/pile/list whatever
        self.dicebag.remove(dice)
        return msg
    def take_dmg(self):
        if self.shield > 0:
            self.action = "DEF" #with shield, block attack, without shield, get hurt
            self.anim_update(6,0.1)
        else:
            self.action = "Hurt"
            self.anim_update(6,0.1)
        return self.action
#dice menu
    def dice_menu(self,leftB,rightB,already_displayed):
        dicebag_menu = []
        for index in range (self.indexL,self.indexR):
            dicebag_menu.append(dice_button(100+120*(index-self.indexL),500, self.dicebag[index], 1)) #add the dices in range to list
            #x-self.indexL ensures dice draw is drawn relative to the first dice in this list, no matter where it is in dicebag
            #if dices drawn are 3,4,5,6 then dice 3 is treated as dice 0 as when drawn dices 0,1,2,3 
            dicebag_menu[index-self.indexL].draw() #draw added dice
            if dicebag_menu[index-self.indexL].click_check():
                self.selected_diceB = dicebag_menu[index-self.indexL]
                use_button.coor_mod(100+120*(index-self.indexL),590)
                absorb_button.coor_mod(100+120*(index-self.indexL), 615)
                #make use button always drawn under selected dice
            if self.selected_diceB!= "" and already_displayed == False: #if a dice was selected and its info has not been displayed
                self.selected_diceB.info(850,465) #display info
                global level_msg
                level_msg = []
                already_displayed = True #if info has been displayed then drawing it again in the same loop is not required
                #use button may move outside screen if its assigned dice is not displayed due to menu navigation
                if use_button.rect.topleft[0] >= 100 and use_button.rect.topleft[0] < 580 and self.selected_diceB != self.SPdice_button: #if the button is of a displayed dice
                    use_button.draw() #display use/absorb button
                    if self.selected_diceB.dice.cost > 0:
                        absorb_button.draw()
            if index >= len(self.dicebag)-1: #if there's less than 4 dices then stop drawing at the last dice
                break
        self.SPdice_button.draw() #draw SP dice
        if self.SPdice_button.click_check(): #separate click check for SP dice since it's separated from normal dices
            self.selected_diceB = self.SPdice_button
        if self.selected_diceB == self.SPdice_button: #draw use button for SP dice if it is selected
            SPuse_button.draw()
        if self.indexL != 0: #only draw left arrow if game is not displaying the very first dice already
            leftB.draw()
            if leftB.click_check(): #menu change when Left arrow/Right arrow is clicked
                self.indexL -= 1
                self.indexR -= 1
                use_button.coor_mod(use_button.rect.topleft[0]+120,590) #if use/absorb button is displayed then it should be moved to
                absorb_button.coor_mod(absorb_button.rect.topleft[0]+120, 615) #under the corresponding dice after they're moved
        if self.indexR < len(self.dicebag): #only draw right arrow if game is not displaying very last dice
            rightB.draw()
            if rightB.click_check():
                self.indexL += 1
                self.indexR += 1
                use_button.coor_mod(use_button.rect.topleft[0]-120,590)
                absorb_button.coor_mod(absorb_button.rect.topleft[0]-120, 615)


class warrior(character):
    def __init__(self):
        character.__init__(self, 20, 20, 20, 20, 10, 25)
        self.SPdice = dc.warriorSP()
        self.SPdice_button = dice_button(700, 500, self.SPdice, 1)
        self.dicebag = [dc.doubleATKd6(), dc.baseDEFd6(), dc.baseRegend6(),dc.doubleATKd6(), dc.baseATKd20()] #starting ability for Warrior        

class enemy(character):
    def __init__(self):
        character.__init__(self, 20, 10, 10, 10, 10,825)
        self.dicebag = [dc.baseATKd6(), dc.baseDEFd6(), dc.baseATKd8()]
        self.rect.center = (800,300)
        self.shield = 3

game_is_running = True
class_option = ""
screen_state = "Menu" # what screen should be displayed
level = 1
leftB = button(50, 515, pygame.image.load("Misc/left.png"),1.5) #arrow buttons for main level loop. Outside loop to prevent reset by redeclare
rightB = button(570, 515, pygame.image.load("Misc/right.png"),1.5)

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
            opp = enemy()
            sleep(1)
        if return_to_menu_b.click_check(): #allow return button to change screen to main menu
            screen_state = "Menu"
            pygame.display.set_caption("Main Menu")
            class_option = "" #reset class option since the player exits the class selection
    elif screen_state == "level":
        draw_background()
        for x in [player,opp]:
            x.attr_draw()
            x.animate()
        player.dice_menu(leftB,rightB,False) #include dice selection step
        #perform dice action
        if absorb_button.click_check() and player.selected_diceB.dice.cost > 0:
            level_msg = player.absorb() #function returns the messages for display
            player.selected_diceB = "" #reset selected dice since it has been used
        if use_button.click_check():
            skill = player.selected_diceB.dice #actual dice used, not the button
            if skill.cost > player.current_mp: #if insufficient MP then do not use dice
                level_msg.append("Insufficient MP")
            else:
                match skill.type:
                    case "DEF": level_msg = player.gain_shield() #if DEF dice used then gives player shield
                    case "Regen": level_msg = player.regen() #if Regen dice used then heal
                    case "ATK": #if ATK dice used then deals DMG
                        if skill.copies == 1: #if dice is single then play random atk anim
                            player.action = f"ATK {randint(1,3)}" #random atk animation
                            player.anim_update(6, 0.1)
                        else: #if dice is multihit (currently goes up to 2 max) 
                            action_list = ["ATK 1", "ATK 2", "ATK 3"] 
                            action_list.pop(randint(1,3)-1) #remove random animation from list so that 2 is played (1+2 or 1+3 or 2+3)
                            player.anim_chain(action_list, 0.1)
                        level_msg = player.attack(opp)
                    case _: pass #temporary ignore all other types
                player.current_mp -= skill.cost #reduce MP equal to cost
            player.selected_diceB = "" #reset selected dice since it has been used
        level_msg_display() #display messages
    for event in pygame.event.get(): #checks input
        if event.type == pygame.QUIT: #click X corner closes the program
            game_is_running = False
    
    pygame.display.update()

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
def draw_background(scale = 1):
    image = pygame.image.load(f"Background/bg_{screen_state}.png")
    image = pygame.transform.scale(image, (1200*scale,650*scale))
    screen.blit(image.convert_alpha(), (0,0)) #draw background at the origin

#text
#set font
title_font = pygame.font.SysFont("Consolas", 64) 
normal_font = pygame.font.SysFont("Consolas", 24)
small_font = pygame.font.SysFont("Consolas", 16)
mini_font = pygame.font.SysFont("Consolas",15)
#set color
black = (0,0,0)
red = (255,0,0)
green = (0,255,0)
blue = (0,0,255)
gold = (255,217,0)
white = (255,255,255)
purple = (255,0,255)

def draw_text(text, font, font_color, x, y): #function to draw text on screen as an image
    text_img = font.render(text, True, font_color)
    screen.blit(text_img, (x, y))

level_msg = []
def level_msg_display(x = 850, y = 465):
    to_red = ["DMG","Critical","Hit","HP","ATK"] #words that will have red color
    to_blue = ["Shield","MP", "DEF"] #words that will have blue color
    to_gold = ["SP"]
    to_green = ["Regen","SPD"]
    to_purple = ["Essence","Essences"]
    for line in range(len(level_msg)): #checks line to be displayed
        words = level_msg[line].split() #split line into words
        for word in words: #for every word, checks if it needs to be colored different
            if word in to_red: color = (255,0,0)
            elif word in to_blue: color = (0,0,255)
            elif word in to_gold: color = (255,217,0)
            elif word in to_green: color = (0,255,0)
            elif word in to_purple: color = (255,0,255)
            else: #normal text is black
                color = (0,0,0)
            draw_text(word, mini_font, color, x, y) #display word
            x = x + 8*len(word) + 12 #adjust coordinate to draw next word next to the previous word
            #move right by 7px per letter in word, +11px for spaces
        (x,y) = (850,y+18) #at next line, return to left side and goes down by 18px

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
        self.rank_icon = pygame.image.load("Type_Icons/Rank.png")
        if "SP" in dice.type:
            self.cost_icon = pygame.image.load("Type_Icons/cost_bgSP.png")
        else:
            self.cost_icon = pygame.image.load("Type_Icons/cost_bg.png")
#overwrites button draw method
    def draw(self): 
        screen.blit(self.image, (self.rect.x, self.rect.y))
        screen.blit(self.type_icon, (self.rect.x - 8, self.rect.y + 64)) #add icon to bottom left corner of dice image
        screen.blit(self.cost_icon, (self.rect.x + 72, self.rect.y + 64)) #add icon to bottom right corner
        screen.blit(self.rank_icon, (self.rect.x + 72, self.rect.y + 1)) #add rank to top right corner
        draw_text(f"{self.dice.rank}", small_font, black, self.rect.x + 91, self.rect.y) #rank number
        if self.cost != 0: #display cost only if there's a cost
            draw_text(self.cost, small_font, black, self.rect.x + 76, self.rect.y + 65)
#display dice information
    def info(self,x,y):
#split string into list of lines
        desc_lines = self.dice.desc.split(". ") 
        draw_text(f"{self.dice.name}", normal_font, black, x, y)
        draw_text(f"Type: {self.dice.type}", small_font, black, x, y+35)
        draw_text(f"Rank: {self.dice.rank}", small_font, black, x, y+55)
        draw_text(f"Cost: {self.dice.cost}", small_font, black, x, y+75)
        for line in range (len(desc_lines)): #display the desc lines one by one
            draw_text(f"{desc_lines[line]}", small_font, black, x, 570+20*line) #line display goes down by 20px per line
#upgrade attributes
class attr_button():
    def __init__(self, x, y, attr, attr_val): #init button
        self.txt = attr
        self.val = attr_val
        self.x = x
        self.y = y
        match attr: #coloring
            case "HP": self.color = (255,0,0)
            case "MP": self.color = (0,0,255)
            case "ATK": self.color = (255,0,0)
            case "DEF": self.color = (0,0,255)
            case "SPD": self.color = (0,255,0)
        self.plus = button(x-30, y-2, pygame.image.load("Button/button_plus.png"),1) #button to allow increasing attr
    def draw(self): #draw attribute text and +/- button
        draw_text(f"{self.txt}:",small_font,self.color,self.x,self.y)
        draw_text(str(self.val),small_font,self.color,self.x+13*len(self.txt),self.y)#adaptive to HP/MP (2 letters) and ATK/DEF/SPD (3)
        self.plus.draw()
    def click_check(self): #increase/attribute
        global level_msg
        if self.plus.click_check(): #if button is clicked
            if player.essence >= 20: #cost 20 Essences per upgrade. If Essences is sufficient then perform upgrade
                self.val += 1
                player.essence -= 20
                level_msg = [f"-20 Essences , + 1 {self.txt}"] #for message display
                return True #click caused an upgrade
            else: #insufficient Essences
                level_msg = ["Insufficient Essences"]
        return False #click didn't causes upgrade

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
        draw_text(f"{round(self.current,2)}/{round(self.max,2)}", small_font, self.color,self.x + 188, self.y - 5) #number representation
        
class cycle_button: #has a L/R arrow to cycle through values
    def __init__(self, prompt, values,x,y):
        self.index = 0
        self.prompt = prompt
        self.values = values #list of values for display
        self.left = button(x-20,y,pygame.image.load("Button/left.png"),0.75)
        self.right = button(x+50,y,pygame.image.load("Button/right.png"),0.75)
        (self.x,self.y) = (x,y)
        self.displayed = self.values[self.index] #value being displayed. Assigned to attribute for access outside
    def draw(self): #display buttons
        draw_text(f"{self.prompt}",small_font,black,self.x-25-(9*len(self.prompt)),self.y+2) #vary prompt position based on its length
        draw_text(self.values[self.index], mini_font, black,self.x,self.y+2) #value being displayed
        self.displayed = self.values[self.index]
        self.left.draw() #L/R arrow buttons
        self.right.draw()
    def click_check(self): #checks if any of its button is clicked
        if self.right.click_check():
            self.index += 1 #if right arrow is clicked then move to next value
            if self.index >= len(self.values):
                self.index = 0 #return to first value if the end is reached
        if self.left.click_check(): #if left arrow is clicked then move to prev value
            self.index -= 1
            if self.index < 0: #goes to last value if the start is reached
                self.index = len(self.values)-1

exit_button = button(16, 566, pygame.image.load("Button/button_exit.png"), 1) #exit button
exit_button_lost = button(438, 400, pygame.image.load("Button/button_exit.png"), 1)
new_game_button = button(16, 466, pygame.image.load("Button/button_newg.png"), 1) #start button
#character selection screen buttons:
warrior_icon = button(100, 120, pygame.image.load("Warrior/Icon.png"), 2)
confirm_button = button(990, 470, pygame.image.load("Button/button_confirm.png"), 1)
return_to_menu_b = button(990, 560, pygame.image.load("Button/button_return_menu.png"), 1)
use_button = button(0, 590, pygame.image.load("Button/button_use.png"),1)
absorb_button = button(0, 615, pygame.image.load("Button/button_absorb.png"),1)
SPuse_button = button(700, 590, pygame.image.load("Button/button_use.png"),1)
retry_button = button(630,400,pygame.image.load("Button/button_retry.png"),1)
rest_button = button(500,300,pygame.image.load("Button/button_rest.png"),1)
upgrade_button = button(750,300,pygame.image.load("Button/button_upgrade.png"),1)
next_button = button(1000,400,pygame.image.load("Button/button_next.png"),1)
forge_button = button(323,590,pygame.image.load("Button/button_forge.png"),0.75)

class character:
    def __init__(self, max_hp, max_mp, base_atk, base_def, base_spd,attr_x):
#base attributes
        self.attr_x = attr_x
        self.max_hp = max_hp
        self.current_hp = max_hp
        self.max_mp = max_mp
        self.current_mp = max_mp
        self.max_sp = max_mp
        self.current_sp = 0
        self.base_atk = base_atk
        self.base_def = base_def
        self.shield = 0
        self.base_spd = base_spd
        self.AV = 10000/self.base_spd #determines action order
        self.char_class = ""
        self.alive = True
        self.action = "Idle"
        self.anim_spd = 0.5
        self.discard_bag = [] #discard pile
        self.essence = 0 #for upgrade/dice forge
#animation
        self.anim_list = []
        self.frame = 0
        self.max_frame = 7
#for dice menu
        self.indexL = 0 #range of dice display. At start always display first 4 dices
        self.indexR = 4
        self.displayinfo = False
        self.selected_diceB = ""
#display attributes on level screen
    def attr_draw(self): 
        for x in [bar(self.attr_x,25,"HP",self.current_hp, self.max_hp),bar(self.attr_x,40,"MP",self.current_mp, self.max_mp),bar(self.attr_x,55,"SP",self.current_sp, self.max_sp)]:
            x.draw()
        draw_text(f"ATK: {round(self.base_atk,2)}", small_font, red,self.attr_x,75)
        draw_text(f"DEF: {round(self.base_def,2)}", small_font, blue,self.attr_x,90)
        draw_text(f"SPD: {round(self.base_spd,2)}", small_font, green,self.attr_x,105)
        draw_text(f"Shield: {round(self.shield,2)}", small_font, (0,255,255),self.attr_x,125)
#display character sprites
    def animate(self):
        self.image = self.anim_list[floor(self.frame)] #ensures an integer is used for index
        self.frame += self.anim_spd #update new frame once per x ticks. 0.1 => per 10 ticks and 0.2 => per 5 ticks
        if self.frame >= self.max_frame: #loop animation
            self.frame = 0
            if not self.alive: #keeps character dead if they're dead
                self.anim_update(["Dead"],[1])
            elif self.action != "Idle": #after doing a non-idle anim, returns to idle
                self.anim_update(["Idle"],[self.idle_frames])
        screen.blit(self.image, self.rect)  
#update animation when action is changed. allow chaining animations
    def anim_update(self,action_list,frame_list, new_spd=0.5, chain=False):
        if not chain: #determines if animation to be played is reset since death animation may override hurt/block animation
            self.anim_list = []
        index = 0
        for action in action_list: #for every action, adds all of its frame to the list
            self.action = action
            for frame in range(frame_list[index]): #for every frame of action, add and scale up
                image = pygame.image.load(f"{self.char_class}/{self.action}/{frame}.png")
                image = pygame.transform.scale(image, (self.img_scale*image.get_width(), self.img_scale*image.get_height()))
                self.anim_list.append(image)
            index += 1
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
        dice = self.selected_diceB.dice #get the selected dice (actual dice instead of the button)
        msg = self.conversion(dice.cost) #messages to be displayed
        res = dice.roll() 
        gain_shield = res[0]*(self.base_def*5/100) #every 1 def increase efficiency of shield gain by 5%
        self.shield += gain_shield #adds shield
        msg.append(f"{dice.name} rolled a {res}") #messages
        msg.append(f"{gain_shield} Shield gained")
        self.discard_bag.append(dice) #remove used dice from list of available dice and put it in discard zone/pile/list whatever
        self.dicebag.remove(dice)
        return msg #return the lines for display
#heal
    def regen(self):
        msg = [] #messages to be displayed
        dice = self.selected_diceB.dice #get the selected dice (actual dice instead of the button)
        res = dice.roll() 
        regen = res[0]*(self.base_def*5/100)#increase HP by roll result. Regen is affected by DEF
        msg.append(f"{dice.name} rolled a {res}") #messages
        if self.current_hp + regen > self.max_hp: #extra HP is lost
            overflow = self.current_hp + regen - self.max_hp
            regen = (self.max_hp - self.current_hp)
            self.current_hp = self.max_hp
            msg.append(f"{regen} HP regenerated")
            msg.append(f"{overflow} overflowed HP lost")
        else:
            self.current_hp += regen
            msg.append(f"{regen} HP regenerated")
        self.discard_bag.append(dice) #remove absorbed dice from list of available dice and put it in discard zone/pile/list whatever
        self.dicebag.remove(dice)
        return msg #return the lines for display
#attack dice
    def attack(self, target):
        target_response = []
        dice = self.selected_diceB.dice #get the selected dice (actual dice instead of the button)
        msg = self.conversion(dice.cost) #messages to be displayed
        res = dice.roll() #roll dice
        for baseDMG in res: #multi hit requires recalculation of damage
            target_response.append(target.take_dmg())
            msg.append(f"{dice.name} rolled a {baseDMG}")
            DMG = baseDMG*(self.base_atk*5/100) #every 1 ATK increases DMG dealt by 5%
            if baseDMG-dice.rank in dice.crit_val:
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
                msg.append(f"{round(reduced,2)} DMG blocked by {target.name}'s Shield") #message
            target.current_hp -= DMG #reduce target's HP by DMG dealt
            msg.append(f"{self.name} deals {round(DMG,2)} DMG to {target.name}")
            msg.append(" ")
        target.anim_update(target_response,[target.hurt_frames,target.hurt_frames],0.5)
        if "SP" not in dice.type: #only remove dice if it's not SP dice
            self.discard_bag.append(dice) #remove used dice from list of available dice and put it in discard zone/pile/list whatever
            self.dicebag.remove(dice)
        return msg
#damaged animation
    def take_dmg(self):
        if self.shield > 0:
            self.action = "DEF" #with shield, block attack, without shield, get hurt
        else:
            self.action = "Hurt"
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
#convert mp to sp
    def conversion(self,cost):
        self.current_sp += cost #gain SP equal to dice cost
        if self.current_sp > self.max_sp: #if SP overflows
            trueSP = cost - self.current_sp - self.max_sp #real amount of SP gained
            self.current_sp = self.max_sp #if SP overflows then set it to the cap
        else:
            trueSP = cost #if no overflow then SP gained is the cost
        return [f"-{cost} MP | +{trueSP} SP"] #information
    
class warrior(character):
    def __init__(self):
        character.__init__(self, 20, 20, 20, 20, 10,25)
        self.name = "Player"
        self.char_class = "Warrior"
        self.SPdice = dc.warriorSP()
        self.SPdice_button = dice_button(700, 500, self.SPdice, 1)
        self.dicebag = [dc.baseATKd6(), dc.baseDEFd6(), dc.baseATKd8()] #starting ability for Warrior
        self.idle_frames = 7 #frames in corresponding animation
        self.death_frames = 12
        self.hurt_frames = 6
        self.img_scale = 3
        self.atk_anims = ["ATK 1", "ATK 2", "ATK 3"] #atk animations
        self.anim_update(["Idle"], [self.idle_frames], 0.5) #idle
        self.image = self.anim_list[0] #get image so that game can position the character correctly
        self.rect = self.image.get_rect()
        self.rect.center = (400,290)
    def attack(self, target):
        dice = self.selected_diceB.dice #get the selected dice (actual dice instead of the button)
        if dice.type == "SP-ATK":
            opp.shield = 0 #Warrior SP dice can delete all shields
        return super().attack(target)

class enemy(character):
    def __init__(self):
        character.__init__(self, 20, 20, 20, 20, 10,825)
        self.char_class = "Orc"
        self.name = "Enemy"
        self.dicebag = [dc.baseATKd6(), dc.baseDEFd6()]
        self.idle_frames = 6 #frames in corresponding animation
        self.death_frames = 4
        self.hurt_frames = 4
        self.img_scale = 4
        self.atk_anims = ["ATK 1", "ATK 2"] #atk animations
        self.anim_update(["Idle"], [self.idle_frames], 0.5)
        self.image = self.anim_list[0] #get image so that game can position the character correctly
        self.rect = self.image.get_rect()
        self.rect.center = (800,315)
#action select during level
    def select_dice(self):
        self.selected_diceB = ""
        preferAction = "Use"
        preferType = ["ATK","DEF","Regen"]
        if self.current_hp < self.max_hp*0.3: #if HP is low then prioritize DEF or Regen
            if self.shield <= 6*(player.base_atk*5/100): #if Shield is low then prioritize DEF
                preferType = ["DEF","Regen","ATK"]
            else: #if Shield is high but HP is low then prioritize Regen
                preferType = ["Regen","DEF","ATK"]
        elif self.current_mp <= 3: #if MP is low then prioritize Absorbing dices
            preferAction = "Absorb"
        else: #if at safe conditions then ATK
            pass
        if preferAction == "Absorb": #if absorption required 
            for dice in self.dicebag: #checks every dice
                if dice.type != preferType[0] and dice.cost > 0: #if it's not most prioritized then absorb it
                    self.selected_diceB = dice_button(0,0,dice,1)
            #if no dice has been selected for absorption due to all being of most prioritized type or not having cost
            if self.selected_diceB == "":
                for dice in self.dicebag: #checks why no dices have been chosen
                    if dice.cost != 0: #if any dice has a cost but not chosen then its typing must've been most prioritized
                        self.selected_diceB = dice_button(0,0,dice,1) #ignore typing and absorb it
            #after that if there's no dice for absorption then there must've been no valid target
            if self.selected_diceB == "": #(which also means all other dices have 0 cost)
                preferAction = "Use" #switch to use mode
                self.selected_diceB = dice_button(0,0,dice,1)
        else: #if absorption is not required then use dice
            for order in preferType:
                for dice in self.dicebag: #check every dice
                    if dice.type == order and dice.cost <= self.current_mp:
                        #if dice type is prioritized and its cost can be sufficed
                        self.selected_diceB = dice_button(0,0,dice,1) #select it for use
                        break #no need to check further
                if self.selected_diceB != "": #break a second time
                    break
            #if all check fails then the dices must have had too high cost (since all typing priority has been checked)
            if self.selected_diceB == "":
                for dice in self.dicebag:
                    if dice.cost > 0: #in which case absorbs the first dice with a cost
                        self.selected_diceB = dice_button(0,0,dice,1)  
                        preferAction = "Absorb"
        return preferAction           
#stronger for higher levels
    def upgrade(self,currentLV):
    #every 5 levels, add random new dice or increase an existing dice's rank by 1
        if currentLV % 5 == 0:
            c = randint(1,2)
            if c == 1: #create new dice
                possible_sides = [4,6,8,10,12,20]
                sides = possible_sides[currentLV//10] #can get D4 at lv<10, increase to D6 at 10<=lv<20, D8 at 20<=lv<30
                sides = [i for i in range(1,sides+1)]                
                randtype = choice(["ATK", "DEF", "Regen"])
                randdice = dc.unmadeDice("", "", sides, randtype, 1, 0, sides[-1], 0)
                randdice.update(sides, randtype, 0, 1)
                self.dicebag.append(randdice)
            else: #randomly increases a rank of a dice by 1
                choice(self.dicebag).rank += 1
    #if no new dice was added, increases 3 random attributes by 1:
        else:
            for up in range(3):
                match randint(1,5):
                    case 1: self.max_hp += 1
                    case 2: self.max_mp += 1
                    case 3: self.base_atk += 1
                    case 4: self.base_def += 1
                    case 5: self.base_spd += 1


#calculate turn order
def turn_order(player,opp):
    if player.AV <= opp.AV:
        opp.AV -= player.AV
        player.AV = 10000/player.base_spd
        return [player, opp, True]
    else:
        player.AV -= opp.AV
        opp.AV = 10000/opp.base_spd
        return [opp, player, True]
#use dice
def dice_use_phase(turnP, target):
    global action_pending
    level_msg = []
    skill = turnP.selected_diceB.dice #actual dice used, not the button
    if skill.cost > player.current_mp and "SP" not in skill.type: #if insufficient MP then do not use dice
        level_msg.append("Insufficient MP")
    elif skill.cost > player.current_sp and skill.type == "SP-ATK": #as above but SP dice
        level_msg.append("Insufficient SP")
    else:
        match skill.type:
            case "DEF": 
                level_msg = turnP.gain_shield() #if DEF dice used then gives player shield
                turnP.current_mp -= skill.cost #reduce MP equal to cost
            case "Regen": 
                level_msg = turnP.regen()
                turnP.current_mp -= skill.cost #reduce MP equal to cost
            case "ATK":
                if skill.copies == 1: #if dice is single then play random atk anim
                    turnP.action = [choice(turnP.atk_anims)] #random atk animation from preset list that each class has
                    turnP.anim_update(turnP.action,[6])
                else: #if dice is multihit (currently goes up to 2 max) 
                    action_list = turnP.atk_anims #list of atk animations
                    if len(action_list) != 2: #if there's more than 2 possible animations to be played
                        action_list.pop(randint(1,3)-1) #remove random animation from list so that 2 is played (1+2 or 1+3 or 2+3)
                        turnP.anim_update(action_list, [6,6])
                level_msg = turnP.attack(target)
                if target.current_hp <= 0:
                    target.anim_update(["Death"], [target.death_frames],chain = True) #if HP < 0 then play death animation AFTER hurt/block
                    target.alive = False
                turnP.current_mp -= skill.cost #reduce MP equal to cost
            case "SP-ATK":
                action_list = ["SP-ATK"] #SP dice plays custom animation
                turnP.anim_update(action_list, [6])
                level_msg = turnP.attack(target)
                if target.current_hp <= 0:
                    target.anim_update(["Death"], [target.death_frames],chain = True) #if HP < 0 then play death animation AFTER hurt/block
                    target.alive = False
            case _: pass #temporary ignore all other types
        action_pending = False
    turnP.selected_diceB = "" #reset selected dice since it has been used
    return level_msg
#reset variables for next level
def next_level():
    opp.current_hp = opp.max_hp #reset opp status since it died last level
    opp.alive = True
    opp.anim_update(["Idle"], [opp.idle_frames]) #reset animation
    opp.action = "Idle"
    opp.AV = 10000/opp.base_spd #reset turn calc
    player.AV = 10000/player.base_spd
    opp.dicebag = opp.dicebag + opp.discard_bag

game_is_running = True
class_option = ""
screen_state = "Menu" # what screen should be displayed
level = 1
action_pending = False #prevents game from attempting turn order calculation if it's still a side's turn
turnCD = 60 #time between end of a turn and start of next turn
leftB = button(50, 515, pygame.image.load("Button/left.png"),1.5) #arrow buttons for main level loop. Outside loop to prevent reset by redeclare
rightB = button(570, 515, pygame.image.load("Button/right.png"),1.5)

while game_is_running: #main game loop
    clock.tick(FPS)
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
    elif screen_state == "level": #main level
        draw_background()
        for x in [player,opp]: #draw character and their attributes
            x.attr_draw()
            x.animate()
        #perform dice action
        if not action_pending and turnCD == 60: #calculate turn order if no side is having an action and it's not turn change
            if not player.alive: #if player died
                screen_state = "Lost"
                pygame.display.set_caption("Lost") #change screen caption
            elif not opp.alive: #if enemy died
                screen_state = "Won"
                player.essence += 60
                pygame.display.set_caption("Won")
            else: #if neither side died then perform turn calculation as normal
                [turnP, target, action_pending] = turn_order(player,opp)
                level_msg = [f"{turnP.name}'s turn"]
                turnCD = 0 #reset turn CD since a turn started
        if turnCD == 0: #perform turn if it's not in CD and not extended(both side is still alive)
            if len(turnP.dicebag) == 0: #if dicebag is empty then reset it and auto skips turn
                (turnP.dicebag, turnP.discard_bag) = (turnP.discard_bag, turnP.dicebag)
                level_msg = [f"{turnP.name} is out of dice","Perform reset", f"{turnP.name}'s turn skipped"]
                action_pending = False
            elif turnP == player: #player-only actions
                player.dice_menu(leftB,rightB,False) #include dice selection step
                if absorb_button.click_check() and player.selected_diceB.dice.cost > 0: #dice absorption
                    level_msg = player.absorb() #function returns the messages for display
                    player.selected_diceB = "" #reset selected dice since it has been used
                    action_pending = False
                    (player.indexL, player.indexR) = (0,4) #reset dice menu display
                if use_button.click_check(): #use dice
                    level_msg = dice_use_phase(turnP, target)
                    (player.indexL, player.indexR) = (0,4) #reset dice menu display
                if player.selected_diceB == player.SPdice_button and SPuse_button.click_check(): #use SP dice
                    level_msg = dice_use_phase(turnP, target)
                    (player.indexL, player.indexR) = (0,4) #reset dice menu display
                    player.current_sp = 0
            else: #opponent-only actions
                action = opp.select_dice()
                if action == "Absorb": #opponent absorbs dice
                    level_msg = opp.absorb()
                    action_pending = False
                else: #opponent uses dice
                    level_msg = dice_use_phase(opp, player)
                    action_pending = False                
        level_msg_display() #display messages
        if not action_pending: #check turn state and increment CD is no player's having a turn 
            turnCD += 1
    elif screen_state == "Lost": #if player lost then draw retry screen
        screen.fill(white)
        draw_text("You Lost", title_font, black, 460, 100)
        retry_button.draw()
        exit_button_lost.draw()
        if exit_button_lost.click_check(): #if exit then exit
            game_is_running = False
        if retry_button.click_check(): #if retry then return to character selection
            screen_state = "char_select"
            pygame.display.set_caption("Character Selection")
            action_pending = False
            turnCD = 60
            level_msg = []
            class_option = "" 
    elif screen_state == "Won":
        screen.fill(white) #empty screen
        draw_text(f"Level {level} won", title_font, black, 25, 25)
        draw_text("Select option to progress to the next level", small_font, black, 25, 85)
        rest_button.draw()
        upgrade_button.draw()
        if rest_button.click_check(): 
            (player.current_hp,player.current_mp) = (player.max_hp,player.max_mp) #reset HP/MP
            screen_state = "level" #go level screen since heal doesn't need separate screen, it just happens
            level += 1 #next level
            opp.upgrade(level)
            pygame.display.set_caption(f"Level {level}") #screen caption
            next_level() #reset class attributes for next level
            action_pending = False
            turnCD = 60
            level_msg = []
            player.dicebag = player.dicebag + player.discard_bag #reset dices
            player.discard_bag = []
        if upgrade_button.click_check(): 
            screen_state = "Upgrade" #go upgrade screen
            HP = attr_button(800,145,"HP",player.max_hp)
            MP = attr_button(800,175,"MP",player.max_mp)
            ATK = attr_button(800,205,"ATK",player.base_atk)
            DEF = attr_button(800,235,"DEF",player.base_def)
            SPD = attr_button(800,265,"SPD",player.base_spd)
            unmade_dice = dc.unmadeDice("Forging...", "Properties uncarved", [1,2,3,4,5,6], "ATK", "1", "6", [6])
            level_msg = "" #reset msg display
            sides_bar_buttons = cycle_button("Number of sides:",["4","6","8","10","12","20"],200,525) #for cycling through when selecting sides/types
            type_bar_buttons = cycle_button("Type:",["ATK","DEF","Regen"],200,550)
            rank_bar_buttons = cycle_button("Rank:", [str(i) for i in range (0,13)],200,575)
    elif screen_state == "Upgrade":
#upgrade
        draw_background()
        pygame.display.set_caption("Upgrade")
        draw_text("Upgrade", title_font, black, 25, 25) #title
        draw_text(f"{player.char_class}", normal_font,black, 283, 122) #class info
        draw_text("Owned dices:",normal_font,black,25,240)
        (tx,ty) = (50,275) #display all dices player owns
        list = player.dicebag+player.discard_bag
        for ind in range(len(player.dicebag + player.discard_bag)):
            dice = list[ind]
            tempbutton = dice_button(tx, ty, dice, 1)
            tempbutton.draw()
            tx += 110
            if ind == 4:#5 dices per row
                ty += 90
                tx = 50
        draw_text(f"{player.essence}",small_font,black, 880, 98) #amount of essence
        warrior_icon.draw() #character icon
        for a in [HP,MP,ATK,DEF,SPD]: #upgrade buttons
            a.draw()
            if a.click_check(): #if button click causes an upgrade
                match a.txt: #actually raise attribute instead of just display
                    case "HP": (player.max_hp,player.current_hp) = (player.max_hp+1, player.current_hp+1)
                    case "ATK": player.base_atk += 1
                    case "DEF": player.base_def += 1
                    case "SPD": player.base_spd += 1
                    case "MP": (player.max_mp, player.current_mp) = (player.max_mp+1, player.current_mp+1)
#forge
        unmade_dice_button = dice_button(320, 500, unmade_dice,1) #for forging dices
        unmade_dice_button.draw() #display dice button
        unmade_dice_button.info(825,470) #display dice info
        for b in [sides_bar_buttons,type_bar_buttons,rank_bar_buttons]:
            b.draw()
            b.click_check()
        newSides = [str(i) for i in range(1,int(sides_bar_buttons.displayed)+1)] #takes number of sides, convert to list of side values
        newType = type_bar_buttons.displayed
        newRank = rank_bar_buttons.displayed
        essence_cost = unmade_dice.update(newSides,newType,newRank,1) #update displayed dice
        draw_text("Essence", small_font, purple, 425, 520) #essence cost of dice
        draw_text(f"cost: {essence_cost}",small_font, black, 496, 520)
        forge_button.draw()
        if forge_button.click_check(): #if attempt to forge
            if player.essence >= essence_cost: #if sufficient essence then add dice or upgrade existing   
                newDice = dc.dice(unmade_dice.name,unmade_dice.desc,unmade_dice.sides,unmade_dice.type,1,unmade_dice.cost,unmade_dice.crit)       
                for inpos in player.dicebag + player.discard_bag: #checks both dicebag and discard
                    if newDice.name == inpos.name and newDice.rank == inpos.rank and inpos.rank < 12: 
                        #if forged dice is already present and has same rank then rank dice up instead of adding to bag
                        inpos.rank += 1
                        level_msg = [f"- {essence_cost} Essences , {unmade_dice.name} upgraded to rank {inpos.rank}"]
                        player.essence -= essence_cost
                        upgraded = True #a dice has been upgraded
                        break #upgrades 1 dice only in case the player has 2 identical dices somehow
                    else: upgraded = False
                if not upgraded: #if dice doesn't already exist (no upgrade occurred) then add to dicebag
                    if len(player.dicebag) < 10: #limit the player's number of dices to 10 if a dice is added
                        player.dicebag.append(newDice)
                        level_msg = [f"-{essence_cost} Essences , {unmade_dice.name} Rank {unmade_dice.rank} added"]
                        player.essence -= essence_cost
                    else:
                        level_msg = ["Too many dices!"]
            else: #if insufficient essence then ignore
                level_msg = ["Insufficient Essences"]
        level_msg_display(800,300)
        next_button.draw()
        if next_button.click_check(): #click to go next level
            screen_state = "level"
            action_pending = False #reset global variables to allow new level
            turnCD = 60
            level_msg = []
            level += 1
            opp.upgrade(level)
            next_level()
            pygame.display.set_caption(f"Level {level}")
    for event in pygame.event.get(): #checks input
        if event.type == pygame.QUIT: #click X corner closes the program
            game_is_running = False
    clock.tick(FPS)
    pygame.display.update()

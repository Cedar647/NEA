import os
from random import randint, choice
from sys import argv
script_directory = os.path.dirname(os.path.abspath(argv[0])) #change file path to current file so don't have to use file path
os.chdir(script_directory)
import pygame
pygame.init()

class dice:
    def __init__(self, name, desc, sides, type, copies, cost, crit, rank = 0):
        self.name = name #dice name
        self.desc = desc #dice description
        self.sides = sides #list of possible rolls of the dice. Allows implementing non-standard die
        self.sides_number = len(sides) #determines how many faces the die has
        self.type = type #determine dice type
        self.copies = int(copies) #determine number of rolls per dice
        self.cost = int(cost) #determines cost of dice
        self.crit_val = crit
        self.rank = int(rank)
        if "SP" in self.type:
            self.image = pygame.image.load(f"Dices/{copies}D{self.sides_number}SP.png")
        else:   
            self.image = pygame.image.load(f"Dices/{copies}D{self.sides_number}.png")
    def roll(self):#roll the dice
        roll = [int(choice(self.sides)) for i in range(self.copies)] #roll dice a number of time = copies
        return [r+int(self.rank) for r in roll] #increase roll result by rank
    
class unmadeDice(dice):
    def __init__(self, name, desc, sides, type, copies, cost, crit, rank = 0):
        super().__init__(name, desc, sides, type, copies, cost, crit, rank = 0)
    def update(self, sides, type, rank,copies): #update dice info
        match len(sides): #generate name prefix and cost
            case 4:
                name_pre = "Weak"
                cost = 0
            case 6:
                name_pre = "Basic"
                cost = 0
            case 8:
                name_pre = "Good"
                cost = 1
            case 10:
                name_pre = "Enhanced"
                cost = 2
            case 12:
                name_pre = "Strong"
                cost = 2
            case 20:
                name_pre = "Extreme"
                cost = 3
        match type:
            case "ATK": #generate name and description
                name_suff = "ATK"
                self.desc = f"Deal 1->{len(sides)} DMG randomly"
            case "DEF":
                name_suff = "Shield"
                self.desc = f"Gain 1->{len(sides)} Shield randomly"
            case "Regen":
                name_suff = "Heal"
                self.desc = f"Gain 1->{len(sides)} HP randomly"
        self.name = name_pre + " " + name_suff #name
        self.cost = cost #cost
        self.sides = sides #sides
        self.sides_number = len(self.sides) #number of sides
        self.image = pygame.image.load(f"Dices/{self.copies}D{self.sides_number}.png") #image
        self.type = type #type
        self.crit = [self.sides[-1]] #crit region
        self.rank = int(rank)
        essence_cost = (self.sides_number*10+self.rank*20)*copies #calculate essence cost. 10 per face x number of copies, +20 per rank
        return essence_cost
        

class baseATKd6(dice):
    def __init__(self):
        super().__init__("Basic ATK", "Deal 1->6 DMG randomly", [1,2,3,4,5,6], "ATK", 1, 0, [6])

class doubleATKd6(dice):
    def __init__(self):
        super().__init__("Double ATK", "Deal 1->6 DMG randomly twice", [1,2,3,4,5,6], "ATK", 2, 2, [6])

class baseDEFd6(dice):
    def __init__(self):
        super().__init__("Basic Shield", "Gain 1-6 Shield(s) randomly", [1,2,3,4,5,6], "DEF", 1, 0,[0])

class baseRegend6(dice):
    def __init__(self):
        super().__init__("Basic Regen", "Gain 1-6 HP randomly", [1,2,3,4,5,6], "Regen", 1, 1,[0])

class baseATKd8(dice):
    def __init__(self):
        super().__init__("Good ATK", "Deal 1->8 DMG randomly", [1,2,3,4,5,6,7,8], "ATK", 1, 1, [8])

class baseATKd10(dice):
    def __init__(self):
        super().__init__("Enhanced ATK", "Deal 1->10 DMG randomly", [i for i in range(1,11)], "ATK", 1, 1, [8])

class baseATKd12(dice):
    def __init__(self):
        super().__init__("Strong ATK", "Deal 1->12 DMG randomly", [1,2,3,4,5,6,7,8,9,10,11,12], "ATK", 1, 2, [12])

class baseATKd20(dice):
    def __init__(self):
        super().__init__("Extreme ATK", "Deal 1->20 DMG randomly", [x for x in range (1,21)], "ATK", 1, 3, [20])

class baseATKd4(dice):
    def __init__(self):
        super().__init__("Weak ATK", "Deal 1->4 DMG randomly", [1,2,3,4], "ATK", 1, 0, [4])

class warriorSP(dice):
    def __init__(self):
        super().__init__("SP Slash", "Remove enemy Shield. Then, deal 1->20 DMG randomly", [x for x in range (1, 21)], "SP-ATK", 1,20, [20])
    def roll(self):#roll the dice
        return [choice(self.sides)]
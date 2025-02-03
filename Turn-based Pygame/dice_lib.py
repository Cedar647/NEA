import os
from random import randint, choice
from sys import argv
script_directory = os.path.dirname(os.path.abspath(argv[0])) #change file path to current file so don't have to use file path
os.chdir(script_directory)
import pygame
pygame.init()

class dice:
    def __init__(self, name, desc, sides, type, copies, cost):
        self.name = name #dice name
        self.desc = desc #dice description
        self.sides = sides #list of possible rolls of the dice. Allows implementing non-standard die
        self.sides_number = len(sides) #determines how many faces the die has
        self.type = type #determine dice type
        self.copies = copies #determine number of rolls per dice
        self.cost = cost #determines cost of dice
        if "SP" in self.type:
            self.image = pygame.image.load(f"Dices/{copies}D{self.sides_number}SP.png")
        else:   
            self.image = pygame.image.load(f"Dices/{copies}D{self.sides_number}.png")
    def roll(self):#roll the dice
        return [choice(self.sides) for i in range(self.copies)] #roll dice a number of time = copies

class baseATKd6(dice):
    def __init__(self):
        super().__init__("Standard ATK D6", "Equal chance to roll 1->6. Deal result as DMG", [1,2,3,4,5,6], "ATK", 1, 0)

class baseATKd8(dice):
    def __init__(self):
        super().__init__("Standard ATK D8", "Equal chance to roll 1->8. Deal result as DMG", [1,2,3,4,5,6,7,8], "ATK", 1, 1)

class baseATKd12(dice):
    def __init__(self):
        super().__init__("Standard ATK D12", "Equal chance to roll 1->12. Deal result as DMG", [1,2,3,4,5,6,7,8,9,10,11,12], "ATK", 1, 1)

class baseATKd20(dice):
    def __init__(self):
        super().__init__("Standard ATK D20", "Equal chance to roll 1->20. Deal result as DMG", [x for x in range (1,21)], "ATK", 1, 2)

class baseATKd4(dice):
    def __init__(self):
        super().__init__("Standard ATK D4", "Equal chance to roll 1->4. Deal result as DMG", [1,2,3,4], "ATK", 1, 1)

class baseDEFd6(dice):
    def __init__(self):
        super().__init__("Standard DEF D6", "Equal chance to roll 1->6. Gain roll result as Shield", [1,2,3,4,5,6], "DEF", 1, 0)

class warriorSP(dice):
    def __init__(self):
        super().__init__("Warrior SP ATK D20", "Equal chance to roll 1->20. Deal result as DMG. Always CRIT.", [x for x in range (1, 21)], "SP-ATK", 1, 20)

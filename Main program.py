import pygame
pygame.init()

dimension_w = 1200 #screen width
dimension_h = 800 #screen height

screen = pygame.display.set_mode((dimension_w, dimension_h))
pygame.display.set_caption("Game")

def draw_text(text, font, color, x, y):
    img = font.rander(text, True, color)
    screen.blit(x,y)

run = True
while run:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
           run = False
    pass
pygame.quit()

import pygame

SCREEN_WITDH = 800
SCREEN_HEIGHT = 480

screen = pygame.display.set_mode((SCREEN_WITDH, SCREEN_HEIGHT))
pygame.display.set_caption('Main Menu')

def menu():
    background_img_menu = pygame.image.load('Space-side-scroller/Images/background_menu.jpg')
    background_img_menu = pygame.transform.scale(background_img_menu, (900, 600))

    while True:
        screen.blit(background_img_menu, (0,0))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.display.quit()
                exit()
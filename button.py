import pygame

#This class draws the button on the screen and figures out if it has been pressed
class Button():
    def __init__(self, x, y, image, scale):
        width = image.get_width()
        height = image.get_height()
        self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.clicked = False

    def draw(self, surface):
        #This variable determines if it has been pressed or not
        action = False


        pos = pygame.mouse.get_pos()

        #Checks for collision
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                action = True
        
        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        #prints the button on the sreen
        surface.blit(self.image, (self.rect.x, self.rect.y))

        return action
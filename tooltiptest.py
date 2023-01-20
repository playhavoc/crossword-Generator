import pygame
pygame.init()

class Button():
    def __init__(self, x, y, sx, sy, bcolour, fbcolour, font, fontsize, fcolour, text, tiptext):
        self.rect = pygame.Rect(x, y, sx, sy)
        self.bcolour = bcolour
        self.fbcolour = fbcolour
        self.fcolour = fcolour
        self.fontsize = fontsize
        self.current = False
        self.buttonf = pygame.font.SysFont(font, fontsize)
        self.textsurface = self.buttonf.render(text, False, self.fcolour)
        self.tiptextsurface = self.buttonf.render(tiptext, False, (0, 0, 0), (255, 255, 0))
        
    def showButton(self, display):
        color = self.fbcolour if self.current else self.bcolour
        pygame.draw.rect(display, color, self.rect)
        display.blit(self.textsurface, self.textsurface.get_rect(center = self.rect.center))

    def showTip(self, display):
        if self.current:
            mouse_pos = pygame.mouse.get_pos()
            display.blit(self.tiptextsurface, (mouse_pos[0]+16, mouse_pos[1]))

    def focusCheck(self, mousepos, mouseclick):
        self.current = self.rect.collidepoint(mousepos)
        return mouseclick if self.current else True
                
screen = pygame.display.set_mode((400, 600))
clock = pygame.time.Clock()
font = pygame.font.Font('freesansbold.ttf', 32)
shopButton = Button(125, 500, 150, 50, "black", "red", "arial", 20, "white", "Shop", "Enter the shop")

done = False
while not done:    
    clock.tick(60)
    for event in pygame.event.get():
        if(event.type == pygame.QUIT):
            done = True
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_click = True

    mouse_pos = pygame.mouse.get_pos()
    mouse_click = False
    screen2button = shopButton.focusCheck(mouse_pos, mouse_click)

    screen.fill((255, 255, 255))
    shopButton.showButton(screen)
    shopButton.showTip(screen)
    pygame.display.update()

pygame.quit()
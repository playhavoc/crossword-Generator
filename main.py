import pygame
import button
import generation
import dropdown
pygame.font.init()
pygame.init()


#Variables
WIDTH, HEIGHT = 750, 750
FPS = 30
BLUE = 174, 198, 207
GREEN = 179, 203, 185
BLACK = 0, 0, 0
WHITE = 255, 255, 255
GREY = 128, 128, 128
PASSIVE_BLUE = 111, 171, 194
ACTIVE_BLUE = 160, 206, 224


#Main window initialsation
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Crossword Generator')

#Loading the button graphics
teacher_graphic = pygame.image.load('Assets/teacherbutton.png')
student_graphic = pygame.image.load('Assets/studentbutton.png')
generateGraphic = pygame.image.load('Assets/GenerateCrosswordButton.png')
explenationGraphic = pygame.image.load('Assets/explenation.png')
saveGraphic = pygame.image.load('Assets/save.png')
loadGraphic = pygame.image.load('Assets/load.png')
helpGraphic = pygame.image.load('Assets/HelpPage.png')
openningGraphic = pygame.image.load('Assets/OpennigScreen.png')
teacher1Graphic = pygame.image.load('Assets/TeacherPage1.png')
teacher2Graphic = pygame.image.load('Assets/TeacherPage2.png')
student1Graphic = pygame.image.load('Assets/StudentPage1.png')
student2Graphic = pygame.image.load('Assets/StudentPage2.png')
helpGraphicButton = pygame.image.load('Assets/helpButton.png')
backGraphic = pygame.image.load('Assets/backButton.png')
savedGraphic = pygame.image.load('Assets/savedPage.png')
quitGraphic = pygame.image.load('Assets/quit.png')
homeGraphic = pygame.image.load('Assets/home.png')
home2Graphic = pygame.image.load('Assets/home2.png')
home3Graphic = pygame.image.load('Assets/alwaysHome.png')
ViewGridButtonGraphic = pygame.image.load('Assets/ViewGridButton.png')
FileLocatedGraphic = pygame.image.load('Assets/FileLocatedPage.png')
errorSreen1 = pygame.image.load('Assets/errorScreen1.png')


#Creating the buttons
teacher_button = button.Button(238, 310, teacher_graphic, 1)
student_button = button.Button(-125, 310, student_graphic, 1)
student2_button = button.Button(100, 400, student_graphic, 2)
generateButton = button.Button(63, 597, generateGraphic, 1)
saveButton = button.Button(559, 661, saveGraphic, 1)
loadButton = button.Button(221, 536, loadGraphic, 1)
helpButton = button.Button(267, 443, helpGraphicButton, 1)
backButton = button.Button(256, 622, backGraphic, 1)
homeButton = button.Button(224, 177, homeGraphic, 1)
quitButton = button.Button(224, 415, quitGraphic, 1)
home2Button = button.Button(543, 661, home2Graphic, 1)
home3Button = button.Button(679, 11, home3Graphic, 1)
viewButton = button.Button(63, 449, ViewGridButtonGraphic, 1)
homeButton4 = button.Button(224, 564, homeGraphic, 1)

#collects the names of the grids form the database
def dropNames():
    return generation.fetchCrosswordNames()
#Creating drop down menus
COLOR_LIST_INACTIVE = 148, 66, 67
COLOR_LIST_ACTIVE = 234, 115, 117


#FONTS
font = pygame.font.SysFont('RocknRoll One', 92)
font2 = pygame.font.SysFont('RocknRoll One', 42)
img = font.render('Crossy-Word', True, BLACK)
cwName = font2.render(generation.inputedNames, True, BLACK)

# This fuction runs the first/main window
def main():
    clock = pygame.time.Clock()
    run = True
    WIN.fill(GREEN)
    WIN.blit(openningGraphic, (0, 0))
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            #Allows me to quit the window
            if event.type == pygame.QUIT:
                run = False

        #Makes the buttons work
        if teacher_button.draw(WIN):
            teacher()
        if student_button.draw(WIN):
            student()

        pygame.display.update()
    pygame.quit()

#This fuction takes care of the teacher window
def teacher():
    clock = pygame.time.Clock()
    run = True
    clock.tick(FPS)
    WIN.fill(GREEN)
    WIN.blit(teacher1Graphic, (0, 0))
    grid = []
    #what keeps the screen on the screen
    while run:

        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            #displays help if F1 key is pressed
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F1:
                    helpPage()
            
        #runs the genertion algo
        if generateButton.draw(WIN):
            grid, possible = generation.newGeneration()
            if possible == False:
                errorScreen()
            else:
                fileLocated(grid)

        #The buttons
        if helpButton.draw(WIN):
            helpPage()
        if home3Button.draw(WIN):
            main()
        pygame.display.update()
    pygame.quit()

#This fuction takes care of the teacher window
def helpPage():
    clock = pygame.time.Clock()
    run = True
    clock.tick(FPS)
    WIN.blit(helpGraphic, (0, 0))
    while run:

        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        #Allows us to return to the generation
        if backButton.draw(WIN):
            teacher()

        pygame.display.update()
    pygame.quit()

#This function takes care of the students window
def student():
    clock = pygame.time.Clock()
    run = True

    # displays the drop down menu
    list2 = dropdown.DropDown(
        [PASSIVE_BLUE, ACTIVE_BLUE],
        [COLOR_LIST_INACTIVE, COLOR_LIST_ACTIVE],
        221, 294, 308, 68, 
        pygame.font.SysFont(None, 30), 
        "Select Grid", dropNames())

    while run:
        event_list = pygame.event.get()
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            
            #the buttons
            if loadButton.draw(WIN):
                grid = generation.loadFromDatabase()
                studentDisplay(grid)
            if home3Button.draw(WIN):
                main()

        selected_option = list2.update(event_list)
        if selected_option >= 0:
            list2.main = list2.options[selected_option]
            generation.inputedNames = list2.main

        WIN.blit(student1Graphic, (0,0))
        list2.draw(WIN)
        pygame.display.flip()
    pygame.quit()

#This function takes care of the create crossword window
def teacherDisplay(grid):
    clock = pygame.time.Clock()
    run = True
    WIN.blit(teacher2Graphic, (0,0))
    user_text = ''
    input_rect = pygame.Rect(558, 582, 179, 63)
    # color_active stores color(lightskyblue3) which
    # gets active when input box is clicked by user
    color_active = ACTIVE_BLUE

    # color_passive store color(chartreuse4) which is
    # color of input box.
    color_passive = PASSIVE_BLUE
    color = (255, 255, 255)

    active = False
    
    #Runs the cube function
    generation.cubes(grid)

    #Runs the clues function
    generation.printClues()

    #Main while loop
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            #Allows me to quit the window
            if event.type == pygame.QUIT:
                run = False
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if input_rect.collidepoint(event.pos):
                    active = True
                else:
                    active = False

            if home3Button.draw(WIN):
                main()

            if event.type == pygame.KEYDOWN and active == True:

			    # Check for backspace
                if event.key == pygame.K_BACKSPACE:

				    # get text input from 0 to -1 i.e. end.
                    user_text = user_text[:-1]

			    # Unicode standard is used for string
			    # formation
                else:
                    user_text += event.unicode
        
        if active:
            color = color_active
        else:
            color = color_passive
		
	    # draw rectangle and argument passed which should
	    # be on screen
        pygame.draw.rect(WIN, color, input_rect)

        text_surface = font2.render(user_text, True, (0 ,0 ,0))
	
	    # render at position stated in arguments
        WIN.blit(text_surface, (input_rect.x+10, input_rect.y+15))
	
	    # set width of textfield so that text cannot get
	    # outside of user's text input
        input_rect.w = max(179, text_surface.get_width()+10)

        generation.name = user_text

        if saveButton.draw(WIN) and user_text != '':
            generation.updateDatabase()
            saved()


        pygame.display.update()
    pygame.quit()

#This function takes care of the student window on the teachers side
def studentDisplay(grid):
    clock = pygame.time.Clock()
    run = True
    clock.tick(FPS)
    WIN.fill(GREEN)
    WIN.blit(student2Graphic, (0,0))
    cwName = font2.render(generation.inputedNames, True, BLACK)
    #Runs the cube function
    generation.cubes(grid)

    #Runs the clues function
    generation.printClues()
    while run:
        
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            #buttons
            if home2Button.draw(WIN):
                main()
            if home3Button.draw(WIN):
                main()
        WIN.blit(cwName, (558, 582))
        pygame.display.update()
    pygame.quit()

#Displays once the grid has succefully been saved
def saved():
    clock = pygame.time.Clock()
    run = True
    clock.tick(FPS)
    WIN.fill(GREEN)
    WIN.blit(savedGraphic, (0,0))
    while run:
        
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        
        if homeButton.draw(WIN):
            main()
        if quitButton.draw(WIN):
            run = False
        WIN.blit(cwName, (558, 582))
        pygame.display.update()
    pygame.quit()

#Displays once the file has been located and can run the generation
def fileLocated(grid):
    clock = pygame.time.Clock()
    run = True
    clock.tick(FPS)
    WIN.fill(GREEN)
    WIN.blit(FileLocatedGraphic, (0,0))
    while run:
        
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        
        if viewButton.draw(WIN):
            teacherDisplay(grid)

        pygame.display.update()
    pygame.quit()  

#displays when it can't create a grid from the given words
def errorScreen():
    clock = pygame.time.Clock()
    run = True
    clock.tick(FPS)
    WIN.fill(GREEN)
    WIN.blit(errorSreen1, (0,0))
    while run:
        
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        
        if homeButton4.draw(WIN):
            main()

        pygame.display.update()
    pygame.quit()   
#This allows the program to start running
if __name__ == '__main__':
    main()

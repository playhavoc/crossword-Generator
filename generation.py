import re
from textwrap import fill
from turtle import clear
import pygame
import csv
import sqlite3

data = []

#reads the text file
def readFromFile():
    try: 
        with open('crossyword.txt') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            for row in csv_reader:
                temp = []
                temp.append(row[0])
                temp.append(row[1])
                data.append(temp)
    except:
        print('ERROR: No file found in the directory')
    finally:
        print('Success')


#array for the 6 words
chosenWords = []
#array for the 6 clues
chosenClues = []
#array for the row of the previous horizontal word
previousROW = [0]
#array for the col of the previous vertical word
previousCOL = [0]
#The 2D array of the CWID, words and clues
records = []
#database records
databaseRecords = []
#Name of the crossword
name = ''
#inputed names
inputedNames = ''
#the crosswordID
cwID = '1'


grid = []

def fillGrid(grid):
    for i in range(19):
        grid.append(['#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#'])

#Sorts out the words in alfabetical order
def bubbleSort(data):
    swap = True
    count = 0
    temp = 0
    while swap == True and count < len(data):
        swap = False
        for i in range(len(data) - 1):
            if len(data[i][0]) < len(data[i + 1][0]):
                temp = data[i]
                data[i] = data [i + 1]
                data[i + 1] = temp
                swap = True
        count += 1
    
    return data

#inserts the first and longest word into the grid
def insertFirstWord():
    firstWord = data[0][0]
    for i in range(len(firstWord)):
        grid[0][i] = firstWord[i]
    chosenWords.append(firstWord)
    chosenClues.append(data[0][1])
    previousROW.append(0)
    data.pop(0)

#Replaces the '#' with the correct letter in that position
def printWordsOnGrid(bo, rot):
    word = chosenWords[-1]
    if rot == True: # Horizontal
        row = previousROW[-1]
        col = previousCOL[-1]
        for i in range(len(word)):
            bo[row][col] = word[i]
            col += 1
    else: # Vertical
        col = previousCOL[-1]
        row = previousROW[-1]
        for i in range(len(word)):
            bo[row][col] = word[i]
            row += 1


#Will look at the current words first letter and the previous word
#It then scans the previous word for a letter in common
def findCommonLetter(currentWord, rot):
    previousWord = chosenWords[-1]
    for i in range(2, len(previousWord)):
        if currentWord[0] == previousWord[i]:
            if rot == False:
                temp = previousCOL[-1] + i
                previousCOL.append(temp)
            else:
                temp = previousROW[-1] + i
                previousROW.append(temp)
            return True
    return False

#the main procedure, looks at the next word and sends it to a function   
def generation(data):

    bubbleSort(data)
    #Inserts the first word
    insertFirstWord()

    rotation = False
    wordsPlaced = 1
    check = False
    counter1 = 0
    possible = True
    while wordsPlaced < 6 and check == False:
        for i in range(len(data)):
            currentWord = data[i][0]
            currentClue = data[i][1]
            successfull = findCommonLetter(currentWord, rotation)
            if successfull == True: # If found a common letter
                wordsPlaced += 1
                chosenWords.append(currentWord)
                chosenClues.append(currentClue)
                printWordsOnGrid(grid, rotation)
                #Sets the rotation for the next word
                if rotation == True:
                    rotation = False
                else:
                    rotation = True
                #Break the for loop if we have enough words
                if wordsPlaced >= 6:
                    break
        #This is to stop the program looking for words infintly
        if counter1 > 20:
            check = True
            print('ERROR : Words are NOT going to fit, tried 20 Times')
            print('PLEASE INPUT DIFFERENT OR MORE WORDS')
            possible = False
        else:
            check = False
            counter1 += 1
    
    return grid, possible

#Used when i created the tables
def createTables():
    myCursor.execute(
        '''CREATE TABLE IF NOT EXISTS names(
            crosswordID CHAR(2) PRIMARY KEY,
            name VARCHAR(20) NOT NULL,
            );'''
    )

    myCursor.execute(
        '''CREATE TABLE IF NOT EXISTS grid(
            crosswordID CHAR(2) PRIMARY KEY,
            words VARCHAR(7) NOT NULL,
            clues VARCHAR(50) NOT NULL,
            );'''
    )

#fetch the crossword id from the database
def fetchCrosswordID():
    tempID = []
    ID = ''
    select = 'SELECT crosswordID FROM names WHERE name = (?)'
    myCursor.execute(select, [(name)])

    tempID.append(myCursor.fetchall())
    ID = tempID[0][0][0]
    return ID

#fetch the crossword name from the database
def fetchCrosswordNames():
    temp = []
    temp2 = []
    select = 'SELECT name FROM names'
    myCursor.execute(select)
    temp = myCursor.fetchall()
    for i in range(len(temp)):
        temp2.append(temp[i][0])
    return temp2

#creates a 2d array which will allow me to input data into the database
def createRecord():
    for i in range(len(chosenClues)):
        temp = []
        temp.append(str(fetchCrosswordID()))
        temp.append(chosenWords[i])
        temp.append(chosenClues[i])
        records.append(temp)

#updates the database with the chosen words
def updateDatabaseGrid():

    createRecord()

    insert = 'INSERT INTO grid (crosswordID, words, clues) VALUES(?,?,?)'
    myCursor.executemany(insert, records)
    
    db.commit()

#inserts the chosen name for a grid into the database
def updateDatabaseNames():
    insertName = 'INSERT INTO names (name) VALUES(?)'
    myCursor.execute(insertName, [(name)]) 

    db.commit()

#fetches the cross word names
def fetchData(records):
    select = 'SELECT words, clues FROM grid, names WHERE grid.crosswordID = names.crosswordID AND names.name = (?)'
    myCursor.execute(select, [(inputedNames)])

    records = myCursor.fetchall()
    return records

#updates which words have been chosen
def updateChosenWords(databaseWords):
    for i in range(len(databaseWords)):
        data.append(databaseWords[i])

with sqlite3.connect('crossyword.db') as db:
    myCursor = db.cursor()


pygame.font.init()
pygame.init()

#Variables
WIDTH, HEIGHT = 750, 750
FPS = 60

BLUE = 174, 198, 207
GREEN = 179, 203, 185
BLACK = 0, 0, 0
WHITE = 255, 255, 255

#Main window initialsation
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Crossword Generator')

#Fonts
mainFont = pygame.font.SysFont('RocknRoll One', 24)
mainFontBig = pygame.font.SysFont('RocknRoll One', 90)

#Graphics
HORIZONTAL = mainFont.render('HORIZONTAL', True, BLACK)
VERTICAL = mainFont.render('VERTICAL', True, BLACK)

#Cubes for each letter
def cubes(grid1):
    for i in range(len(grid1)):
        for j in range(len(grid1[i])):
            if grid1[i][j] != '#':
                pygame.draw.rect(WIN, BLACK , pygame.Rect((40 * j) + 30 , (40 *i) + 30, 40, 40),  2)


#Print the clues onto the screen
def printClues():
    #The buffer is the distance between the clues
    bufferHorizontal = 30
    bufferVertical = 30
    for i in range(len(chosenClues)):
        #This separates the horizontal clues and the vertical ones
        if i % 2 == 0:
            img = mainFont.render(chosenClues[i], True, BLACK)
            WIN.blit(img, (9, 605 + bufferHorizontal))
            bufferHorizontal += 30
        else:
            img = mainFont.render(chosenClues[i], True, BLACK)
            WIN.blit(img, (297, 605 + bufferVertical))
            bufferVertical += 30
    
records1 = []
# This fuction runs the first/main window
def main():
    clock = pygame.time.Clock()
    run = True
    WIN.fill(WHITE)
    
    #Runs the cube function
    cubes(grid)

    #Runs the clues function
    printClues()

    #Main while loop
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            #Allows me to quit the window
            if event.type == pygame.QUIT:
                run = False

        pygame.display.update()
    pygame.quit()

#clears the data so that the process can start again
def clearData():
    previousCOL.clear()
    previousROW.clear()
    previousROW.append(0)
    previousCOL.append(0)
    data.clear()
    chosenClues.clear()
    chosenWords.clear()
    grid.clear()
    fillGrid(grid)

#runs on the teacher side of the application
def newGeneration():
    clearData()
    temp = []
    readFromFile()
    temp = generation(data)
    return temp

#updates the database
def updateDatabase():
    updateDatabaseNames()
    updateDatabaseGrid()

#Rund on the student side of the app
def loadFromDatabase():
    clearData()
    temp = []
    databaseData = fetchData(databaseRecords)
    updateChosenWords(databaseData)
    temp, temp2 = generation(data)
    return temp

#This allows the program to start running
if __name__ == '__main__':
    #newGeneration()
    loadFromDatabase()
    main()
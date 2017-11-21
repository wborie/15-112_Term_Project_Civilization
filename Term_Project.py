############################################################
"""
Functionality:
1. Clicking on an empty tile causes nothing to happen.

2. Clicking on a tile with a unit on it highlights that tile and allows
you to move that unit. If (after clicking on the unit) you want to move
it, press 'm' and a display of possible moves will be brought up. You can
move to any of the tiles that are newly highlighted (currently in blue) by
clicking on the desired tile. Illegal moves (such as moving outside the
board, onto another unit, or through another unit) will not be executed.

3. Clicking on units will bring up a little box on the bottom-left corner
of the window, the first line of information in that box displays the type
of that unit, the second line displays the health of that unit.

4. If you are currently selecting a "settler" unit (a settler unit is
highlighted), pressing 'p' will place a city on the current tile of that
settler unit, destroying that unit in the process. A city is for now just
a specially colored tile (a lot more to be done here).

5. Clicking on a tile with a city will bring up a little box on the
bottom-right corner of the window, which displays the name of that city and
it's production. You can choose production by highlighting a city and
using the '1' '2' '3' and '4' keys.

6. Pressing 'r' will end the current turn and start a new turn. New turns
reset the movement ability of each unit and spawn (and move) enemy units.

7. Pressing 'a' while one of your units is highlighted will display the
tiles that can be attacked that turn. Clicking on a tile after pressing
'a' while a unit is selected will
cause the selected unit to attack the unit on the clicked tile.

Modules: I'm just using Tkinter (standard) so there shouldn't be any other
modules to install.

Attribution: I used Tkinter for drawing and displaying images

Features:
- My hybrid hexagonal doubly linked list/2-D list representation for my board
is definitely the accomplishment I'm most proud of. It took a lot of designing
to come up with the best way to create the grid
- Board creation (not in the original game), this was very frustrating to design
(although not too hard to implement afterwards). I would've liked to have
been able to save maps to text files and then be able to access them upon
creating a new game, but this turned out to be too difficult (saving unit data
as well as tile data was just too hard to format perfectly and I was low on
time when working on this feature).

Notes: Remove the '#" before run() to test the game out! (bottom of file)
"""
############################################################

import random
#===========================================================
#Tile Object, stores the data of tiles in the game
class Tile(object):
    
    #Tile Constructor, initializes data
    def __init__(self , up , up_right , down_right , down , down_left ,\
                 up_left , centerX , centerY , radius , color , outlineColor):
        self.up = up
        self.up_right = up_right
        self.down_right = down_right
        self.down = down
        self.down_left = down_left
        self.up_left = up_left
        self.centerX = centerX
        self.centerY = centerY
        self.radius = radius
        self.color = color
        self.outlineColor = outlineColor
        self.value = 0
        self.containsUnit = False
        self.currentUnit = None
        self.isCity = False
        self.city = None
        self.category = "land"
        self.movable = True

    #Tile mutator
    def setMovable(self , movable):
        self.movable = movable

    #Tile mutator
    def setCategory(self , category):
        self.category = category

    #Tile mutator
    def setRadius(self , radius):
        self.radius = radius

     #Tile mutator
    def setUp(self , up):
        self.up = up

    #Tile mutator
    def setUp_Right(self , up_right):
        self.up_right = up_right

    #Tile mutator
    def setDown_Right(self , down_right):
        self.down_right = down_right

    #Tile mutator
    def setDown(self , down):
        self.down = down

    #Tile mutator
    def setDown_Left(self , down_left):
        self.down_left = down_left

    #Tile mutator
    def setUp_Left(self , up_left):
        self.up_left = up_left

    #Tile mutator
    def setCenterX(self, centerX):
        self.centerX = centerX

    #Tile mutator
    def setCenterY(self, centerY):
        self.centerY = centerY

    #Tile mutator
    def setValue(self , value):
        self.value = value

    #Tile mutator
    def setContainsUnit(self , hasUnit):
        self.containsUnit = hasUnit

    #Tile mutator
    def setColor(self , newColor):
        self.color = newColor

    #Tile mutator
    def setOutlineColor(self , newOutlineColor):
        self.outlineColor = newOutlineColor

    #Tile mutator
    def placeUnit(self , unit):
        self.currentUnit = unit

    #Tile accessor, returns coordinates of a tile's corners
    def getCoordinates(self):
        lstOfCoords = []
        radius = self.radius
        x = self.centerX
        y = self.centerY
        halfRadius = radius / 2
        displacementMid = int(round(((3 ** 0.5) / 2) * radius))
        tupleTopLeft = x - halfRadius , y - displacementMid
        tupleTopRight = x + halfRadius , y - displacementMid
        tupleMidRight = x + displacementMid , y
        tupleBotRight = x + halfRadius , y + displacementMid
        tupleBotLeft = x - halfRadius , y + displacementMid
        tupleMidLeft = x - displacementMid , y
        lstOfCoords.append(tupleTopLeft)
        lstOfCoords.append(tupleTopRight)
        lstOfCoords.append(tupleMidRight)
        lstOfCoords.append(tupleBotRight)
        lstOfCoords.append(tupleBotLeft)
        lstOfCoords.append(tupleMidLeft)
        return lstOfCoords

    #String representation of a tile object, this representation returns the
    #center x and y of a tile in a formatted string
    def __str__(self):
       return str(self.centerX) + "|" + str(self.centerY) + "-"

#===========================================================
#Board class, stores tiles in a list and contains methods to create pointers
#between tiles as well as get some information about tiles
class Board(object):

    #Board constructor, initializes some basic data
    def __init__(self , width , height , radius):
        self.boardList = self.createBoardList(width , height)
        self.numRows = height
        self.numCols = width
        self.tileRadius = radius

    #Creates the boardList using the width and height of the board
    def createBoardList(self , width , height):
        boardList = []
        for row in xrange(height):
            boardList += [[None] * width]
        return boardList

    #Initializes the boardList with newly created tiles
    def initBoardList(self):
        for row in xrange(self.numRows):
            for col in xrange(self.numCols):
                self.boardList[row][col] = Tile(None , None , None , \
                        None , None , None , 0 , 0 , self.tileRadius , "green"\
                                                , "black")

    #Sets the tile center X and tile center Y of each tile in boardList, 
    #this is based off of topLeftRootX and topLeftRootY
    def setTileCenters(self , topLeftRootX , topLeftRootY):
        for row in xrange(self.numRows):
            for col in xrange(self.numCols):
                radius = self.boardList[row][col].radius
                difference = int(round(((3 ** 0.5) / 2) * radius))
                #Set centerX
                if col == 0: #Any row, first column
                    self.boardList[row][col].setCenterX(topLeftRootX)
                else: #Any row, every column except the first
                    self.boardList[row][col].setCenterX((self.boardList\
                                [row][col - 1].centerX) + (difference + \
                                                           (radius / 2)))
                #Set centerY
                if row == 0 and col % 2 == 0: #First row, even column
                    self.boardList[row][col].setCenterY(topLeftRootY)
                elif row == 0 and col % 2 == 1: #First row, odd column
                    self.boardList[row][col].setCenterY(topLeftRootY - \
                                                        difference)
                else: #Any row but the first, all columns
                    self.boardList[row][col].setCenterY(self.boardList[row - 1]\
                                [col].centerY + (2 * difference))

    #Goes through the boardList and sets the "up" pointers of each tile
    def initUpPointers(self):
        numCols = self.numCols
        numRows = self.numRows
        for row in xrange(self.numRows):
            for col in xrange(self.numCols):
                currentTile = self.boardList[row][col]
                if row == 0:
                    currentTile.setUp(None)
                else:
                    currentTile.setUp(self.boardList[row - 1][col])

    #Goes through the boardList and sets the "up_right" pointers of each tile
    def initUp_RightPointers(self):
        numCols = self.numCols
        numRows = self.numRows
        for row in xrange(self.numRows):
            for col in xrange(self.numCols):
                currentTile = self.boardList[row][col]
                if col == numCols - 1: # Right Side col: off grid
                    currentTile.setUp_Right(None)
                elif col % 2 == 1 and row == 0: #Top Row: off grid
                    currentTile.setUp_Right(None)
                elif col % 2 == 0: #Even column
                    currentTile.setUp_Right(self.boardList[row][col + 1])
                else: #Odd column
                    currentTile.setUp_Right(self.boardList[row - 1][col + 1])

    #Goes through the boardList and sets the "down_right" pointers of each tile
    def initDown_RightPointers(self):
        numCols = self.numCols
        numRows = self.numRows
        for row in xrange(self.numRows):
            for col in xrange(self.numCols):
                currentTile = self.boardList[row][col]
                if col == numCols - 1: #Right Side col: off grid
                    currentTile.setDown_Right(None)
                elif col % 2 == 0 and row == numRows - 1: #Bottom Row: off grid
                    currentTile.setDown_Right(None)
                elif col % 2 == 0: #Even column
                    currentTile.setDown_Right(self.boardList[row + 1][col + 1])
                else: #Odd column
                    currentTile.setDown_Right(self.boardList[row][col + 1])

    #Goes through the boardList and sets the "down" pointers of each tile
    def initDownPointers(self):
        numCols = self.numCols
        numRows = self.numRows
        for row in xrange(self.numRows):
            for col in xrange(self.numCols):
                currentTile = self.boardList[row][col]
                if row == numRows - 1:
                    currentTile.setDown(None)
                else:
                    currentTile.setDown(self.boardList[row + 1][col])
                    
    #Goes through the boardList and sets the "down_left" pointers of each tile
    def initDown_LeftPointers(self):
        numCols = self.numCols
        numRows = self.numRows
        for row in xrange(self.numRows):
            for col in xrange(self.numCols):
                currentTile = self.boardList[row][col]
                if col == 0: #Left Side col: off grid
                    currentTile.setDown_Left(None)
                elif col % 2 == 0 and row == numRows - 1: #Bottom Row: off grid
                    currentTile.setDown_Left(None)
                elif col % 2 == 0: #Even column
                    currentTile.setDown_Left(self.boardList[row + 1][col - 1])
                else: #Odd column
                    currentTile.setDown_Left(self.boardList[row][col - 1])
                    
    #Goes through the boardList and sets the "up_left" pointers of each tile
    def initUp_LeftPointers(self):
        numCols = self.numCols
        numRows = self.numRows
        for row in xrange(self.numRows):
            for col in xrange(self.numCols):
                currentTile = self.boardList[row][col]
                if col == 0: #Left Side col: off grid
                    currentTile.setUp_Left(None)
                elif col % 2 == 1 and row == 0: #Top Row: off grid
                    currentTile.setUp_Left(None)
                elif col % 2 == 0: #Even column
                    currentTile.setUp_Left(self.boardList[row][col-1])
                else: #Odd column
                    currentTile.setUp_Left(self.boardList[row - 1][col - 1])

    #Returns a 2-D list of all of the tile centers
    def listOfTileCenters(self):
        resLst = self.createBoardList(self.numCols , self.numRows)
        for row in xrange(self.numRows):
            for col in xrange(self.numCols):
                temp = (self.boardList[row][col].centerX) , (self.boardList\
                                [row][col].centerY)
                resLst[row][col] = temp
        return resLst

    #Returns a string representation of the board (calls the tile toString)
    # for each tile
    def __str__(self):
        returnStr = ""
        for row in xrange(self.numRows):
            for col in xrange(self.numCols):
                returnStr += str(self.boardList[row][col])
            returnStr += "\n"
        return returnStr

    #Assigns special values to each tile in boardList
    def setTestingValues(self):
        count = 0
        for row in xrange(self.numRows):
            for col in xrange(self.numCols):
                self.boardList[row][col].setValue(count)
                count += 1

#===========================================================
#Unit class, stores unit data and methods
class Unit(object):
    unitValue = 0 #used for unique identification of units
    #Unit Constructor, initializes basic unit data
    def __init__(self , category , strength , isRanged , amountRange , \
                 moveSpeed , movesLeft , currentTile , playerUnit):
        self.category = category
        self.health = 100
        self.strength = strength
        self.isRanged = isRanged
        self.amountRange = amountRange
        self.moveSpeed = moveSpeed
        self.movesLeft = movesLeft
        self.currentTile = currentTile
        self.graphicsList = []
        self.playerUnit = playerUnit
        for rows in xrange(2):
            self.graphicsList += [[True] * 10]
        currentTile.setContainsUnit(True)
        self.uniqueValue = Unit.unitValue
        Unit.unitValue += 1
        
    #Does damage to two units based on their respective strengths
    def attack(self , unit):
        "Attack was made."
        attackingUnitStrength = self.strength
        defendingUnitStrength = unit.strength
        self.setHealth(self.health - defendingUnitStrength)
        #Attacker always deals slightly more damage
        unit.setHealth(unit.health - (attackingUnitStrength + \
                    ((attackingUnitStrength * random.randint(0 , 1)) / 10)))
        self.movesLeft = 0

    #Sets the health of a unit
    def setHealth(self , newHealth):
        self.health = newHealth
        self.graphicsList = self.setGraphicsList()

    #Sets the representation of each "soldier" in a unit (the little circles),
    #changes graphicsList to reflect the current condition of a unit
    def setGraphicsList(self):
        healthIterator = self.health
        oneSoldier = 5
        graphicsList = self.graphicsList
        for row in xrange(len(graphicsList)):
            for col in xrange(len(graphicsList[row])):
                if healthIterator > 0:
                    graphicsList[row][col] = True
                else:
                    graphicsList[row][col] = False
                healthIterator -= oneSoldier
        return graphicsList

    #Moves a given unit to a new tile
    def move(self , direction):
        currentTile = self.currentTile
        oldTile = self.currentTile
        if direction == "up" and currentTile.up != None:
            self.currentTile = currentTile.up
        elif direction == "up_right" and currentTile.up_right != None:
            self.currentTile = currentTile.up_right
        elif direction == "down_right" and currentTile.down_right != None:
            self.currentTile = currentTile.down_right
        elif direction == "down" and currentTile.down != None:
            self.currentTile = currentTile.down
        elif direction == "down_left" and currentTile.down_left != None:
            self.currentTile = currentTile.down_left
        elif direction == "up_left" and currentTile.up_left != None:
            self.currentTile = currentTile.up_left
        else: return
        self.movesLeft -= 1
        oldTile.setContainsUnit(False)
        self.currentTile.setContainsUnit(True)
        oldTile.placeUnit(None)
        self.currentTile.placeUnit(self)

    #Returns string representation of a unit's basic data
    def __str__(self):
       return "Type: " + str(self.category) + ", Health: " + \
                  str(self.health) + ", Unique Value: " + str(self.uniqueValue)
    
#===========================================================
#UnitList class, stores a list of Units to be used by the main game
class UnitList(object):

    #UnitList constructor, initializes the unitList
    def __init__(self):
        self.unitList = []
        self.numUnits = len(self.unitList)
        
    #Adds a unit to the unitList
    def addUnit(self , newUnit):
        self.unitList.append(newUnit)
        self.numUnits += 1

    #Removes a unit from the unitList
    def removeUnit(self , deadUnit):
        unitList = self.unitList
        unitList.remove(deadUnit)
        self.numUnits -= 1

    #String representation of UnitList, returns the string representation
    #of each unit in the unitList
    def __str__(self):
        returnStr = ""
        for current in xrange(self.numUnits):
            returnStr += str(self.unitList[current]) + " | "
        return returnStr
    
#===========================================================
#City class, stores data about a city and contains functions to change
#that data
class City(object):

    #City constructor, initializes basic city data
    def __init__(self , tile , unit , name):
        self.health = 100
        self.currentProduction = 0
        self.centerTile = tile
        self.unitContained = unit
        self.centerTile.isCity = True
        self.centerTile.color = 'red'
        self.name = name
        self.isProducing = False
        self.producing = None
        self.finishedProducing = False
        self.turnsToProduceUnit = -1
        
    #Starts the production of a unit
    def setProduction(self , unit , turnsToProduce):
        self.isProducing = True
        self.producing = unit
        self.turnsToProduceUnit = turnsToProduce
        
    #Checks to see if production has been completed
    def checkIfFinishedProducingUnit(self):
        if self.turnsToProduceUnit == self.currentProduction:
            self.finishedProducing = True

    #Sets the name of the city
    def setName(self , newName):
        self.name = newName

    #Adds to the production of the city
    def addToProduction(self):
        self.currentProduction += 1

    #Restarts production of the city
    def resetProduction(self):
        self.currentProduction = 0
        self.turnsToProduceUnit = -1
        self.finishedProducing = False
        self.isProducing = False
        self.producing = None

    #String representation of a city, returns the tile location of that city
    def __str__(self):
        return "Located on tile " + str(tile.value)

#===========================================================
#CityList class, stores a list of Cites to be used by the main game
class CityList(object):

    #CityList constructor, initializes the cityList
    def __init__(self):
        self.cityList = []
        self.numCities = len(self.cityList)

    #Adds a city to cityList
    def addCity(self , newCity):
        self.cityList.append(newCity)
        self.numCities += 1
        
    #String representation of a CityList , returns the string representation
    #of each city in the cityList
    def __str__(self):
        returnStr = ""
        for current in xrange(self.numCities):
            returnStr += str(self.cityList[current]) + " | "
        return returnStr
    
#===========================================================
from Tkinter import *

#Called whenever a key is pressed, handles that event
def keyPressed(event):
    if event.keysym == "space" and canvas.inCustomMapCreatorMode:
        canvas.inCustomMapCreatorMode = False
        canvas.inNormalGameMode = True
        playCustomGame()
    elif event.keysym == "m" and canvas.isUnitSelected:
        canvas.desiresMove = True
        displayPossibleMoves(canvas.unitSelected , \
                             canvas.unitSelected.currentTile , 0 , "cyan")
        highlightTile(canvas.unitSelected.currentTile , "yellow")
        drawUnits()
    elif event.keysym == "p" and canvas.isUnitSelected:
        currentUnit = canvas.unitSelected
        if currentUnit.category == "settler":
            createCity(currentUnit.currentTile , currentUnit)
            drawBoard()
            drawUnits()
    elif event.keysym == "r": nextTurn()
    elif event.keysym == "a" and canvas.isUnitSelected:
        canvas.desiresAttack = True
        displayPossibleAttacks(canvas.unitSelected.currentTile , "orange")
    productionCheck(event)

#Helper function fo keyPressed, checks on city production
def productionCheck(event):
    fakeTile = Tile(None , None , None , None , None , None , 10000, \
                    10000 , 100 , "orange" , "black")
    if event.keysym == "1" and canvas.isCitySelected:
        unitToProduce = Unit("scout" , 10 , False , 0 , 3 , 3 , \
               fakeTile , True)
        canvas.citySelected.setProduction(unitToProduce , 1)
        drawCityInfoBox(canvas.citySelected)
    elif event.keysym == "2" and canvas.isCitySelected:
        unitToProduce = Unit("warrior" , 15 , False , 0 , 2 , 2 , \
               fakeTile , True)
        canvas.citySelected.setProduction(unitToProduce , 2)
        drawCityInfoBox(canvas.citySelected)
    elif event.keysym == "3" and canvas.isCitySelected:
        unitToProduce = Unit("settler" , 5 , False , 0 , 1 , 1 , \
               fakeTile , True)
        canvas.citySelected.setProduction(unitToProduce , 3)
        drawCityInfoBox(canvas.citySelected)
    elif event.keysym == "4" and canvas.isCitySelected:
        canvas.citySelected.resetProduction()
        drawCityInfoBox(canvas.citySelected)
        
#Called whenever the mouse is pressed, handles that event
def mousePressed(event):
    if canvas.inNormalGameMode:
        redrawAll()
        board = canvas.board
        tileLocation = findTile(event.x , event.y)
        if tileLocation[0] < 0 or tileLocation[0] < 0:
            clickedOutsideBoardDuringGame()
        else:
            clickedInsideBoardDuringGame(tileLocation)
    elif canvas.inMainMenuMode:
        if event.x <= 900 and event.x >= 500 and event.y >= 200 and \
           event.y <= 415:
            canvas.inMainMenuMode = False
            runCustomMapCreator()
        elif event.x <= 900 and event.x >= 500 and event.y >= 415 and \
             event.y <= 630:
            playGame()
    elif canvas.inCustomMapCreatorMode:
        tileLocation = findTile(event.x , event.y)
        if not(tileLocation[0] < 0 or tileLocation[0] < 0):
            clickedInsideBoardDuringCustomMapCreation(tileLocation)

#Helper function for mousePressed(), called when the mouse is clicked
#inside the board during the game.
def clickedInsideBoardDuringGame(tileLocation):
    board = canvas.board
    currentTile = board.boardList[tileLocation[0]][tileLocation[1]]
    if canvas.isUnitSelected and canvas.desiresMove:
        canvas.desiredTile = currentTile
        if canvas.unitSelected.movesLeft == 0: resetSelection()
        else: tryToMove(canvas.unitSelected)
    elif currentTile.isCity and currentTile.containsUnit and \
         currentTile.currentUnit.playerUnit:
        resetSelection()
        selectCityAndUnit(currentTile , currentTile.currentUnit)
    elif currentTile.containsUnit and currentTile.currentUnit.playerUnit:
        resetSelection()
        selectUnit(currentTile , currentTile.currentUnit)
    elif currentTile.isCity:
        resetSelection()
        selectCity(currentTile)
    elif canvas.isUnitSelected and canvas.desiresMove:
        canvas.desiredTile = currentTile
        if canvas.unitSelected.movesLeft == 0: resetSelection()
        else: tryToMove(canvas.unitSelected)
    elif canvas.isUnitSelected and canvas.desiresAttack:
        canvas.desiredTile = currentTile
        if canvas.unitSelected.movesLeft == 0: resetSelection()
        else: tryToAttack(canvas.unitSelected , canvas.desiredTile)

#Helper function for mousePressed(), called when the mouse is clicked
#inside the board during the game. Used to change the category of a
#tile.
def clickedInsideBoardDuringCustomMapCreation(tileLocation):
    board = canvas.board
    currentTile = board.boardList[tileLocation[0]][tileLocation[1]]
    if currentTile.category == "land":
        currentTile.setCategory("water")
        currentTile.setColor("blue")
        currentTile.setMovable(False)
    else:
        currentTile.setCategory("land")
        currentTile.setColor("green")
        currentTile.setMovable(True)
    drawBoard()

#Resets the current selection by resetting selection data
def resetSelection():
    canvas.isUnitSelected = False
    canvas.unitSelected = None
    canvas.desiredTile = None
    canvas.desiresMove = False
    canvas.desiresAttack = False
    canvas.isCitySelected = False
    canvas.citySelected = None
    canvas.isCityAndUnitSelected = False
    canvas.cityAndUnitSelected = None , None
    
#Selects a unit by setting selection data for units
def selectUnit(currentTile , currentUnit):
    canvas.isUnitSelected = True
    canvas.unitSelected = currentUnit
    highlightTile(currentTile , "yellow")
    drawUnits()
    drawUnitInfoBox(currentUnit)

#Selects a unit by setting selection data for cities
def selectCity(currentTile):
    canvas.isCitySelected = True
    currentCity = currentTile.city
    canvas.citySelected = currentCity
    highlightTile(currentTile , "magenta")
    drawUnits()
    drawCityInfoBox(currentCity)

#Selects both a unit and a city by setting selection data for both units
#and cities.
def selectCityAndUnit(currentTile , currentUnit):
    canvas.isCitySelected = True
    canvas.citySelected = currentTile.city
    canvas.isUnitSelected = True
    canvas.unitSelected = currentUnit
    highlightTile(currentTile , "yellow")
    drawUnits()
    drawCityInfoBox(currentTile.city)
    drawUnitInfoBox(currentUnit)

#Helper function for mousePressed(). Resets some selection data
def clickedOutsideBoardDuringGame():
    canvas.isUnitSelected = False
    canvas.unitSelected = None
    canvas.desiresMove = False

#Tries to move the currentUnit to a new tile, setting data appropriately
#based on its success
def tryToMove(currentUnit):
    lstOfPaths = []
    determineMovementPath(currentUnit , currentUnit.currentTile , \
                              canvas.desiredTile , 0 , [] , lstOfPaths)
    if lstOfPaths == []:
        canvas.isUnitSelected = False
        canvas.desiresMove = False
    else:
        shortestPath = lstOfPaths[0]
        for possiblePath in lstOfPaths:
            if len(possiblePath) < len(shortestPath):
                shortestPath = possiblePath
        for direction in shortestPath:
            if not moveCurrentUnit(currentUnit , direction): #unit collision
                break
        canvas.isUnitSelected = False
        canvas.desiresMove = False

#Tries to attack the unit on a given tile, setting data appropriately
#based on its success
def tryToAttack(currentUnit , desiredTile):
    if canvas.desiredTile.containsUnit and \
       canvas.desiredTile.currentUnit.playerUnit == False:
        currentUnit.attack(canvas.desiredTile.currentUnit)
    if currentUnit.health <= 0:
        killUnit(currentUnit)
    if canvas.desiredTile.currentUnit.health <= 0:
        killUnit(canvas.desiredTile.currentUnit)
    redrawAll()
    resetSelection()

#Resets unit movement, deals with city production, and plays the
#A.I.'s turn
def nextTurn():
    board = canvas.board
    unitList = canvas.unitList
    cityList = canvas.cityList
    for currentUnit in unitList.unitList:
        currentUnit.movesLeft = currentUnit.moveSpeed
        if currentUnit.currentTile.isCity:
            currentUnit.setHealth(currentUnit.health + 10)
    for currentCity in cityList.cityList:
        currentCity.checkIfFinishedProducingUnit()
        if currentCity.finishedProducing:
            if currentCity.centerTile.containsUnit:currentCity.resetProduction()
            else:
                newUnit = currentCity.producing
                createUnit(newUnit , currentCity.centerTile)
                currentCity.resetProduction()
        elif currentCity.isProducing:
            currentCity.addToProduction()
    spawnEnemyUnits()
    actEnemyUnits()
    resetSelection()
    redrawAll()

#Spawns enemy units on tiles not containing player units, cities, or water
#Units are spawned randomly, having a 1/100 chance of spawning on each
#valid tile
def spawnEnemyUnits():
    currentBoard = canvas.board
    for row in xrange(currentBoard.numRows):
        for col in xrange(currentBoard.numCols):
            currentTile = currentBoard.boardList[row][col]
            if (not currentTile.containsUnit) and (not currentTile.isCity) \
            and (currentTile.movable):
                chanceOfSpawning = random.randint(1 , 200)
                if chanceOfSpawning == 100:
                    createNewUnit("warrior" , 10 , False , 0 , 2 , 2 , \
                            currentBoard.boardList[row][col] , False)

#Moves enemy unit, called on the A.I.'s turn. Units are moved randomly
def actEnemyUnits():
    unitList = canvas.unitList
    for currentUnit in unitList.unitList:
        if not currentUnit.playerUnit:
            selectUnit(currentUnit.currentTile , currentUnit)
            chanceOfMoving = random.randint(1 , 7)
            if chanceOfMoving == 1:
                canvas.desiredTile = currentUnit.currentTile.up
            elif chanceOfMoving == 2:
                canvas.desiredTile = currentUnit.currentTile.up
            elif chanceOfMoving == 3:
                canvas.desiredTile = currentUnit.currentTile.up
            elif chanceOfMoving == 4:
                canvas.desiredTile = currentUnit.currentTile.up
            elif chanceOfMoving == 5:
                canvas.desiredTile = currentUnit.currentTile.up
            elif chanceOfMoving == 6:
                canvas.desiredTile = currentUnit.currentTile.up
            canvas.desiredTile = currentUnit.currentTile
            if not canvas.desiredTile.isCity:
                tryToMove(currentUnit)
        resetSelection()

#Creates the canvas, sets some basic canvas data, and runs the game
def run():
    # create the root and the canvas
    global canvas
    root = Tk()
    windowWidth = 1400
    windowHeight = 830
    canvas = Canvas(root, width = windowWidth , height = windowHeight)
    canvas.windowWidth = windowWidth
    canvas.windowHeight = windowHeight
    canvas.pack()
    class Struct: pass
    canvas.data = Struct()
    root.bind("<Button-1>", mousePressed)
    root.bind("<Key>", keyPressed)
    root.resizable(width = 0, height = 0)
    runMainMenu()
    root.mainloop()

#Displays the main menu and sets some data so that the game knows that
#it is in main menu mode.
def runMainMenu():
    canvas.inMainMenuMode = True
    canvas.inNormalGameMode = False
    canvas.create_rectangle(0 , 0 , canvas.windowWidth , canvas.windowHeight , \
                            fill = "white")
    image = PhotoImage(file = "Main_Menu.pgm")
    canvas.image = image
    canvas.create_image(0 , 0 , image = image,anchor = 'nw')
    canvas.create_text(canvas.windowWidth / 2 , canvas.windowHeight / 8 , \
                text = "Will Borie's Civilization I" , font = "Helvetica 64" \
                       , fill = "blue")
    canvas.create_rectangle(500 , 200 , 900 , 415 , fill = "grey" , \
                            outline = "blue")
    canvas.create_text(700 , 300 , text = "Create a custom map" , \
                       font = "Helvetica 30" , fill = "red")
    canvas.create_rectangle(500 , 415 , 900 , 630 , fill = "grey" , \
                            outline = "blue")
    canvas.create_text(700, 515 , text = "Use a built-in/pre-saved map" , \
                       font = "Helvetica 30" , fill = "red")

#Initializes game data and calls drawing methods for a default game
def playGame():
    initBoard()
    canvas.inNormalGameMode = True
    currentBoard = canvas.board
    initCanvasData()
    createNewUnit("settler" , 5 , False , 0 , 1 , 1 , \
                currentBoard.boardList[0][0] , True)
    drawGame()

#Initializes game data and calls drawing methods for a custom game
def playCustomGame():
    currentBoard = canvas.board
    initCanvasData()
    findPlaceableTile()
    drawGame()

#Runs the custom map creator by initializing the board and setting some data
def runCustomMapCreator():
    initBoard()
    canvas.inCustomMapCreatorMode = True
    currentBoard = canvas.board
    drawBoard()

#Finds the first tile (from the top-left to bot-right) to place the starting
#unit on.
def findPlaceableTile():
    condition = False
    for row in xrange(len(canvas.board.boardList)):
        if condition:
            break
        for col in xrange(len(canvas.board.boardList[row])):
            if condition:
                break
            if canvas.board.boardList[row][col].movable:
                createNewUnit("settler" , 5 , False , 0 , 1 , 1 , \
               canvas.board.boardList[row][col] , True)
                condition = True
    redrawAll()

#Initializes basic canvas data.
def initCanvasData():
    canvas.unitList = UnitList()
    canvas.cityList = CityList()
    canvas.isUnitSelected = False
    canvas.unitSelected = None
    canvas.desiredTile = None
    canvas.desiresMove = False
    canvas.desiresAttack = False
    canvas.isCitySelected = False
    canvas.citySelected = None
    canvas.isCityAndUnitSelected = False
    canvas.cityAndUnitSelected = None , None

#Initializes basic game board data                         
def initBoard():
    canvas.board = Board(23 , 10 , 40) #Width , Height , "Radius"
    board = canvas.board
    board.initBoardList()
    board.setTileCenters(100 , 100) #Top Left center X , Top Left center Y
    board.initUpPointers()
    board.initUp_RightPointers()
    board.initDown_RightPointers()
    board.initDownPointers()
    board.initDown_LeftPointers()
    board.initUp_LeftPointers()
    board.setTestingValues()

#Redraws the screen and calls drawGame()
def redrawAll():
    canvas.delete(ALL)
    drawGame()

#Draws the board and units
def drawGame():
    drawBoard()
    drawUnits()

#Draws the board of hexagons
def drawBoard():
    currentBoard = canvas.board
    canvas.create_rectangle(0 , 0 , canvas.windowWidth , canvas.windowHeight , \
                            fill = "white")
    for row in xrange(currentBoard.numRows):
        for col in xrange(currentBoard.numCols):
            currentTile = currentBoard.boardList[row][col]
            topLeft = currentTile.getCoordinates()[0]
            topRight = currentTile.getCoordinates()[1]
            midRight = currentTile.getCoordinates()[2]
            botRight = currentTile.getCoordinates()[3]
            botLeft = currentTile.getCoordinates()[4]
            midLeft = currentTile.getCoordinates()[5]
            points = [topLeft[0] , topLeft[1] ,  topRight[0] , topRight[1] , \
                      midRight[0] , midRight[1] , botRight[0] ,botRight[1] , \
                      botLeft[0] , botLeft[1] , midLeft[0] , midLeft[1]]
            canvas.create_polygon(points , outline = currentTile.outlineColor ,\
                                  fill = currentTile.color)

#Draws every unit in the unitList
def drawUnits():
    currentBoard = canvas.board
    unitList = canvas.unitList
    for currentUnit in unitList.unitList:
        currentTile = currentUnit.currentTile
        pointX = currentTile.centerX - (currentTile.radius / 2)
        pointY = currentTile.centerY - 3
        color = "blue"
        if not currentUnit.playerUnit:
            color = "red"
        for row in xrange(len(currentUnit.graphicsList)):
            for col in xrange(len(currentUnit.graphicsList[row])):
                if currentUnit.graphicsList[row][col]:
                    canvas.create_oval(pointX , pointY , pointX + 3 , \
                                       pointY + 3 , fill = color)
                    pointX += 4
            pointX = currentTile.centerX - (currentTile.radius / 2)
            pointY += 4

#Creates a new unit and adds it to the unitList
def createNewUnit(category , strength , isRanged , amountRange , \
                 moveSpeed , movesLeft , currentTile , playerUnit):
    unitList = canvas.unitList
    newUnit = Unit(category , strength , isRanged , amountRange , \
                 moveSpeed , movesLeft , currentTile , playerUnit)
    unitList.addUnit(newUnit)
    currentTile.currentUnit = newUnit
    newUnit.setHealth(100)

#Takes in an already created unit and adds it to the unitList, also setting
# some unit data at the same time.
def createUnit(unit , tile):
    unitList = canvas.unitList
    unit.currentTile = tile
    tile.currentUnit = unit
    unitList.addUnit(unit)
    tile.setContainsUnit(True)

#Moves a unit to a different tile
def moveCurrentUnit(unit , direction):
    successfulMove = False
    tileMovingTo = None
    if direction == "up":
        tileMovingTo = unit.currentTile.up
    elif direction == "up_right":
        tileMovingTo = unit.currentTile.up_right
    elif direction == "down_right":
        tileMovingTo = unit.currentTile.down_right
    elif direction == "down":
        tileMovingTo = unit.currentTile.down
    elif direction == "down_left":
        tileMovingTo = unit.currentTile.down_left
    elif direction == "up_left":
        tileMovingTo = unit.currentTile.up_left
    if not tileMovingTo.containsUnit:
        unit.move(direction)
        successfulMove = True
    redrawAll()
    return successfulMove

#Removes a unit from the game
def killUnit(unit):
    currentTile = unit.currentTile
    currentTile.setContainsUnit(False)
    currentTile.placeUnit(None)
    canvas.unitList.removeUnit(unit)

#Creates a new city on a given tile and deletes the settler that placed the city
def createCity(tile , unit):
    newCity = City(tile , None , "New City")
    tile.city = newCity
    cityList = canvas.cityList
    cityList.addCity(newCity)
    killUnit(unit)
    canvas.isUnitSelected = False
    canvas.unitSelected = None
    redrawAll()

#Finds the tile with the closest centerX and centerY to x and y
def findTile(x , y):
    board = canvas.board
    lstOfCenters = board.listOfTileCenters()
    lstOfDifferences = []
    for row in xrange(len(lstOfCenters)):
        lstOfDifferences += [[0] * len(lstOfCenters[row])]
    for row in xrange(len(lstOfCenters)):
        for col in xrange(len(lstOfCenters[row])):
            currentX = lstOfCenters[row][col][0]
            currentY = lstOfCenters[row][col][1]
            lstOfDifferences[row][col] = ((x - currentX)**2) + \
                                         ((y - currentY)**2)
    currentMin = lstOfDifferences[0][0]
    currentMinLocation = 0 , 0
    for row in xrange(len(lstOfDifferences)):
        for col in xrange(len(lstOfDifferences[row])):
            if lstOfDifferences[row][col] < currentMin:
                currentMin = lstOfDifferences[row][col]
                currentMinLocation = row , col
    if currentMin > (board.boardList[0][0].radius)**2: return -1 , -1 #off
    else: return currentMinLocation #on board

#Sets a tile to water
def setTileToWater(tile):
    tile.movable = False
    tile.category = "water"
    tile.color = "blue"

#Sets a tile to land
def setTileToLand(tile):
    tile.movable = True
    tile.category = "land"
    tile.color = "green"

#Highlights the given tile with the color color
def highlightTile(tile , color):
    board = canvas.board
    topLeft = tile.getCoordinates()[0]
    topRight = tile.getCoordinates()[1]
    midRight = tile.getCoordinates()[2]
    botRight = tile.getCoordinates()[3]
    botLeft = tile.getCoordinates()[4]
    midLeft = tile.getCoordinates()[5]
    points = [topLeft[0] , topLeft[1] ,  topRight[0] , topRight[1] , \
                      midRight[0] , midRight[1] , botRight[0] ,botRight[1] , \
                      botLeft[0] , botLeft[1] , midLeft[0] , midLeft[1]]
    canvas.create_polygon(points , outline = color , fill = tile.color)

#Draws the unit information box
def drawUnitInfoBox(currentUnit):
    topLeftX = 0
    topLeftY = canvas.windowHeight - 200
    bottomRightX = 300
    bottomRightY = canvas.windowHeight
    displayText = currentUnit.category + "\n" + str(currentUnit.health)
    canvas.create_rectangle(topLeftX , topLeftY , bottomRightX , \
                            bottomRightY , outline = "yellow" , fill = "orange")
    canvas.create_text(150 , canvas.windowHeight - 100 , text = displayText)

#Draws the city information box
def drawCityInfoBox(currentCity):
    topLeftX = canvas.windowWidth - 300
    topLeftY = canvas.windowHeight - 200
    bottomRightX = canvas.windowWidth
    bottomRightY = canvas.windowHeight
    if currentCity.producing != None:
        displayText = currentCity.name + "\n" + "Currently Producing: " + \
                str(currentCity.producing.category) + \
                "\n" + str((currentCity.turnsToProduceUnit - \
                currentCity.currentProduction) + 1) + \
                " turns left for production."
    else:
        displayText = currentCity.name + "\n" + "No current production"
    canvas.create_rectangle(topLeftX , topLeftY , bottomRightX , \
                            bottomRightY , outline = "magenta", fill = "orange")
    canvas.create_text(canvas.windowWidth - 150 , canvas.windowHeight - 100 , \
                       text = displayText)

#Displays the possible moves a unit can make
def displayPossibleMoves(unit , tileRoot , countMoves , colorDisplay):
    if tileRoot == None  or tileRoot.movable == False:
        return None
    elif countMoves == unit.movesLeft and tileRoot != None:
        highlightTile(tileRoot , colorDisplay)
        return None
    else:
        highlightTile(tileRoot , colorDisplay)
        displayPossibleMoves(unit , tileRoot.up , countMoves + 1 , \
                             colorDisplay)
        displayPossibleMoves(unit , tileRoot.up_right , countMoves + 1 , \
                             colorDisplay)
        displayPossibleMoves(unit , tileRoot.down_right , countMoves + 1 , \
                             colorDisplay)
        displayPossibleMoves(unit , tileRoot.down , countMoves + 1 , \
                             colorDisplay)
        displayPossibleMoves(unit , tileRoot.down_left , countMoves + 1 , \
                             colorDisplay)
        displayPossibleMoves(unit , tileRoot.up_left , countMoves + 1 , \
                             colorDisplay)

#Displays the possible tiles that a unit can attack
def displayPossibleAttacks(tileRoot , colorDisplay):
    if tileRoot.up != None and tileRoot.up.category == "land":
        highlightTile(tileRoot.up , colorDisplay)
    if tileRoot.up_right != None and tileRoot.up_right.category == "land":
        highlightTile(tileRoot.up_right , colorDisplay)
    if tileRoot.down_right != None and tileRoot.down_right.category == "land":
        highlightTile(tileRoot.down_right , colorDisplay)
    if tileRoot.down != None and tileRoot.down.category == "land":
        highlightTile(tileRoot.down , colorDisplay)
    if tileRoot.down_left != None and tileRoot.down_left.category == "land":
        highlightTile(tileRoot.down_left , colorDisplay)
    if tileRoot.up_left != None and tileRoot.up_left.category == "land":
        highlightTile(tileRoot.up_left , colorDisplay)
    drawUnits()

#Recursively determines all of the available movement paths to a unit
def determineMovementPath(unit , tileRoot , tileDesired, countMoves, path ,\
                          lstOfPaths):
    if tileRoot == None or countMoves > unit.movesLeft or \
       tileRoot.movable == False:
        return
    elif tileRoot == tileDesired and countMoves <= unit.movesLeft:
        lstOfPaths += [path]
        return
    else:
        determineMovementPath(unit , tileRoot.up , tileDesired , \
                        countMoves + 1 , path + ["up"] , lstOfPaths)
        determineMovementPath(unit , tileRoot.up_right , tileDesired , \
                        countMoves + 1 , path + ["up_right"] , lstOfPaths)
        determineMovementPath(unit , tileRoot.down_right , tileDesired , \
                        countMoves + 1 , path  + ["down_right"] , lstOfPaths)
        determineMovementPath(unit , tileRoot.down , tileDesired , \
                        countMoves + 1 , path + ["down"] , lstOfPaths)
        determineMovementPath(unit , tileRoot.down_left , tileDesired , \
                        countMoves + 1 , path + ["down_left"] , lstOfPaths)
        determineMovementPath(unit , tileRoot.up_left , tileDesired , \
                        countMoves + 1 , path + ["up_left"] , lstOfPaths)
        return

run()

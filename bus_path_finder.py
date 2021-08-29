import random
import pygame

pygame.init()
screen = pygame.display.set_mode([500,  500])
running = True
width = 20
height = 20
grass = pygame.transform.scale(pygame.image.load('grass.jpg').convert_alpha(), (round(600/width), round(600/height)))
busImgDown = pygame.transform.scale(pygame.image.load('buss.PNG').convert_alpha(), (round(500/width), round(500/height)))
busImgUp = pygame.transform.rotate(pygame.transform.scale(pygame.image.load('buss.PNG').convert_alpha(), (round(500/width), round(500/height))), 180)
busImgLeft = pygame.transform.rotate(pygame.transform.scale(pygame.image.load('buss.PNG').convert_alpha(), (round(500/width), round(500/height))), 90)
busImgRight = pygame.transform.rotate(pygame.transform.scale(pygame.image.load('buss.PNG').convert_alpha(), (round(500/width), round(500/height))), 270)
stopSign = pygame.transform.scale(pygame.image.load('stop.PNG').convert_alpha(), (20, 40))
cell = 'c'
wall = 'w'
startHeight = random.randint(0, height-1)
startWidth = random.randint(0, width-1)
correctPath = []

if startHeight == 0:
    startHeight +=1
if startHeight == height-1:
    startHeight -=1
if startWidth == 0:
    startWidth +=1
if startWidth == width-1:
    startWidth -=1

def drawStops(array):
    for i in range(0, len(array)):
        screen.blit(stopSign, [500/width*(array[i][0]-0.3), 500/height*(array[i][1]-1.5)])

#function
def drawBus(amount, array, i, direction):
    if direction == 'left':
        screen.blit(busImgRight, [500/width*(array[i][0]-amount), 500/height*array[i][1]])
    if direction == 'right':
        screen.blit(busImgLeft, [500/width*(array[i][0]+amount), 500/height*array[i][1]])
    if direction == 'up':
        screen.blit(busImgUp, [500/width*array[i][0], 500/height*(array[i][1]-amount)])
    if direction == 'down':
        screen.blit(busImgDown, [500/width*array[i][0], 500/height*(array[i][1]+amount)])
    
def createMaze(width, height):
    maze = []
    for i in range(0, width):
        line = []
        for j in range(0, height):
            line.append('u')
        maze.append(line)
    return maze

def printMaze(maze):
    for height in range(0, len(maze[0])):
        for width in range(0, len(maze)):
            print(maze[width][height], end="")
        print('\n', end="")
def drawMaze(maze):
    for h in range(0, len(maze[0])):
        for w in range(0, len(maze)):
            if maze[w][h]=='w':
                screen.blit(grass, [500/width*w-50/width, 500/height*h-50/height])
def drawCells(maze):
    for h in range(0, len(maze[0])):
        for w in range(0, len(maze)):
            if maze[w][h]=='c':
                pygame.draw.rect(screen, (80, 80, 80), (500/width*w, 500/height*h, 500/width+0.5, 500/height+0.5))
def checkSides(block, side):
    if side=='left' and block[0]!=0:
        return maze[block[0]-1][block[1]]
    elif side=='right' and block[0]!=width-1:
        return maze[block[0]+1][block[1]]
    elif side=='up' and block[1]!=0:
        return maze[block[0]][block[1]-1]
    elif side=='down' and block[1]!=height-1:
        return maze[block[0]][block[1]+1]
    else:
        return ' '

def checkCells(wall):
    cells = 0
    if checkSides(wall, 'left')=='c':
        cells+=1
    if checkSides(wall, 'right')=='c':
        cells+=1
    if checkSides(wall, 'up')=='c':
        cells+=1
    if checkSides(wall, 'down')=='c':
        cells+=1
    return cells

def cellList(maze):
    celllist = []
    for i in range(0, len(maze)):
        for j in range(0, len(maze[0])):
            if maze[i][j]=='c':
                celllist.append([i, j])
    return celllist
    
def deleteWall(wall):
    for i in walls:
        if i[0]==wall[0] and i[1]==wall[1]:
            walls.remove(i)

def makeWalls(w, h):
    for i in range(0, w):
        for j in range(0, h):
            if maze[i][j]=='u':
                maze[i][j] = 'w'

def entranceExit(w, h):
    for a in range(0, h):
        if maze[1][a]=='c':
            maze[0][a] = 'c'
            break
    for i in range(h-1, 0, -1):
        if maze[w-2][i]=='c':
            maze[w-1][i] = 'c'
            break
    return [[0, a], [w-1, i]]

def setBlock(block, side, value):
    if side=='left' and block[0]!=0:
        maze[block[0]-1][block[1]] = value
    elif side=='right' and block[0]!=width-1:
        maze[block[0]+1][block[1]] = value
    elif side=='up' and block[1]!=0:
        maze[block[0]][block[1]-1] = value
    elif side=='down' and block[1]!=height-1:
        maze[block[0]][block[1]+1] = value
    elif side=='center':
        maze[block[0]][block[1]] = value
        

def generateMaze(width, height):
    while walls:
        randomWall = walls[random.randint(0, len(walls)-1)]
        check1 = checkSides(randomWall, 'right')=='u' and checkSides(randomWall, 'left')=='c'
        check2 = checkSides(randomWall, 'up')=='u' and checkSides(randomWall, 'down')=='c'
        check3 = checkSides(randomWall, 'up')=='c' and checkSides(randomWall, 'down')=='u'
        check4 = checkSides(randomWall, 'left')=='u' and checkSides(randomWall, 'right')=='c'
        if check1 or check2 or check3 or check4:
            if checkCells(randomWall)<2:
                setBlock(randomWall, 'center', 'c')
                if randomWall[0]!=0:
                    if checkSides(randomWall, 'left')!='c':
                        setBlock(randomWall, 'left', 'w')
                        if [randomWall[0]-1, randomWall[1]] not in walls:
                            walls.append([randomWall[0]-1, randomWall[1]])

                if randomWall[0]!= width-1:
                    if checkSides(randomWall, 'right', )!='c':
                        setBlock(randomWall, 'right', 'w')
                        if [randomWall[0]+1, randomWall[1]] not in walls:
                            walls.append([randomWall[0]+1, randomWall[1]])

                if randomWall[1]!=0:
                    if checkSides(randomWall, 'up', )!='c':
                        setBlock(randomWall, 'up', 'w')
                        if [randomWall[0], randomWall[1]-1] not in walls:
                            walls.append([randomWall[0], randomWall[1]-1])

                if randomWall[1]!=height-1:
                    if checkSides(randomWall, 'down', )!='c':
                        setBlock(randomWall, 'down', 'w')
                        if [randomWall[0], randomWall[1]+1] not in walls:
                            walls.append([randomWall[0], randomWall[1]+1])

        deleteWall(randomWall)

def navigateMaze(start, end, steps, direction, path):
        if start == end:
            path.append(start)
            return direction
        if checkSides(start, 'left')=='c' and direction!='right':
            if navigateMaze([start[0]-1, start[1]], end, steps+1, 'left', path)=='left':
                path.append(start)
                return direction
        if checkSides(start, 'right')=='c' and direction!='left':
            if navigateMaze([start[0]+1, start[1]], end, steps+1, 'right', path)=='right':
                path.append(start)
                return direction
        if checkSides(start, 'up')=='c' and direction!='down':
            if navigateMaze([start[0], start[1]-1], end, steps+1, 'up', path)=='up':
                path.append(start)
                return direction
        if checkSides(start, 'down')=='c' and direction!='up':
            if navigateMaze([start[0], start[1]+1], end, steps+1, 'down', path)=='down':
                path.append(start)
                return direction
        return False
    
maze = createMaze(width, height)
maze[startWidth][startHeight] = cell
walls = []
walls.append([startWidth-1, startHeight])
walls.append([startWidth, startHeight-1])
walls.append([startWidth, startHeight+1])
walls.append([startWidth+1, startHeight])
maze[startWidth-1][startHeight] = wall
maze[startWidth+1][startHeight] = wall
maze[startWidth][startHeight-1] = wall
maze[startWidth][startHeight+1] = wall



tempPath = []
pathsList = []
shortestPath = []
for i in range(0, width*height):
    shortestPath.append('filler')
pathsIndex = ' '
generateMaze(width, height)
makeWalls(width, height)
entrance_exit = entranceExit(width, height)
stopsList = []
stopsCopy = []
cellsList = cellList(maze)
#variables
busPos = 0
busIndex = 0
busDirection = ' '
for i in range(0, random.randint(5, 10)):
    newStop = cellsList[random.randint(0, len(cellsList)-1)]
    stopsList.append(newStop)
    stopsCopy.append(newStop)
    cellsList.remove(newStop)
for i in range(0, len(stopsList)):
    navigateMaze(entrance_exit[1], stopsList[i], 0, ' ', tempPath)
    tempPath.reverse()
    pathsList.append(tempPath)
    tempPath = []
for i in range(0, len(pathsList)):
    if len(pathsList[i])<len(shortestPath):
        shortestPath = pathsList[i]
stopsList.remove(shortestPath[len(shortestPath)-1])
correctPath.extend(shortestPath)
correctPath.remove(shortestPath[len(shortestPath)-1])
pathsList = []
stopsLen = len(stopsList)
for a in range(0, stopsLen):
    for i in range(0, len(stopsList)):
        navigateMaze(shortestPath[len(shortestPath)-1], stopsList[i], 0, ' ', tempPath)
        tempPath.reverse()
        pathsList.append(tempPath)
        tempPath = []
    shortestPath = []
    for i in range(0, width*height):
        shortestPath.append('filler')
    for i in range(0, len(pathsList)):
        if len(pathsList[i])<len(shortestPath):
            shortestPath = pathsList[i]
    #print(shortestPath[len(shortestPath)-1])
    stopsList.remove(shortestPath[len(shortestPath)-1])
    correctPath.extend(shortestPath)
    correctPath.remove(shortestPath[len(shortestPath)-1])
    pathsList = []
tempPath = []
navigateMaze(shortestPath[len(shortestPath)-1], entrance_exit[0], 0, ' ', tempPath)
tempPath.reverse()
correctPath.extend(tempPath)

if correctPath[busIndex][0]<correctPath[busIndex+1][0]:
    busDirection = 'right'
if correctPath[busIndex][0]>correctPath[busIndex+1][0]:
    busDirection = 'left'
if correctPath[busIndex][1]<correctPath[busIndex+1][1]:
    busDirection = 'down'
if correctPath[busIndex][1]<correctPath[busIndex+1][1]:
    busDirection = 'up'
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((255, 255, 255))
    drawCells(maze)
    drawMaze(maze)
    drawStops(stopsCopy)
    #drawing
    if busIndex<len(correctPath):
        drawBus(busPos, correctPath, busIndex, busDirection)
        if abs(busPos-1)<0.00001:
            busIndex+=1
            if busIndex<len(correctPath)-1:
                if correctPath[busIndex][0]<correctPath[busIndex+1][0]:
                    busDirection = 'right'
                if correctPath[busIndex][0]>correctPath[busIndex+1][0]:
                    busDirection = 'left'
                if correctPath[busIndex][1]<correctPath[busIndex+1][1]:
                    busDirection = 'down'
                if correctPath[busIndex][1]>correctPath[busIndex+1][1]:
                    busDirection = 'up'
                busPos = 0
        if busIndex!=len(correctPath)-1:
            busPos+=0.25
    pygame.display.update()
    pygame.time.Clock().tick(30)
    pygame.display.flip()
pygame.quit()
            


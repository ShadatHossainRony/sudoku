import pygame
import random

import pygame.display
pygame.init()

HEIGHT = 740 # 80 pixels for each number
WIDTH = 740

#create a new window
screen = pygame.display.set_mode([WIDTH,HEIGHT])
pygame.display.set_caption('Sudoko')

# Set game font variables
font = pygame.font.Font('freesansbold.ttf',20)
big_font = pygame.font.Font('freesansbold.ttf', 32)
timer = pygame.time.Clock()
fps = 60
white = (255,255,255)
blue = (0,0,128)
green = (0, 255, 0)
red = (255, 0, 0)

# to specify game level
level = 0
# to indicate game over
game_over = []
selection = 100

# open image and transform their resolution
one = pygame.image.load('./images/one.png')
one = pygame.transform.scale(one, (70,70))
two = pygame.image.load('./images/two.png')
two = pygame.transform.scale(two, (70,70))
three = pygame.image.load('./images/three.png')
three = pygame.transform.scale(three, (70,70))
four = pygame.image.load('./images/four.png')
four = pygame.transform.scale(four, (70,70))
five = pygame.image.load('./images/five.png')
five = pygame.transform.scale(five, (70,70))
six = pygame.image.load('./images/six.png')
six = pygame.transform.scale(six, (70,70))
seven = pygame.image.load('./images/seven.png')
seven = pygame.transform.scale(seven, (70,70))
eight = pygame.image.load('./images/eight.png')
eight = pygame.transform.scale(eight, (70,70))
nine = pygame.image.load('./images/nine.png')
nine = pygame.transform.scale(nine, (70,70))
arrow = pygame.image.load('./images/arrow.png')
arrow = pygame.transform.scale(arrow, (30,30))

# create a list of images for easier access
images = [one, two, three, four, five, six, seven, eight, nine]


numbers = []
for i in range(9):  # Loop over rows
    t = []
    for j in range(9):  # Loop over columns
        t.append(0)
    numbers.append(t)

solve = [[0,0,0,0,0,0,0,0,0],
         [0,0,0,0,0,0,0,0,0],
         [0,0,0,0,0,0,0,0,0],
         [0,0,0,0,0,0,0,0,0],
         [0,0,0,0,0,0,0,0,0],
         [0,0,0,0,0,0,0,0,0],
         [0,0,0,0,0,0,0,0,0],
         [0,0,0,0,0,0,0,0,0],
         [0,0,0,0,0,0,0,0,0]]

# check for valid moves in every numbers, row and column
def is_valid(numbers, row, col, num):
    for i in range(9):
        if numbers[row][i] == num:
            return False
        
    for i in range(9):
        if numbers[i][col] == num:
            return False
        
    corner_row = row - row%3
    corner_col = col - col%3
    for x in range(3):
        for y in range(3):
            if numbers[corner_row+x][corner_col+y] == num:
                return False
    return True


# solve an empty grid, numbers with all the values set to 0
def GenerateGrid(numbers, row, col):
    if col == 9:
        if row == 8:
             return True
        row += 1
        col = 0
    if numbers[row][col] > 0:
        return GenerateGrid(numbers, row, col+1)
    for num in range(1,10):
        if is_valid(numbers, row, col, num):
            numbers[row][col] = num
            if GenerateGrid(numbers, row, col+1):
                return True
        numbers[row][col] = 0
    return False

        
# draw the board
def DrawBoard():
# fill the screen white
    screen.fill(white)
    # draw vertical lines
    for i in range(10):
        if i%3==0:
            pygame.draw.line(screen,'black', (i*82, 0), (i*82, WIDTH), 2)
        else:
            pygame.draw.line(screen, 'black', (i*82,0), (i*82, WIDTH), 1)

    # draw the horizontal lines
    for i in range(10):
        if i%3==0:
            pygame.draw.line(screen, 'black', (0, i*82), (HEIGHT, i*82), 2)
        else:
            pygame.draw.line(screen, 'black', (0, i*82), (HEIGHT, i*82), 1)


# draw numbers on the board
def DrawNumbers():
    for i in range(9):
        for j in range(9):
            if solve[i][j] != 0:
                screen.blit(images[solve[i][j]-1], (j*82+7,i*82+7))


# draw box for the selected cell
def DrawBox(x , y, color):
    pygame.draw.line(screen, color, (x*82, y*82), (x*82, y*82+81), 4)
    pygame.draw.line(screen, color, (x*82+81, y*82), (x*82+81, y*82+81), 4)
    pygame.draw.line(screen, color, (x*82, y*82), (x*82+81, y*82), 4)
    pygame.draw.line(screen, color, (x*82, y*82+81), (x*82+81, y*82+81), 4)


# Create solving grid. We will use this to insert the input and compare it 
# with numbers list for validation
def SolvingGrid():
    j = 0
    global solve
    while j < game_over[0]:
        x = random.randint(0,8)
        y = random.randint(0,8)
        if (solve[x][y] == 0):
            solve[x][y] = numbers[x][y]
            j = j + 1
        # print(solve)

# control the game from here
def Main():
    timer.tick(fps)

    # generate a solved grid
    # fill some cells with random numbers
    k = random.randint(10,20)
    print(k)
    for i in range(k):
        x = random.randint(0,8)
        y = random.randint(0,8)
        num = random.randint(1,9)
        # print(x,y) # test_line
        if is_valid(numbers, x, y, num):
            numbers[x][y] = num
    # if GenerateGrid(numbers, 0, 0):
    #     print("Generated Grid....") # test_line
    # else:
    #     print("Failed to generate a grid") # test_line

    SolvingGrid()
    DrawBoard()
    DrawNumbers()
    pygame.display.flip()

    # get the coordinate of mouse stroke
    x = 0
    y = 0
    global selection
    inpt = -1

    # main game loop
    running = True
    while running:
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                x = event.pos[0]//82
                y = event.pos[1]//82
                sel = y*9 + x
                if solve[y][x] != 0:
                    continue
                if selection != 100 and sel == selection:
                    DrawBox(x,y, green)
                    pygame.display.update()
                    # selection = x*9 + y
                else:
                    DrawBoard()
                    DrawNumbers()
                    DrawBox(x,y, green)
                    pygame.display.update()
                    selection = sel
                # print(x,y, selection,sel)

            # get keyboard inputs
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    inpt = 1
                if event.key == pygame.K_2:
                    inpt = 2
                if event.key == pygame.K_3:
                    inpt = 3
                if event.key == pygame.K_4:
                    inpt = 4
                if event.key == pygame.K_5:
                    inpt = 5
                if event.key == pygame.K_6:
                    inpt = 6
                if event.key == pygame.K_7:
                    inpt = 7
                if event.key == pygame.K_8:
                    inpt = 8
                if event.key == pygame.K_9:
                    inpt = 9
                # check the input and add it to the grid
                if numbers[y][x] == inpt:
                    solve[y][x] = inpt
                    DrawNumbers()
                    pygame.display.update()
                    selection = 100
                    game_over[0] = game_over[0]+1
                else:
                    DrawBox(x, y, red)
                    pygame.display.update()
                print(inpt)
        if game_over[0] == 80:
            finish = big_font.render('Game Over', True, blue)
            finishRect = finish.get_rect()
            finishRect.center = (WIDTH//2, 300)
            pygame.quit()
    pygame.quit()

# greetings screen
def StartingScren():
    flag = False
    sudoku = big_font.render('Sudoku-Game Mode', True, blue)
    sudokuRect = sudoku.get_rect()
    sudokuRect.center = (WIDTH//2, 300)

    easy = big_font.render('1.Easy', True, blue, green)
    easyRect = easy.get_rect()
    easyRect.center = (WIDTH//2, 350)

    medium = big_font.render('2.Medium', True, blue, green)
    mediumRect = medium.get_rect()
    mediumRect.center = (WIDTH//2, 400)

    hard = big_font.render('3.Hard', True, blue, green)
    hardRect = hard.get_rect()
    hardRect.center = (WIDTH//2, 450)
    while True:
        screen.fill(white)
        screen.blit(sudoku, sudokuRect)
        screen.blit(easy, easyRect)
        screen.blit(medium, mediumRect)
        screen.blit(hard, hardRect)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                x = event.pos[1]
                y = event.pos[0]
                
                if x >= 430 and x <= 470:
                    if y >= 320 and y <= 420:
                        level = 3
                        flag = True
                        game_over.append(random.randint(25,32))

                if x >= 330 and x <= 370:
                    if y >= 320 and y <= 420:
                        level = 1
                        flag = True
                        game_over.append(random.randint(35,40))

                if x >= 380 and x <= 420:
                    if y >= 295 and y <= 445:
                        level = 2
                        flag = True
                        game_over.append(random.randint(41,48))
            # found the game level. 
            if flag:
                if level == 1:
                    screen.blit(arrow, (430, 335))
                elif level == 2:
                    screen.blit(arrow, (455, 385))
                elif level == 3:
                    screen.blit(arrow, (430, 440))
                pygame.display.update()
                pygame.time.wait(2000)
                # print(level) # test_line
                return

            pygame.display.update()


if __name__ == "__main__":
    StartingScren()
    # SolvingGrid()
    Main()
    # print(numbers)
    #print(column)
    # print(solve)
    print(game_over[0])

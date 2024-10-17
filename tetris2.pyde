import random
# from processing import *

# Define colors
BLACK = color(0, 0, 0)
WHITE = color(255, 255, 255)
RED = color(255, 0, 0)
GREEN = color(0, 255, 0)
BLUE = color(0, 0, 255)
from random import randint
#GLOBAL VARIABLES
speed = 0
key_flag = True
screen = 0

#DEFINE RESOLUTION (CHANGE VALUES ACCORDING TO BLOCK SIZE)
NUM_WIDTH = 400
NUM_HEIGHT = 200

#CALCULATE ROWS AND COLS
NUM_ROWS = NUM_WIDTH/20
NUM_COLS = NUM_HEIGHT/20

#LIST HOLDING COLOR COMBINATION
COLORS = [[210,210,210],[255, 51, 52],[12, 150, 228],[30, 183, 66], [246, 187,0], [76, 0 ,153], [255,255,255], [0,0,0]]
#LIST HOLDING VERTICAL CHECK VALUE OF 4 SAME COLORED BLOCKS (REPRESENTS INDEXES OF COLORED LIST)
CHECK = ['1111', '2222', '3333', '4444', '5555', '6666','7777']

#INITIALIZING BLOCK SIZE
BLOCK_SIZE = 20

#BLOCK CLASS    
class Block:
    def __init__(self, row, col, clr):
        self.block_size = BLOCK_SIZE
        self.block_color = clr 
        self.row = row
        self.col = col
        
    def __str__(self):
        return str((self.row, self.col, self.block_color))

    def display_block(self):
        temp = COLORS[self.block_color]
        stroke(180, 180, 180)
        strokeWeight(1)
        fill(int(temp[0]), int(temp[1]), int(temp[2]))
        rect(self.col * BLOCK_SIZE, self.row * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE)
       
#RETURNS THE SPECIFIC INDEX FROM COLORS LIST THAT HOLDS THE BLOCK COLOR 
    def __getitem__(self, a):
        return self.block_color
           
#GAME CLASS (INHERITS FROM LIST)    
class Game(list):
    def __init__(self):
        #VARIABLE SELF.ROW TO COUNT ROWS INORDER FOR BLOCKS TO NOT FALL BELOW THE LAST ROW
        self.row = 0
        #LIST THAT HOLDS TOP ROW VALS FOR CHECKING GAME OVER
        self.top_list = []
        self.cnt = 0
        self.score = 0
        #HORIZONTAL MOVEMENT
        self.direction = 0
        
        #INITIALLY APPENDS GRAY BLOCKS TO THE LIST
        for r in range(NUM_ROWS):
            for c in range(NUM_COLS):
                self.append(Block(r,c,0))
                
        #CHANGING A GRAY BLOCK TO A DIFFERENT COLOR AT THE START
        self.new_block()
        
#METHOD THAT CREATES RANDOM COLORED BLOCKS AT RANDOM COLUMN
    def new_block(self):
        self.row_var = 0
        self.rand_col = randint(0,NUM_COLS-1)
        while self.rand_col in self.top_list:
            self.rand_col = randint(0,NUM_COLS-1)
        self.direction = self.rand_col
        self.clr = randint(1,7)
        self.temp = Block(self.row_var, self.rand_col, self.clr) 
        self[(self.row_var * NUM_COLS) + self.rand_col] = self.temp

#DISPLAY METHOD    
    def display(self):
#DECLARATION OF GLOBAL VARIABLES
        global key_flag, speed, screen
        
#CHECK GAME OVER
        if self.game_over() == True:
            #CHANGE SCREEN
            screen = 2
            
#CHECK IF VERTICAL ALIGNMENT OF SAME COLOR BLOCKS ARE SATISFIED
        for i in range(NUM_COLS):
            check = ""
            for j in range(NUM_ROWS):
                #CONCATENATES BLOCK COLOR VALUE FROM EACH COLUMN
                check += str(self[j*NUM_COLS + i][2])
        
            for k in CHECK:
                #IF CONCATENATED STRING CONTAINS ANY ITEM FROM THE CHECK LIST THE BLOCKS ARE REMOVED/ SCORE IS INCREMENTED
                if k in check:
                    self.score += 1
                    self.cnt = 1 
                    speed = 0
                    c = check.index(k)
                    while c<check.index(k)+4:
                        #CHANGING BLOCK COLORS BACK TO GRAY
                        self[(c)*NUM_COLS + i] = Block(c*NUM_COLS, i, 0)
                        c += 1

#CHECK KEY PRESS (RIGHT OR LEFT)                        
        if keyPressed == True and self.cnt!=1:
            if keyCode == LEFT and self.row<NUM_ROWS-1 and self.direction>0 and key_flag == True and self[(self.row+1)*NUM_COLS + self.direction - 1][2] == 0 and self[(self.row+1)*NUM_COLS + self.direction][2] == 0:
                key_flag = False
                self.direction -= 1
            elif keyCode == RIGHT and self.row<NUM_ROWS-1 and self.direction<NUM_COLS - 1 and key_flag ==True and self[(self.row+1)*NUM_COLS + self.direction + 1][2] == 0 and self[(self.row+1)*NUM_COLS + self.direction][2] == 0:
                key_flag = False
                self.direction += 1

#DISPLAY BOARD AND BLOCKS        
        for t in self:
            t.display_block()

#DISPLAY SCORE
        fill(0)
        textSize(12)
        text("Score: " + str(self.score), (NUM_COLS*20*75)/100, 15)
            
#MAKE BLOCKS FALL EVERYTIME GAME.DISPLAY IS CALLED
        if self.row<NUM_ROWS-1 and self[(self.row+1)*NUM_COLS + self.direction][2] == 0:
            #CHANGE COLOR OF LAST BLOCK AFTER 4 CONSECUTIVE COLOR BLOCKS ARE MATHCED 
            if self.cnt==1 and self[(self.row)*NUM_COLS + self.direction][2] == 0 and (self.row+1)!=NUM_COLS-1:
                self[(self.row + 1)*NUM_COLS + self.direction] = Block(self.row + 1, self.direction, 0)
                
            #REMOVE THE BLOCK FROM PREVIOUS ROW WHEN RIGHT/LEFT KEY IS PRESSED
            if self.cnt!=1 and self.direction<NUM_COLS-1 and self[(self.row+1)*NUM_COLS + self.direction + 1][2] == 0 and self[(self.row)*NUM_COLS + self.direction + 1][2] == self[(self.row)*NUM_COLS + self.direction + 1][2]:
                self[(self.row)*NUM_COLS + self.direction + 1] = Block(self.row, self.direction+1, 0)
            if self.cnt!=1 and self.direction>0 and self[(self.row+1)*NUM_COLS + self.direction - 1][2] == 0 and self[(self.row)*NUM_COLS + self.direction - 1][2] == self[(self.row)*NUM_COLS + self.direction - 1][2]:
                self[(self.row)*NUM_COLS + self.direction - 1] = Block(self.row, self.direction -1, 0)

            #REMOVE PREVIOUS ROWS BLOCK (VERTICAL)
            self[(self.row)*NUM_COLS + self.direction] = Block(self.row, self.direction, 0)
            #MOVE ONE BLOCK DOWN 
            if self.cnt!=1:
                self[(self.row+1)*NUM_COLS + self.direction] = Block(self.row+1, self.direction, self.temp[2])
            
            #INCREMENT ROW COUNT
            self.row += 1
        else: 
        #REINITIALIZE VARIABLES AND CHANGING GAME SPEED
            self.cnt = 0
            self.row = 0
            game.speed(0.25)
            self.new_block()
            #CHECKING TOP ROW AND APPENDING TOP_LIST
            for i in range(NUM_COLS):
                if len(self.top_list)<NUM_COLS-1 and i not in self.top_list and self[i][2] != 0 and self[NUM_COLS+i][2]!=0:
                    self.top_list.append(i)
            
#SPEED METHOD TO CHANGE SPEED OF GAME    
    def speed(self, a):
        global speed 
        speed += a
        return speed   
    
#METHOD THAT CHECKS GAME OVER
    def game_over(self):
        for i in range(NUM_COLS):
            if self[i][2] == 0 or self[NUM_COLS+i][2]==0:
                return  False
        return True


#KEY CHECK FOR START OF GAME
def keyPressed():
    global screen
    if key == 's' and screen != 1:
        screen = 1
        
#MOUSE PRESS CHECK TO RESTART GAME
def mousePressed():
    global screen, game, speed
    if mousePressed == True and screen == 2:
        screen = 1
        game = Game()
        speed = 0

#SETUP FUNCTION    
def setup():
    size(NUM_HEIGHT, NUM_WIDTH)
    background(210,210,210)

#KEY RELEASED TO AVOID REPETITIVE KEY PRESS
def keyReleased():
    global key_flag
    key_flag = True

#DRAW FUNCTION DRAWS SCREEN ACCORDING TO GAME STATE    
def draw():
    global screen
    if screen == 0:
        background(0,0,0)
        text("PRESS S TO START THE GAME!!", 10, (NUM_COLS*40)/2)
    
    if screen == 1:
        if frameCount%(max(1, int(8 - game.speed(0))))==0 or frameCount==1:
            game.display()
            
    if screen == 2:
        background(0,191,255)
        fill(180,0,0)
        textSize(16)
        text("Click Mouse to Restart", 10, (NUM_WIDTH)/2)
        
game = Game()
 
        
    

    


    

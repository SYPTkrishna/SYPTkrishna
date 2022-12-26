import pygame
import random
from collections import namedtuple
from enum import Enum
pygame.init()
font = pygame.font.SysFont('arial', 25)
class Direction(Enum) :
    RIGHT = 1
    LEFT = 2
    UP = 3
    DOWN = 4
Point = namedtuple('Point',['x','y'])
WHITE = (255, 255, 255)
RED = (200, 0, 0)
BLUE1 = (0, 0, 255)
BLUE2 = (0, 100, 255)
BLACK = (0, 0, 0)
BLOCK_SIZE = 20
SPEED = 40
class SnakeGame:
    def __init__(self,w=700,h=500):
        self.w=w
        self.h=h
        #screendisplay
        self.display=pygame.display.set_mode((self.w,self.h))
        pygame.display.set_caption("Snakegame")
        self.clock=pygame.time.Clock()
        #init game state[direction,place snkae,food]
        self.head = Point[self.w/2, self.h/2]
        self.snake=[self.head, Point[self.head.x-BLOCK_SIZE,self.head.y],Point[self.head.x-(2*BLOCK_SIZE),self.head.y]]
        self.score = 0
        self.direction=Direction.RIGHT
        self.food = None
        self.place_food()
    def place_food(self):
        x = random.randint(0,(self.w-BLOCK_SIZE)//BLOCK_SIZE)*BLOCK_SIZE
        y = random.randint(0,(self.h-BLOCK_SIZE)//BLOCK_SIZE)*BLOCK_SIZE
        self.food=Point[x,y]
        if self.food in self.snake:
            self.place_food()
    def playstep(self):
        #1.collect user input
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
                quit()
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_LEFT:
                    self.direction=Direction.LEFT
                elif event.key==pygame.K_RIGHT:
                    self.direction=Direction.RIGHT
                elif event.key==pygame.K_UP:
                    self.direction=Direction.UP
                elif event.key==pygame.K_DOWN:
                    self.direction=Direction.DOWN
        #2.Move
        self._move(self.direction)
        self.snake.insert(0,self.head)
        #3gameover
        game_over=False
        if _iscollision():
            game_over=True
            return game_over,self.score
        #place new food
        if self.head==self.food:
            self.score+=1
            self.place_food()
        else:
            self.snake.pop()
        #5.update ui and clock
        self._update_ui()
        self._clock.tick(SPEED)
        #6.return and final step in playstep
        return game_over,self.score
    def _iscollision(self):
        if self.head.x>self.w-BLOCK_SIZE or self.head.x<0 or self.head.y>self.h-BLOCK_SIZE or self.head.y<0:
            return True
        if self.head in self.snake[1:]:
            return True
        return False

    def _update_ui(self):
        self.display.fill(BLACK)
        for pt in self.snake:
            pygame.draw.rect(self.display,BLUE1,pygame.Rect(pt.x,pt.y,BLOCK_SIZE,BLOCK_SIZE))
            pygame.draw.rect(self.display,BLUE2,pygame.Rect(pt.x+4,pt.y+4,12,12))
        pygame.draw.rect(self.display,RED,pygame.Rect(self.food.x,self.food.y,BLOCK_SIZE,BLOCK_SIZE))
        text = font.render("Score "+str(self.score),True,WHITE)
        self.display.blit(text,[0,0])
        pygame.display.flip()
    def _move(self,direction):
        x= self.head.x
        y= self.head.y
        if direction==Direction.RIGHT:
            x+=BLOCK_SIZE
        elif direction==Direction.LEFT:
            x-=BLOCK_SIZE
        elif direction==Direction.UP:
            y+=BLOCK_SIZE
        else:
            y-=BLOCK_SIZE
        self.head(Point[x,y])
if __name__=='__main__':
    game = SnakeGame()
    while True:
        game_over,score=game.playstep()
        if game_over==True:
            break
    print('Final Score:',score)
    pygame.quit()
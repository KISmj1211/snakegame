import pygame
import random
pygame.init()
WIDTH =500
win = pygame.display.set_mode((WIDTH,WIDTH))
pygame.display.set_caption("Snake Game-2")
running = True

ROWS=20
def draw_grid(surface):
    size_btwn = WIDTH//ROWS
    for i in range(ROWS):
        x,y = size_btwn*i, size_btwn*i
        pygame.draw.line(surface,(255,255,255),(x,0),(x,WIDTH))
        pygame.draw.line(surface,(255,255,255),(0,y), (WIDTH,y))
class Cube:
    def __init__(self,pos,color=(255,0,0)):
        self.pos = pos
        self.color= color
        self.dirnx, self.dirny = 0,1
    def move(self,dirnx,dirny):
        self.dirnx, self.dirny = dirnx, dirny
        self.pos = (self.pos[0]+self.dirnx, self.pos[1]+self.dirny)
    def draw(self,surface):
        dis = WIDTH//ROWS
        i,j = self.pos
        pygame.draw.rect(surface, self.color, (i*dis,j*dis,dis,dis))

class Snake:
    def __init__(self,color,pos):
        self.body = [Cube(pos)]
        self.dirnx, self.dirny = 0,1
    def move(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.dirnx,self.dirny = -1,0
        elif keys[pygame.K_RIGHT]:
            self.dirnx,self.dirny = 1,0
        elif keys[pygame.K_UP]:
            self.dirnx,self.dirny = 0,-1
        elif keys[pygame.K_DOWN]:
            self.dirnx,self.dirny = 0,1
        for i in range(len(self.body)-1,0,-1):
            self.body[i].pos=self.body[i-1].pos
        self.body[0].move(self.dirnx,self.dirny)
    def addCube(self):
        tail = self.body[-1]
        new_cube = Cube((tail.pos[0]-self.dirnx,tail))
        self.body.append(new_cube)
    def draw(self,surface):
        for cube in self.body:
            cube.draw(surface)
def randomSnack(snake):
    while True:
        x,y=random.randrange(ROWS), random.randrange(ROWS)
        is_valid=True
        for cube in snake.body:
            if cube.pos==(x,y):
                is_valid=False
                break
        if is_valid:
            return x,y
        
s= Snake((255,0,0), (10,10))
snack= Cube(randomSnack(s), color = (0,255,0))
running = True
while running:
    pygame.time.delay(100)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    s.move()
    if s.body[0].pos == snack.pos:
        s.addCube()
        snack = Cube(randomSnack(s),color = (0,255,0))
    win.fill((0,0,0))
    draw_grid(win)
    
    s.draw(win)
    
    snack.draw(win)
    pygame.display.update()
pygame.quit()
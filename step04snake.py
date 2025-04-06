import pygame
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
    def move(self):
        self.pos = (self.pos[0]+self.dirnx, self.pos[1]+self.dirny)
    def draw(self,surface):
        dis = WIDTH//ROWS
        i,j = self.pos
        pygame.draw.rect(surface, self.color, (i*dis,j*dis,dis,dis))
snake =Cube((10,10))
running = True
while running:
    pygame.time.delay(100)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            runnign = False
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        snake.dirnx,snake.dirny = -1,0
    elif keys[pygame.K_RIGHT]:
        snake.dirnx,snake.dirny = 1,0
    elif keys[pygame.K_UP]:
        snake.dirnx,snake.dirny = 0,-1
    elif keys[pygame.K_DOWN]:
        snake.dirnx,snake.dirny = 0,1
    snake.move()
    win.fill((0,0,0))
    draw_grid(win)
    snake.draw(win)
    pygame.display.update()
pygame.quit()
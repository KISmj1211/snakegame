import pygame
import random

pygame.init()

WIDTH = 500
ROWS = 20
win = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("Snake Game - 단계 9")
FONT = pygame.font.SysFont("Arial",30)
high_score = 0
def drawGrid(surface):
    """격자 그리기"""
    sizeBtwn = WIDTH // ROWS
    for i in range(ROWS):
        x, y = sizeBtwn * i, sizeBtwn * i
        pygame.draw.line(surface, (255, 255, 255), (x, 0), (x, WIDTH))
        pygame.draw.line(surface, (255, 255, 255), (0, y), (WIDTH, y))

def draw_score(surface, score, high_score):
    score_text=FONT.render(f"Score: {score}",True,(255,255,255))
    high_score_text = FONT.render(f"High Score: {high_score}",True,(255,255,255))
    surface.blit(score_text, (10,10))
    surface.blit(high_score_text, (10,40))
    
class Cube:
    """뱀과 먹이를 표현하는 클래스"""
    def __init__(self, pos, color=(255, 0, 0)):
        self.pos = pos
        self.dirnx, self.dirny = 0, 1  # 기본 이동 방향 (아래쪽)
        self.color = color

    def move(self, dirnx, dirny):
        """큐브 이동"""
        self.dirnx, self.dirny = dirnx, dirny
        self.pos = (self.pos[0] + self.dirnx, self.pos[1] + self.dirny)

    def draw(self, surface):
        """큐브 그리기"""
        dis = WIDTH // ROWS
        i, j = self.pos
        pygame.draw.rect(surface, self.color, (i * dis, j * dis, dis, dis))

class Snake:
    """뱀을 관리하는 클래스"""
    def __init__(self, color, pos):
        self.body = [Cube(pos)]  # 뱀의 머리 추가
        self.dirnx, self.dirny = 0, 1  # 기본 이동 방향 (아래쪽)
        self.score = 0

    def move(self):
        """뱀 이동"""
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.dirnx, self.dirny = -1, 0
        elif keys[pygame.K_RIGHT]:
            self.dirnx, self.dirny = 1, 0
        elif keys[pygame.K_UP]:
            self.dirnx, self.dirny = 0, -1
        elif keys[pygame.K_DOWN]:
            self.dirnx, self.dirny = 0, 1

        # 몸을 앞으로 이동
        for i in range(len(self.body) - 1, 0, -1):
            # self.body[i].pos = self.body[i - 1].pos
            self.body[i].pos = self.body[i - 1].pos

        self.body[0].move(self.dirnx, self.dirny)  # 머리 이동

        if (self.body[0].pos[0]>=ROWS and self.dirnx == 1)or \
            (self.body[0].pos[0]<0 and self.dirnx==-1) or \
            (self.body[0].pos[1]>=ROWS and self.dirny==1) or \
            (self.body[0].pos[1]<0 and self.dirny==-1):
                game_over(self.score)
        for i in range(1,len(self.body)):
            if self.body[0].pos==self.body[i].pos:
                game_over(self.score)
                break

    def addCube(self):
        """먹이를 먹으면 몸을 길게 추가"""
        tail = self.body[-1]
        # new_cube = Cube((tail.pos[0] - self.dirnx, tail.pos[1] - self.dirny))
        new_cube = Cube((tail.pos[0] - self.dirnx, tail.pos[1] - self.dirny))

        self.body.append(new_cube)
        self.score +=10
    def reset(self,pos):
        self.body=[Cube(pos)]
        self.dirnx,self.dirny=0,1
        self.score = 0
        
    def draw(self, surface):
        """뱀 그리기"""
        for cube in self.body:
            cube.draw(surface)

def randomSnack(snake):
    """랜덤한 위치에 먹이 생성 (뱀과 겹치지 않도록)"""
    while True:
        x, y = random.randrange(ROWS), random.randrange(ROWS)
        is_valid = True  # 유효한 위치인지 확인하는 변수

        for cube in snake.body:  # 뱀의 모든 큐브와 비교
            if cube.pos == (x, y):
                is_valid = False
                break  # 뱀과 겹치면 다시 뽑기

        if is_valid:
            return x, y
def game_over(score):
    
    """게임 오버 화면"""
    global s, snack, high_score  # 뱀과 먹이를 다시 초기화할 수 있도록 global 사용

    if score> high_score:
        high_score = score
    win.fill((0,0,0))
    game_over_text = FONT.render(f"Game Over! Score:{score}",True,(255,255,255))
    high_score_text = FONT.render(f"High Score: {high_score}",True,(255,255,255))
    win.blit(game_over_text, (WIDTH//4, WIDTH//3))
    win.blit(high_score_text, (WIDTH//5,WIDTH//3+40))
    pygame.display.update()
    pygame.time.delay(2000)

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                waiting=False
    s = Snake((255, 0, 0), (10, 10))  # 뱀 생성
    # snack = Cube(randomSnack(s), color=(0, 255, 0))  # 먹이 생성
    snack = Cube(randomSnack(s), color=(0, 255, 0))

s = Snake((255, 0, 0), (10, 10))  # 뱀 생성
# snack = Cube(randomSnack(s), color=(0, 255, 0))  # 먹이 생성
snack = Cube(randomSnack(s), color=(0, 255, 0))

running = True
while running:
    pygame.time.delay(100)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    s.move()

    # 먹이를 먹으면 몸이 길어짐
    if s.body[0].pos == snack.pos:
        s.addCube()
        snack = Cube(randomSnack(s), color=(0, 255, 0))

    win.fill((0, 0, 0))
    drawGrid(win)
    s.draw(win)
    snack.draw(win)
    draw_score(win, s.score, high_score)
    pygame.display.update()

pygame.quit()
"""
10번마다 보라색 아이템이 나옴.
보라색 아이템은 3배의 점수를 얻음. 보라색 아이템을 먹으면 좌우상하 반전이 됨.
예를 들어, 오른쪽 화살표 키를 누르면 왼쪽으로 가게됨.
보라색 아이템과 일반 아이템은 같이 보일 수 있음. 보라색 아이템을 먹지 않으면 보라색 아이템은 계속 남아있음.
"""
import pygame
import random

pygame.init()

WIDTH = 500
ROWS = 20
win = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("Snake Game")

# 폰트 설정
FONT = pygame.font.SysFont("Arial", 30)

# 최고 점수 저장 변수
high_score = 0
base_speed = 150  # 기본 속도 설정
reverse_controls = False  # 보라색 아이템 효과 (좌우/상하 반전)

def drawGrid(surface):
    """격자 그리기"""
    sizeBtwn = WIDTH // ROWS
    for i in range(ROWS):
        x, y = sizeBtwn * i, sizeBtwn * i
        pygame.draw.line(surface, (255, 255, 255), (x, 0), (x, WIDTH))
        pygame.draw.line(surface, (255, 255, 255), (0, y), (WIDTH, y))

def draw_score(surface, score, high_score):
    """화면에 현재 점수와 최고 점수 표시"""
    score_text = FONT.render(f"Score: {score}", True, (255, 255, 255))
    high_score_text = FONT.render(f"High Score: {high_score}", True, (255, 255, 255))
    surface.blit(score_text, (10, 10))
    surface.blit(high_score_text, (10, 40))

class Cube:
    """뱀과 아이템을 표현하는 클래스"""
    def __init__(self, pos, color=(255, 0, 0)):
        self.pos = pos
        self.color = color

    def draw(self, surface):
        """큐브 그리기"""
        dis = WIDTH // ROWS
        i, j = self.pos
        pygame.draw.rect(surface, self.color, (i * dis, j * dis, dis, dis))

class Snake:
    """뱀을 관리하는 클래스"""
    def __init__(self, color, pos):
        self.body = [Cube(pos)]
        self.dirnx, self.dirny = 0, 1
        self.score = 0

    def move(self): # making the snake move
        """뱀 이동"""
        global reverse_controls  # 방향 반전 변수 사용

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.dirnx, self.dirny = (-1, 0) if not reverse_controls else (1, 0)
        elif keys[pygame.K_RIGHT]:
            self.dirnx, self.dirny = (1, 0) if not reverse_controls else (-1, 0)
        elif keys[pygame.K_UP]:
            self.dirnx, self.dirny = (0, -1) if not reverse_controls else (0, 1)
        elif keys[pygame.K_DOWN]:
            self.dirnx, self.dirny = (0, 1) if not reverse_controls else (0, -1)

        for i in range(len(self.body) - 1, 0, -1):
            self.body[i].pos = self.body[i - 1].pos

        self.body[0].pos = (self.body[0].pos[0] + self.dirnx, self.body[0].pos[1] + self.dirny)

        # 벽 충돌 확인
        if (self.body[0].pos[0] >= ROWS or self.body[0].pos[0] < 0 or
            self.body[0].pos[1] >= ROWS or self.body[0].pos[1] < 0):
            game_over(self.score)

        # 자기 자신과 충돌하면 게임 오버
        for i in range(1, len(self.body)):
            if self.body[0].pos == self.body[i].pos:
                game_over(self.score)
                break

    def addCube(self): #making the snake longer
        """먹이를 먹으면 몸을 길게 추가"""
        tail = self.body[-1]
        new_cube = Cube((tail.pos[0] - self.dirnx, tail.pos[1] - self.dirny))
        self.body.append(new_cube)
        self.score += 10  # 점수 증가

    def reset(self, pos): 
        """게임 리셋"""
        global reverse_controls
        self.body = [Cube(pos)]
        self.dirnx, self.dirny = 0, 1
        self.score = 0
        reverse_controls = False  # 방향 반전 효과 해제

    def draw(self, surface):
        """뱀 그리기"""
        for cube in self.body:
            cube.draw(surface)

def randomSnack(snake): #the source for thee snake getting longer
    """랜덤한 위치에 먹이 생성 (뱀과 겹치지 않도록)"""
    while True:
        x, y = random.randrange(ROWS), random.randrange(ROWS)
        is_valid = all(cube.pos != (x, y) for cube in snake.body)
        if is_valid:
            return x, y

def game_over(score): # the interaction when colliding to self or wall
    """게임 오버 화면"""
    global s, snack, purple_item, high_score, base_speed, reverse_controls

    if score > high_score:
        high_score = score

    win.fill((0, 0, 0))
    game_over_text = FONT.render(f"Game Over! Score: {score}", True, (255, 255, 255))
    high_score_text = FONT.render(f"High Score: {high_score}", True, (255, 255, 255))
    win.blit(game_over_text, (WIDTH // 5, WIDTH // 3))
    win.blit(high_score_text, (WIDTH // 5, WIDTH // 3 + 40))
    pygame.display.update()

    pygame.time.delay(2000)

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                waiting = False

    s = Snake((255, 0, 0), (10, 10))
    snack = Cube(randomSnack(s), color=(0, 255, 0))
    purple_item = None  # 보라색 아이템 초기화
    base_speed = 200
    reverse_controls = False

s = Snake((255, 0, 0), (10, 10))
snack = Cube(randomSnack(s), color=(0, 255, 0))
purple_item = None

running = True
while running:
    speed = max(50, base_speed - s.score // 10 * 5)
    pygame.time.delay(speed)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    s.move()

    if s.body[0].pos == snack.pos:
        s.addCube()
        snack = Cube(randomSnack(s), color=(0, 255, 0))
        base_speed = max(50, base_speed - 5)
        # if s.score % 100 == 0 and s.score != 0: # 10번마다
        # if s.score % 30 == 0 and s.score != 0: # 3번마다 보라색 아이템 나옴 - 테스트용
        if s.score % 20 == 0 and s.score != 0:  # 2번마다 보라색 아이템 나옴 - 테스트용
            purple_item = Cube(randomSnack(s), color=(128, 0, 128))

    if purple_item and s.body[0].pos == purple_item.pos: #making special items snacks
        s.score += 30
        reverse_controls = not reverse_controls
        purple_item = None  # 보라색 아이템 제거

    win.fill((0, 0, 0))
    drawGrid(win)
    s.draw(win)
    snack.draw(win)
    if purple_item:
        purple_item.draw(win)
    draw_score(win, s.score, high_score)
    pygame.display.update()

pygame.quit()
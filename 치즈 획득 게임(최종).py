import pygame
import sys
import random
import time

#1. Pygame 초기화, 화면 설정
pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("치즈 획득 게임")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 40)

# 플레이어 설정
player = pygame.Rect(380, 280, 40, 40)
player_speed = 5

# 고정 장애물 위치
obstacles = [
    pygame.Rect(200, 150, 100, 50),
    pygame.Rect(500, 400, 120, 60),
    pygame.Rect(300, 250, 80, 80),
    pygame.Rect(100, 100, 80, 50),
    pygame.Rect(500, 50, 100, 70)
]

# 움직이는 장애물 설정
moving_obs = pygame.Rect(random.randint(0, 750), 50, 50, 30)
moving_obs_speed_x = 3
moving_obs_speed_y = 0.2

# 치즈 생성 함수 정의
def create_cheese():

    size = 30
    while True:
        x = random.randint(0, 800 - size)
        y = random.randint(0, 600 - size)
        cheese_rect = pygame.Rect(x, y, size, size)

        overlaps = False
        # 고정 장애물과의 충돌 확인
        for obs in obstacles:
            if cheese_rect.colliderect(obs):
                overlaps = True
                break
        # 움직이는 장애물과의 충돌 확인
        if cheese_rect.colliderect(moving_obs):
            overlaps = True
            break

        if not overlaps:
            return cheese_rect

# 초기 치즈 생성
cheese = create_cheese()
score = 0

# 제한 시간 설정
TOTAL_TIME = 30
start_time = time.time()

# 게임 상태 변수
running = True
game_over = False

#2. 메인 게임 루프
while running:
    current_time = time.time()
    elapsed_time = int(current_time - start_time)
    remaining_time = TOTAL_TIME - elapsed_time

    # 이벤트 처리
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if not game_over:
        keys = pygame.key.get_pressed()
        old_x, old_y = player.x, player.y

        if keys[pygame.K_LEFT]:
            player.x -= player_speed
        if keys[pygame.K_RIGHT]:
            player.x += player_speed
        if keys[pygame.K_UP]:
            player.y -= player_speed
        if keys[pygame.K_DOWN]:
            player.y += player_speed

        # 경계 안 벗어나게
        player.left = max(player.left, 0)
        player.right = min(player.right, 800)
        player.top    = max(player.top, 0)
        player.bottom = min(player.bottom, 600)

        # 고정 장애물과의 충돌 처리
        for obs in obstacles:
            if player.colliderect(obs):
                player.x, player.y = old_x, old_y
                break

        # 움직이는 장애물과의 충돌 처리
        if player.colliderect(moving_obs):
            player.x, player.y = old_x, old_y


        # 치즈 먹기 처리
        if player.colliderect(cheese):
            score += 1
            cheese = create_cheese() # 새 열쇠 생성

    # 타겟 이동 (지그재그 + 서서히 하강)
    moving_obs.x += moving_obs_speed_x
    moving_obs.y += moving_obs_speed_y
    if moving_obs.right >= 800 or moving_obs.left <= 0:
        moving_obs_speed_x = -moving_obs_speed_x
        moving_obs.y += 20

    # 시간 초과 처리
    if remaining_time <= 0:
        game_over = True

    # 화면 그리기
    screen.fill((30, 30, 30))
    pygame.draw.rect(screen,(0,15,255),player)
    pygame.draw.rect(screen,(255,215,0),cheese)
    pygame.draw.rect(screen, (255, 100, 0), moving_obs)

    # 고정 장애물 그리기
    for obs in obstacles:
        pygame.draw.rect(screen, (200, 50, 50), obs)

    # 점수 및 시간 표시
    if not game_over:
        text_surface = font.render(f"score: {score} / time: {remaining_time}", True, (255, 255, 255))
    else:
        text_surface = font.render(f"Game Over! Your score is {score}", True, (255, 255, 0))

    screen.blit(text_surface, (20, 20))


    pygame.display.flip()
    clock.tick(60)

#3. Pygame 종료
pygame.quit()
sys.exit()

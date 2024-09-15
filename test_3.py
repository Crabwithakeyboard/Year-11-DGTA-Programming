import pygame
import math

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
FPS = 60
clock = pygame.time.Clock()
screen_x = 900
screen_y = 500
ball_x = 40
ball_y = 40
time = 0
screen = pygame.display.set_mode((screen_x, screen_y))
pygame.display.set_caption("Basketball Game")

jumping = False
X_POSITION = 400
Y_POSITION = 375
Y_GRAVITY = 1
JUMP_HEIGHT = 20
Y_VELOCITY = JUMP_HEIGHT

VEL_BALL = 15
ARROW_X = 500
ARROW_Y = 300
LENGHT_FORCE = 49

ANGLE = 0

ball = pygame.image.load("Data/images/Entity_sprites/Arrow/arrow.png")
ball = pygame.transform.scale(ball, (80, 80))
ball_rect = ball.get_rect(center = (X_POSITION, Y_POSITION))
ball_width = ball.get_width()

def ball_path():
    Vx = math.cos(angle)* JUMP_HEIGHT
    Vy = math.sin(angle)* JUMP_HEIGHT
    distx = Vx * time
    disty = (Vy * time) +((-4.9 * (time)**2)/2)
    
    newx = round(distx + X_POSITION)
    newy = round(Y_POSITION-disty)

    return(newx, newy)

    #X_POSITION = newx
    #Y_POSITION = newy

def find_angle(pos):

    sX = X_POSITION
    sY = Y_POSITION
    try:
        angle = math.pi / 2
    except:
        angle = math.pi / 2
    if pos[1] < sY and pos[0] > sX:
        angle = abs(angle)
    elif pos[1] < sY and pos[0] < sX:
        angle = math.pi - angle
    elif pos[1] > sY and pos[0] < sX:
        angle = math.pi + abs(angle)
    elif pos[1] > sY and pos[0] > sX:
        angle = (math.pi * 2) - angle

    return angle


run = True
while run:
    VECTOR_STARTPOINT = pygame.math.Vector2(X_POSITION, Y_POSITION)
    VECTOR_ENDPOINT = pygame.math.Vector2(100, 100)
    CURRENT_ENDPOINT = VECTOR_STARTPOINT + VECTOR_ENDPOINT.rotate(ANGLE)

    screen.fill(BLACK)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False


    keys_pressed = pygame.key.get_pressed()

    if keys_pressed[pygame.K_SPACE]:
        jumping = True
    if keys_pressed[pygame.K_d] and X_POSITION < screen_x-ball_width//2:
        X_POSITION += VEL_BALL
    if keys_pressed[pygame.K_a] and X_POSITION > 0 + ball_width//2:
        X_POSITION -= VEL_BALL

    screen.fill(BLACK)
    
    #draw force line, red below, white above
    FORCE_MAX = pygame.draw.line(screen, (255, 0, 0) , (400, 50), (50, 50), 5)
    FORCE = pygame.draw.line(screen, WHITE , (LENGHT_FORCE, 50), (50, 50), 5)


    if keys_pressed[pygame.K_r] and LENGHT_FORCE <= 400:
        LENGHT_FORCE += 5

        #coould do it with no hard coding
        if LENGHT_FORCE <= 200 and LENGHT_FORCE > 99:
            print("low")
            JUMP_HEIGHT = 20
            Y_VELOCITY = JUMP_HEIGHT

        if LENGHT_FORCE > 200 and LENGHT_FORCE < 300:
            print("medium")
            JUMP_HEIGHT = 25
            Y_VELOCITY = JUMP_HEIGHT

        if LENGHT_FORCE >= 300 and LENGHT_FORCE < 400:
            print("strong")
            JUMP_HEIGHT = 30
            Y_VELOCITY = JUMP_HEIGHT

        if LENGHT_FORCE == 399:
            print("maximum")
            JUMP_HEIGHT = 35
            Y_VELOCITY = JUMP_HEIGHT

    #start moving vector
    if keys_pressed[pygame.K_w]:
        ANGLE = (ANGLE + 5) % 360
        VECTOR_LINE = pygame.draw.line(screen, WHITE, VECTOR_STARTPOINT, CURRENT_ENDPOINT, 4)
    
    #stop moving vector
    if event.type == pygame.KEYUP :
        if event.key == pygame.K_w :
            if Y_POSITION < screen_y and Y_POSITION >= 0:
                pos = CURRENT_ENDPOINT[0], CURRENT_ENDPOINT[1]
                angle = find_angle(pos)

                VECTOR_LINE = pygame.draw.line(screen, (255, 0, 0), VECTOR_STARTPOINT, CURRENT_ENDPOINT, 4)
                
                time += 0.05
                po = ball_path()
                X_POSITION = po[0]
                Y_POSITION = po[1]
                
            else:
                time = 0
                Y_POSITION = 375


    if jumping:
        Y_POSITION -= Y_VELOCITY
        Y_VELOCITY -= Y_GRAVITY
        if Y_VELOCITY < -JUMP_HEIGHT:
            jumping = False
            Y_VELOCITY = JUMP_HEIGHT
        ball_rect = ball.get_rect(center = (X_POSITION, Y_POSITION))
        screen.blit(ball, ball_rect)
    else:
        ball_rect = ball.get_rect(center = (X_POSITION, Y_POSITION))
        screen.blit(ball, ball_rect)


    pygame.display.flip()
    clock.tick(FPS)
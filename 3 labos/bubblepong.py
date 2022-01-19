import random
import sys
from time import sleep

from pygame import (
    K_ESCAPE,
    K_LEFT,
    K_RIGHT,
    KEYDOWN,
    KEYUP,
    QUIT,
    Rect,
    display,
    draw,
    event,
    font,
    init,
    time,
)

init()

width = 1000
height = 700

screen = display.set_mode((width, height))
display.set_caption("BubblePong")
myfont = font.SysFont("arial", 60)
myfont2 = font.SysFont("arial", 60)
score = 0
scoreGraphic = myfont.render(str(score), True, (255, 255, 255))
testGraphic = myfont2.render("GAME OVER", True, (255, 255, 255))
animationTimer = time.Clock()

# list of lists:
# 	0: Rect
# 	1: dx
# 	2: dy
# 	3: color = (R,G,B)
# 	4: counter - for shrinking green balls
# 	5: flag - to reborn ball (only for green balls)
balls = []
dy = [2, -2, 3, -3, -2, -3]
dx = [1, -1, 2, -2, 3, -3]
#mjesto gdje nastaju kugle
start_x = width / 2
start_y = height / 4

# The RED balls
balls.append(
    [
        Rect(start_x, start_y, 60, 60),
        random.choice(dx),
        random.choice(dy),
        (255, 0, 0),
        0,
        0,
    ]
)
balls.append(
    [
        Rect(start_x + 60, start_y, 60, 60),
        random.choice(dx),
        random.choice(dy),
        (255, 0, 0),
        0,
        0,
    ]
)

# The BLUE balls
balls.append(
    [
        Rect(start_x + 60, start_y + 60, 40, 40),
        random.choice(dx),
        random.choice(dy),
        (0, 0, 255),
        0,
        0,
    ]
)
balls.append(
    [
        Rect(start_x + 60, start_y - 60, 40, 40),
        random.choice(dx),
        random.choice(dy),
        (0, 0, 255),
        0,
        0,
    ]
)

# The GREEN balls
balls.append(
    [
        Rect(start_x, start_y - 60, 60, 60),
        random.choice(dx),
        random.choice(dy),
        (0, 255, 0),
        1,
        1,
    ]
)
balls.append(
    [
        Rect(start_x, start_y + 60, 60, 60),
        random.choice(dx),
        random.choice(dy),
        (0, 255, 0),
        50,
        1,
    ]
)

# The PADDLE
paddle = Rect(width / 2 - 50, height - 50, 200, 10)
paddleDX = 0
endProgram = False

# Game loop
start_g = 60
flag = 1
while not endProgram:
    for e in event.get():
        if e.type == QUIT:
            sys.exit()
        if e.type == KEYDOWN:
            if e.key == K_LEFT and paddle.left > 0:
                paddleDX = -6
            if e.key == K_RIGHT and paddle.right < width:
                paddleDX = 6
            if e.key == K_ESCAPE:
                sys.exit()
        if e.type == KEYUP:
            if e.key == K_LEFT or e.key == K_RIGHT:
                paddleDX = 0

    # Update position
    for ball in balls:
        # If ball green, shrink it
        if ball[4] > 0 and ball[4] % 50 == 0 and ball[0].width > 1:
            ball[0].inflate_ip(-1, -1)
            color = ball[3][1] - 4
            ball[3] = (0, color, 0)
        if ball[4] > 0:
            if flag == 1 and ball[4] == 50:
                flag = 0
                ball[4] = 50
            else:
                ball[4] += 1

        # Remove green ball if too small, reborn if can
        if ball[0].width <= 10 and ball[4] > 0:
            if ball[5] == 1:
                balls.append(
                    [
                        Rect(start_x, start_y - start_g, 60, 60),
                        random.choice(dx),
                        random.choice(dy),
                        (0, 255, 0),
                        1,
                        0,
                    ]
                )
                start_g *= -1
            balls.remove(ball)
            if len(balls) == 0:
                endProgram = True
        else:
            ball[0].move_ip(ball[1], ball[2])
    paddle.move_ip(paddleDX, 0)

    ###############################################################
    # Border check for the ball
    for ball in balls:
        if ball[0].y < 0:
            ball[2] *= -1
        if ball[0].x > width - ball[0].width or ball[0].x < 0:
            ball[1] *= -1

        # Remove ball that hits the bottom wall
        if ball[0].y > height:
            balls.remove(ball)
            if len(balls) == 0:
                print("GAME OVER")
                endProgram = True

    ###############################################################
    # Check collision with paddle
    balls_to_append = []
    for ball in balls:

        # Add score for hitting the ball
        if ball[0].colliderect(paddle):
            if ball[3] == (0, 0, 255):
                score += 1
            elif ball[3][0] > 0:
                score += 2
            else:
                score += 3
            scoreGraphic = myfont.render(str(score), True, (255, 255, 255))

            # If there is only one (not green) ball left, speed it up every time it hits the paddle:
            if len(balls) == 1 and balls[0][3][1] == 0:
                if balls[0][1] > 0:
                    balls[0][1] += 1
                else:
                    ball[0][1] -= 1
                if balls[0][2] > 0:
                    balls[0][2] += 1
                else:
                    balls[0][2] -= 1

            # When ball stucks between the bottom wall and the paddle
            if paddle.top < ball[0].top:
                balls.remove(ball)
                if len(balls) == 0:
                    endProgram = True

            else:
                # IF the ball hits the left side of the paddle
                if (
                    (ball[0].centerx <= paddle.left)
                    and (ball[0].left < paddle.left)
                    and (ball[0].bottom > paddle.centery)
                ):
                    ball[0].y = ball[0].y - ball[0].width / 2

                # IF the ball hits the right side of the paddle
                elif (
                    (ball[0].centerx >= paddle.right)
                    and (ball[0].right > paddle.right)
                    and (ball[0].bottom > paddle.centery)
                ):
                    ball[0].y = ball[0].y - ball[0].width / 2

                # If the ball hits the paddle normally
                # First checking if the red ball hits the paddle, then split the ball in 2
                if ball[3] == (255, 0, 0):
                    ball1 = Rect(ball[0].x, ball[0].y + ball[0].width / 2, ball[0].width / 2, ball[0].width / 2)
                    ball2 = Rect(ball[0].x, ball[0].y + ball[0].width / 2, ball[0].width / 2, ball[0].width / 2)
                    balls_to_append.append(
                        [
                            ball1,
                            abs(random.choice(dx)) * (-1),
                            abs(random.choice(dy)) * (-1),
                            (255, 0, 100),
                            0,
                            0,
                        ]
                    )
                    balls_to_append.append(
                        [
                            ball2,
                            abs(random.choice(dx)),
                            abs(random.choice(dy)) * (-1),
                            (255, 0, 100),
                            0,
                            0,
                        ]
                    )
                    balls.remove(ball)
                else:
                    ball[1] = abs(ball[1])

                # IF the ball hits the left half of the paddle
                if ball[0].centerx <= paddle.centerx:
                    ball[1] = abs(ball[1]) * -1
                    ball[2] = abs(ball[2]) * (-1)

                # IF the ball hits the right half of the paddle
                else:
                    ball[1] = abs(ball[1])
                    ball[2] = abs(ball[2]) * (-1)

    # Add the new red balls
    for b in balls_to_append:
        balls.append(b)

    ########################################################################
    # DRAWING
    screen.fill((0, 0, 0))

    # Balls
    for ball in balls:
        draw.ellipse(screen, ball[3], ball[0])
    # Draw paddle
    draw.rect(screen, (255, 255, 255), paddle)

    # IF GAME OVER, print on screen the points
    if endProgram is True:
        screen.blit(testGraphic, (width / 3, height / 4))
        screen.blit(scoreGraphic, (width / 2, height / 2))
    # Print the score in the upper left corner
    else:
        screen.blit(scoreGraphic, (50, 0))
    # FPS
    animationTimer.tick(110)
    # Update the screen
    display.update()

    if endProgram is True:
        sleep(3)

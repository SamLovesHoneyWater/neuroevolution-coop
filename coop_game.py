# RealThink Standard Pygame Framework
import pygame, random
import numpy as np
from bat_ai import Bat, Imm, Hax, FC

# screen and render constants
SCREEN_H = 512
SCREEN_W = 1024
# color constants
PALETTE = ((64,64,64),(255,255,255),(64, 255-64, 255-64),(0,0,0))
BG_COLOR = 0
DARK_COLOR = 3
BALL_COLOR = 1
BAT_COLOR = 2
# ball constants
BALL_SIZE = 16
# bat constants
BAT_OFFSET = 32
BAT_SPEED = 8 * -1  # intuitively inverted y-axis
# dark constants
DARK_FRAME = 10

def runAI(bat, ball_x, ball_y, guider=None):
    if type(bat.ai) == str:
        if bat.ai == "Imm":
            bat.move = Imm()
        elif bat.ai == "Hax":
            bat.move = Hax(bat.x, bat.y, ball_x, ball_y)
    elif type(bat.ai) == list:
        if guider is not None:
            _ = FC(guider, bat.x/SCREEN_W, bat.y/SCREEN_H,\
                          ball_x/SCREEN_W, ball_y/SCREEN_H, guider.z[2])
            bat.move = FC(bat, bat.x/SCREEN_W, bat.y/SCREEN_H,\
                          guider.z[0], guider.z[1], guider.z[2])
        else:
            bat.move = FC(bat, bat.x/SCREEN_W, bat.y/SCREEN_H,\
                          ball_x/SCREEN_W, ball_y/SCREEN_H, bat.z[2])
    else:
        print("No such AI as " + bat.ai)
        return 0
    return 1

def runOB(bat, ball_x, ball_y):
    runAI(bat, ball_x, ball_y)
    return bat.z

def drawBall(screen, x, y, color = BALL_COLOR):
    rgb = PALETTE[color]
    pygame.draw.rect(screen, rgb, (x, y, BALL_SIZE, BALL_SIZE), 0)
    return
def drawBat(screen, bat, color = BAT_COLOR):
    rgb = PALETTE[color]
    pygame.draw.rect(screen, rgb, (bat.x, bat.y, bat.w, bat.h), 0) 
    return
def getBallDY():    # dy <- [-4, 4)
    return (random.random() - 0.5) * 16
def endGame(left, right, v):    # end game clean up; returns 1/0 upon S/E
    try:
        if v:
            pygame.quit()
        return 1
    except:
        return 0

def runCoopGame(ai_0, ai_1, observers=[], v=False, timeout=0):
    score = 0
    # ball init
    ball_dx = 16      # right > 0, left < 0
    ball_dy = getBallDY()
    ball_x = SCREEN_W // 2
    ball_y = SCREEN_H // 2
    # bat init
    left = Bat(0, ai_0)
    left.x = BAT_OFFSET
    left.y = SCREEN_H//2 - left.h//2
    shadow_left = Bat(0, ai_1)
    shadow_left.x = left.x
    shadow_left.y = left.y
    observer_bats = []
    for i in observers:
        ob = Bat(0, i)
        ob.x = left.x
        ob.y = left.y
        observer_bats.append(ob)
    right = Bat(1, "Hax")
    right.x = SCREEN_W - BAT_OFFSET
    right.y = SCREEN_H//2 - right.h//2
    # visualization
    if v:
        pygame.init()
        clock = pygame.time.Clock()
        screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
        pygame.display.set_caption("game")
    # main game loop
    while True:
        # timer
        score += 1
        if timeout:
            if score > timeout:
                endGame(left, right, v)
                return score
        # ball motion
        ball_x += ball_dx
        ball_y += ball_dy
        # ball collide with bounds
        if ball_y <= 0:
            ball_dy *= -1
            ball_y = 0
        elif ball_y >= SCREEN_H - BALL_SIZE:
            ball_dy *= -1
            ball_y = SCREEN_H - BALL_SIZE
        # ball out of bounds
        if ball_x <= 0:
            # left loses game
            endGame(left, right, v)
            return score
        elif ball_x >= SCREEN_W - BALL_SIZE:
            # right loses game
            endGame(left, right, v)
            return score
        # bat motion
        runAI(left, ball_x, ball_y, guider=shadow_left) # default left side blind, right side Mom
        z_list = []
        z_list.append(runOB(shadow_left, ball_x, ball_y))
        for ob_bat in observer_bats:
            z_list.append(runOB(ob_bat, ball_x, ball_y))
        runAI(right, ball_x, ball_y)
        left.y += left.move * BAT_SPEED
        right.y += right.move * BAT_SPEED
        # bats out of bounds
        if left.y < 0:
            left.y = 0
            left.move = 0
        if left.y > SCREEN_H - left.h:
            left.y = SCREEN_H - left.h
            left.move = 0
        if right.y < 0:
            right.y = 0
            right.move = 0
        if right.y > SCREEN_H - right.h:
            right.y = SCREEN_H - right.h
            right.move = 0
        # sync shadow with real left
        shadow_left.y = left.y
        for ob_bat in observer_bats:
            ob_bat.y = left.y
        # ball collide with bat
        if ball_x <= left.x + left.w and ball_y < left.y + left.h and ball_y > left.y - BALL_SIZE:
            # left bat
            ball_dx *= -1
            ball_dy = getBallDY()
            ball_x = left.x + left.w
        elif ball_x >= right.x - BALL_SIZE and ball_y < right.y + right.h and ball_y > right.y - BALL_SIZE:
            # right bat
            ball_dx *= -1
            ball_dy = getBallDY()
            ball_x = right.x - BALL_SIZE
        # visualization
        if v:
            # traverse events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    endGame(left, right, v)
                    return score
            # render
            else:
                screen.fill(PALETTE[BG_COLOR])
            drawBall(screen, ball_x, ball_y)
            drawBat(screen, left)
            drawBat(screen, right)
            pygame.display.update()
            clock.tick(144)
        z_arr = np.array(z_list)
        if score % 3 and len(observers) != 0:
            print(z_arr.transpose())
            print()

if __name__ == "__main__":
    print("> Warning: running game as __main__")
    runCoopGame(v=True)

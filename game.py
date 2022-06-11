# RealThink Standard Pygame Framework
import pygame, random
from bat_ai import Bat, Imm, Hax, FC

# screen and render constants
SCREEN_H = 512
SCREEN_W = 1024
# color constants
PALETTE = ((64,64,64),(255,255,255),(255,0,255),(0,0,0))
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

def runAI(bat, ball_x, ball_y, is_dark):
    # dark_k is legacy. What matter is only whether it is zero or not.
    if type(bat.ai) == str:
        if bat.ai == "Imm":
            bat.move = Imm()
        elif bat.ai == "Hax":
            bat.move = Hax(bat.x, bat.y, ball_x, ball_y)
    elif type(bat.ai) == list:
        if is_dark:
            bat.move = FC(bat, bat.x/SCREEN_W, bat.y/SCREEN_H,\
                          bat.z[0], bat.z[1], bat.z[2])
        else:
                bat.move = FC(bat, bat.x/SCREEN_W, bat.y/SCREEN_H,\
                              ball_x/SCREEN_W, ball_y/SCREEN_H, bat.z[2])
    else:
        print("No such AI as " + bat.ai)
    return

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

def endGame(left, right, save_0, save_1, v):    # end game clean up; returns 1/0 upon S/E
    if save_0:
        left.save(save_0)
    if save_1:
        right.save(save_1)
    try:
        if v:
            pygame.quit()
        return 1
    except:
        return 0

def runGame(ai_0="Imm", ai_1="Hax", save_0=None, save_1=None, dark_k=0, v=False, timeout=0):
    if save_0 and type(ai_0.ai) == str:
        print(">  AITypeError: Left AI of type " + ai_0 + " cannot be saved.")
        return -1
    if save_1 and type(ai_1.ai) == str:
        print(">  AITypeError: Right AI of type \"" + ai_1 + "\" cannot be saved.")
        return -1
    score = 0
    is_dark = False
    # ball init
    ball_dx = 16      # right > 0, left < 0
    ball_dy = getBallDY()
    ball_x = SCREEN_W // 2
    ball_y = SCREEN_H // 2
    # bat init
    left = Bat(0, ai_0)
    left.x = BAT_OFFSET
    left.y = SCREEN_H//2 - left.h//2
    right = Bat(1, ai_1)
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
                endGame(left, right, save_0, save_1, v)
                return score
        # ball motion
        ball_x += ball_dx
        ball_y += ball_dy
        # ball collide with bounds
        if ball_y <= 0 or ball_y >= SCREEN_H - BALL_SIZE:
            ball_dy *= -1
        # ball out of bounds
        if ball_x <= 0:
            # left loses game
            endGame(left, right, save_0, save_1, v)
            return score
        elif ball_x >= SCREEN_W - BALL_SIZE:
            # right loses game
            endGame(left, right, save_0, save_1, v)
            return score
        # bat motion
        '''
        is_dark = False
        if ball_x < left.x + SCREEN_W * dark_k:
            is_dark = True
        elif ball_x > right.x - SCREEN_W * dark_k:
            is_dark = True
            #'''
        '''
        if score % DARK_FRAME == 1:
            if dark_k:
                is_dark = random.random() < dark_k
                #'''
        if dark_k:
            is_dark = not is_dark
        #is_dark = random.random() < dark_k
        runAI(left, ball_x, ball_y, is_dark)
        runAI(right, ball_x, ball_y, is_dark)
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
                    endGame(left, right, save_0, save_1, v)
                    return score
            # render
            if is_dark:
                screen.fill(PALETTE[DARK_COLOR])
            else:
                screen.fill(PALETTE[BG_COLOR])
            drawBall(screen, ball_x, ball_y)
            drawBat(screen, left)
            drawBat(screen, right)
            pygame.display.update()
            clock.tick(144)

if __name__ == "__main__":
    print("> Warning: running game as __main__")
    run_game(v=True)

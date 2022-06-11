# -*- coding: utf-8 -*-
"""
Created on Sun May 29 18:42:58 2022

@author: Sammy
"""

import numpy as np

# bat constants
BAT_H = 48
BAT_W = 16
RECUR_SIZE = 3
L1_HIDDEN = 8
L2_HIDDEN = 4
OUT_SIZE = 3
class Bat(object):
    def __init__(self, pos, ai):
        self.pos = pos      # 0 = left, 1 = right
        self.x = 0
        self.y = 0
        self.ai = ai
        if type(self.ai) == str:
            if self.ai == "FC":
                self.ai = self.initParams()
        self.h = BAT_H
        self.w = BAT_W
        self.move = 0   # 1 up, -1 down, 0 still
        self.z = np.zeros((RECUR_SIZE,))      # language unit
    def initParams(self):
        params = []
        params.append(np.zeros((4+RECUR_SIZE-2, L1_HIDDEN)))     # w1
        params.append(np.zeros((1, L1_HIDDEN)))     # b1
        params.append(np.zeros((L1_HIDDEN, L2_HIDDEN)))     # w2
        params.append(np.zeros((1, L2_HIDDEN)))             # b2
        params.append(np.zeros((L2_HIDDEN, OUT_SIZE + RECUR_SIZE)))     # w3
        params.append(np.zeros((RECUR_SIZE,)))                          # b3
        
        return params
# Save and load ai params
def save(ai, filename):
    np.save(filename, ai)
def load(filename):
    ai = list(np.load(filename+".npy", allow_pickle=True))
    return ai
# With this AI, the bat stays still
def Imm():
    return 0
# With this AI, the bat follows the ball
def Hax(bat_x, bat_y, ball_x, ball_y):
    if bat_y + BAT_H // 2 > ball_y + 4:
        return 1
    else: return -1
# Fully connected neural network AI
def FC(bat, x1, y1, x2, y2, z):
    w1 = bat.ai[0]
    b1 = bat.ai[1]
    w2 = bat.ai[2]
    b2 = bat.ai[3]
    w3 = bat.ai[4]
    b3 = bat.ai[5]
    if bat.pos:     # standardize perspective: when ball is near, ball_x ~ 0
        x1 = 1 - x1
        x2 = 1 - x2
    x_list = [x1, y1, x2, y2, z]
    x = np.array(x_list)
    z1 = np.dot(x, w1) + b1
    a1 = np.maximum(z1, 0)
    z2 = np.dot(a1, w2) + b2
    a2 = np.maximum(z2, 0)
    z3 = np.dot(a2, w3).flatten()
    bat.z = z3[OUT_SIZE:] + b3
    y = np.argsort(z3[:OUT_SIZE])[-1]
    if y == 0:
        return 1
    elif y == 1:
        return -1
    else:
        return 0

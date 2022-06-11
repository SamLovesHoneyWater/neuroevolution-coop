# -*- coding: utf-8 -*-
"""
Created on Tue May 31 18:28:00 2022

@author: Sammy
"""

import numpy as np
from statistics import median
from coop_game import runCoopGame
from game import runGame
from bat_ai import load, save
from local_evolution import ParamPrint
from get_coop_agents import SAVE_DIR
ELITE_PATH = "saved_agents/elites/"
DUMMY_PATH = "saved_agents/dummies/"
TIMEOUT = 6000
CANDIDATE_TIMEOUT = 1000

def evaluateAI(ai, dark=1, trials=1, mode="max", v=False):
    scores = []
    for i in range(trials):
        score = runGame(ai_0=ai, dark_k=dark, v=False, timeout=TIMEOUT)
        #score = runCoopGame(ai, ai, v=v, timeout=TIMEOUT)
        scores.append(score)
        if mode == 'max':
            if score >= TIMEOUT:
                return score
    if mode == 'max':
        return max(scores)
    elif mode == 'avg':
        return sum(scores)//trials
    else:
        print("> Error: Unknown evaluateAI mode \"" + mode + "\".")
        return None
def cleanSpecies(species, trials, pop_size, desired_size, dark=1):
    fitness_list = np.zeros((pop_size,), dtype=np.int32)
    for i in range(pop_size):
        ai = loadPath((species, i))
        score = evaluateAI(ai, dark=dark, trials=trials)
        fitness_list[i] = score
    print("Species", species, ", score", fitness_list)
    ranks = np.argsort(fitness_list)
    for i in range(desired_size):
        if(fitness_list[ranks[-i-1]] < TIMEOUT):
            continue
        ai = loadPath((species, ranks[-i-1]))
        save(ai, ELITE_PATH + "elite_" + str(species) + "_" + str(i))
    return
def roundRobin(trials, max_index, desire_size=1, v=False):
    ai_list = []
    for i in range(max_index + 1):
        for j in range(desire_size):
            name = "elite_" + str(i) + "_" + str(j)
            try:
                ai = load(ELITE_PATH + name)
            except:
                print("> Warning: Failed to load AI", name)
                ai = None
            if ai is not None:
                ai_list.append(ai)
    total_ai = len(ai_list)
    result_list = np.zeros((total_ai, total_ai))
    for i in range(total_ai):
        for j in range(total_ai):
            if i == j:
                result = 0
            else:
                result = testCompat(ai_list[i], ai_list[j], trials, v=v)
                result_list[i][j] = result
        print(result_list[i])
    return result_list
def testCompat(actor, ghost, trials, mode="median", v=False):
    scores = []
    for i in range(trials):
        score = runCoopGame(actor, ghost, v=v, timeout=CANDIDATE_TIMEOUT)
        # if able to produce enough output, it should be rigorous!
        if score >= CANDIDATE_TIMEOUT:
            return score
        scores.append(score)
        if v:
            print("Trial", i, "received score", score)
    if mode == 'max':
        return max(scores)
    elif mode == 'avg':
        return sum(scores)//trials
    elif mode == 'median':
        return median(scores)
    else:
        print("> Error: Unknown testCompat mode \"" + mode + "\".")
        return None
def runOneControl(dummy, trials, max_index, desire_size=1, v=False):
    name = "elite_" + str(dummy) + "_" + str(0)
    try:
        dummy = load(DUMMY_PATH + name)
    except:
        print("> Warning: Failed to load dummy AI", name)
        return None
    ai_list = []
    for i in range(max_index + 1):
        for j in range(desire_size):
            name = "elite_" + str(i) + "_" + str(j)
            try:
                ai = load(ELITE_PATH + name)
            except:
                print("> Warning: Failed to load AI", name)
                ai = None
            if ai is not None:
                ai_list.append(ai)
    total_ai = len(ai_list)
    result_list = np.zeros((total_ai, ))
    for i in range(total_ai):
        result = testCompat(ai_list[i], dummy, trials, v=v)
        result_list[i] = result
    return result_list
def runAllControl(minmax, trials, max_index, desire_size=1, v=False):
    result_list = []
    for i in range(minmax[0], minmax[1]+1):
        r = runOneControl(i, trials, max_index, desire_size=desire_size, v=v)
        result_list.append(r)
        print(r)
    return result_list

def runCoop(ai_0, ai_1, trials=1, v=False):
    left = loadPath(ai_0)
    right = loadPath(ai_1)
    max_score = 0
    for i in range(trials):
        score = runCoopGame(left, right, v=v, timeout=CANDIDATE_TIMEOUT)
        if score >= CANDIDATE_TIMEOUT:
            return score
        max_score = max(score, max_score)
        if v:
            print("Trial", i, "received score", score)
    return max_score

def getCoopResult(species_0, species_1, trials, pop_size):
    high_score = 0
    significants = []
    for a in range(0, pop_size):
        print("Starting child", a)
        for b in range(pop_size):
            score = runCoop((species_0, a), (species_1, b), trials=trials)
            if score > high_score:
                high_score = score
                print("> New high score:", score, "by individuals", a, "and", b)
            if score >= CANDIDATE_TIMEOUT:
                significants.append(((species_0, a), (species_1, b)))
    return significants
def loadPath(identifier):
    (species, indiv) = identifier
    filename = SAVE_DIR + str(species) + "/" + "pop_" + str(indiv)
    try:
        ai = load(filename)
    except:
        print("> Error: Failed to load saved agent", identifier)
        return None
    return ai
def printAI(identifier):
    ai = loadPath(identifier)
    ParamPrint(ai)
    return
def monitorZ(main_ai, ob_list):
    ai = loadPath(main_ai)
    for i in range(len(ob_list)):
        ai = loadPath(ob_list[i])
        ob_list[i] = ai
    runCoopGame(ai, ai, observers=ob_list, v=False, timeout=9000)
    return

if __name__ == "__main__":
    runAllControl((100, 124), 20, 26)
    '''
    for i in range(100, 125):
         cleanSpecies(i, 5, 100, 1, dark=0)
         '''
    '''
    name = "elite_" + str(12) + "_" + str(0)
    try:
        actor = load(ELITE_PATH + name)
    except:
        print("> Warning: Failed to load AI", name)
    name = "elite_" + str(1) + "_" + str(0)
    try:
        ghost = load(ELITE_PATH + name)
    except:
        print("> Warning: Failed to load AI", name)
    testCompat(actor, ghost, 5, v=True)
    '''
    #proximity_matrix = roundRobin(20, 26)
    #np.savetxt("median.csv", proximity_matrix, delimiter=",", fmt="%d")
    '''
    for i in range(0, 27):
        cleanSpecies(i, 5, 100, 1)
        '''
    #print(getCoopResult(0, 3, 3, 30))
    #runCoop((0, 1), (1, 92), v=True)
    #runCoop((2, 52), (0, 33), v=True)
    #runCoop((1, 7), (2, 36), v=True)
    #runCoop((1, 78), (2, 34), v=True)
    #runCoop((2, 0), (1, 3), v=True)
    #runCoop((2, 0), (1, 36), v=True)
    #runCoop((2, 0), (1, 66), v=True)
    #runCoop((2, 1), (1, 66), v=True)
    ##runCoop((2, 8), (1, 0), v=True)
    #runCoop((2, 8), (1, 1), v=True)
    #runCoop((2, 8), (1, 22), v=True)
    #runCoop((2, 8), (1, 29), v=True)
    #runCoop((2, 8), (1, 47), v=True)
    #runCoop((2, 9), (1, 66), v=True)
    #runCoop((2, 9), (1, 85), v=True)
    #runCoop((2, 11), (1, 22), v=True)
    #runCoop((2, 11), (1, 50), v=True)
    ##runCoop((2, 11), (1, 60), v=True)
    #runCoop((2, 11), (1, 66), v=True)
    #runCoop((2, 11), (1, 84), v=True)
    #runCoop((2, 11), (1, 85), v=True)
    #runCoop((2, 13), (1, 22), v=True)
    #runCoop((2, 13), (1, 66), v=True)
    #runCoop((2, 14), (1, 66), v=True)
    #runCoop((2, 16), (1, 36), v=True)
    #runCoop((2, 16), (1, 66), v=True)
    ##runCoop((2, 16), (1, 85), v=True)
    #runCoop((2, 17), (1, 66), v=True)  # interesting performance!
    #runCoop((2, 18), (1, 43), v=True)
    ##runCoop((2, 18), (1, 85), v=True)
    #runCoop((2, 21), (1, 23), v=True)
    #runCoop((2, 21), (1, 38), v=True)
    #runCoop((2, 21), (1, 85), v=True)
    #runCoop((2, 29), (1, 66), v=True)
    ##runCoop((3, 36), (0, 33), v=True)     # bad but fun performance!
    #runCoop((3, 63), (0, 71), v=True)
    #runCoop((3, 75), (0, 33), v=True)
    #runCoop((3, 75), (0, 71), v=True)
    #runCoop((3, 75), (0, 72), v=True)
    ##runCoop((3, 75), (0, 78), trials=100, v=True)   # bad but fun performance!
    '''
    runCoop((0, 1), (1,92), v=True)
    printAI((0, 1))
    printAI((1, 92))
    printAI((1, 0))
    '''
    
# -*- coding: utf-8 -*-
"""
Created on Sun May 29 20:06:33 2022

@author: Sammy
"""

import random
import numpy as np
from game import runGame
from bat_ai import Bat, save, load

# game constants
SAVE_DIR = "saved_agents/recurlonewolf_temp/"
TIMEOUT = 6000     # 0 -> no timeout; positive int -> end game when score reached
# dark constant
MAX_DARK = .8
# evolution constants
CONSEQ_MAX_N = 6
MUTATION_RATE = .05     # mutated params / total params

# visualize_per_n_rounds: v when g%n == 0; if n == 0, do not visualize; if n == -1, visualize at end
def evolveLoneWolf(generations, pop_size, eval_runs, savepath, init_pops=None, dark_k=0 , vpn=-1):
    fitness_list = np.zeros((pop_size,))
    best_fitness_history = []
    if not init_pops:   # no prescribed pops list
        pops = []
        for i in range(pop_size):
            agent = Bat(0, "FC").ai
            pops.append(agent)
    else:
        if type(init_pops) != list:     # type check
            print("> Error: population argument expected a list, got "+str(type(init_pops)))
            return None
        elif len(init_pops) != pop_size: # size check
            print("> Error: arguments pop_size and length of init_pops do not match.")
        else:
            pops = init_pops
    # start evolution
    for g in range(generations):
        children = []
        for i in range(pop_size):
            score = 0     # cummulative score
            agent = pops[i]
            for j in range(eval_runs):
                score += runGame(ai_0=agent, dark_k=dark_k, timeout=TIMEOUT)
            fitness_list[i] = score     # overwrites previous scores
        fitness_list /= eval_runs
        best_fitness_history.append(np.max(fitness_list))
        if(g >= CONSEQ_MAX_N):
            best_fitness_history.pop(0)
        recent_avg_fitness = int(sum(best_fitness_history)/len(best_fitness_history))
        print("> Generation "+str(g)+": best = "+str(np.max(fitness_list))+\
              "\trecent avg best = "+str(recent_avg_fitness))
        best_ai = pops[np.argsort(fitness_list)[-1]]
        if vpn > 0 and g % vpn == 0 and g:
            score = runGame(ai_0=best_ai, dark_k=dark_k, v=True, timeout=3000)
            for i in range(len(pops)):
                save(pops[i], SAVE_DIR + "pop_" + str(i))
            print("> The AI scored "+str(int(score))+" points in this visualization.")
            ParamPrint(best_ai)
        fitness_list -= np.min(fitness_list)
        fitness_list += 0.0000001       # prevent divByZero error with small offset
        fitness_list /= np.sum(fitness_list)
        offspring_parent_indices = np.random.choice(pop_size, size=pop_size, p=fitness_list)
        for i in offspring_parent_indices:
            if dark_k:
                children.append(mutate_mask(pops[i], .1))
            else:
                children.append(mutate_mask(pops[i], .1))
        children[0] = pops[np.argsort(fitness_list)[-1]]
        children[1] = pops[np.argsort(fitness_list)[-1]]
        children[2] = pops[np.argsort(fitness_list)[-1]]
        children[3] = pops[np.argsort(fitness_list)[-2]]
        children[4] = pops[np.argsort(fitness_list)[-2]]
        children[5] = pops[np.argsort(fitness_list)[-3]]
        pops = children
        if recent_avg_fitness >= TIMEOUT:
            break
    if vpn != 0:
        score = runGame(ai_0=best_ai, dark_k=dark_k, v=True, timeout=3000)
        print("> The AI scored "+str(int(score))+" points in this visualization.")
        ParamPrint(best_ai)
    for i in range(len(pops)):
        save(pops[i], savepath + "pop_" + str(i))
    return pops

def evolveDarkWolf(pop_size, savepath, v=False):
    if v:
        vpn = 20
    else:
        vpn = 0
    score = 0
    while score < TIMEOUT:
        pops = evolveLoneWolf(149, pop_size, 1, savepath, vpn=0)    # start from scratch
        score = 0     # species score
        for i in range(3):
            agent = pops[i]
            score += runGame(ai_0=agent, timeout=TIMEOUT)
        score /= 3
    '''
    else:       # start from pretrained pops
        pops = []
        for i in range(pop_size):
            pops.append(load("saved_agents/rigorous_starter_pack_1/" + "pop_" + str(i)))
        pops = evolveLoneWolf(1, pop_size, 1, init_pops=pops, vpn=0)
        '''
    pops = evolveLoneWolf(20, pop_size, 12, savepath, init_pops=pops, dark_k=1, vpn=vpn)
    pops = evolveLoneWolf(20, pop_size, 12, savepath, init_pops=pops, dark_k=1, vpn=vpn)
    pops = evolveLoneWolf(20, pop_size, 12, savepath, init_pops=pops, dark_k=1, vpn=vpn)
    pops = evolveLoneWolf(20, pop_size, 12, savepath, init_pops=pops, dark_k=1, vpn=vpn)
    return pops

def mutate_point(parent):
    child = [param.copy() for param in parent]
    for i in range(len(child)):
        arr = child[i]
        shape = arr.shape
        if len(shape) == 1:    # bias vector
            for x in range(shape[0]):
                child[i][x] += random.gauss(0)
        else:       # weight matrix
            for y in range(shape[0]):
                for x in range(shape[1]):
                    if random.random() < 0.3:
                        child[i][y][x] += random.gauss(0)
    return child


def mutate_mask(parent, sigma=0.05):
    child = [param.copy() for param in parent]
    for i in range(len(child)):
        mask = np.random.normal(0, sigma, size=child[i].shape)    # gaussian mask
        child[i] += mask
    return child

def ParamPrint(ai):
    print("> Info: AI matrix structure:")
    print("Layer 1 weights:")
    print("", end = '')
    print(ai[0])
    print("Layer 1 biases:")
    print("", end = '')
    print(ai[1])
    print("Layer 2 weights:")
    print("", end = '')
    print(ai[2])
    print("Layer 2 biases:")
    print("", end = '')
    print(ai[3])
    print("Layer 3 weights:")
    print("", end = '')
    print(ai[4])
    print("Layer 3 biases:")
    print("", end = '')
    print(ai[5])
    print("")

if __name__ == "__main__":
    import os
    for i in range(110, 125):
         score = 0
         os.mkdir("saved_agents/species_"+str(i)+'/')
         while score < TIMEOUT:
             pops = evolveLoneWolf(117, 100, 3, "saved_agents/species_"+str(i)+'/', vpn=0)
             score = 0     # species score
             for j in range(3):
                 agent = pops[j]
                 score += runGame(ai_0=agent, timeout=TIMEOUT)
             score /= 3
    #evolveDarkWolf(100, SAVE_DIR, v=True)

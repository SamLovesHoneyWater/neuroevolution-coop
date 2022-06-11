# -*- coding: utf-8 -*-
"""
Created on Sun May 29 20:06:33 2022

@author: Sammy
"""

import numpy as np
from game import run_game
from bat_ai import Bat

# game constants
SAVE_DIR = "save_agents/lonewolf_temp"
TIMEOUT = 9000     # 0 -> no timeout; positive int -> end game when score reached

# visualize_per_n_rounds: v when g%n == 0; if n == 0, do not visualize; if n == -1, visualize at end
def evolveLoneWolf(generations, pop_size, eval_runs, visualize_per_n_rounds = 0):
    pops = []
    fitness_list = np.zeros((pop_size,))
    for i in range(pop_size):
        agent = Bat(0, "FC").ai
        pops.append(agent)
    for g in range(generations):
        children = []
        for i in range(pop_size):
            score = 0     # cummulative score
            agent = pops[i]
            #agent = mutate(pops)
            for j in range(eval_runs):
                score += run_game(ai_0=agent, timeout=TIMEOUT)
            fitness_list[i] = score     # overwrites previous scores
        print("> Generation "+str(g)+": best fitness = "+str(np.max(fitness_list)))
        best_ai = pops[np.argsort(fitness_list)[-1]]
        if visualize_per_n_rounds > 0 and g % visualize_per_n_rounds == 0:
            score = run_game(ai_0=best_ai, v=True, timeout=0)
            print("> The AI scored "+str(score)+" points in this visualization.")
            print("\tHere is its matrix structure:")
            print("\t\tLayer 1 weights:")
            print("\t\t", end = '')
            print(best_ai[0])
            print("\t\tLayer 1 biases:")
            print("\t\t", end = '')
            print(best_ai[1])
            print("\t\tLayer 2 weights:")
            print("\t\t", end = '')
            print(best_ai[2])
            print("\t\tLayer 2 biases:")
            print("\t\t", end = '')
            print(best_ai[3])
        fitness_list -= np.min(fitness_list)
        fitness_list += 0.0000001       # prevent divByZero error with small offset
        fitness_list /= np.sum(fitness_list)
        offspring_parent_indices = np.random.choice(pop_size, size=pop_size, p=fitness_list)
        for i in offspring_parent_indices:
            children.append(mutate(pops[i]))
        pops = children
    if visualize_per_n_rounds == -1:
        _ = run_game(ai_0=best_ai, v=True, timeout=TIMEOUT)
    return

def mutate(parent):
    child = [param.copy() for param in parent]
    for i in range(len(child)):
        mask = np.random.normal(0, 0.1, size=child[i].shape)
        child[i] += mask
    return child
    
if __name__ == "__main__":
    evolveLoneWolf(100, 100, 1, 40)

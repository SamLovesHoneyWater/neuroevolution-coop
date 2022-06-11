# -*- coding: utf-8 -*-
"""
Created on Tue May 31 17:59:10 2022

@author: Sammy
"""

from local_evolution import evolveDarkWolf
import os
SAVE_DIR = "saved_agents/species_"

def get_coop_agents(n_species):
    start = eval(input("What is the numbering of the last existing species?\t"))
    for i in range(start + 1, n_species):
        savepath = SAVE_DIR + str(i) + "/"
        try:
            os.mkdir(savepath)
        except:
            print("Folder creation failed for species " + str(i))
        pops = evolveDarkWolf(100, savepath)
        
if __name__ == "__main__":
    get_coop_agents(100)

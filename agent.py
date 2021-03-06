# -*- coding: utf-8 -*-
"""
Created on Wed Mar 25 10:26:20 2020

@author: metalcorebear
"""

from mesa import Agent
import model_functions

#Agent class
class tweeter(Agent):
    
    def __init__(self, unique_id, pos, model, neg_bias, meme_density):
        super().__init__(unique_id, model)
        self.pos = pos
        self.valence = model_functions.set_magnitude(neg_bias)
        self.meme_state = model_functions.set_meme(meme_density, self.valence)
        
    def step(self):
        edge_valences = []
        homophily = 0.0
        if self.meme_state == False:
            for neighbor in self.model.grid.get_neighbors(self.pos):
                neighbor_obj = self.model.schedule.agents[neighbor]
                if neighbor_obj.meme_state == True:
                    edge_valence = model_functions.find_edge_valence(self.valence, neighbor_obj.valence)
                    edge_valences.append(edge_valence)
                else:
                    edge_valences.append(0.0)
            
            if len(edge_valences) != 0:
                homophily = sum(edge_valences)/float(len(edge_valences))
            else:
                homophily = 0.0
            if homophily > 0:
                self.meme_state = model_functions.set_meme(homophily, self.valence)
            else:
                self.meme_state = self.meme_state
            if self.meme_state == True:
                self.model.meme += 1
        
        else:
            self.model.meme += 0

# -*- coding: utf-8 -*-
"""
Created on Fri Apr 15 18:55:01 2022

@author: reffay_m
"""


import sys
import math

# Save humans, destroy zombies!
while True: #while True, another turn begins
    
    list_humans=[]
    list_zombies=[]
    list_save_index=[]
    
    # Part 1 : get the different infos about the current situation
    
    # we get our character Ash position infos
    x, y = [int(i) for i in input().split()]
    # we get the positions of all the other humans
    human_count = int(input())
    for i in range(human_count):
        list_humans.append([int(j) for j in input().split()])
    # we get the positions of all zombies
    zombie_count = int(input())
    for i in range(zombie_count):
        list_zombies.append([int(j) for j in input().split()])
    count_zombie_nearest=[0]*zombie_count # initialization of the nearest zombie
    
    # Part 2 : look for the individual that would allow us to save the most people if we go towards him
    
    distance_Ash_indiv=0 #distance between Ash and a given individual
    nb_turns_save_indiv=0
    distance_indiv_zombie=0
    distance_indiv_zombie_min=math.sqrt(16000**2+9000**2) #initiate with the maximum distance possible
    nb_turns_kill_indiv=0
    index_better_indiv_choice=0

    for i in list_humans:
        distance_Ash_indiv=math.sqrt((x-i[1])**2+(y-i[2])**2)
        list_save_index.append(0)
        nb_turns_save_indiv=distance_Ash_indiv//1000 # calculation of the number of turns needed to get at a distance sufficient to save the individual
        for j in list_zombies:
            distance_indiv_zombie=math.sqrt((i[1]-j[1])**2+(i[2]-j[2])**2)
            if distance_indiv_zombie<distance_indiv_zombie_min:
                distance_indiv_zombie_min=distance_indiv_zombie
                nb_turns_kill_indiv=distance_indiv_zombie//400
        if nb_turns_kill_indiv>=nb_turns_save_indiv: # if the individual can be saved
            distance_indiv_indiv=0 # distance between this individual and other individuals
            indice_indiv2_dead=0
            for k in list_humans:
                distance_indiv_indiv=math.sqrt((i[1]-k[1])**2+(i[2]-k[2])**2)
                if distance_indiv_indiv<2000: # if this distance is lower than the distance to which Ash can shoot
                    for j in list_zombies:
                        distance_indiv2_zombie=math.sqrt((j[1]-k[1])**2+(j[2]-k[2])**2)
                        if distance_indiv2_zombie//400<nb_turns_save_indiv:
                            indice_indiv2_dead=1
                            break
                    if indice_indiv2_dead==0:
                        list_save_index[-1]+=1 # if by the time we arrive to individual 1, individual 2 is not yet killed, we also save him
    index_better_indiv_choice=list_save_index.index(max(list_save_index)) # we get the index of the individual that saves the most individuals
    
    # Part 3 : go towards the chosen indivual or the nearest zombie from this individual if more efficient
    
    distance_chosenindiv_zombie=math.sqrt(16000**2+9000**2)
    x_zombie=0
    x_zombie_next=0
    y_zombie=0
    y_zombie_next=0
    for j in list_zombies:
        if math.sqrt((list_humans[index_better_indiv_choice][1]-j[1])**2+(list_humans[index_better_indiv_choice][2]-j[2])**2)<distance_chosenindiv_zombie: # get the distance from the chosen individual to the closest zombie
            x_zombie=j[1]
            y_zombie=j[2]
            x_zombie_next=j[3]
            y_zombie_next=j[4]
            distance_chosenindiv_zombie=math.sqrt((list_humans[index_better_indiv_choice][1]-j[1])**2+(list_humans[index_better_indiv_choice][2]-j[2])**2)
    if math.sqrt((x-list_humans[index_better_indiv_choice][1])**2+(y-list_humans[index_better_indiv_choice][2])**2)>math.sqrt((list_humans[index_better_indiv_choice][1]-x_zombie)**2+(list_humans[index_better_indiv_choice][2]-y_zombie)**2): 
        print(list_humans[index_better_indiv_choice][1],list_humans[index_better_indiv_choice][2]) # if the distance between chosen individual and Ash is greater than the istance between the zombie and the individual, we go towards the individual
    else:
        # else we go to the closest zombie from the chosen individual
        for j in list_zombies:
            if math.sqrt((list_humans[index_better_indiv_choice][1]-j[1])**2+(list_humans[index_better_indiv_choice][2]-j[2])**2)<distance_chosenindiv_zombie:
                x_zombie=j[3]
                y_zombie=j[4]
        print(x_zombie,y_zombie)
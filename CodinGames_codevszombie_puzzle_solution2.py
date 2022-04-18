import sys
import math
import numpy as np


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

    matrix_subscores=np.zeros((human_count,4))
    

    print(human_count, file=sys.stderr, flush=True)

    # Part 2 : look for the individual that would allow us to save the most people if we go towards him
    
    distance_Ash_indiv=0 #distance between Ash and a given individual
    nb_turns_save_indiv=0
    distance_indiv_zombie=0
    distance_indiv_zombie_min=math.sqrt(16000**2+9000**2) #initiate with the maximum distance possible
    nb_turns_kill_indiv=0
    index_better_indiv_choice=0
    index_human_count=0

# let s get the number of turns to get killed, the diff between number of turns to get killed and number of turns to be saved and the number of people around
    for i in list_humans:
        index_human_count+=1
        distance_Ash_indiv=math.sqrt((x-i[1])**2+(y-i[2])**2)
        list_save_index.append(0)
        nb_turns_save_indiv=distance_Ash_indiv//1000 # calculation of the number of turns needed to get at a distance sufficient to save the individual
        matrix_subscores[index_human_count-1,1]=nb_turns_save_indiv
        for j in list_zombies:
            distance_indiv_zombie=math.sqrt((i[1]-j[1])**2+(i[2]-j[2])**2)
            if distance_indiv_zombie<distance_indiv_zombie_min:
                distance_indiv_zombie_min=distance_indiv_zombie
                nb_turns_kill_indiv=distance_indiv_zombie//400
                matrix_subscores[index_human_count-1,2]=nb_turns_kill_indiv-matrix_subscores[index_human_count-1,1]
        for k in list_humans:
            distance_indiv_indiv=math.sqrt((i[1]-k[1])**2+(i[2]-k[2])**2)
            if distance_indiv_indiv<2000: # if this distance is lower than the distance to which Ash can shoot
                matrix_subscores[index_human_count-1,2]+=1

    matrix_subscores_sum=matrix_subscores.sum(axis=1)

    l=[]
    for i in range(human_count):
        for j in range(0,3):
            matrix_subscores[i,j]=matrix_subscores[i,j]/matrix_subscores_sum[i]
    for i in range(human_count):
        matrix_subscores[i,3]=matrix_subscores[i,2]-matrix_subscores[i,1]-matrix_subscores[i,0]
        l.append(matrix_subscores[i,3])
    index_better_indiv_choice=l.index(max(l))


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

    

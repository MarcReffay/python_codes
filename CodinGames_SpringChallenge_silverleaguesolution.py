# -*- coding: utf-8 -*-

import sys
import math
import random

###### STEP 1 : GET THE INITIAL INPUT INFO AND DEDUCT DEFENSIVE POSITION OF HEROES 

# location of my base
base_x, base_y = [int(i) for i in input().split()]
heroes_per_player = int(input())  # Always 3

if base_x<5000: # if the base is up left
    hero0_def_position_x=round(7000*math.cos(math.pi/9))
    hero0_def_position_y=round(7000*math.sin(math.pi/9))
    hero1_def_position_x=round(7000-7000*math.cos(math.pi/4)/2) # I don’t want this hero to go too far
    hero1_def_position_y=round(17360-7000*math.sin(math.pi/4)/2) # I don’t want this hero to go too
    hero2_def_position_x=round(7000*math.sin(math.pi/9))
    hero2_def_position_y=round(7000*math.cos(math.pi/9))
    base_enemy_x=17630
    base_enemy_y=9000
else: # if the base is down right
    hero0_def_position_x=round(7000-7000*math.cos(math.pi/9))
    hero0_def_position_y=round(17360-7000*math.sin(math.pi/9))
    hero1_def_position_x=round(7000*math.cos(math.pi/4)/2) # I don’t want this hero to go too far
    hero1_def_position_y=round(7000*math.sin(math.pi/4)/2# I don’t want this hero to go too far
    hero2_def_position_x=round(7000-7000*math.sin(math.pi/9))
    hero2_def_position_y=round(7000*math.cos(math.pi/9))
    base_enemy_x=0
    base_enemy_y=0

# print(base_x,base_y,file=sys.stderr,flush=True)

# game loop
while True:

    ###### STEP 2 : FOR EACH TURN, GET THE UPDATED INPUT INFOS + STORE INTO SPIDERS, MYHERO AND ENEMYHERO LISTS + SORT THE SPIDERS BY DANGEROUSITY IN SPIDERS_RANKED LIST

    # health and mana of i and my enemy
    my_health, my_mana = [int(j) for j in input().split()]
    enemy_health, enemy_mana=[int(j) for j in input().split()]
    
    # Amount of heros and spiders seeable in the map
    entity_count = int(input())

    # list that will store the infos on spiders, my heroes and my enemy's heroes
    spiders = []
    my_heroes = []
    enemy_heroes = []
    
    # for each entity, we get the infos and store them in the right list
    for i in range(entity_count):
        _id, _type, x, y, shield_life, is_controlled, health, vx, vy, near_base, threat_for = [int(j) for j in input().split()]
        entity = {
            'id':_id,            # _id: Unique identifier
            'type':_type,          # _type: 0=monster, 1=your hero, 2=opponent hero
            'x':x, 
            'y':y,           # x,y: Position of this entity
            'shield_life':shield_life,    # shield_life: Ignore for this league; Count down until shield spell fades
            'is_controlled':is_controlled,  # is_controlled: Ignore for this league; Equals 1 when this entity is under a control spell
            'health':health,         # health: Remaining health of this monster
            'vx':vx, 
            'vy':vy,         # vx,vy: Trajectory of this monster
            'near_base':near_base,      # near_base: 0=monster with no target yet, 1=monster targeting a base
            'threat_for':threat_for,      # threat_for: Given this monster's trajectory, is it a threat to 1=your base, 2=your opponent's base, 0=neither
            'id_target':'', # will be the id of the entity targeted by this entity (for myhero only)
            'action_target':'', # will be the action attempted by this entity (for myhero only)
            'x_target':'', # will be the x this entity will target (for myhero only)
            'y_target':'', # will be the y this entity will target (for myhero only)
            'targeted':'' # index to know if this entity is targeted
        }

        # storage of the info in the right list
        if _type == 0:
            spiders.append(entity)
        elif _type == 1:
            my_heroes.append(entity)
        elif _type == 2:
            enemy_heroes.append(entity)
        else:
            assert False

    # determine the most dangerous spiders and store them in a list
    spiders_ranked=[]
    for spider in spiders:
        threat_level=0
        dist_spider_base=0
        if spider['near_base']==1 and spider['threat_for']==1:
            threat_level=1000
        elif spider['threat_for']==1:
            threat_level=500
        dist_spider_base=math.hypot(base_x-spider['x'],base_y-spider['y'])
        dist_spider_base=1/(1+dist_spider_base)
        threat_level+=500*dist_spider_base
        spiders_ranked.append((threat_level,spider))
    spiders_ranked.sort(reverse=True)

    ###### STEP 3 : FOR EACH TURN DETERMINE THE ACTION OF EVERY OF MYHERO

    ### First priority of action : if a spider_ranked targets the base or will reach it eventually, allocate the closest myhero to attack this spider_ranked

    for spider_ranked in spiders_ranked:
        id_my_hero=''
        if (spider_ranked[1]['near_base']==1 and math.hypot(base_x-spider_ranked[1]['x'],base_y-spider_ranked[1]['y'])<6000) or (spider_ranked[1]['threat_for']==1 and math.hypot(base_x-spider_ranked[1]['x'],base_y-spider_ranked[1]['y'])<8000): # if the spider targets our base (it targets a base and is not far from ours) or will target our base and is not so far
            print("Target first priority",file=sys.stderr,flush=True)
            # then allocate the closest myhero to attack him
            dist_myheroes_spider=math.sqrt(17630**2+7000**2)
            for my_hero in my_heroes:
                if math.hypot(my_hero['x']-spider_ranked[1]['x'],my_hero['y']-spider_ranked[1]['y'])<dist_myheroes_spider:
                    if my_hero['id_target']=='':
                        dist_myheroes_spider=math.hypot(my_hero['x']-spider_ranked[1]['x'],my_hero['y']-spider_ranked[1]['y'])
                        id_my_hero=my_hero['id']
                        spider_ranked[1]['targeted']=="1"
            for my_hero in my_heroes:
                if my_hero['id']==id_my_hero and my_hero['id_target']=="": # if this hero is the closest to the dangerous spider and is not allocated to a more dangerous spider
                    my_hero['id_target']=spider_ranked[1]['id']
                    if my_mana>10 and dist_myheroes_spider<1280: # if i have enough mana, cast a spell
                        my_hero['action_target']="SPELL WIND"
                        my_hero['x_target']=17630-base_x
                        my_hero['y_target']=9000-base_y
                    else:
                        my_hero['action_target']="MOVE"
                        my_hero['x_target']=spider_ranked[1]['x']
                        my_hero['y_target']=spider_ranked[1]['y']   
                    print("1st priority" + str(my_hero['id']) + " " + my_hero['action_target'] ,file=sys.stderr,flush=True)                

    ### Second priority of action : for each myhero, if he is still available after first priority of action, see if he acts against an enemy

    for my_hero in my_heroes:
        if my_hero['id_target']=="": # if the hero has not target after the first priority of action
            dist_myhero_enemyhero=math.sqrt(17360**2+9000**2)
            for enemy_hero in enemy_heroes:
                dist_myhero_enemyhero=math.hypot(my_hero['x']-enemy_hero['x'],my_hero['y']-enemy_hero['y'])
                if dist_myhero_enemyhero<=2200 and my_mana>=10 and enemy_hero['shield_life']==0: # if i am close and can cast a spell to an unprotected enemy, i cast a spell
                    print("Target second priority",file=sys.stderr,flush=True)
                    if enemy_hero['y']>4500:
                        my_hero['action_target']="SPELL CONTROL"
                        my_hero['id_target']=enemy_hero['id']
                        my_hero['x_target']=0
                        my_hero['y_target']=9000
                        enemy_hero['targeted']==1
                        #print("SPELL","CONTROL",enemy_hero['id'],0,9000)
                        #index_closeness=1
                        break
                    else:
                        my_hero['action_target']="SPELL CONTROL"
                        my_hero['id_target']=enemy_hero['id']
                        my_hero['x_target']=17630
                        my_hero['y_target']=0
                        enemy_hero['targeted']==1
                        #print("SPELL","CONTROL",enemy_hero['id'],17630,0)
                        #index_closeness=1
                        break
                elif dist_myhero_enemyhero>2200 and dist_myhero_enemyhero<=3000: # if the enemy can be reached in a turn
                    if my_hero['shield_life']==0 and my_mana>=10: # if i dont have a shield, i shield
                        my_hero['action_target']="SPELL SHIELD"
                        my_hero['id_target']=my_hero['id'] 
                        #print("SPELL","SHIELD",my_hero['id'])
                        #index_closeness=1
                        break
                    elif my_hero['shield_life']>3 and my_mana>20: # if i already have a shield and enough mana to cast a spell, i come closer
                        my_hero['action_target']="MOVE"
                        my_hero['id_target']=enemy_hero['id']
                        my_hero['x_target']=enemy_hero['x']
                        my_hero['y_target']=enemy_hero['y']
                        enemy_hero['targeted']==1
                        #print("MOVE", enemy_hero['x'],enemy_hero['y'])
                        #index_closeness=1
                        break
                    elif enemy_mana>=10: # if the enemy can cast me a spell, i run away from him
                        if my_hero['x']+800**2*(my_hero['x']-enemy_hero['x'])/dist_myhero_enemyhero**2>0 and my_hero['x']+800**2*(my_hero['x']-enemy_hero['x'])/dist_myhero_enemyhero**2<17360 and my_hero['y']+800**2*(my_hero['y']-enemy_hero['y'])/dist_myhero_enemyhero**2>0 and my_hero['y']+800**2*(my_hero['y']-enemy_hero['y'])/dist_myhero_enemyhero**2<9000:
                            my_hero['action_target']="MOVE"
                            my_hero['id_target']=enemy_hero['id']
                            my_hero['x_target']=my_hero['x']+800**2*(my_hero['x']-enemy_hero['x'])/dist_myhero_enemyhero**2
                            my_hero['y_target']=my_hero['y']+800**2*(my_hero['y']-enemy_hero['y'])/dist_myhero_enemyhero**2                            
                            enemy_hero['targeted']==1
                            #print("MOVE",my_hero['x']+800**2*(my_hero['x']-enemy_hero['x'])/dist_myhero_enemyhero**2,my_hero['y']+800**2*(my_hero['y']-enemy_hero['y'])/dist_myhero_enemyhero**2)
                            #index_closeness=1
                        elif my_hero['id']==0:
                            my_hero['action_target']="MOVE"
                            my_hero['id_target']=enemy_hero['id']
                            my_hero['x_target']=hero0_def_position_x
                            my_hero['y_target']=hero0_def_position_y 
                            enemy_hero['targeted']==1
                            #print("MOVE",hero0_def_position_x,hero0_def_position_y)
                            #index_closeness=1
                        elif my_hero['id']==1:
                            my_hero['action_target']="MOVE"
                            my_hero['id_target']=enemy_hero['id']
                            my_hero['x_target']=hero1_def_position_x
                            my_hero['y_target']=hero1_def_position_y 
                            enemy_hero['targeted']==1
                            #print("MOVE",hero1_def_position_x,hero1_def_position_y)
                            #index_closeness=1
                        else:
                            my_hero['action_target']="MOVE"
                            my_hero['id_target']=enemy_hero['id']
                            my_hero['x_target']=hero2_def_position_x
                            my_hero['y_target']=hero2_def_position_y 
                            enemy_hero['targeted']==1
                            #print("MOVE",hero2_def_position_x,hero2_def_position_y)
                            #index_closeness=1
                print("2nd priority" + str(my_hero['id']) + " " + my_hero['action_target'],file=sys.stderr,flush=True)              

    ### Third priority of action : for each myhero, if he is still available after first and second priority of action, let him attack the closest spider

    for my_hero in my_heroes:
        if my_hero['id_target']=="" and my_hero['id']!=1: # if the hero has not target after the first priority of action
            dist_myhero_rankedspider=math.sqrt(17360**2+9000**2)
            id_ranked_spider=''
            for spider_ranked in spiders_ranked:
                if math.hypot(my_hero['x']-spider_ranked[1]['x'],my_hero['y']-spider_ranked[1]['y'])<dist_myhero_rankedspider and spider_ranked[1]['targeted']!=1 :
                    dist_myhero_rankedspider=math.hypot(my_hero['x']-spider_ranked[1]['x'],my_hero['y']-spider_ranked[1]['y'])
                    id_ranked_spider=spider_ranked[1]['id']
                    spider_ranked[1]['targeted']=="1"
            for spider_ranked in spiders_ranked:
                if spider_ranked[1]['id']==id_ranked_spider:
                    my_hero['action_target']="MOVE"
                    my_hero['id_target']=spider_ranked[1]['id']
                    my_hero['x_target']=spider_ranked[1]['x']
                    my_hero['y_target']=spider_ranked[1]['y']
                    print("3rd priority" + str(my_hero['id']) + " " + my_hero['action_target'],file=sys.stderr,flush=True)              
                     

    ### Fourth priority of action : for each myhero, if he is still available after first and second and third priority of action, let him go towards his defensive position

    for my_hero in my_heroes:
        if my_hero['id_target']=="" and my_hero['id']!=1: # if the hero has not target after the first priority of action
            if my_hero['id']==0:
                my_hero['action_target']="MOVE"
                #my_hero['id_target']=enemy_hero['id']
                my_hero['x_target']=hero0_def_position_x
                my_hero['y_target']=hero0_def_position_y 
            elif my_hero['id']==1:
                my_hero['action_target']="MOVE"
                #my_hero['id_target']=enemy_hero['id']
                my_hero['x_target']=hero1_def_position_x
                my_hero['y_target']=hero1_def_position_y 
            else:
                my_hero['action_target']="MOVE"
                #my_hero['id_target']=enemy_hero['id']
                my_hero['x_target']=hero2_def_position_x
                my_hero['y_target']=hero2_def_position_y
            print("4th priority" + str(my_hero['id']) + " " + my_hero['action_target'],file=sys.stderr,flush=True)               
            

    ### Print the action decided for each my_hero

    for my_hero in my_heroes:
        if my_hero['action_target']=="MOVE":
            print("MOVE",my_hero['x_target'],my_hero['y_target'])
        elif my_hero['action_target']=="SPELL WIND":
            print("SPELL WIND",my_hero['x_target'],my_hero['y_target'])
        elif my_hero['action_target']=="SPELL CONTROL":
            print("SPELL CONTROL",my_hero['id_target'],my_hero['x_target'],my_hero['y_target'])
        elif my_hero['action_target']=="SPELL SHIELD":
            print("SPELL SHIELD",my_hero['id_target'])
        else:
            print("WAIT")




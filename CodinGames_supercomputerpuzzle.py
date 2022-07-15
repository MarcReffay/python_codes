# -*- coding: utf-8 -*-
"""
Created on Fri Jul 15 11:29:20 2022

@author: reffay_m
"""

import sys

n = int(input())
l=[]
for i in range(n):
    j, d = [int(j) for j in input().split()]   
    l.append([j,j+d-1])


# sort by end date
new_list = sorted(l, key=lambda x:x[-1])

print(*new_list, file=sys.stderr, flush=True)

r=1
l_c=0
# chose each element one by one
for i in range(1,len(new_list)):
    if new_list[i][0]<=new_list[l_c][1]:
        print(new_list[i], file=sys.stderr, flush=True)
    else:
        l_c=i
        r+=1

print(r)

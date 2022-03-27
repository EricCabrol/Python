# -*- coding: utf-8 -*-
"""
Created on Thu Apr 30 16:29:31 2020

@author: ericc
"""

from scipy.optimize import linprog
import numpy as np

nb_races=10 
nb_swimmers=50
product = nb_races*nb_swimmers
score_indiv = np.random.rand(nb_races,nb_swimmers)
score_reshape=-1*np.reshape(score_indiv,(1,product))

lb = np.zeros((product,1))
ub = np.ones((product,1))

A = np.zeros((nb_swimmers,product))
for i in range(0,nb_swimmers):
    tmp=(i-1)*nb_races
    for j in range (0,nb_races):
        A[i][j+tmp]=1

b=np.ones((nb_swimmers,1))

Aeq = np.zeros((nb_races,product))
for i in range(0,nb_races):
    for j in range (0,nb_swimmers):
        Aeq[i][i+(j-1)*nb_races]=1

beq=np.ones((nb_races,1))

x = linprog(score_reshape,A_ub=A,b_ub=b,A_eq=Aeq,b_eq=beq,bounds=[lb,ub])
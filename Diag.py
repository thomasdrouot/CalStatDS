#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 27 18:35:37 2019

@author: thomas
"""


import h5py
import matplotlib.pyplot as plt


f = h5py.File('Experience1.hdf5', 'r')

list_groupe = [key for key in f['/'].keys()]

list_dsetXe = [key for key in f[list_groupe[0]].keys()]
list_dsetXi = [key for key in f[list_groupe[1]].keys()]
list_dsetVe = [key for key in f[list_groupe[2]].keys()]
list_dsetVi = [key for key in f[list_groupe[3]].keys()]


temps=[float(list_dsetXe[i][2:]) for i in range(len(list_dsetXe))]

Xe=np.array([list(f[list_groupe[0]][list_dsetXe[i]]) for i in range(len(list_dsetXe))])
Xi=np.array([list(f[list_groupe[0]][list_dsetXi[i]]) for i in range(len(list_dsetXi))])
Ve=np.array([list(f[list_groupe[0]][list_dsetVe[i]]) for i in range(len(list_dsetVe))])
Vi=np.array([list(f[list_groupe[0]][list_dsetVi[i]]) for i in range(len(list_dsetVi))])
#Xe=list(f['/'][list_elmts[0]])
#Xi=list(f['/'][list_elmts[1]])
#Ve=
#Vi=
#plt.plot(X,Y,'.')

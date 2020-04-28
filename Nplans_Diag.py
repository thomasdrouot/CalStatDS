# -*- coding: utf-8 -*-

"""
***********************************
CODE Pb N_Corps
Created on Thu Mar 24 15:47:36 2016
@author: gravier
Version avec 
Conditions aux limites périodiques (30 mai 2016)
***********************************
"""

from math import pi, cos, sqrt
from random import random
import matplotlib.pyplot as plt
import numpy as np
import time
import h5py


"""
*************************************************************************
Définition de la classe UnPlan, avec ses paramètres et ses méthodes
"""
class UnPlan : # Mise en place de la classe Plan
    def __init__(self, identite, position, vitesse, acceleration, masse, signe, Qg): # Méthode constructeur du plan
        self.identite = identite # Numéro du plan, reste constant tout au long de la simulation (entier positif)
        self.position = position # Position du plan (réel)
        self.vitesse = vitesse # Vitesse du plan (réel)
        self.acceleration = acceleration # Accéleration du plan (réel)
        self.masse = masse # Masse d'une des particules du plan (la masse de référence est celle de l'électron : m_e = 1) 
        self.signe=signe # Signe du plan (+1 ou -1)
        self.Qg=Qg # Charge totale à gauche de ce plan (entier relatif)
    
    def caracteristiques(self) : # Méthode pour afficher toutes les caractéristiques du plan sous forme de liste
        return([self.identite,self.position,self.vitesse,self.acceleration,self.masse,self.signe,self.Qg])
        
    
# Indicateurs pour la mesure du temps d'exécution de parties du code
tps1 = time.clock()
        
"""
*****************
# Main parameters
*****************
"""

# Length of the box (en longueurs de Debye)
L=2.0*pi

# Number of sheets
N=15
# N ion sheets + N electron sheets (a total of 2N sheets)

# Nb d'itérations max
Nmax=10 #(nb d'itérations, entier)

# ion mass and electron mass
mi=1836.0
#mi=1.0
#mi=1.0e5
me=1.0

# paramètre d'ajustement (précision) pour le croisement des plans
precision_machine = 1.0e-8

# Choix des vitesses initiales : paramètre choix_vit_init
    # 1 pour vitesses nulles, 
    # 2 pour vitesses aléatoires, 
    # 3 pour double faisceau (v_0 = +/- 1 uniquement pour électrons, ions à 0)
choix_vit_init = 3

"""
****************
# Initialisation
****************
"""

# Distributions
Plans=[] # cette liste contiendra les objets "UnPlan"

positions_initiales=[] # cette liste contiendra les abscisses initiales de tous les plans
vitesses_initiales=[] # cette liste contiendra les vitesses initiales de tous les plans
accelerations_initiales=[] # cette liste contiendra les accélérations initiales de tous les plans

les_x_e=[] # cette liste contiendra les abscisses des plans e- (pour la représentation de l'espace des phases)
les_v_e=[] # cette liste contiendra les vitesses des plans e- (pour la représentation de l'espace des phases) 
les_x_i=[] # cette liste contiendra les abscisses des plans ioniques (pour la représentation de l'espace des phases)
les_v_i=[] # cette liste contiendra les vitesses des plans ioniques (pour la représentation de l'espace des phases)



if choix_vit_init == 1:
    for i in range(1,2*N+1):
        positions_initiales.append(random()*L) # Répartition aléatoire entre 0 et L
        vitesses_initiales.append(0.0) # Toutes les vitesses initiales sont à 0
        accelerations_initiales.append(0.0) # Toutes les accélérations initiales sont à 0
    positions_initiales=sorted(positions_initiales) # réarrangement des positions initiales par x croissant
        
if choix_vit_init == 2:
    for i in range(1,2*N+1):
        positions_initiales.append(random()*L) # Répartition aléatoire entre 0 et L
        vitesses_initiales.append(random()*2.0-1) # Les vitesses initiales sont réparties aléatoirement entre -1 et +1
        accelerations_initiales.append(0.0) # Toutes les accélérations initiales sont à 0
    positions_initiales=sorted(positions_initiales)  # réarrangement des positions initiales par x croissant

        
        
if choix_vit_init == 3:
    for i in range(1,2*N+1):
        positions_initiales.append(random()*L) # Répartition aléatoire entre 0 et L
        vitesses_initiales.append(0.0) # Les vitesses initiales sont mises à 0 (provisoirement)
        accelerations_initiales.append(0.0) # Toutes les accélérations initiales sont à 0
    positions_initiales=sorted(positions_initiales)  # réarrangement des positions initiales par x croissant
    for i in range(1,2*N+1,4): # vitesses indicées 1, 5, 9, 13 ... sont mises à +1 (plus éventuelle perturbation)
        vitesses_initiales[i] = 1.0+0.01*cos(2.0*positions_initiales[i])
    for i in range(3,2*N+1,4): # vitesses indicées 3, 7, 11, 15 ... sont mises à -1 (plus éventuelle perturbation)
        vitesses_initiales[i] = -1.0
    

# Création de la liste d'objets "plans"
# Alternance des plans positifs et négatifs / Le premier plan est positif
for j in range(1,2*N+1,2):
    # Création des plans positifs
    Plans.append(UnPlan(j,positions_initiales[j-1],vitesses_initiales[j-1],accelerations_initiales[j-1],mi,1,0))
    # Création des plans négatifs    
    Plans.append(UnPlan(j+1,positions_initiales[j],vitesses_initiales[j],accelerations_initiales[j],me,-1,1))

"""
*****************************
Diagnostics de l'état initial
*****************************
"""

# Diagnostics distribution initiale
for j in range(1,2*N+1):
    #print Plans[j-1].caracteristiques()
    if Plans[j-1].signe == -1:
        les_x_e.append(Plans[j-1].position)
        les_v_e.append(Plans[j-1].vitesse)
    else :
        les_x_i.append(Plans[j-1].position)
        les_v_i.append(Plans[j-1].vitesse)    
        
        

### Enregistrement hdf5
mon_fichier = h5py.File('./Experience1.hdf5', 'w')
Ve = mon_fichier.create_group(name='VitesseElectron')
Xe = mon_fichier.create_group(name='PositionElectron')
Vi = mon_fichier.create_group(name='VitesseProton')
Xi = mon_fichier.create_group(name='PositionProton')
dataset_Ve = Ve.create_dataset(name='t=0', data=les_v_e, dtype="float16")
dataset_Xe = Xe.create_dataset(name='t=0', data=les_x_e, dtype="float16")
dataset_Vi = Vi.create_dataset(name='t=0', data=les_v_i, dtype="float16")
dataset_Xi = Xi.create_dataset(name='t=0', data=les_x_i, dtype="float16")
mon_fichier.close()


# Représentation de l'espace des phases à l'état initial
plt.figure(1)
plt.plot(les_x_e,les_v_e,"rs",les_x_i,les_v_i,"bs")    
plt.xlabel('x')
plt.ylabel('v')
plt.title('Etat initial - Espace des phases')
plt.axis([0, L, min([min(les_v_e),min(les_v_i)])-0.5, max([max(les_v_e),max(les_v_i)])+0.5])
plt.show()

# Représentation de la fonction de distribution électronique à l'état initial (histogramme)

n_cases=51 # Nb de segments pour l'histogramme, choisir un entier impair

delta_ve_init = 2.0*max(abs(min(les_v_e)),abs(max(les_v_e)))/(n_cases) # calcul de l'intervalle
depart_init=-max(abs(min(les_v_e)),abs(max(les_v_e))) # point de départ

# traitement du cas particulier où toutes les vitesses initiales sont à 0
if delta_ve_init < 1.0e-5:
    delta_ve_init = 1.0e-5  
    depart_init=-1.0e-5*n_cases/2.0

x_cases_ve_init=[] # liste des abscisses pour l'histogramme
cases_ve_init=[] # listes des ordonnées pour l'histogramme
for i in range (1, n_cases+1):
    cases_ve_init.append(0)
    x_cases_ve_init.append(depart_init+(i-1)*delta_ve_init+delta_ve_init/2.0) # les abscisses se trouvent au milieu des intervalles
    
for j in range(1,N+1): # remplissage de l'histogramme
    for i in range (1, n_cases+1):
        if (les_v_e[j-1] >= (depart_init+(i-1)*delta_ve_init)) and (les_v_e[j-1] < (depart_init+i*delta_ve_init)) :
            cases_ve_init[i-1] += 1 
    
# Représentation de la fonction de distribution électronique initiale
plt.figure(2)
plt.plot(x_cases_ve_init,cases_ve_init,"ks")    
plt.xlabel('v')
plt.ylabel('F_e')
plt.title('Etat initial')
#plt.axis([0, L, min([min(les_v_e),min(les_v_i)])-0.5, max([max(les_v_e),max(les_v_i)])+0.5])
plt.show() 


  
"""
*********************
# BOUCLE SUR LE TEMPS
*********************
"""
n_WARNING=0 # variable permettant d'indiquer que tout s'est bien passé pour le déplacement des plans si nulle à la fin
temps_total=0.0 # Calcul du temps (en 1/w_p)
N_iter=0 # Nb d'itérations

temps_boucle_tau = 0.0 # servira à la mesure du temps passé dans la boucle (partie recherche de tau)
temps_boucle_deplacement = 0.0 # servira à la mesure du temps passé dans la boucle (partie déplacement des plans)

# début boucle sur le temps
while (N_iter < Nmax) and (n_WARNING == 0) :
    # Calcul des accélérations subies par tous les plans
    for j in range(1,2*N+1):
        Plans[j-1].acceleration=L/2.0/N*Plans[j-1].signe/(Plans[j-1].masse)*(2.0*Plans[j-1].Qg+Plans[j-1].signe)
        #print Plans[j-1].caracteristiques()
        
        
    tps2 = time.clock() # pour mesure du temps d'exécution 
    
    
    
    """
    Recherche des temps de croisement et de collisions avec les murs
    Le minimum de ces temps sera appelé tau_min_tot
    """        
    
    # Recherche du temps de croisement minimum, ce temps sera appelé tau_min
    tau=[] # cette liste contiendra les temps de croisement entre les plans j et j+1
    for j in range(1,2*N): # boucle sur les plans de 1 à 2N-1 
        # calcul discriminant
        delta=(Plans[j].vitesse-Plans[j-1].vitesse)**2-2.0*(Plans[j].acceleration-Plans[j-1].acceleration)*(Plans[j].position-Plans[j-1].position)
        if delta < 0.0 or Plans[j-1].position == Plans[j].position : # cas discriminant négatif ou plans à la même position
            tau.append(1.0e15) # valeur arbitraire très grande
        else: # cas du discriminant positif 
            racine_delta=sqrt(delta)
            tau_plus=(Plans[j-1].vitesse-Plans[j].vitesse+racine_delta)/(Plans[j].acceleration-Plans[j-1].acceleration)
            tau_moins=(Plans[j].vitesse-Plans[j-1].vitesse+racine_delta)/(Plans[j-1].acceleration-Plans[j].acceleration)                       
            if tau_plus <= tau_moins and tau_plus > 0.0 : # recherche de la plus petite racine positive
                tau.append(tau_plus)
            elif tau_moins > 0.0:
                tau.append(tau_moins)
            else:
                tau.append(1.0e15) # cas où il n'y a pas de racine positive
   
    # recherche du minimum de ces temps de croisement (appelé tau_min)   
    tau_min=min(tau)
    index_min=np.argmin(tau) # Cela signifie que le croisement a lieu entre le plan n° index_min+1 et le plan n° index_min+2
    #print tau_min, index_min
                
    # recherche du temps de collision entre le 1er plan et le mur de gauche (sera appelé tauL)
    delta=(Plans[0].vitesse)**2-2.0*(Plans[0].acceleration)*(Plans[0].position)
    if delta < 0.0 or Plans[0].position == 0.0 : # cas discriminant négatif ou plan en 0
            tauL=1.0e15
    else:
        racine_delta=sqrt(delta)
        tauL_plus=(-Plans[0].vitesse+racine_delta)/(Plans[0].acceleration)
        tauL_moins=(-Plans[0].vitesse-racine_delta)/(Plans[0].acceleration)                       
        if tauL_plus <= tauL_moins and tauL_plus > 0.0:
            tauL=tauL_plus
        elif tauL_moins > 0.0:
            tauL=tauL_moins
        else:
            tauL=1.0e15 # cas où il n'y a pas de racine positive             
                
    # recherche du temps de collision entre le dernier plan et le mur de droite (sera appelé tauR)
    delta=(Plans[2*N-1].vitesse)**2-2.0*(Plans[2*N-1].acceleration)*(Plans[2*N-1].position-L)
    if delta < 0.0 or Plans[0].position == L : # cas discriminant négatif ou plan en L
            tauR=1.0e15
    else:
        racine_delta=sqrt(delta)
        tauR_plus=(-Plans[2*N-1].vitesse+racine_delta)/(Plans[2*N-1].acceleration)
        tauR_moins=(-Plans[2*N-1].vitesse-racine_delta)/(Plans[2*N-1].acceleration)                       
        if tauR_plus <= tauR_moins and tauR_plus > 0.0:
            tauR=tauR_plus
        elif tauR_moins > 0.0:
            tauR=tauR_moins
        else:
            tauR=1.0e15 # cas où il n'y a pas de racine positive 
    
    tps3 = time.clock() # pour mesure du temps d'exécution        
    
    #print "tau_min", tau_min, "tau_R", tauR, "tau_L", tauL            
    
    tau_min_tot=min([tau_min,tauR,tauL]) # temps minimum entre le minimum des temps de croisement 
    # et les 2 temps de collision / Les plans vont évoluer sur ce temps
    index_min_tot=np.argmin([tau_min,tauR,tauL]) # pour repérer si c'est un croisement, une collision sur le
    # mur de gauche, ou une collision sur le mur de droite    
    
    """
    Fin de recherche des temps de croisement et de collisions avec les murs
    """     
    
    tps2bis = time.clock() # pour mesure du temps d'exécution       
   
   
    """
    Evolution de tous les plans sur le temps minimum total
    Dans un premier temps, on fait juste bouger les plans, sans traiter le croisement ou la collision
    """
    
     #if index_min_tot !=0 :
     #   print "COLLISION"
    #print "imin", index_min, "imintot", index_min_tot
    #print tau_min,tauR,tauL
    for j in range(1,2*N+1):
        vitesse_inter = Plans[j-1].vitesse
        Plans[j-1].vitesse = Plans[j-1].acceleration * tau_min_tot + vitesse_inter
        Plans[j-1].position = 0.5*Plans[j-1].acceleration*tau_min_tot**2 + vitesse_inter * tau_min_tot + Plans[j-1].position
        if Plans[j-1].position > (L+precision_machine) or Plans[j-1].position < (0.0-precision_machine) :
            n_WARNING +=1
    
    """
    Fin de l'évolution de tous les plans sur le temps minimum total
    """
       
    """
    Gestion du croisement ou de la collision
    """       
       
    # Gestion du croisement de 2 plans ou du choc sur un des murs 
    
        
    if index_min_tot == 0 :
        Plan_inter = Plans[index_min]
        Plans[index_min] = Plans[index_min+1]
        Plans[index_min+1]=Plan_inter
        Plans[index_min+1].Qg=Plans[index_min+1].Qg + Plans[index_min].signe
        Plans[index_min].Qg=Plans[index_min].Qg - Plans[index_min+1].signe
        Plans[index_min+1].position += precision_machine
        
    if index_min_tot == 1 :
        Plans[2*N-1].position = 0.0+precision_machine
        Plan_inter=Plans[2*N-1]
#        Plans=[Plan_inter,Plans[0:2*N-1]]
        for ja in range(1,2*N):
            Plans[2*N-ja]=Plans[2*N-ja-1]
            Plans[2*N-ja].Qg+=Plan_inter.signe
        Plans[0]=Plan_inter
        Plans[0].Qg=0
        
    if index_min_tot == 2 :
        Plans[0].position = L-precision_machine
        Plan_inter=Plans[0]
#        Plans=[Plans[1:2*N],Plan_inter]
        for ja in range(1,2*N):
            Plans[ja-1]=Plans[ja]
            Plans[ja-1].Qg-=Plan_inter.signe
        Plans[2*N-1]=Plan_inter
        Plans[2*N-1].Qg=Plans[2*N-2].Qg+Plans[2*N-2].signe
        
        
#    if index_min_tot == 1 :
#        Plans[2*N-1].vitesse = - Plans[2*N-1].vitesse # si rebond
#        Plans[2*N-1].position = L-precision_machine # si rebond
#        
#    if index_min_tot == 2 :
#        Plans[0].vitesse = - Plans[0].vitesse
#        Plans[0].position = 0.0+precision_machine  
#    
    """
    Fin du traitement du croisement ou de la collision
    """
    tps3bis = time.clock() # pour la mesure du temps d'exécution    
    
    # On reprend la boucle sur le temps tant que N_iter n'est pas plus grand que Nmax
    temps_total +=tau_min_tot # calcul du temps physique
    N_iter += 1
    #print tau_min_tot, temps_total, N_iter
    
    #if N_iter % (N_iter/10) == 0 :
    #    print "Temps phys. ",temps_total, "Iterations : ", N_iter

    temps_boucle_tau += (tps3-tps2) # indicateur temps d'exécution
    temps_boucle_deplacement += (tps3bis-tps2bis) # indicateur temps d'exécution
    
    
    
    ### Diagnostique
    
    les_x_i=[]
    les_v_i=[]
    les_x_e=[]
    les_v_e=[]
    for j in range(1,2*N+1):
        #print Plans[j-1].caracteristiques()
        if Plans[j-1].signe == -1:
            les_x_e.append(Plans[j-1].position)
            les_v_e.append(Plans[j-1].vitesse)
        else :
            les_x_i.append(Plans[j-1].position)
            les_v_i.append(Plans[j-1].vitesse)    
    
    
    f= h5py.File('Experience1.hdf5', 'w')
    dataset_Ve = f.create_dataset(name='VitesseElectron/t='+str(temps_total), data=les_v_e, dtype="float16")
    dataset_Xe = f.create_dataset(name='PositionElectron/t='+str(temps_total), data=les_x_e, dtype="float16")
    dataset_Vi = f.create_dataset(name='VitesseProton/t='+str(temps_total), data=les_v_i, dtype="float16")
    dataset_Xi = f.create_dataset(name='PositionProton/t='+str(temps_total), data=les_x_i, dtype="float16")
    f.flush()
    f.close()

"""
*******************************
# FIN DE LA BOUCLE SUR LE TEMPS
*******************************
"""

# Diagnostics à l'état final
les_x_i=[]
les_v_i=[]
les_x_e=[]
les_v_e=[]
for j in range(1,2*N+1):
    #print Plans[j-1].caracteristiques()
    if Plans[j-1].signe == -1:
        les_x_e.append(Plans[j-1].position)
        les_v_e.append(Plans[j-1].vitesse)
    else :
        les_x_i.append(Plans[j-1].position)
        les_v_i.append(Plans[j-1].vitesse)    


# Représentation de l'espace des phases à l'état final
plt.figure(3)
plt.plot(les_x_e,les_v_e,"rs",les_x_i,les_v_i,"bs")    
plt.xlabel('x')
plt.ylabel('v')
plt.title('Etat final')
plt.axis([0, L, min([min(les_v_e),min(les_v_i)])-0.5, max([max(les_v_e),max(les_v_i)])+0.5])
plt.show()


# Représentation de la fonction de distribution électronique à l'état final (histogramme)
delta_ve = 2.0*max(abs(min(les_v_e)),abs(max(les_v_e)))/n_cases
depart=-max(abs(min(les_v_e)),abs(max(les_v_e)))

x_cases_ve=[]
cases_ve=[]
for i in range (1, n_cases+1):
    cases_ve.append(0)
    x_cases_ve.append(depart+(i-1)*delta_ve+delta_ve/2.0)
    
for j in range(1,N+1):
    for i in range (1, n_cases+1):
        if (les_v_e[j-1] >= (depart+(i-1)*delta_ve)) and (les_v_e[j-1] < (depart+i*delta_ve)) :
            cases_ve[i-1] += 1 
    
 # Représentation de la fonction de distribution électronique
plt.figure(4)
plt.plot(x_cases_ve,cases_ve,"r:s")    
plt.xlabel('v')
plt.ylabel('F_e')
plt.title('Etat final')
#plt.axis([0, L, min([min(les_v_e),min(les_v_i)])-0.5, max([max(les_v_e),max(les_v_i)])+0.5])
plt.show()   

# Fin diagnostics état final

tps4 = time.clock() # pour mesure du temps d'exécution


# Représentation de la force subie par chaque plan
    
#les_xi_i=[]
#les_a_i=[]
#les_xe_e=[]
#les_a_e=[]
#for j in range(1,2*N+1):
#    if Plans[j-1].signe == -1:
#        les_xe_e.append(Plans[j-1].position)
#        les_a_e.append(Plans[j-1].acceleration*(Plans[j-1].masse))
#    else :
#        les_xi_i.append(Plans[j-1].position)
#        les_a_i.append(Plans[j-1].acceleration*(Plans[j-1].masse))   
#plt.figure(101)
#plt.plot(les_xe_e,les_a_e,"rs",les_xi_i,les_a_i,"bs")     
#plt.xlabel('x')
#plt.ylabel('F')
#plt.axis([0, L, min([min(les_a_e),min(les_a_i)])-0.5, max([max(les_a_e),max(les_a_i)])+0.5])
#plt.show()     
#    




# Affichage des caractéristiques d'exécution du code

print ("*************************************************************************")
print ("Longueur = ", L)
print ("Nb de plans pour une espèce = ", N)
print ("Masse électron = ", me)
print ("Masse ion = ", mi)
print ("Précision machine = ", precision_machine)
print ("Choix pour les vitesses initiales = ", choix_vit_init)
print ("*************************************************************************")
print ("Nb iterations", N_iter )
print ("Temps total physique (en 1/w_p) : ",temps_total )
print ("Graininess parameter g = ",L/N)
print ("*************************************************************************")
print ("Nb de warnings : ", n_WARNING)
print ("Tps total d'exécution = %.2f s" % (tps4-tps1), "(%.3f" % ((tps4-tps1)/3600.0), "h)")
print ("Tps dans la boucle (partie tau) = %.2f s" % temps_boucle_tau, "(%.2f" % (temps_boucle_tau/(tps4-tps1)*100), "%)")
print ("Tps dans la boucle (partie deplacement) = %.2f s" % temps_boucle_deplacement, "(%.2f" % (temps_boucle_deplacement/(tps4-tps1)*100), "%)")
print ("*************************************************************************" )     
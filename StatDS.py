#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 29 11:01:52 2019

@author: drouot
"""

import csv
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from matplotlib.colors import Normalize
import os
import statistics as stat

###
NbDS="7"     ###  Numéro du DS







FichierRoot=[]
Fichier=[]
FichierBareme=[]

########  Lecture résultat ###################################
File1='DS'+NbDS+'.csv'
with open(File1, newline='') as csvfile:
     reader1 = csv.reader(csvfile, delimiter=';', quotechar='|')  # le ; delimite les élements des listes.
     for row in reader1:
         FichierRoot.append(row)                                # la variable FichierRoot contient toutes les lignes dans une liste.
         

         

         
#####   Suppression des ligne en trop 

for i in range(len(FichierRoot)):
    if not('"ABS"' in FichierRoot[i]):
         Fichier.append(FichierRoot[i])
   
NbEleve=len(Fichier)-1                            ##     Calculé à partir du nombre de de ligne dans le fichie



##############  Liste du nom des questions  ###################

NomQuestion=[ Fichier[0][i] for i in range(4,len(Fichier[0]),2)]

for i in range(len(NomQuestion)):
    if "9" in NomQuestion[i] and NomQuestion[i][-3:-1]!="-9":             ## Permet de suprimer les '9' pour ordonner les questions
        NomQuestion[i]=NomQuestion[i].replace('-9','-')
        
        
        
        
        

##########        Creation du bareme
File2='BaremeDS'+NbDS+'.csv'

if os.path.isfile(File2)==False:
    Bareme=[]
    f = open(File2, 'w')
    for i in range(len(NomQuestion)-1):
        a=input('entrer le barème de la question'+NomQuestion[i])
        FichierBareme.append(int(a))
        ligneEntete =a+ ";"
        f.write(ligneEntete)
    a=input('entrer le barème de la question'+NomQuestion[-1])
    FichierBareme.append(int(a))
    ligneEntete =a
    f.write(ligneEntete)
    f.close()
    
else :
    with open(File2, newline='') as csvfile:
     reader2 = csv.reader(csvfile, delimiter=';', quotechar='|')  # le ; delimite les élements des listes.
     for row in reader2:
         FichierBaremetemp=row    

    FichierBareme=[float(FichierBaremetemp[i]) for i in range(len(FichierBaremetemp))] # Le barème est stocké dans une liste.   
    
    

######### Lecture Barème ####################################         
#File2='BaremeDS'+NbDS+'.csv'
#with open(File2, newline='') as csvfile:
#     reader2 = csv.reader(csvfile, delimiter=';', quotechar='|')  # le ; delimite les élements des listes.
#     for row in reader2:
#         FichierBaremetemp=row    

#FichierBareme=[float(FichierBaremetemp[i]) for i in range(len(FichierBaremetemp))] # Le barème est stocké dans une liste.   
    
#####  Détections d'erreur  ###########################################   
if len(Fichier)!=NbEleve+1:   ### +1 représente la ligne d'en tête.
    print("Le nombre de ligne ne correspond pas à la valeur attendue")
       
    
if int((len(Fichier[0])-4)/2)!=len(FichierBareme):
    print("Problème avec le bareme")
#######################################################################
 
    
    
########################### Enregistrement des résultats de chaque question    
ResultatQ=[]                                                                   ### ResultatQ=[[Q1chaque eleve],[Q2],.....]                                               

for j in range(len(FichierBareme)):
    Question=[]
    for i in range(1,len(Fichier)): 
        if int(Fichier[i][4+j*6][1])!=0:
            Question.append(int(Fichier[i][4+j*6][1]))
        else:
            if '1' in Fichier[i][4+j*6+1:4+(j+1)*6]:
                Question.append(int(Fichier[i][4+j*6][1]))
            else:
                Question.append(-1)                       ###############  -1 signifie sans réponse.
            
    ResultatQ.append(Question)            
  

ResultatQSNeg=[[0]*len(ResultatQ[0]) for i in range(len(ResultatQ))]
for i in range(len(ResultatQ)):
    for j in range(len(ResultatQ[0])):
        if ResultatQ[i][j]==-1:
            ResultatQSNeg[i][j]=0
        else:
            ResultatQSNeg[i][j]=ResultatQ[i][j]          
       

########################### Enregistrement des résultats de chaque Eleve       
ResultatElev=[]   
NomEleve=[]                                                             ### ResultatElev=[[nom1,Q1,Q2,Q3,....],[nom2,Q1,Q2,Q3,....],.....]     
for j in range(0,NbEleve):
    Eleve=[Fichier[j+1][2]]
    print(Eleve)
    NomEleve.append(Fichier[j+1][2][1:-1])
    for i in range(0,len(FichierBareme)): 
        Eleve.append(ResultatQSNeg[i][j])
    ResultatElev.append(Eleve)         
     






########################### Enregistrement de la note globale
NoteBrute=[]                                                                    ### NoteBrute=[Note1,Note2,....] 
for j in range(len(ResultatElev)):
    s=0
    for i in range(1,len(ResultatElev[0])):
        if ResultatElev[j][i]!=-1:
            s+=ResultatElev[j][i]*FichierBareme[i-1]/4    
        
    NoteBrute.append(s)        
            
    
    
    
################  indices de chaque exercice ############################
    
Nom=[NomQuestion[i][1:-1] for i in range(len(NomQuestion))]
NbExoMax=int(Nom[-1][0])
IndexExos=[0]
index=0
for i in range(1,NbExoMax+1): 
        while index!=len(Nom) and int(Nom[index][0])==i :
            index+=1
        IndexExos.append(index)

    
    
##################  Moyennes des exo  ################################################


            



PointsExo=[]
MoyenneExo=[]
kk=0
while kk<NbExoMax:
    s=0
    s2=0
    a=IndexExos[kk]
    b=IndexExos[kk+1]
    for i in range(a,b):
        s+=FichierBareme[i]
        s2+=sum(ResultatQSNeg[i])*FichierBareme[i]/(4*NbEleve)       
    PointsExo.append(s)
    MoyenneExo.append(s2)
    kk+=1
    
    
    
    
MoyennExoEleve=[]    
kk=0
while kk<NbExoMax:
    L=[]
    for k in range(len(NomEleve)):
       
        s=0
        a=IndexExos[kk]
        b=IndexExos[kk+1]
        for i in range(a,b):
            s+=ResultatQSNeg[i][k]*FichierBareme[i]/4           
        L.append(s)
    MoyennExoEleve.append(L)
    kk+=1
    



    
    
    
########################### Enregistrement de la note sur 20 avant modification           
NoteSur20=[NoteBrute[i]*20/sum(FichierBareme) for i in range(len(NoteBrute))]            
           





###############    Moyenne de la classe    #############################
    
MoyenneClasseB=sum(NoteBrute)/NbEleve
MoyenneClasseB2=sum(MoyenneExo)   
    

MoyenneClasse=sum(NoteSur20)/NbEleve




################################    Classement Brute  ########################

ListePourTri=[[i,NoteBrute[i]] for i in range(NbEleve)]
ListeTriee = sorted(ListePourTri, key=lambda v: v[1], reverse=True)
ClassementBrute=[0 for i in range(NbEleve)]

s=1
for i in range(NbEleve):
    ClassementBrute[ListeTriee[i][0]]=s
    s+=1




################################    Classement Sur 20  ########################

ListePourTri=[[i,NoteSur20[i]] for i in range(len(NoteSur20))]
ListeTriee = sorted(ListePourTri, key=lambda v: v[1], reverse=True)
ClassementSur20=[0 for i in range(NbEleve)]

s=1
for i in range(NbEleve):
    ClassementSur20[ListeTriee[i][0]]=s
    s+=1



################################    Classement par Exo  ########################

ClassementExo=[]

for j in range(NbExoMax):
    ListePourTri=[[i,MoyennExoEleve[j][i]] for i in range(len(NoteSur20))]
    ListeTriee = sorted(ListePourTri, key=lambda v: v[1], reverse=True)
    ClassementPrelim=[0 for i in range(NbEleve)]

    s=1
    for i in range(NbEleve):
        ClassementPrelim[ListeTriee[i][0]]=s
        s+=1
    ClassementExo.append( ClassementPrelim)




################    Notes retravaillees       #########################
#manuel=False
manuel=False
Moy=MoyenneClasse
Sigma=stat.stdev(NoteSur20)


if manuel :
    MoyV=12
    SigmaV=2
else:
    MoyV=Moy             #######   V comme voulue
    SigmaV=Sigma



NoteRetenue=[(SigmaV/Sigma)*(NoteSur20[i]-Moy)+MoyV for i in range(len(NoteSur20))]
Mediane=stat.median(NoteRetenue)



################################    Classement Retravaille  ########################

ListePourTri=[[i,NoteRetenue[i]] for i in range(NbEleve)]
ListeTriee = sorted(ListePourTri, key=lambda v: v[1], reverse=True)
ClassementRetenue=[0 for i in range(NbEleve)]

s=1
for i in range(NbEleve):
    ClassementRetenue[ListeTriee[i][0]]=s
    s+=1






################      Diagnostiques           #####################################



###################  Resultats Eleves ################################## 
plt.xlim(0,20)   
plt.xticks([0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20]  )   
#plt.yticks([])      

plt.hist(NoteRetenue,bins=int(max(NoteRetenue)-min(NoteRetenue))+1,edgecolor = 'black',color='red',alpha=0.5)    
plt.hist(NoteSur20,bins=int(max(NoteSur20)-min(NoteSur20))+1,edgecolor = 'black',color='yellow',alpha=0.5)    
 
plt.axvline(x=MoyV,linestyle=':',color='Black',label="Moyenne")
plt.axvline(x=Mediane,color='Black',label="Médiane")
plt.legend()

plt.savefig("HistogramDS" , bbox_inches='tight',dpi=300)




###################  Nombre de réponse par question ################################## 

NBRep=[]                                        ## Liste contenant le nombre de réponse à chaque questions
for i in range(len(FichierBareme)):
    comp=0
    for k in range(NbEleve):
        if ResultatQ[i][k]!=-1:
            comp+=1
    NBRep.append(comp)

fig=plt.figure(figsize=(15,7.5))
Absc=[i for i in range(len(NomQuestion)) ]
my_cmap=cm.get_cmap('Spectral')
my_norm=Normalize(vmin=min(NBRep),vmax=max(NBRep))
plt.bar(Absc,NBRep,color=my_cmap(my_norm(NBRep)))    
plt.xticks(Absc,Nom,rotation='vertical')

for i in range(NbExoMax):
    plt.axvline(x=IndexExos[i+1]-0.5,color='Black',linewidth=5)



plt.savefig("NbReponsesDS" , bbox_inches='tight',dpi=300)

plt.show()


###################  Taux de réussite par question ################################## 

TauxRep=[]
TauxRepAbs=[]
for i in range(len(ResultatQ)):
    s=0
    s1=0
    for k in range(len(ResultatQ[0])):
        if ResultatQ[i][k]!=-1:
            s+=ResultatQ[i][k]
            s1+=1
    TauxRep.append(s/len(ResultatQ[i])*100/4)
    if s1!=0:
        TauxRepAbs.append(s/s1*100/4)
    else:
        TauxRepAbs.append(0)
   
fig=plt.figure(figsize=(15,7.5))  
my_cmap=cm.get_cmap('Spectral')
my_norm=Normalize(vmin=0,vmax=100)
plt.bar(Absc,TauxRep,color=my_cmap(my_norm(TauxRep)))     
plt.xticks(Absc,Nom,rotation='vertical')
for i in range(NbExoMax):
    plt.axvline(x=IndexExos[i+1]-0.5,color='Black',linewidth=5)
    
plt.savefig("TauxDeReussiteDS" , bbox_inches='tight',dpi=300)
plt.show()    



    
fig=plt.figure(figsize=(15,7.5)) 
my_cmap=cm.get_cmap('Spectral')
my_norm=Normalize(vmin=0,vmax=100)
plt.bar(Absc,TauxRepAbs,color=my_cmap(my_norm(TauxRepAbs)))       
plt.xticks(Absc,Nom,rotation='vertical')
for i in range(NbExoMax-1):
    plt.axvline(x=IndexExos[i+1]-0.5,color='Black',linewidth=5)

plt.savefig("TauxDeReussiteAvecReponseDS", bbox_inches='tight',dpi=300)

plt.show()



import xlwt

style = xlwt.easyxf('font: bold off, color black; borders: top_color black, bottom_color black, right_color black, left_color black, left thin, right thin, top thin, bottom thin; pattern: pattern solid, fore_color white; alignment: horizontal center', num_format_str ='#,##0.00')

style1 = xlwt.easyxf('font: bold off, color black; borders: top_color black, bottom_color black, right_color black, left_color black, left thin, right thin, top thin, bottom thin; pattern: pattern solid, fore_color white; alignment: horizontal center')

style2 = xlwt.easyxf('font: bold on, color black; borders: top_color black, bottom_color black, right_color black, left_color black, left medium, right medium, top medium, bottom medium; pattern: pattern solid, fore_color white; alignment: horizontal center', num_format_str ='#,##0.00')


wb = xlwt.Workbook()
ws = wb.add_sheet("Global",xlwt.Style.default_style)
ws.col(2).width = 0x1b00
ws.write(5, 2, "Nom prénom",style)
ws.write(5, 3, "Note",style)
ws.write(5, 4, "Note retenue",style)
ws.write(5, 5, "Classement",style)

ws.write(5, 6, "Moy",style)
ws.write(6, 6, "Moy Voulue",style)
ws.write(7, 6, "Ecart Type",style)
ws.write(8, 6, "E-T Voulue",style)
ws.write(5, 9, "Note Retenue",style)
ws.write(5, 10, "Verif",style)

ws.write(5, 7, Moy ,style)
ws.write(6, 7, MoyV, style)
ws.write(7, 7, Sigma ,style)
ws.write(8, 7, SigmaV ,style)

for i in range(len(NomEleve)):
    ws.write(i+6, 2, NomEleve[i],style)
    ws.write(i+6, 3, NoteSur20[i],style)
    ws.write(i+6, 4, NoteRetenue[i],style)
    chaine="($H$9/$H$8)*($D"+str(7+i)+'-$H$6)+$H$7'
    ws.write(i+6, 9, xlwt.Formula(chaine),style)
    ws.write(i+6, 5,str(ClassementSur20[i])+'/'+str(NbEleve) ,style)
    chaine2='E'+str(7+i)+'-J'+str(7+i)
    ws.write(i+6, 10, xlwt.Formula(chaine2),style)
    

e=0
Coupure=1       ############### Pour ajuster la coupure   ##############"

for eleve in NomEleve:
    ws = wb.add_sheet(eleve)
    index=0
    ws.write(1, 1, eleve)
    ws.col(2).width = 0x0800
    ws.col(3).width = 0x0800
    ws.col(7).width = 0x0800
    ws.col(8).width = 0x0800
    ws.write(3, 2, "Note",style1)
    ws.write(3, 3, "Barème",style1)
    ws.write(3, 7, "Note",style1)
    ws.write(3, 8, "Barème",style1)
    for i in range(1,len(ResultatElev[0])//2+Coupure):        
        ws.write(i+3, 1, Nom[i-1],style1)
        ws.write(i+3, 2, ResultatElev[e][i]*FichierBareme[i-1]/4 ,style1)
        ws.write(i+3, 3, FichierBareme[i-1],style1)
        if IndexExos[index]== (i-1):
            ws.write(i+3, 0, "Exercice"+str(index+1),style)
            index+=1
    for i in range(len(ResultatElev[0])//2+Coupure,len(ResultatElev[0])):
        ws.write(i+4-len(ResultatElev[e])//2-Coupure, 6, Nom[i-1],style1)
        ws.write(i+4-len(ResultatElev[e])//2-Coupure, 7, ResultatElev[e][i]*FichierBareme[i-1]/4 ,style1)
        ws.write(i+4-len(ResultatElev[e])//2-Coupure, 8, FichierBareme[i-1],style1)
        if IndexExos[index]== (i-1):
            ws.write(i+4-len(ResultatElev[e])//2-Coupure, 5, "Exercice"+str(index+1),style1)
            index+=1
    

    ws.write(4+len(ResultatElev[0])//2+Coupure, 2, "Note",style)    
    ws.write(4+len(ResultatElev[0])//2+Coupure, 3, "Barème",style)
    ws.write(4+len(ResultatElev[0])//2+Coupure, 4, "Moy. classe",style) 
    ws.write(4+len(ResultatElev[0])//2+Coupure, 5, "Classement",style)          
    for i in range(0,NbExoMax) :
        ws.write(5+i+len(ResultatElev[0])//2+Coupure, 1, "Exercice"+str(i+1),style1)  
        ws.write(5+i+len(ResultatElev[0])//2+Coupure, 2, MoyennExoEleve[i][e],style) 
        ws.write(5+i+len(ResultatElev[0])//2+Coupure, 3, PointsExo[i],style)
        ws.write(5+i+len(ResultatElev[0])//2+Coupure, 4, MoyenneExo[i],style)
        ws.write(5+i+len(ResultatElev[0])//2+Coupure, 5, str(ClassementExo[i][e])+'/'+str(NbEleve),style)
        
    ws.write(4+len(IndexExos)+len(ResultatElev[0])//2+Coupure, 1, "TOTAL",style1)   
    ws.write(4+len(IndexExos)+len(ResultatElev[0])//2+Coupure, 2,NoteBrute[e] ,style)
    ws.write(4+len(IndexExos)+len(ResultatElev[0])//2+Coupure, 3,sum(PointsExo) ,style)
    ws.write(4+len(IndexExos)+len(ResultatElev[0])//2+Coupure, 4,MoyenneClasseB ,style)
    ws.write(4+len(IndexExos)+len(ResultatElev[0])//2+Coupure, 5,str(ClassementBrute[e])+'/'+str(NbEleve) ,style)   
    
    ws.write(4+len(IndexExos)+1+len(ResultatElev[0])//2+Coupure, 1, "TOTAL /20",style1)   
    ws.write(4+len(IndexExos)+1+len(ResultatElev[0])//2+Coupure, 2,NoteSur20[e] ,style)
    ws.write(4+len(IndexExos)+1+len(ResultatElev[0])//2+Coupure, 3,'20' ,style)
    ws.write(4+len(IndexExos)+1+len(ResultatElev[0])//2+Coupure, 4,MoyenneClasse ,style)
    ws.write(4+len(IndexExos)+1+len(ResultatElev[0])//2+Coupure, 5,str(ClassementSur20[e])+'/'+str(NbEleve) ,style)
    
    
    ws.write(6+len(IndexExos)+1+len(ResultatElev[0])//2+Coupure, 1, "Note Finale",style2)   
    ws.write(6+len(IndexExos)+1+len(ResultatElev[0])//2+Coupure, 2, str(round(NoteRetenue[e],2))+'/20',style2) 
   # ws.write(6+len(IndexExos)+1+len(ResultatElev[0])//2+Coupure, 3,'',style2) 
    ws.write(6+len(IndexExos)+1+len(ResultatElev[0])//2+Coupure, 4,  str(round(MoyV,2))+'/20',style2) 
    ws.write(6+len(IndexExos)+1+len(ResultatElev[0])//2+Coupure, 5,str(ClassementRetenue[e])+'/'+str(NbEleve) ,style2)
    
    ####################  Gardes fous  si tous se passe bien cela affiche 2 zeros ######
    
    ws.write(4+len(IndexExos)+len(ResultatElev[0])//2+Coupure, 0,sum(PointsExo)-sum(FichierBareme))
    
    fin2=str(len(ResultatElev[0])+4-len(ResultatElev[e])//2-Coupure)
    fin1=str(len(ResultatElev[0])//2+Coupure+3)
    
    SommeVerif=str(NoteBrute[e])
    SommeStr='SUM(C5:C'+fin1+')+SUM(H5:H'+fin2+')-'+SommeVerif
    
    
    ws.write(4+len(IndexExos)+1+len(ResultatElev[0])//2+Coupure, 0, xlwt.Formula(SommeStr))
    
    ws.write(3+len(IndexExos)+len(ResultatElev[0])//2+Coupure, 0, MoyenneClasseB-MoyenneClasseB2)
    
    ws.write(2+len(IndexExos)+len(ResultatElev[0])//2+Coupure, 0, ClassementSur20[e]-ClassementRetenue[e])
    ##############################################################################################
    
    
    e+=1
    
wb.save("ResultatEleveDS"+NbDS+".xls")
 





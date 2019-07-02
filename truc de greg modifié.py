import json
import os
import copy
import numpy as np
import matplotlib.pyplot as plt
import csv
from mpl_toolkits.mplot3d import Axes3D
from datetime import datetime,timedelta

#RMQ : ordre des données de Russell : A,V,D

os.chdir("C:/Users/Mathieu42468/DEEZER_Project/small")

###########################################################################################Calculs débiles############################################################################################################

def moyenne(liste):
    return sum(liste)/len(liste)

def variance(liste):
    m = moyenne(liste)
    return moyenne([(x-m)**2 for x in liste])

##########################################################################################Traitement du JSON##########################################################################################################

cs_logs_dict = []
cs_song_dict = []

for line in open("centralesupelec_logs.json","r") :
    cs_logs_dict.append(json.loads(line))

for line in open("centralesupelec_song_infos.json","r") :
    cs_song_dict.append(json.loads(line))

keys_logs = cs_logs_dict[0].keys()
keys_song = cs_song_dict[0].keys()

##########################################################################Création du dictionnaire écoute + info chanson###############################################################################################

cs_full_dict = copy.deepcopy(cs_logs_dict)
n = len(cs_full_dict)

for i in range(len(cs_song_dict)):
    current_id=cs_song_dict[i]['media_id']
    current_dico=cs_song_dict[i]
    for j in range(len(cs_full_dict)):
        if cs_full_dict[j]['media_id']==current_id:
            for key in current_dico.keys():
                cs_full_dict[j][key]=current_dico[key]

####################################################################################Détermination intervalle de temps##################################################################################################

times = np.array([cs_full_dict[i]['ts_listen'] for i in range(n)])
time_max = max(times) # 6/6/2018 à 23:55:50 1528329350
time_min = min(times) # 14/5/2018 à 15:46:16 1526312776

#######################################################################################Tri liste en fonction du temps##################################################################################################

def fctSortDict(value):
    return value['ts_listen']

cs_full_dict = sorted(cs_full_dict, key=fctSortDict, reverse=False)

#{'media_id': 469235892, 'ts_listen': 1528195490, 'loc_city': 'Nantes', 'genres_names': ['hip hop', 'french hip hop'], 'artist_id': 14289, 'anon_user_id': 'f6beec01c5aadf247abb636b69047ef2515614c2', 'is_listened': 1, 'mood_global_value': [0.062405698001384735, 0.2025985587388277, 0.1322154535446316]}

##################################################################################Vérification répartition dans le temps################################################################################################
"""
entry = [i for i in range(n-100,n)]
time_red = [cs_full_dict[i]['ts_listen'] - time_min for i in entry]

plt.plot(entry, time_red)
plt.show()
"""

# Au début les données sont assez espacées, à la fin elles sont très proches -> plutôt utiliser la fin

################################################################################################PARTIE DU CODE A MODIFIER################################################################################################
###################################################################################Retrait des valeurs où il manque le Russell###########################################################################################

#Jsais pas pourquoi mais il manque des Russell parfois, donc on vire direct

new=[]
for dico in cs_full_dict:
    if 'mood_global_value' in dico:
        new.append(dico)
cs_full_dict=new

###################################################################Fusion avec les données météo (a compléter quand on aura toutes les bonnes données météo)###############################################################

csv.register_dialect('myDialect', delimiter = ';')
with open("2018_donnees_synop_Nantes.csv",'r') as csvfile:
    reader = csv.DictReader(csvfile, dialect='myDialect')
    meteo_nantes = []
    for row in reader:
        meteo_nantes.append(dict(row))

with open("2018_donnees_synop_Nice.csv",'r') as csvfile1:
    reader = csv.DictReader(csvfile1, dialect='myDialect')
    meteo_nice = []
    for row in reader:
        meteo_nice.append(dict(row))


decalage = timedelta(hours=1, minutes=30)

for entree in meteo_nantes:
    entree['Date']=entree['Date'][:19] #on supprime la partie "décalage horaire" de la date, inutile
    entree['logs']=[] #Les logs seront stockés dans une liste
    date = datetime.strptime(entree['Date'], "%Y-%m-%dT%H:%M:%S") #ISO 8601 converti en date
    for log in cs_full_dict:
        if log['loc_city']=='Nantes':
            ts = datetime.fromtimestamp(log['ts_listen']) ##le timestamp unix converti en date
            if date-decalage<ts and ts<=date+decalage:
                entree['logs'].append(log)

for entree in meteo_nice:
    entree['Date']=entree['Date'][:19] #on supprime la partie "décalage horaire" de la date, inutile
    entree['logs']=[] #Les logs seront stockés dans une liste
    date = datetime.strptime(entree['Date'], "%Y-%m-%dT%H:%M:%S") #ISO 8601 converti en date
    for log in cs_full_dict:
        if log['loc_city']=='Nice':
            ts = datetime.fromtimestamp(log['ts_listen']) #le timestamp unix converti en date
            if date-decalage<ts and ts<=date+decalage:
                entree['logs'].append(log)

#print([meteo_nantes[i]['logs'] for i in range(len(meteo_nantes))])

###################################Arousal en fonction du temps et de la météo EN GLOBAL (pas pour un unique user : on considère la moyenne de l'arousal de ce que chacun écoute)#########################################
time_list=[entree['Date'] for entree in meteo_nice]
mean_arousal_list=[]
for entree in meteo_nice:
    if entree['logs']!=[]:
        moy=moyenne([log['mood_global_value'][1] for log in entree['logs']])
        mean_arousal_list.append(moy)
    else:
        mean_arousal_list.append(0)

weather_list=[entree['Temps passÃ© 1'] for entree in meteo_nice]
plt.plot(time_list,weather_list,'ro')
plt.plot(time_list,mean_arousal_list,'b^')
plt.show()

"""
##########################################################################################Visualisation des Russell######################################################################################################

russell_global = [[cs_full_dict[i]['mood_global_value'][0], cs_full_dict[i]['mood_global_value'][1], cs_full_dict[i]['mood_global_value'][2]] for i in entry]

russell_global_x = [russell_global[i][0] for i in entry]
russell_global_y = [russell_global[i][1] for i in entry]
russell_global_z = [russell_global[i][2] for i in entry]

x_global_moy, x_global_var = moyenne(russell_global_x), variance(russell_global_x)
y_global_moy, y_global_var = moyenne(russell_global_y), variance(russell_global_y)
z_global_moy, z_global_var = moyenne(russell_global_z), variance(russell_global_z)

# fig = plt.figure()
# ax = fig.gca(projection='3d')
# ax.scatter3D(russell_x, russell_y, russell_z)

plt.plot(entry, russell_global_x, 'b')
plt.plot(entry, russell_global_y, 'r')
plt.plot(entry, russell_global_z, 'g')

plt.show()

# C'est assez anarchique pour l'ensemble des utilisateurs, mais peut-être qu'on peut chercher utilisateur par utilisateur

####################################################################################Utilisateurs présents à cette période################################################################################################

liste_user = []

for i in entry :
    if cs_full_dict[i]['anon_user_id'] not in liste_user :
        liste_user.append(cs_full_dict[i]['anon_user_id'])

# Y'a que 9 utilisateurs pour 94 entrées : beaucoup de répétitions et ça c'est coooooooooooooooooooooooooool. Ca veut dire qu'on peut se permettre d'étudier le comportement d'un utilisateur sur une période courte

##############################################################################################Test pour un utilisateur##################################################################################################

user = liste_user[2]

donnees_user = [cs_full_dict[i] for i in range(n) if cs_full_dict[i]['anon_user_id'] == user]
n_user = len(donnees_user)

russell_user = [[donnees_user[i]['mood_global_value'][0], donnees_user[i]['mood_global_value'][1], donnees_user[i]['mood_global_value'][2]] for i in range(n_user)]

russell_user_x = [russell_user[i][0] for i in range(n_user)]
russell_user_y = [russell_user[i][1] for i in range(n_user)]
russell_user_z = [russell_user[i][2] for i in range(n_user)]

x_user_moy, x_user_var = moyenne(russell_user_x), variance(russell_user_x)
y_user_moy, y_user_var = moyenne(russell_user_y), variance(russell_user_y)
z_user_moy, z_user_var = moyenne(russell_user_z), variance(russell_user_z)

plt.plot([i for i in range(n_user)], russell_user_x, 'b')
plt.plot([i for i in range(n_user)], russell_user_y, 'r')
plt.plot([i for i in range(n_user)], russell_user_z, 'g')

print([[x_user_moy, x_user_var], [y_user_moy, y_user_var], [z_user_moy, z_user_var]])
plt.show()

# Alors on obtient que pour certains utilisateurs, la variance est moindre que la variance globale. C'est cool mais il faut voir à quel point c'est pertinent.

#####################################################################################################Test PCA#############################################################################################################

russell_global_x_PCA = [russell_global_x[i] - x_global_moy for i in range(n)]
russell_global_y_PCA = [russell_global_y[i] - y_global_moy for i in range(n)]
russell_global_z_PCA = [russell_global_z[i] - z_global_moy for i in range(n)]


tD = np.array([russell_global_x_PCA, russell_global_y_PCA, russell_global_z_PCA])
D = np.transpose(tD)

M = np.dot(tD,D)/n
M_diag = np.linalg.eig(M)[0]

# Une valeur propre est très très faible devant les autres : on peut la négliger, et dire que seulement 2 variables sont utiles
"""

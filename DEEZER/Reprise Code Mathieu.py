import json
import os
import copy
import numpy as np
import matplotlib.pyplot as plt
import csv
from mpl_toolkits.mplot3d import Axes3D
from datetime import datetime,timedelta

#RMQ : ordre des données de Russell : A,V,D

#os.chdir("C:/Users/Mathieu42468/DEEZER_Project/small")

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
with open("2018-donnees-synop-Nantes-Mathieu.csv",'r') as csvfile:
    reader = csv.DictReader(csvfile, dialect='myDialect')
    meteo_nantes = []
    for row in reader:
        meteo_nantes.append(dict(row))

with open("2018-donnees-synop-Nice-Mathieu.csv",'r') as csvfile1:
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

print([meteo_nantes[i]['logs'] for i in range(len(meteo_nantes))])

import pandas as pd
import json
import copy
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import csv
from datetime import datetime,timedelta

cs_logs = []
for line in open('centralesupelec_logs.json', 'r'):
    cs_logs.append(json.loads(line))

#{'media_id': 1176220, 'mood_global_value': [0.2669834867119789, -0.13525773119181395, 0.35506816394627094], 'genres_names': ['alternative', 'pop']}

cs_song_infos=[]
for line in open('centralesupelec_song_infos.json', 'r'):
    cs_song_infos.append(json.loads(line))

#{'anon_user_id': '5446b828bebb9e4a6bf7464747e32da9278c75db', 'media_id': 491449632, 'artist_id': 174351, 'loc_city': 'Nantes', 'ts_listen': 1528292798, 'is_listened': 1}

####################################### Création du dictionnaire écoute + info chanson #######################################

cs_joint=copy.deepcopy(cs_logs)
for i in range(len(cs_song_infos)):
    current_id=cs_song_infos[i]['media_id']
    current_dico=cs_song_infos[i]
    for j in range(len(cs_joint)):
        if cs_joint[j]['media_id']==current_id:
            for key in current_dico.keys():
                cs_joint[j][key]=current_dico[key]


csv.register_dialect('myDialect', delimiter = ';')
with open("2018-donnees-synop-Nantes.csv",'r') as csvfile:
    reader = csv.DictReader(csvfile, dialect='myDialect')
    meteo_nantes = []
    for row in reader:
        meteo_nantes.append(dict(row))

with open("2018-donnees-synop-Nice.csv",'r') as csvfile1:
    reader = csv.DictReader(csvfile1, dialect='myDialect')
    meteo_nice = []
    for row in reader:
        meteo_nice.append(dict(row))

#print(meteos)
#print(meteos[0]['Date'])

meteos_bonne_date_nantes=[]
for entree in meteo_nantes:
    entree['Date']=entree['Date'][:19] ##on supprime la partie "décalage horaire" de la date, inutile
    if datetime.strptime(entree['Date'], "%Y-%m-%dT%H:%M:%S")>=datetime(2018, 5, 14, 15, 46, 16) and datetime.strptime(entree['Date'], "%Y-%m-%dT%H:%M:%S")<=datetime(2018, 6, 6, 23, 55, 50):
         entree['Date'] = datetime.strptime(entree['Date'], "%Y-%m-%dT%H:%M:%S") ##ISO 8601 converti en date
         meteos_bonne_date_nantes.append(entree)

meteos_bonne_date_nice=[]
for entree in meteo_nice:
    entree['Date']=entree['Date'][:19] ##on supprime la partie "décalage horaire" de la date, inutile
    if datetime.strptime(entree['Date'], "%Y-%m-%dT%H:%M:%S")>=datetime(2018, 5, 14, 15, 46, 16) and datetime.strptime(entree['Date'], "%Y-%m-%dT%H:%M:%S")<=datetime(2018, 6, 6, 23, 55, 50):
         entree['Date'] = datetime.strptime(entree['Date'], "%Y-%m-%dT%H:%M:%S") ##ISO 8601 converti en date
         meteos_bonne_date_nice.append(entree)
#print(datetime(2018, 5, 14, 15, 46, 16))
#print(meteos_bonne_date_nantes[0])


##Go trier les logs par date !

decalage = timedelta(hours=1, minutes=30)

for entree in meteos_bonne_date_nantes:
     date = entree['Date']
     entree['logs']=[] ##Les logs seront stockés dans une liste
     for log in cs_joint:
         if log['loc_city']=='Nantes':
             ts = datetime.fromtimestamp(log['ts_listen']) ##le timestamp unix converti en date
             if date-decalage<ts and ts<=date+decalage :
                 entree['logs'].append(log)

for entree in meteos_bonne_date_nice:
     date = entree['Date']
     entree['logs']=[] ##Les logs seront stockés dans une liste
     for log in cs_joint:
         if log['loc_city']=='Nice':
             ts = datetime.fromtimestamp(log['ts_listen']) ##le timestamp unix converti en date
             if date-decalage<ts and ts<=date+decalage :
                 entree['logs'].append(log)

print(len([meteos_bonne_date_nantes[i]['logs'] for i in range(len(meteos_bonne_date_nantes))]))
print(meteos_bonne_date_nantes[0])
print(cs_joint[0])

####################################### Print Russell en fonction précipitation #######################################

Arousal=[]
Valence=[]
Précipitation=[]
for entree in meteos_bonne_date_nantes:
    for log in entree['logs']:
        if 'mood_global_value' in log:
            Arousal.append(log['mood_global_value'][0])
            Valence.append(log['mood_global_value'][1])
            Précipitation.append(float(entree['PrÃ©cipitations dans les 3 derniÃ¨res heures']))

#print(Arousal)
#print(Précipitation)
plt.plot(Arousal,Précipitation, "r^")
plt.show()
plt.plot(Valence,Précipitation, "bo")
plt.show()


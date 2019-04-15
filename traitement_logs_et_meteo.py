import json
import os
import matplotlib.pyplot as plt

## On commence par créer les listes des logs et chansons séparés
logs = []
for line in open('centralesupelec_logs.json', 'r'):
    logs.append(json.loads(line))

songs = []
for line in open('centralesupelec_song_infos.json', 'r'):
    songs.append(json.loads(line))



## On vire les logs pour lesquels on a pas la chanson

truelogs=[]
for log in logs:
    b = False
    id=log['media_id']
    for song in songs:
        if song['media_id']==id:
            b=True
    if b:
        truelogs.append(log)

songdict={}

for song in songs:
    songdict[song['media_id']]=song

for log in truelogs:
    log['song_info']=songdict[log['media_id']]



## Forme des logs : truelogs = liste de dictionnaires log, truelogs[0]={'anon_user_id': '5446b828bebb9e4a6bf7464747e32da9278c75db', 'media_id': 491449632, 'artist_id': 174351, 'loc_city': 'Nantes', 'ts_listen': 1528292798, 'is_listened': 1, 'song_info': {'media_id': 491449632, 'mood_global_value': [0.26812779406706494, -0.18350800250967345, 0.34582894543806714], 'genres_names': ['pop']}}


## Maintenant, on s'occupe de la météo : liste de dictionnaires (1 dict =  1 entrée météo)

import csv
from datetime import datetime,timedelta

csv.register_dialect('myDialect', delimiter = ';')
with open("donnees_synop.csv", 'r') as csvfile:
    reader = csv.DictReader(csvfile, dialect='myDialect')
    meteos = []
    for row in reader:
        meteos.append(dict(row))


##Go trier les logs par date !

decalage = timedelta(hours=1, minutes=30)

for entree in meteos:
    entree['Date']=entree['Date'][:19] ##on supprime la partie "décalage horaire" de la date, inutile
    entree['logs']=[] ##Les logs seront stockés dans une liste
    date = datetime.strptime(entree['Date'], "%Y-%m-%dT%H:%M:%S") ##ISO 8601 converti en date
    for log in truelogs:
        ts = datetime.fromtimestamp(log['ts_listen']) ##le timestamp unix converti en date
        if date-decalage<ts and ts<=date+decalage :
            entree['logs'].append(log)














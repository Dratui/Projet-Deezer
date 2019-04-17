import json
import os 
import copy
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import requests

os.chdir("D:\\Documents\\Cours\\Deezer_Données\\Données\\small")

## Calculs débiles

def moyenne(liste) :
    return sum(liste)/len(liste)
    
def variance(liste) :
    m = moyenne(liste)
    return moyenne([(x-m)**2 for x in liste])
 
## Traitement du JSON data 
    
cs_logs_dict = []
cs_song_dict = []

for line in open("centralesupelec_logs.json","r") :
    cs_logs_dict.append(json.loads(line))
    
for line in open("centralesupelec_song_infos.json","r") :
    cs_song_dict.append(json.loads(line))
    
keys_logs = cs_logs_dict[0].keys()
keys_song = cs_song_dict[0].keys()

## Création du dictionnaire écoute + info chanson

cs_full_dict = copy.deepcopy(cs_logs_dict)
n = len(cs_full_dict)

for i in range(len(cs_song_dict)):
    current_id=cs_song_dict[i]['media_id']
    current_dico=cs_song_dict[i]
    for j in range(len(cs_full_dict)):
        if cs_full_dict[j]['media_id']==current_id:
            for key in current_dico.keys():
                cs_full_dict[j][key]=current_dico[key]
                
cs_full_dict_ref = copy.deepcopy(cs_full_dict) # Référence à ne pas toucher
n_ref = len(cs_full_dict_ref)
                
# Par exemple cs_full_dict {'artist_id': 174351, 'genres_names': ['pop'], 'anon_user_id': '5446b828bebb9e4a6bf7464747e32da9278c75db', 'mood_global_value': [0.26812779406706494, -0.18350800250967345, 0.34582894543806714], 'loc_city': 'Nantes', 'is_listened': 1, 'ts_listen': 1528292798, 'media_id': 491449632}

                
## Détermination intervalle de temps

times = np.array([cs_full_dict[i]['ts_listen'] for i in range(n)])
time_min = min(times) # 14/5/2018 à 15:46:16 1526312776
time_max = max(times) # 6/6/2018 à 23:55:50 1528329350

## Tri liste en fonction du temps

def fctSortDict(value):
    return value['ts_listen']
    
cs_full_dict = sorted(cs_full_dict, key=fctSortDict, reverse=False)

## Retrait des valeurs où il manque le Russell 

entry = [i for i in range(n_ref-100,n_ref)]
liste_manquant = []

for i in entry :
    if 'mood_global_value' not in cs_full_dict[i].keys() :
        liste_manquant.append(i)

cs_full_dict = [cs_full_dict[i] for i in entry if i not in liste_manquant]

n = len(cs_full_dict)
entry = [i for i in range(min(50,n))]

# Jsais pas pourquoi mais il manque des Russell parfois, donc on vire direct

## Ajout bpm gain

for i in entry :
    media_id = cs_full_dict[i]['media_id']
    URL = "https://api.deezer.com/track/" + str(media_id)
    r = requests.get(url = URL)
    data = r.json()
    cs_full_dict[i]['gain'] = data['gain']
    cs_full_dict[i]['bpm'] = data['bpm']

## Corrélation BPM Gain autre

liste_bpm = [cs_full_dict[i]['bpm'] for i in entry]
liste_gain = [cs_full_dict[i]['gain'] for i in entry]
liste_arousal = [cs_full_dict[i]['mood_global_value'][0] for i in entry]
liste_valence = [cs_full_dict[i]['mood_global_value'][1] for i in entry]

valence_moy = moyenne(liste_valence)
arousal_moy = moyenne(liste_arousal)

liste_valence_PCA = [liste_valence[i] - valence_moy for i in entry]
liste_arousal_PCA = [liste_arousal[i] - arousal_moy for i in entry]

Dt = np.array([liste_valence_PCA, liste_arousal_PCA])
D = np.transpose(Dt)

M = np.dot(Dt,D)/50
M_diag = np.linalg.eig(M)

plt.plot(liste_arousal, liste_valence, 'b+')
plt.show()

## Corrélation mais sans erreur

liste_bpm = [cs_full_dict[i]['bpm'] for i in entry]
liste_gain = [cs_full_dict[i]['gain'] for i in entry]
liste_arousal = [cs_full_dict[i]['mood_global_value'][0] for i in entry]
liste_valence = [cs_full_dict[i]['mood_global_value'][1] for i in entry]

bpm_moy, bpm_var = moyenne(liste_bpm), variance(liste_bpm)
gain_moy, gain_var = moyenne(liste_gain), variance(liste_gain)
arousal_moy, arousal_var = moyenne(liste_arousal), variance(liste_arousal)
valence_moy, valence_var = moyenne(liste_valence), variance(liste_valence)

liste_valence_PCA = [(liste_valence[i] - valence_moy)/(valence_var**0.5) for i in entry]
liste_arousal_PCA = [(liste_arousal[i] - arousal_moy)/(arousal_var**0.5) for i in entry]
liste_bpm_PCA = [(liste_bpm[i] - bpm_moy)/(bpm_var)**0.5 for i in entry]
liste_gain_PCA = [(liste_gain[i] - gain_moy)/(gain_var)**0.5 for i in entry]

Dt = np.array([liste_bpm_PCA, liste_gain_PCA, liste_valence_PCA, liste_arousal_PCA])
D = np.transpose(Dt)

M = np.dot(Dt,D)/50
M_diag = np.linalg.eig(M)

plt.plot(liste_valence_PCA, liste_gain_PCA, 'b+')
plt.show()


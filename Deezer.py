import json
import copy
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime,timedelta

def moyenne(liste) :
    return sum(liste)/len(liste)

def variance(liste) :
    m = moyenne(liste)
    return moyenne([(x-m)**2 for x in liste])

## Traitement du JSON (merci léo)

cs_logs_dict = []
cs_song_dict = []

for line in open("centralesupelec_logs.json","r") :
    cs_logs_dict.append(json.loads(line))

for line in open("centralesupelec_song_infos.json","r") :
    cs_song_dict.append(json.loads(line))

keys_logs = cs_logs_dict[0].keys()
keys_song = cs_song_dict[0].keys()

cs_full_dict = copy.deepcopy(cs_logs_dict)
n = len(cs_full_dict)

for i in range(len(cs_song_dict)):
    current_id=cs_song_dict[i]['media_id']
    current_dico=cs_song_dict[i]
    for j in range(len(cs_full_dict)):
        if cs_full_dict[j]['media_id']==current_id:
            for key in current_dico.keys():
                cs_full_dict[j][key]=current_dico[key]

dico_nuit_id, dico_jour_id={},{} #dictionnaires sous la forme: dico_id[anon_user_id]=[nombre de morceaux écoutés, arousal moyen, valence moyenne]

print(cs_full_dict)

for hearing in cs_full_dict:
    hour = datetime.fromtimestamp(hearing["ts_listen"]).hour
    if hour < 8 or hour>=20:
        if hearing["anon_user_idea"] in dico_nuit_id.keys():
            tab_moyenne = dico_nuit_id[hearing["anon_user_idea"]]
            dico_nuit_id[hearing["anon_user_id"]]=[tab_moyenne[0]+1,(tab_moyenne[0]*tab_moyenne[1]+hearing["mood_global_value"][0])/tab_moyenne[0]+1,(tab_moyenne[0]*tab_moyenne[2]+hearing["mood_global_value"][1])/tab_moyenne[0]+1]
        else:
            dico_nuit_id[hearing["anon_user_id"]]=[1, hearing["mood_global_value"][0], hearing["mood_global_value"][1]]
    else:
        if hearing["anon_user_idea"] in dico_jour_id.keys():
            tab_moyenne = dico_jour_id[hearing["anon_user_idea"]]
            dico_jour_id[hearing["anon_user_id"]]=[tab_moyenne[0]+1,(tab_moyenne[0]*tab_moyenne[1]+hearing["mood_global_value"][0])/tab_moyenne[0]+1,(tab_moyenne[0]*tab_moyenne[2]+hearing["mood_global_value"][1])/tab_moyenne[0]+1]
        else:
            dico_jour_id[hearing["anon_user_id"]]=[1, hearing["mood_global_value"][0], hearing["mood_global_value"][1]]


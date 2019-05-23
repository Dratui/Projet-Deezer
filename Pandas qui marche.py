import json
import os 
import copy
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import pandas as pd
import matplotlib.patches as pat


cs_logs_dict = []
cs_song_dict = []

os.chdir("D:\\Documents\\Cours\\Deezer_Données\\Données\\medium")

## Création des DataFrame

with open("centralesupelec_logs.json", encoding="utf8") as f:
    data = f.readlines()
    data = [json.loads(line) for line in data]
    
df_logs = pd.DataFrame(data)

with open("centralesupelec_song_infos.json", encoding="utf8") as f:
    data = f.readlines()
    data = [json.loads(line) for line in data]
    
df_songs = pd.DataFrame(data)

df_total = pd.merge(df_songs, df_logs)

df_total.sort_values(by = 'ts_listen')
df_total=df_total.drop(df_total[df_total.mood_global_value == np.NaN].index)
df_total_copy = copy.deepcopy(df_total)

## Couverture temporelle


min_temp = df_total.iloc[0,9] ## 1528190137
max_temp = df_total.iloc[-1,9] ## 1529308893

## Séparation mood_global_value

list_mood = np.concatenate(df_total_copy['mood_global_value'])
list_mood = np.reshape(list_mood, (584153,3))

df_total['Arousal'] = list_mood[:,0]
df_total['Valence'] = list_mood[:,1]

df_total.describe() ## Arousal moy 0.283979 std moy Valence 0.122458

moyA_total, moyV_total, varA_total, varV_total = df_total['Arousal'].mean(), df_total['Valence'].mean(), df_total['Arousal'].std(), df_total['Valence'].std()


## Traitement par utilisateur

list_user = []

list_user = df_total_copy['anon_user_id'].unique()

list_moyA = []
list_varA = []
list_moyV = []
list_varV = []


for user in list_user :
    df_user = df_total.loc[df_total['anon_user_id'] == user]
    moyA, moyV, varA, varV = df_user['Arousal'].mean(), df_user['Valence'].mean(), df_user['Arousal'].std(), df_user['Valence'].std()
    list_moyA.append(moyA)
    list_moyV.append(moyV)
    list_varA.append(varA)
    list_varV.append(varV)
    
## Etude sigma

ratio_sig = []

for i in range(len(list_moyA)) :
    if list_varV[i] == 0 :
        ratio_sig.append(0)
    else :
        ratio_sig.append(list_varA[i]/list_varV[i])
        if list_varA[i]/list_varV[i] > 80 :
            print(i)
        
        
plt.plot([i for i in range(len(list_moyA))], ratio_sig, '+')
plt.show()

ratio_sig = np.array(ratio_sig)
ratio_mean = np.nanmean(ratio_sig)
ratio_std = np.nanstd(ratio_sig)
    
    
## Tracé des moyennes

center = pat.Ellipse((moyA_total, moyV_total), varA_total, varV_total, ec = 'r', fc = 'none')

fig = plt.figure(0)
ax = fig.add_subplot(111, aspect='equal')

for i in range(len(list_moyA)) :
    ell = pat.Ellipse((list_moyA[i], list_moyV[i]), list_varA[i], list_varV[i], ec = 'b', fc = 'none', lw = 1)
    ax.add_artist(ell)
    
ax.add_artist(center)
    

plt.show()

## Pareil mais centré

center = pat.Ellipse((0, 0), varA_total, varV_total, ec = 'r', fc = 'none')

fig = plt.figure(0)
ax = fig.add_subplot(111, aspect='equal')

for i in range(len(list_moyA)) :
    ell = pat.Ellipse((0, 0), list_varA[i], list_varV[i], ec = 'b', fc = 'none', lw = 1)
    ax.add_artist(ell)
    
ax.add_artist(center)
    

plt.show()

## Traitement pour certains users

list_user = []

list_user = df_total_copy['anon_user_id'].unique()
list_user = np.random.choice(list_user, size = 100)

list_moyA = []
list_varA = []
list_moyV = []
list_varV = []


for user in list_user :
    df_user = df_total.loc[df_total['anon_user_id'] == user]
    moyA, moyV, varA, varV = df_user['Arousal'].mean(), df_user['Valence'].mean(), df_user['Arousal'].std(), df_user['Valence'].std()
    list_moyA.append(moyA)
    list_moyV.append(moyV)
    list_varA.append(varA)
    list_varV.append(varV)

## Tracé des moyennes pour certains users

center = pat.Ellipse((moyA_total, moyV_total), varA_total, varV_total, ec = 'r', fc = 'none')

fig = plt.figure(0)
ax = fig.add_subplot(111, aspect='equal')

for i in range(len(list_moyA)) :
    ell = pat.Ellipse((list_moyA[i], list_moyV[i]), list_varA[i], list_varV[i], ec = 'b', fc = 'none', lw = 1)
    ax.add_artist(ell)
    
ax.add_artist(center)
    

plt.show()

## Pareil mais centré pour certains users

center = pat.Ellipse((0, 0), varA_total, varV_total, ec = 'r', fc = 'none')

fig = plt.figure(0)
ax = fig.add_subplot(111, aspect='equal')

for i in range(len(list_moyA)) :
    ell = pat.Ellipse((0, 0), list_varA[i], list_varV[i], ec = 'b', fc = 'none', lw = 1)
    ax.add_artist(ell)
    
ax.add_artist(center)
    

plt.show()



    

    

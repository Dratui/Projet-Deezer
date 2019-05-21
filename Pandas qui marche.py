import json
import os 
import copy
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import pandas as pd


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

df_total = df_logs.join(df_songs, lsuffix = "media_id", rsuffix = "media_id")

df_total_copy = copy.deepcopy(df_total)

## Couverture temporelle

min_temp = df_total.iloc[0,5] ## 1516726862 23/1/2018 à 17:01:02 
max_temp = df_total.iloc[-1,5] ## 1529238761 17/6/2018 à 12:32:41 

## Traitement par utilisateur


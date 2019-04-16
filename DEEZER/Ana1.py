import pandas as pd
import json
import copy
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

cs_logs = []
for line in open('centralesupelec_logs.json', 'r'):
    cs_logs.append(json.loads(line))

cs_song_infos=[]
for line in open('centralesupelec_song_infos.json', 'r'):
    cs_song_infos.append(json.loads(line))

#print(cs_song_infos[0])
#print(cs_logs[0])

cs_joint=copy.deepcopy(cs_logs)

for i in range(len(cs_song_infos)):
    current_id=cs_song_infos[i]['media_id']
    current_dico=cs_song_infos[i]
    for j in range(len(cs_joint)):
        if cs_joint[j]['media_id']==current_id:
            for key in current_dico.keys():
                cs_joint[j][key]=current_dico[key]

#long=len(cs_joint[0])
#for i in range(len(cs_joint)):
#    if len(cs_joint[i])!=long:
#        print('probleme')
#
#print(cs_joint[0])

fig = plt.figure()
#ax = fig.add_subplot(111, projection='3d')
xs=[]
ys=[]
zs=[]
for song in cs_song_infos:
    xs.append(song['mood_global_value'][0])
    ys.append(song['mood_global_value'][1])
    zs.append(song['mood_global_value'][2])
#ax.scatter(xs,ys,zs)
#ax.set_xlabel('X label')

cs_triplet=[]
for song in cs_song_infos:
    cs_triplet.append(song['mood_global_value'])

print(cs_triplet)

t = np.array(cs_triplet)
print(np.argmax(t[:, 0]))

print(cs_song_infos[7470]['media_id'])


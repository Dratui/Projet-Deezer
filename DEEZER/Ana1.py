import pandas as pd
import json
import copy
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

def moyenne(liste) :
    return sum(liste)/len(liste)

def variance(liste) :
    m = moyenne(liste)
    return moyenne([(x-m)**2 for x in liste])

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

#{'anon_user_id': '5446b828bebb9e4a6bf7464747e32da9278c75db', 'media_id': 491449632, 'artist_id': 174351, 'loc_city': 'Nantes', 'ts_listen': 1528292798, 'is_listened': 1, 'mood_global_value': [0.26812779406706494, -0.18350800250967345, 0.34582894543806714], 'genres_names': ['pop']}

#long=len(cs_joint[0])
#for i in range(len(cs_joint)):
#    if len(cs_joint[i])!=long:
#        print('probleme')
#


####################################### Affichage Russell #######################################
'''
print(cs_joint[0])

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
xs=[]
ys=[]
zs=[]
for song in cs_song_infos:
    xs.append(song['mood_global_value'][0])
    ys.append(song['mood_global_value'][1])
    zs.append(song['mood_global_value'][2])
ax.scatter(xs,ys,zs)
ax.set_xlabel('X label')
plt.show()
'''
####################################### Test avec Gilles Chardon #######################################
# cs_triplet=[]
# for song in cs_song_infos:
#     cs_triplet.append(song['mood_global_value'])
#
# print(cs_triplet)
#
# t = np.array(cs_triplet)
# print(np.argmax(t[:, 0]))
#
# print(cs_song_infos[7470]['media_id'])


####################################### Tri liste en fonction du temps #######################################

def fctSortDict(value):
    return value['ts_listen']

cs_full_dict = sorted(cs_joint, key=fctSortDict, reverse=False)

####################################### Retirer les chansons sans russell #######################################

n = len(cs_full_dict)
entry = [i for i in range(n-100,n)]
liste_manquant = []

for i in entry :
    if 'mood_global_value' not in cs_full_dict[i].keys() :
        liste_manquant.append(i)

cs_full_dict = [cs_full_dict[i] for i in entry if i not in liste_manquant]

n = len(cs_full_dict)
entry = [i for i in range(n-100,n)]

# Jsais pas pourquoi mais il manque des Russell parfois, donc on vire direct

####################################### Visualisation des Russell #######################################

russell_global = [[cs_full_dict[i]['mood_global_value'][0], cs_full_dict[i]['mood_global_value'][1], cs_full_dict[i]['mood_global_value'][2]] for i in entry]

russell_global_x = [russell_global[i][0] for i in entry]
russell_global_y = [russell_global[i][1] for i in entry]
russell_global_z = [russell_global[i][2] for i in entry]

x_global_moy, x_global_var = moyenne(russell_global_x), variance(russell_global_x)
y_global_moy, y_global_var = moyenne(russell_global_y), variance(russell_global_y)
z_global_moy, z_global_var = moyenne(russell_global_z), variance(russell_global_z)

fig = plt.figure()
ax = fig.gca(projection='3d')
ax.scatter3D(russell_global_x, russell_global_y, russell_global_z)

#plt.plot(entry, russell_global_x, 'b')
#plt.plot(entry, russell_global_y, 'r')
#plt.plot(entry, russell_global_z, 'g')

plt.show()

# C'est assez anarchique pour l'ensemble des utilisateurs, mais peut-être qu'on peut chercher utilisateur par utilisateur

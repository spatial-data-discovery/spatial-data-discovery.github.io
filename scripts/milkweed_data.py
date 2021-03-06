# -*- coding: utf-8 -*-
"""Preliminary Plots"""

#This script takes a .csv file of morphological data from three different species of milkweed: Asclepias exaltata, Asclepias syriaca, and Asclepias speciosa
#KThe script also conducts a principal component analysis using 6 appropriately scaled variables: leaf width, leaf length, basal angle, tip angle, ratio of petiole to tip, ratio of length by width
#IDE used: Spyder (Anaconda)
import csv
import pandas as pd
import seaborn as sns
#import matplotlib
import numpy as np

from matplotlib import pyplot
from sklearn.decomposition import PCA
from sklearn import preprocessing
from pathlib import Path

data_file = Path("milkweed_leaf_data.csv")
leaf_width_ex = []
leaf_length_ex = []

leaf_width_syr = []
leaf_length_syr = []  

leaf_width_sp = []
leaf_length_sp = []

basal_angle_ex = []
basal_angle_syr = []
basal_angle_sp = []

tip_angle_ex = []
tip_angle_syr = []
tip_angle_sp = []

pbt_ex = []
pbt_syr = []
pbt_sp = []

lbw_ex = []
lbw_syr = []
lbw_sp = []

species_list = []
ID_list = []
var_list = ['leaf length', 'leaf width', 'basal angle', 'tip angle', 'petiole-total ratio', 'length-width ratio']
#making master list of lists
feed_to_PCA = []

#cleaning and conversion
with open (data_file, 'r', newline = '' ) as data:
    asc = csv.DictReader(data)
    for x in asc:
        species_list.append(x['species'])
        ID_list.append(x['ID'])
        if x['species'] == 'exaltata':
            leaf_width_ex.append(100 * (float(x['wlength'])/float(x['tlength'])))
            leaf_length_ex.append(100 * (float(x['llength'])/float(x['tlength'])))
            basal_angle_ex.append(float(x['bangle']))
            tip_angle_ex.append(float(x['tipangle']))
            pbt_ex.append(float(x['petiole_by_total']))
            lbw_ex.append(float(x['length_by_width']))
            
        if x['species'] == 'syriaca':  
            leaf_width_syr.append(100 * (float(x['wlength'])/float(x['tlength'])))
            leaf_length_syr.append(100 * (float(x['llength'])/float(x['tlength'])))
            basal_angle_syr.append(float(x['bangle']))
            tip_angle_syr.append(float(x['tipangle']))
            pbt_syr.append(float(x['petiole_by_total']))
            lbw_syr.append(float(x['length_by_width']))
            
        if x['species'] == 'speciosa':  
            leaf_width_sp.append(100 * (float(x['wlength'])/float(x['tlength'])))
            leaf_length_sp.append(100 * (float(x['llength'])/float(x['tlength'])))
            basal_angle_sp.append(float(x['bangle']))
            tip_angle_sp.append(float(x['tipangle']))
            pbt_sp.append(float(x['petiole_by_total']))
            lbw_sp.append(float(x['length_by_width']))

#creating vectors to feed into matplotlib PCA object
length_vector = leaf_length_ex + leaf_length_syr + leaf_length_sp
width_vector = leaf_width_ex + leaf_width_syr + leaf_width_sp
b_angle_vector = basal_angle_ex + basal_angle_syr + basal_angle_sp
tip_angle_vector = tip_angle_ex + tip_angle_syr + tip_angle_sp
pbt_vector = pbt_ex + pbt_syr + pbt_sp
lbw_vector = lbw_ex + lbw_syr + lbw_sp 

#adding lists to the master list of lists to convert to array
feed_to_PCA.append(length_vector)
feed_to_PCA.append(width_vector)
feed_to_PCA.append(b_angle_vector)
feed_to_PCA.append(tip_angle_vector)
feed_to_PCA.append(pbt_vector)
feed_to_PCA.append(lbw_vector)

#conversion to numpy array (unnecessary but useful if needed for matplotlib PCA)
array = np.array(feed_to_PCA)
array_scaled = preprocessing.scale(array) #scaling data before running PCA
df_scaled = pd.DataFrame(array_scaled) #converting NumPy array to Pandas data frame
df_tp = df_scaled.transpose() # transposing because scikit PCA reads differently from matplotlib PCA
species_df = pd.DataFrame(species_list) #adding species as its own data frame
species_df.columns = ["Species"] #giving the species data frame a column title
ID_df = pd.DataFrame(ID_list)
ID_df.columns = ["ID Number"]
var_df = pd.DataFrame(var_list)
var_df.columns = ['Features']

#creating PCA object
myPCA = PCA(n_components = 2)
principal_comps = myPCA.fit_transform(df_tp) #fit AND transform
principal_df = pd.DataFrame(data = principal_comps, columns = ["PC1", "PC2"])  
feat_df = pd.DataFrame(np.transpose(myPCA.components_))

#final data frame for merging/plotting
final_df = pd.concat([principal_df, species_df], axis = 1)
final_df2 = pd.concat([final_df, ID_df], axis = 1)
final_df2.to_csv('finalDF.csv')


#scatterplot of 
pyplot.figure(1)    
pyplot.scatter(leaf_width_ex, leaf_length_ex, c = 'y', marker = 's', label = 'exaltata', s = 10)
pyplot.scatter(leaf_width_syr, leaf_length_syr, c = 'b', label = 'syriaca', s = 10)
pyplot.scatter(leaf_width_sp, leaf_length_sp, c = 'g', marker = 'd', label = 'speciosa', s = 10)
pyplot.legend(loc = 'upper left')
pyplot.title("Milkweed leaf length vs. width by species")
pyplot.xlabel("Leaf width (mm)")
pyplot.ylabel("Leaf length (mm)")
pyplot.show()

#plotting frequency distribution of basal angle by species
pyplot.figure(2)
sns.distplot(basal_angle_ex, color = "yellow", label = "Exaltata")
sns.distplot(basal_angle_syr, color = "skyblue", label = "Syriaca")
sns.distplot(basal_angle_sp, color = 'green', label   = 'Speciosa')
pyplot.legend(loc = "upper right")
pyplot.title("Frequency distribution of basal angle by species")
pyplot.xlabel("Basal angle (degrees)")
pyplot.ylabel("Frequency")
pyplot.show()

#plotting frequency distribution of tip angle by species
sns.distplot(tip_angle_ex, color = "yellow", label = "Exaltata")
sns.distplot(tip_angle_syr, color = "skyblue", label = "Syriaca")
sns.distplot(tip_angle_sp, color = "green", label = 'Speciosa')
pyplot.legend(loc = "upper right")
pyplot.title("Frequency distribution of tip angle by species")
pyplot.xlabel("Tip angle (degrees)")    
pyplot.ylabel("Frequency")
pyplot.show()

#visualizing Principal Component Analysis of the 3 asclepias species
pyplot.figure(4)
colors = ['yellow', 'skyblue', 'green']
species_names = ['exaltata', 'syriaca', 'speciosa']
for sp, color in zip(species_names, colors):
    keep_this_index = final_df2["Species"] == sp
    pc1 = final_df2.loc[keep_this_index, 'PC1']
    pc2 = final_df2.loc[keep_this_index, 'PC2']
    pc1_scale = 1.0 / (pc1.max() - pc1.min()) # SCALE IT AGAIN!
    pc2_scale = 1.0 / (pc2.max() - pc2.min())
    pyplot.scatter(pc1 * pc1_scale, pc2 * pc2_scale, c = color, alpha = 0.6)
pyplot.legend(species_names)
pyplot.xlabel("Principal Component 1")
pyplot.ylabel("Principal Component 2")
pyplot.grid()










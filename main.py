#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 23 16:16:45 2022

@author: anna chepaikina
"""
#%%

from modules.thesaurus_parser import *
from modules.bsv_parser import *
from modules.tagger import *
from modules.utils import *

import os
os.environ['KMP_DUPLICATE_LIB_OK']='True'

#%%
print("\n######################")
print("Load FCU labels")
print("######################\n")



fcu_labels, fcu_lemmatised_labels, fcu_parents, fcu_children, fcu_parents_of_children = parse_thesaurus(path="ressources/frenchCropUsage_20210525.rdf")
print("Done!\nExample\n")
print("\nLabel: {} ".format(list(fcu_labels.keys())[1]))
print("\nLemma: {} ".format(list(fcu_lemmatised_labels.values())[1]))
print("\nAscendants: {} ".format(", ".join(list(fcu_parents.values())[1])))
print("\nDescendants: {} ".format(", ".join(list(fcu_children.values())[1])))
print("\nAscendants of descendants: {} ".format(", ".join(list(fcu_parents_of_children.values())[1])))
 
   
#%%
print("\n######################")
print("Load filters")
print("######################\n")



print("\nLoad wine bioagressors..")
wine_bioagressors = load_csv(fic = "ressources/wine_bioagressors.csv", sep = ";", header=0)
wine_bioagressors = wine_bioagressors["Organisme_Nuisible"].tolist()
wine_bioagressors = [bioagressor.lower() for bioagressor in wine_bioagressors]
print("Example: {} ".format(",\n".join(wine_bioagressors[:5])))
    
print("\nLoad phenological stages..")
ppdo=load_csv(fic = "ressources/ppdo_20210726.csv", sep= "\t", header=None)
ppdo_labels=ppdo[0].tolist()
ppdo_labels=[label.lower().strip() for label in ppdo_labels]
print("Example: {} ".format(",\n".join(ppdo_labels[:5])))

print("\nLoad NCBI database..")
ncbi = load_csv(fic = "ressources/taxa+id_full.csv", sep="\t", header=None)
ncbi_labels=ncbi[0].tolist()
ncbi_labels=[label.lower().strip() for label in ncbi_labels if isinstance(label, str)]
print("Example: {} ".format(",\n".join(ncbi_labels[:5])))

filters = wine_bioagressors + ppdo_labels + ncbi_labels

#%%
print("\n######################")
print("Load bulletins")
print("######################\n")



bsv = correct_corpus(load_corpus(corpus = "http://ontology.inrae.fr/bsv/html/Corpus/")) # load bulletins from html pages, and make some modifications (encoding, etc.)
print("\nURL: {} ".format("".join(list(bsv.keys())[1])))
print("\nText: {} ".format(list(bsv.values())[1]))


#%%
print("\n######################")
print("Find conjunctions")
print("######################\n")


conjunctions, bsv_lemmatized = find_conjunctions(bsv, filters, wine_bioagressors, ppdo_labels, ncbi_labels) # extract conjunctions
df = conjunctions_to_df(conjunctions, fcu_labels, fcu_lemmatised_labels, fcu_parents, fcu_parents_of_children) # get a dataframe of extracted conjunctions
df = correct_proposals(df) # modify token forms if they are not grammatically correct
print(df[:10])


#%%
print("\n######################")
print("Save results")
print("######################\n")
try:
    df.to_csv("output/conjunctions/test.csv", sep="\t")
    print("Done !")
except:
    print("Something went wrong ...")



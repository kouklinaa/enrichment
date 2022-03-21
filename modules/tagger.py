#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 23 19:01:20 2022

@author: anna chepaikina
"""

import stanza
import torch
import pandas as pd
from nltk.corpus import stopwords
from modules.utils import *


#%%
#########################################################################################
####################################CORRECT PIPELINE#####################################
#########################################################################################


def customize_lemmatiser(path):
    
    # Load word_dict and composite_dict
    model = torch.load(path, map_location='cpu')
    word_dict, composite_dict = model['dicts']
    
    # Customize the dictionary
    
    # chou
    composite_dict[('choux', 'NOUN')] = 'chou'
    word_dict['choux'] = 'chou'
    composite_dict[('choux-fleur', 'NOUN')] = 'chou-fleur'
    word_dict['choux-fleur'] = 'chou-fleur'
    composite_dict[('choux-cabus', 'NOUN')] = 'chou-cabus'
    word_dict['choux-cabus'] = 'chou-cabus'
    composite_dict[('choux-rave', 'NOUN')] = 'chou-rave'
    word_dict['choux-rave'] = 'chou-rave'
    composite_dict[('choux-raves', 'NOUN')] = 'chou-rave'
    word_dict['choux-raves'] = 'chou-rave'

    # framboise
    composite_dict[('framboise', 'NOUN')] = 'framboise'
    word_dict['framboise'] = 'framboise'
    composite_dict[('framboises', 'NOUN')] = 'framboise'
    word_dict['framboises'] = 'framboise'

    # radis
    composite_dict[('radis', 'NOUN')] = 'radis'
    word_dict['radis'] = 'radis'

    # kiwi
    composite_dict[('kiwis', 'NOUN')] = 'kiwi'
    word_dict['kiwis'] = 'kiwi'
    
    # impatiens
    composite_dict[('impatiens', 'NOUN')] = 'impatiens'
    word_dict['impatiens'] = 'impatiens'
    
    # semis
    composite_dict[('semis', 'NOUN')] = 'semis'
    word_dict['semis'] = 'semis'
    
    # Save model
    torch.save(model, '/Users/belka/stanza_resources/fr/lemma/gsd_customized.pt')           
    
    return True

#%%
#########################################################################################
####################################LOAD PIPELINE########################################
#########################################################################################


def load_pipeline(update=True):
    
    if update:
        customize_lemmatiser(path = '/Users/belka/stanza_resources/fr/lemma/gsd.pt')
        nlp = stanza.Pipeline('fr',package="gsd",processors='tokenize,mwt,pos,lemma,depparse',
                              lemma_model_path='/Users/belka/stanza_resources/fr/lemma/gsd_customized.pt',
                              verbose=False)
    
    else:
        nlp = stanza.Pipeline('fr',package="gsd",processors='tokenize,mwt,pos,lemma,depparse',
                              lemma_model_path='/Users/belka/stanza_resources/fr/lemma/gsd_customized.pt',
                              verbose=False)
    return nlp


def lemmatise(mystring):
    doc = nlp(mystring)
    lemma = " ".join([word.lemma.lower() for sent in doc.sentences for word in sent.words])  
    return lemma


nlp = load_pipeline(update=True)




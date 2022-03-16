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
    
    # Save model
    torch.save(model, '/Users/belka/stanza_resources/fr/lemma/gsd_customized.pt')           
    
    return True


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


def lemmatise(str_):
    doc = nlp(str_)
    lemma = " ".join([word.lemma.lower() for sent in doc.sentences for word in sent.words])  
    return lemma



nlp = load_pipeline(update=False)
#print(nlp('choux-cabus'))

#########################################################################################
####################################FIND CONJUNCTIONS####################################
#########################################################################################

def find_conjunctions(bsv, filters, wine_bioagressors, ppdo_labels, ncbi_labels):
    bsv_lemmatized = {}
    conjunctions = {}

    with open('output/junk/filtered_entities.csv', 'w') as f:
        for i, (bulletin, text) in enumerate(bsv.items()):
            print("\n\n\n", i, "--->", bulletin, "\n") # print id of the bulletin to see the progress
            sentence_temp = {}
            lemmatized_sentences = [] # initilalise a list to store lemmatized sentences 
        

            for idx,sentence in enumerate(text): # parse through every sentence of the bulletin
                doc=nlp(sentence) # call nlp pipeline from tagger.py and transform the sentence to a stanza object
                for sent in doc.sentences:
                    conj_temp = {}
                    for word in sent.words: # parse through every word
                    
                        #########################################################
                        # I. Lemmatize sentence from the bulletin ( to use it later with a fasttext model)
                        if word.upos != "PUNCT" and word.lemma.lower() not in stopwords.words('french') and word.lemma.isalpha(): # delete all stopwords and make sure that we save only words 
                            lemmatized_sentences.append(word.lemma.lower()) # append to a temporary list
                        
                        #########################################################
                        # II. Find (NG) conjunctions 
                        if (word.deprel == "conj" and word.upos=="NOUN" and len(word.lemma) > 1) and (sent.words[word.head-1].upos == "NOUN" and len(sent.words[word.head-1].lemma)>1):
                            
                            # if dependent is in a filtered list, then we save it to a csv file "filtered entities"
                            if word.lemma.lower() in filters :
                                if word.lemma.lower() in wine_bioagressors:
                                    f.writelines(bulletin +";"+ word.lemma + ";"+ "wine bioagressor"+ "\n")
                                elif word.lemma.lower() in ppdo_labels:
                                    f.writelines(bulletin +";"+ word.lemma + ";"+ "ppdo label"+ "\n")
                                elif word.lemma.lower() in ncbi_labels:
                                    f.writelines(bulletin +";"+ word.lemma + ";"+ "ncbi label"+ "\n")
                                else:
                                    f.writelines(bulletin +";"+ word.lemma + ";"+ "not known"+ "\n") 
                            
                            # if head is in a filtered list, then we save it to a csv file "filtered entities"
                            elif sent.words[word.head-1].lemma.lower() in filters :
                                if sent.words[word.head-1].lemma.lower() in wine_bioagressors:
                                    f.writelines(bulletin +";"+ sent.words[word.head-1].lemma.lower() + ";"+ "wine bioagressor"+ "\n")
                                elif sent.words[word.head-1].lemma.lower() in ppdo_labels:
                                    f.writelines(bulletin +";"+ sent.words[word.head-1].lemma.lower() + ";"+ "ppdo label"+ "\n")
                                elif sent.words[word.head-1].lemma.lower() in ncbi_labels:
                                    f.writelines(bulletin +";"+ sent.words[word.head-1].lemma.lower() + ";"+ "ncbi label"+ "\n")
                                else:
                                    f.writelines(bulletin +";"+ sent.words[word.head-1].lemma.lower() + ";"+ "not known"+ "\n")
                            
                            
                            # if entity is not in the list,then we can continue creating a conjunction 
                            else:
                                
                                # conjunction head
                                head_id=sent.words[word.head-1].id
                                head_form=sent.words[word.head-1].text.lower()
                                head_lemma=sent.words[word.head-1].lemma.lower()
                                head_upos=sent.words[word.head-1].upos
                                head_parent=sent.words[word.head-1].parent.text.lower()
                                head_feats=sent.words[word.head-1].feats
                                head = (str(head_id), head_form,head_lemma, head_upos,head_parent,str(head_feats))
                                
                                
                                # conjunction dependent
                                dep_id=word.id
                                dep_form=word.text.lower()
                                dep_lemma=word.lemma.lower()
                                dep_upos=word.upos
                                dep_parent=word.parent.text.lower()
                                dep_feats=word.feats
                                dep = (str(dep_id),  dep_form,  dep_lemma,  dep_upos, dep_parent, str(dep_feats))
                                
                                
                                # save conjunction to a dictionary
                                conj_temp.setdefault(head, []).append([dep])
                                
                    
                    # if conjunction is not empty            
                    if conj_temp:
                        print("\n$",sentence) # print the sentence
                        print(conj_temp) # with the conjunction foud inside
                        
                        # get context
                        if idx == 0: # if conjunction is in the first sentence
                            sentence_temp.setdefault(sentence+"\n"+text[idx+1], conj_temp) # get next sentence for context
                        if idx > 0 and idx < len(text)-1: #  if conjunction is in the middle of hte document
                            sentence_temp.setdefault(text[idx-1]+"\n"+sentence+"\n"+text[idx+1], conj_temp) # get before and next sentence for context
                        if idx == len(text)-1: # if conjunction is in the last sentence
                            sentence_temp.setdefault(text[idx-1]+"\n"+sentence, conj_temp) # get before sentence for context
                                
            
            # save conjunctions
            conjunctions.setdefault(bulletin, sentence_temp)                    
            # save lemmatized sentences to a dictionary
            bsv_lemmatized[bulletin] = lemmatized_sentences
            
            if i == 10:
                break
    return conjunctions, bsv_lemmatized

def conjunctions_to_df(conjunctions,fcu_labels, fcu_lemmatised_labels, fcu_parents, fcu_parents_of_children):
    conj_bsv=[]
    conj_sentence=[]
    conj_unique=[]
    conj_form=[]
    conj_lemma=[]
    conj_idx=[]
    conj_upos=[]
    conj_parent=[]
    conj_feats=[]
    conj_match=[]
    conj_proposal=[]
    conj_broader=[]

    for bulletin, found in conjunctions.items():
        print("\n$", bulletin)
        for sentence, conj in found.items():
            for head, dep in conj.items():
                
                # create a list of lists (elements of a conjunction), example : [['5', 'feuilles', 'feuille', 'NOUN', 'feuilles', 'Gender=Fem|Number=Plur']....]
                result = [list(t) for t in flatten(dep)]  # get all dependents
                result.insert(0,list(head))  # insert head as the first element           
                transposed = list(map(list,zip(*result))) # transpose this result, example : [['5', '7'], ['feuilles', 'risque'], ['feuille', 'risque'], ['NOUN', 'NOUN']...]
                
                # get lists of  transposed elements
                idx = transposed[0]
                forms = transposed[1]
                lemmas = transposed[2]
                upos = transposed[3]
                parents = transposed[4]
                feats = transposed[5]

                
                # GET FCU MATCH, SKOS:BROADER, PROPOSAL (NO MATCH)
                match = []
                no_match = []
                skos_broader_references = []
                
                for lemma in lemmas:                
                    new_lemma = lemma.replace("-", " ") # make sure that presence of absence  of "-" character would not effect full match with fcu
                    
                    # FULL FCU MATCH
                    if any(new_lemma == val.replace("-", " ") for val in fcu_lemmatised_labels.values()):
                        for key,val in fcu_lemmatised_labels.items():
                            if new_lemma == val.replace("-", " "):
                                print("\nFCU MATCH :", val) 
                                match.append(key)                                                       
                                
                                # references
                                broader_values=[skos_value+"(->"+", ".join([parent+"="+fcu_labels[parent] for parent in fcu_parents_of_children[lemma]])+")" 
                                                if skos_value == "multi usages" else skos_value+"="+fcu_labels[skos_value] 
                                                for skos_value in fcu_parents[lemma]] # if multi usages, search for parents of children
                                print("SKOS:BROADER : ", broader_values)
                                skos_broader_references.append(broader_values)
                    
                    # NO FULL MATCH  
                    else:
                        #print(lemma)
                        no_match.append(lemma) # save as proposal
                        
                        # still try to get a partial match with FCU (it can help to get more information about the entity)
                        for tok in lemma.split():
                            for key, val in fcu_lemmatised_labels.items():
                                if tok == val:
                                    print("PARTIAL FCU MATCH :", tok)
                                    match.append(key)
                                    
                                    # references
                                    broader_values=[skos_value+"(->"+", ".join([parent+"="+fcu_labels[parent] for parent in fcu_parents_of_children[tok]])+")" 
                                                    if skos_value == "multi usages" else skos_value+"="+fcu_labels[skos_value] 
                                                    for skos_value in fcu_parents[tok]] # if multi usages, search for parents of children
                                    print("SKOS:BROADER : ", broader_values)
                                    skos_broader_references.append(broader_values)
                            
                                
                                
                # save all properties                
                conj_bsv.append(bulletin)
                conj_sentence.append(sentence)
                conj_unique.append(result)
                conj_idx.append(",\n".join(idx))
                conj_lemma.append(",\n".join(lemmas))
                conj_form.append(",\n".join(forms))
                conj_upos.append(",\n".join(upos))
                conj_parent.append(",\n".join(parents))
                conj_feats.append(",\n".join(feats))
                conj_match.append(",\n".join(match))
                conj_proposal.append(",\n".join(no_match))
                conj_broader.append(",\n".join(set(flatten(skos_broader_references))))
                
                

    df = pd.DataFrame(
    		{ 'bsv': conj_bsv,
    		 'context': conj_sentence,
    		 'conj_id': conj_idx,   
    		 'conj_upos':conj_upos,
    		 'conj_feats':conj_feats,
    		 'conj_parent':conj_parent,
    		 'conj_token':conj_form,
    		 'conj_lemma': conj_lemma,    
    		 'fcu_match':conj_match,
    		 'skos:broader':conj_broader,
    		 'proposal_lemma':conj_proposal
    		})


    df = df[df['fcu_match'].str.len() > 2] # keep rows that have at least one fcu match
    df = df[df['proposal_lemma'].str.len() > 2] # keep rows that have at least one proposal
    df = df.assign(proposal_lemma=df['proposal_lemma'].str.split(',\n')).explode('proposal_lemma')
    return df

def correct_proposals(df):
    
    adj_endings=pd.read_csv("ressources/adj_endings.csv", sep=";", header=0)
    adj_dict = adj_endings.set_index('Plural')['Singular'].to_dict()
    #print(adj_dict)
    
    proposals_lemma=df["proposal_lemma"].tolist()
    feats=df["conj_feats"].tolist()
    parents=df["conj_parent"].tolist()
    lemmas=df["conj_lemma"].tolist()
    upos=df["conj_upos"].tolist()

    proposals_ok = {}

    #print(len(proposals_lemma))
    #proposals_lemma = [p.replace("\n","") for p in proposals_lemma]
    for i,line in enumerate(proposals_lemma):
        #line = line.replace("radi", "radis")
        #print()
        #print(i, line, )
        #print("Lemma: ",lemmas[i])
        temp_lemma = lemmas[i].split(",\n")
        temp_feats=feats[i].split(",\n")
        temp_upos=upos[i].split(",\n")
        temp_parents=parents[i].split(",\n")
        idx = temp_lemma.index(line)
        if line in temp_lemma:
            if temp_upos[idx] =="NOUN":
                proposals_ok.setdefault(i, line)
            elif temp_upos[idx] =="NOUN NOUN":
                proposals_ok.setdefault(i, line)
            elif temp_upos[idx] == "NOUN ADJ":
                if temp_feats[idx].split()[1] == "Gender=Masc|Number=Sing":
                    line = line.replace("radi", 'radis')                
                    proposals_ok.setdefault(i, line)
                elif temp_feats[idx].split()[1] == "Gender=Masc|Number=Plur":
                    line = line.replace("radi", 'radis')
                    proposals_ok.setdefault(i, line)
                elif temp_feats[idx].split()[1] == "Gender=Fem|Number=Sing":               
                    change = line.split()[0]+ " "+temp_parents[idx].split()[1]
                    proposals_ok.setdefault(i, change)
                elif temp_feats[idx].split()[1] == "Gender=Fem|Number=Plur":
                    for k,v in adj_dict.items():
                        if temp_parents[idx].endswith(k):
                            end_idx = temp_parents[idx].split()[1].rfind(k)
                            len_idx = len(temp_parents[idx].split()[1])-1
                            change = line.split()[0]+ " "+temp_parents[idx].split()[1][:end_idx]+v
                            proposals_ok.setdefault(i, change)
            elif temp_upos[idx] == "ADJ NOUN":
                if temp_feats[idx].split()[0] == "Gender=Masc|Number=Sing":
                    line = line.replace("radi", 'radis')                
                    proposals_ok.setdefault(i, line)
                elif temp_feats[idx].split()[0] == "Gender=Masc|Number=Plur":
                    line = line.replace("radi", 'radis')
                    proposals_ok.setdefault(i, line)
                elif temp_feats[idx].split()[0] == "Gender=Fem|Number=Sing":
                    change = temp_parents[idx].split()[0] + " "+line.split()[1]
                    proposals_ok.setdefault(i, change)
                elif temp_feats[idx].split()[0] == "Gender=Fem|Number=Plur":
                    for k,v in adj_dict.items():
                        if temp_parents[idx].endswith(k):
                            end_idx = temp_parents[idx].split()[0].rfind(k)
                            len_idx = len(temp_parents[idx].split()[0])-1
                            change = temp_parents[idx].split()[0][:end_idx]+v+ " "+ line.split()[1]
                            proposals_ok.setdefault(i, change)
            elif temp_upos[idx]== "NOUN ADP NOUN" or temp_upos[idx]== "NOUN ADP PROPN":
                if temp_parents[idx].split()[1] == "à":
                    proposals_ok.setdefault(i, line)
                elif temp_parents[idx].split()[1] == "de":
                    proposals_ok.setdefault(i, line)
                else:
                    change = line.split()[0] + " "+temp_parents[idx].split()[1] + line.split()[2]
                    proposals_ok.setdefault(i, change)
            elif temp_upos[idx]=="NOUN ADP DET NOUN" or temp_upos[idx]=="NOUN ADP DET PROPN":
                if temp_parents[idx].split()[1]=="du" and temp_parents[idx].split()[2] == "du":
                    change = line.split()[0] + " " + "du" + " " + line.split()[3]
                    proposals_ok.setdefault(i, change)
                elif temp_parents[idx].split()[1]=="de" and temp_parents[idx].split()[2] == "la":
                    change = line.split()[0] + " " + "de la" + " " + line.split()[3]
                    proposals_ok.setdefault(i, change)
                    #print(change)
            elif  temp_upos[idx]== "NOUN ADJ ADP NOUN" or temp_upos[idx]== "NOUN ADJ ADP PROPN" :
                prep = temp_parents[idx].split()[2]
                if prep == "à":
                    prep=prep
                    if temp_feats[idx].split()[1] == "Gender=Masc|Number=Sing":
                        change = line.split()[0] + " "+ line.split()[1] + " "+prep +" "+ line.split()[3]
                        proposals_ok.setdefault(i, change)
                    elif temp_feats[idx].split()[1] == "Gender=Masc|Number=Plur":
                        change = line.split()[0] + " "+ line.split()[1] + " "+prep +" "+ line.split()[3]
                        proposals_ok.setdefault(i, change)
                    elif temp_feats[idx].split()[1] == "Gender=Fem|Number=Sing":
                        change = line.split()[0] + " "+temp_parents[idx].split()[1] + " "+prep +" "+ line.split()[3]
                        proposals_ok.setdefault(i, change)
                    elif temp_feats[idx].split()[1] == "Gender=Fem|Number=Plur":
                        for k,v in adj_dict.items():
                            if temp_parents[idx].endswith(k):
                                end_idx = temp_parents[idx].split()[1].rfind(k)
                                len_idx = len(temp_parents[idx].split()[1])-1
                                change = line.split()[0]+ " "+temp_parents[idx].split()[1][:end_idx]+v + " "+prep +" "+ line.split()[3]
                                proposals_ok.setdefault(i, change)
                elif prep == "de":
                    prep=prep
                    if temp_feats[idx].split()[1] == "Gender=Masc|Number=Sing":
                        change = line.split()[0] + " "+ line.split()[1] + " "+prep +" "+ line.split()[3]
                        proposals_ok.setdefault(i, change)
                    elif temp_feats[idx].split()[1] == "Gender=Masc|Number=Plur":
                        change = line.split()[0] + " "+ line.split()[1] + " "+prep +" "+ line.split()[3]
                        proposals_ok.setdefault(i, change)
                    elif temp_feats[idx].split()[1] == "Gender=Fem|Number=Sing":
                        change = line.split()[0] + " "+temp_parents[idx].split()[1] + " "+prep +" "+ line.split()[3]
                        proposals_ok.setdefault(i, change)
                    elif temp_feats[idx].split()[1] == "Gender=Fem|Number=Plur":
                        for k,v in adj_dict.items():
                            if temp_parents[idx].endswith(k):
                                end_idx = temp_parents[idx].split()[1].rfind(k)
                                len_idx = len(temp_parents[idx].split()[1])-1
                                change = line.split()[0]+ " "+temp_parents[idx].split()[1][:end_idx]+v + " "+prep +" "+ line.split()[3]
                                proposals_ok.setdefault(i, change)
                elif prep == "d'":
                    #print(prep)
                    if temp_feats[idx].split()[1] == "Gender=Masc|Number=Sing":
                        change = line.split()[0] + " "+ line.split()[1] + " "+prep + line.split()[3]
                        proposals_ok.setdefault(i, change)
                    elif temp_feats[idx].split()[1] == "Gender=Masc|Number=Plur":
                        change = line.split()[0] + " "+ line.split()[1] + " "+prep + line.split()[3]
                        proposals_ok.setdefault(i, change)
                    elif temp_feats[idx].split()[1] == "Gender=Fem|Number=Sing":
                        change = line.split()[0] + " "+temp_parents[idx].split()[1] + " "+prep + line.split()[3]
                        proposals_ok.setdefault(i, change)
                    elif temp_feats[idx].split()[1] == "Gender=Fem|Number=Plur":
                        for k,v in adj_dict.items():
                            if temp_parents[idx].endswith(k):
                                end_idx = temp_parents[idx].split()[1].rfind(k)
                                len_idx = len(temp_parents[idx].split()[1])-1
                                change = line.split()[0]+ " "+temp_parents[idx].split()[1][:end_idx]+v + " "+prep + line.split()[3]
                                proposals_ok.setdefault(i, change)
                    
            else:
                proposals_ok.setdefault(i, line)
                
                    
    proposals_final = list(proposals_ok.values())
    #print(len(proposals_final))
    df["proposal"] = proposals_final
    
    return df




#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar 10 23:15:38 2022

@author: anna chepaikina
"""

import re 
from modules.tagger import *
from modules.utils import *

#%%
#########################################################################################
####################################FIND CONJUNCTIONS####################################
#########################################################################################


def get_noun_group(sent, head_noun, head_noun_id, filters):
    """
    

    Parameters
    ----------
    sent : stanza object
        contains information about a sentence.
    head_noun : str
        noun that we want to expand.
    head_noun_id : int
        index of the noun that we want to expand.
    filters : list of str
        contains different filters.

    Returns
    -------
    result : tuple
        contains information about a noun group
        (id, form, lemma, etc.)

    """
    
    result = ()
    noun_group = {}
    for word in sent.words:
        if head_noun_id == word.head:
            
            if len(word.lemma)>1  and word.lemma.lower() not in filters:
                
                ########################################################
                # if a modifier is an adjective
                ########################################################
                if (word.deprel=="amod" and word.upos == "ADJ"):
                    amod_id=word.id
                    amod_form=word.text.lower()
                    amod_lemma=word.lemma.lower()
                    amod_upos=word.upos
                    amod_parent=word.parent.text.lower()
                    amod_feats=word.feats
                    amod = (str(amod_id),amod_form,amod_lemma,amod_upos,amod_parent,str(amod_feats))
                    noun_group.setdefault(head_noun_id, []).append(amod)
                
                ########################################################
                # if a modifier is an noun or a proper noun
                ########################################################
                if word.deprel== "nmod":
                    if word.upos=="NOUN" or word.upos == "PROPN":
                        nmod_id = word.id
                        nmod_form=word.text.lower()
                        nmod_lemma=word.lemma.lower()
                        nmod_upos=word.upos
                        nmod_parent=word.parent.text.lower()
                        nmod_feats=word.feats
                        nmod = (str(nmod_id),nmod_form,nmod_lemma,nmod_upos,nmod_parent,str(nmod_feats))
                        noun_group.setdefault(head_noun_id, []).append(nmod)
                        
                        ########################################################
                        # if it also contains expensions 
                        ########################################################
                        for word in sent.words:
                            if nmod_id == word.head:
                                
                                
                                if word.deprel=="det":
                                    det_id = word.id
                                    det_form=word.text.lower()
                                    det_lemma=word.lemma.lower()
                                    det_upos=word.upos
                                    det_parent=word.parent.text.lower()
                                    det_feats=word.feats
                                    if det_id > head_noun_id and det_id < nmod_id: # consider determinants only after the noun head 
                                        det = (str(det_id),det_form,det_lemma,det_upos,det_parent,str(det_feats))
                                        noun_group.setdefault(head_noun_id, []).append(det)
                                
                                
                                if word.deprel=="case":
                                    case_id = word.id
                                    case_form=word.text.lower()
                                    case_lemma=word.lemma.lower()
                                    case_upos=word.upos
                                    case_parent=word.parent.text.lower()
                                    case_feats=word.feats
                                    case = (str(case_id),case_form,case_lemma,case_upos,case_parent,str(case_feats))
                                    noun_group.setdefault(head_noun_id, []).append(case)                                    
                                
                                
                                if word.deprel=="amod":
                                    amod_id_bis=word.id
                                    amod_form_bis=word.text.lower()
                                    amod_lemma_bis=word.lemma.lower()
                                    amod_upos_bis=word.upos
                                    amod_parent_bis=word.parent.text.lower()
                                    amod_feats_bis=word.feats
                                    amod_bis = (str(amod_id_bis),amod_form_bis,amod_lemma_bis,amod_upos_bis,amod_parent_bis,str(amod_feats_bis))
                                    noun_group.setdefault(head_noun_id, []).append(amod_bis)
                                    
                                                                                # we need to see if nmod also depends on nmod, for ex. in a sentence:
                                if word.deprel=="nmod" and word.upos=="NOUN":   # "Céleri branche et persil : 10% de plants avec colonie d'aptères pendant tout le cycle"                     
                                    nmod_id_bis = word.id                       # nmod has a head "céleri" 
                                    nmod_form_bis=word.text.lower()
                                    nmod_lemma_bis=word.lemma.lower()
                                    nmod_upos_bis=word.upos
                                    nmod_parent_bis=word.parent.text.lower()
                                    nmod_feats_bis=word.feats
                                    nmod_bis = (str(nmod_id_bis),nmod_form_bis,nmod_lemma_bis,nmod_upos_bis,nmod_parent_bis,str(nmod_feats_bis))
                                    noun_group.setdefault(head_noun_id, []).append(nmod_bis)
                                    
                                    for word in sent.words:
                                        if nmod_id_bis == word.head:
                                            if word.deprel=="det":
                                                det_id_bis = word.id
                                                det_form_bis=word.text.lower()
                                                det_lemma_bis=word.lemma.lower()
                                                det_upos_bis=word.upos
                                                det_parent_bis=word.parent.text.lower()
                                                det_feats_bis=word.feats
                                                if det_id_bis > head_noun_id and det_id_bis < nmod_id_bis:
                                                    det_bis = (str(det_id_bis),det_form_bis,det_lemma_bis,det_upos_bis,det_parent_bis,str(det_feats_bis))
                                                    noun_group.setdefault(head_noun_id, []).append(det_bis)
                                                    
                                            
                                            if word.deprel=="amod":
                                                amod_id_bis_bis=word.id
                                                amod_form_bis_bis=word.text.lower()
                                                amod_lemma_bis_bis=word.lemma.lower()
                                                amod_upos_bis_bis=word.upos
                                                amod_parent_bis_bis=word.parent.text.lower()
                                                amod_feats_bis_bis=word.feats
                                                amod_bis_bis = (str(amod_id_bis_bis),amod_form_bis_bis,amod_lemma_bis_bis,amod_upos_bis_bis,amod_parent_bis_bis,str(amod_feats_bis_bis))
                                                noun_group.setdefault(head_noun_id, []).append(amod_bis_bis)
                                                
                                            if word.deprel=="case":
                                                case_id_bis = word.id
                                                case_form_bis=word.text.lower()
                                                case_lemma_bis=word.lemma.lower()
                                                case_upos_bis=word.upos
                                                case_parent_bis=word.parent.text.lower()
                                                case_feats_bis=word.feats
                                                case_bis = (str(case_id_bis),case_form_bis,case_lemma_bis,case_upos_bis,case_parent_bis,str(case_feats_bis))
                                                noun_group.setdefault(head_noun_id, []).append(case_bis)


                                                    


                                
    # see if  the tuple is not empty                
    if len(noun_group)!= 0:
        noun_group.setdefault(head_noun_id, []).append(head_noun)                   # add all dependents to a list of lists and connect them all to the head
        noun_group = flatten(list(noun_group.values()))                             # convert list of lists to a simple list
        noun_group = sorted(noun_group, key=lambda tup: int(tup[0]), reverse=False) # sort out the elements
        
        
        # delete groups with prepositions other than"de" and "à"
        for group in noun_group:
            if group[3]=="ADP":
                if group[2] == "de" or group[2] == "à":
                    continue                    
                else:
                    noun_group = ""
            else:
                continue
        
        # save ng
        noun_group = tuple(map(" ".join, zip(*noun_group)))                
        result = result + noun_group
        
    return result


#%%
def find_conjunctions(bsv, filters, wine_bioagressors, ppdo_labels, ncbi_labels):
    """
    

    Parameters
    ----------
    bsv : dict
        key = bulletin
        value = text.
    filters : list of str
        contains different filters.
    wine_bioagressors : list of str
        contains bioagressors to filter out.
    ppdo_labels : list of str
        contains phenological stages to filter out.
    ncbi_labels : list of str
        contains scientific names to filter out.

    Returns
    -------
    conjunctions : dict
        key = bulletin
        value = conjunctions.
    lemmatized_bsv : dict
        key = bulletin
        value = lemmatised text

    """
    
    # initialise empty dictionaries
    lemmatized_bsv = {}
    conjunctions = {}   
    
    # start parsing
    with open('output/junk/filtered_entities.csv', 'w') as f:   # start writing a file csv that would include all filtered entities        
        for i, (bulletin, text) in enumerate(bsv.items()):      # start parsing bsv dictionary        
            print("\n\n\n", i, "--->", bulletin, "\n")          # print id of the bulletin to see the progress
            
            conj_plus_context_temp = {}   # initialise a temporary dictionary to store conjunctions with context 
            lemmatized_sentences = []     # initilalise a temporary list to store lemmatized sentences of bsv
            
            for idx,sentence in enumerate(text):    # parse through every sentence of the bulletin
                doc=nlp(sentence)                   # call nlp pipeline from tagger.py  and transform the sentence to a stanza object                
                for sent in doc.sentences:          # access sent object of sentences identified by nlp pipeline
                    
                    conj_temp = {}        # initialise a temporary list to store future extracted conjunctions
                    
                    for word in sent.words:         # parse through every word
                    
                    
                        #########################################################
                        # I. Save lemmatized sentences from the bulletin 
                        #########################################################
                        
                        if word.upos != "PUNCT" \
                                    and word.lemma.lower() not in stopwords.words('french') \
                                    and word.lemma.isalpha():  # not include stopwords or punctuation 
                            lemmatized_sentences.append(word.lemma.lower())                                                        # make sure that we save only words (isalpha)
                                                                                
                                                                                
                        
                        
                        
                        #########################################################
                        # II. Find (NG) conjunctions
                        #########################################################
                        
                        
                        if (word.deprel == "conj" and word.upos=="NOUN" and len(word.lemma) > 1) \
                            and (sent.words[word.head-1].upos == "NOUN" and len(sent.words[word.head-1].lemma)>1):
                            
                            ################################################
                            # if dependent is in a filtered list, not use it                   
                            if word.lemma.lower() in filters : 
                                if word.lemma.lower() in wine_bioagressors:
                                    f.writelines(bulletin +";"+ word.lemma + ";"+ "wine bioagressor"+ "\n")
                                elif word.lemma.lower() in ppdo_labels:
                                    f.writelines(bulletin +";"+ word.lemma + ";"+ "ppdo label"+ "\n")
                                elif word.lemma.lower() in ncbi_labels:
                                    f.writelines(bulletin +";"+ word.lemma + ";"+ "ncbi label"+ "\n")
                                else:
                                    f.writelines(bulletin +";"+ word.lemma + ";"+ "not known"+ "\n") 
                            
                            ################################################
                            # if head is in a filtered list, not use it
                            elif sent.words[word.head-1].lemma.lower() in filters : 
                                if sent.words[word.head-1].lemma.lower() in wine_bioagressors:
                                    f.writelines(bulletin +";"+ sent.words[word.head-1].lemma.lower() + ";"+ "wine bioagressor"+ "\n")
                                elif sent.words[word.head-1].lemma.lower() in ppdo_labels:
                                    f.writelines(bulletin +";"+ sent.words[word.head-1].lemma.lower() + ";"+ "ppdo label"+ "\n")
                                elif sent.words[word.head-1].lemma.lower() in ncbi_labels:
                                    f.writelines(bulletin +";"+ sent.words[word.head-1].lemma.lower() + ";"+ "ncbi label"+ "\n")
                                else:
                                    f.writelines(bulletin +";"+ sent.words[word.head-1].lemma.lower() + ";"+ "not known"+ "\n")
                            
                            

                            #########################################################
                            else: # if entity is not in the filtered list, proceed
                                
                                # conjunction head
                                head_id=sent.words[word.head-1].id
                                head_form=sent.words[word.head-1].text.lower()
                                head_lemma=sent.words[word.head-1].lemma.lower()
                                head_upos=sent.words[word.head-1].upos
                                head_parent=sent.words[word.head-1].parent.text.lower()
                                head_feats=sent.words[word.head-1].feats
                                head = (str(head_id), head_form,head_lemma, head_upos,head_parent,str(head_feats))
                                
                                # try finding noun expensions
                                head_ng = get_noun_group(sent, head, head_id, filters)
                                if head_ng:
                                    head = head_ng
                                else:
                                    head = head
                                
                                
                                
                                
                                # conjunction dependent
                                dep_id=word.id
                                dep_form=word.text.lower()
                                dep_lemma=word.lemma.lower()
                                dep_upos=word.upos
                                dep_parent=word.parent.text.lower()
                                dep_feats=word.feats
                                dep = (str(dep_id),  dep_form,  dep_lemma,  dep_upos, dep_parent, str(dep_feats))
                                
                                # try finding noun expensions
                                dep_ng = get_noun_group(sent, dep, dep_id, filters)
                                if dep_ng:
                                    dep = dep_ng
                                else:
                                    dep = dep
                                
                                # save conjunction to a dictionary
                                conj_temp.setdefault(head, []).append([dep])
                                
                    #########################################################
                    # III. Get context
                    #########################################################                    
                               
                    if conj_temp: # if conjunction is not empty 
                        print("\n\n\t$",sentence) 
                        #print(conj_temp)
                        for key, value in conj_temp.items():
                            print("\n")
                            print("\t\t",key[1])
                            for v in flatten(value):
                                print("\t\t",v[1])
                            #for v in value:
                                #print(v[1])
                                                                         
                        if idx == 0: # if conjunction is in the first sentence                                                                
                            conj_plus_context_temp.setdefault(sentence+"\n"+text[idx+1], conj_temp) # add next sentence 
                                                   
                        if idx > 0 and idx < len(text)-1: # if conjunction is in the middle of the document                                          
                            conj_plus_context_temp.setdefault(text[idx-1]+"\n"+sentence+"\n"+text[idx+1], conj_temp) # get sentences before and after
                                                                         
                        if idx == len(text)-1: # if conjunction is in the last sentence                                                     
                            conj_plus_context_temp.setdefault(text[idx-1]+"\n"+sentence, conj_temp) # get a sentence before

                                
            #########################################################
            # III. Save conjunctions with context
            #########################################################
                        
            conjunctions.setdefault(bulletin, conj_plus_context_temp) # save conjunctions                             
            lemmatized_bsv[bulletin] = lemmatized_sentences # save lemmatized sentences to a dictionary
            
            #if i ==50:
                #break
            
    return conjunctions, lemmatized_bsv

#%%
def conjunctions_to_df(conjunctions,fcu_labels, fcu_lemmatised_labels, fcu_parents, fcu_parents_of_children):
    """
    

    Parameters
    ----------
    conjunctions : dict
        key = bulletin
        value = conjunctions.
    fcu_labels : dict
        key = label
        value = iri.
    fcu_lemmatised_labels : dict
        key = label+"="+iri
        value = lemmatised label
    fcu_parents : dict
        key = label
        value = skos:broader concepts.
    fcu_parents_of_children : dict
        key = label
        value = skos:broader concepts of skos:narrower concepts.

    Returns
    -------
    df : dataframe
        contains all the information about conjunctions.

    """
    
    # initialise empty lists to store all information about conjunction
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

    # start parsing dictionary containing conjunctions
    for bulletin, found in conjunctions.items():
        print("\n$", bulletin)
        for sentence, conj in found.items():
            for head, dep in conj.items():
                
                # create a list of lists (elements of a conjunction), example : [['5', 'feuilles', 'feuille', 'NOUN', 'feuilles', 'Gender=Fem|Number=Plur']....]
                result = [list(t) for t in flatten(dep)]    # get all dependents
                result.insert(0,list(head))                 # insert head as the first element           
                transposed = list(map(list,zip(*result)))   # transpose this result, example : [['5', '7'], ['feuilles', 'risque'], ['feuille', 'risque'], ['NOUN', 'NOUN']...]
                
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
                    #new_lemma = lemma.replace("-", " ") # make sure that presence of absence  of "-" character would not effect full match with fcu
                    
                    # FULL FCU MATCH
                    if any(lemma == val for val in fcu_lemmatised_labels.values()):
                        for key,val in fcu_lemmatised_labels.items():
                            if lemma == val:
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
                
                
    # create a dataframe from lists            
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
    df = df.assign(proposal_lemma=df['proposal_lemma'].str.split(',\n')).explode('proposal_lemma') # have one proposal by line
    return df

#%%
#########################################################################################
#################################CORRECT CONJUNCTIONS####################################
#########################################################################################

def correct_adj(idx_adj, idx_noun, parts_of_proposal,upos_proposal,parent_proposal, feat_proposal):
    """
    

    Parameters
    ----------
    idx_adj : int
        index of an adjective inside the proposal.
    idx_noun : int
        index of a noun inside the proposal.
    parts_of_proposal : list of str
        contains lemmas of the proposal.
    upos_proposal : list of str
        contains POS of the proposal.
    parent_proposal : list of str
        contains parent tokens of the proposal.
    feat_proposal : list of str
        contains morphological features of the proposal.

    Returns
    -------
    parts_of_proposal : list of str
        contains a grammatically correct proposal.

    """
    
    # get references for further modifications
    adj_endings=load_csv("ressources/adj_endings.csv", sep=";", header=0)   # load endings of french adjectives
    adj_dict = adj_endings.set_index('Plural')['Singular'].to_dict()        # create a dictionary from df
    
    
    # get information about adjectif
    adj = parts_of_proposal[idx_adj]        # lemma
    parent_adj = parent_proposal[idx_adj]   # parent
    feat_adj = feat_proposal[idx_adj]       # features
    
    # get information about noun
    noun = parts_of_proposal[idx_noun]      # lemma
    parent_noun = parent_proposal[idx_noun] # parent
    feat_noun = feat_proposal[idx_noun]     # features
    
    
    #################################################################################
    # as the morphological features of adjectives sometimes contain errors of tagging
    # we start by looking at morphological features of nouns
    # the rule is that an adjective should follow the grammar of a noun
    #################################################################################
    
    
    # simple singular forms
    if feat_noun == "Gender=Masc|Number=Sing" or feat_noun == "Gender=Fem|Number=Sing": # if noun has a singular form
        parts_of_proposal[idx_noun] = parent_noun                                       # we can use its parent version
        parts_of_proposal[idx_adj] = parent_adj                                         # same goes to the adjective, for example :
                                                                                        # lemma = ['colza', 'pousser']
                                                                                        # parent forms = ['colza', 'poussant']
                                                                
                                                                
     
    # other cases                  
    else:
        
        # with preposition
        if (upos_proposal[idx_noun-1] == "ADP") or (upos_proposal[idx_noun-2] == "ADP" \
                                                and upos_proposal[idx_noun-1] == "DET"): # if there is a preposition or a determinant with preposition before noun
                                                                                         # then we save parent (mostly plural) forms of this pair noun-adj
            parts_of_proposal[idx_noun] = parent_noun                                    # lemma = ['oignon', 'de', 'semis', 'précoce'] 
            parts_of_proposal[idx_adj] = parent_adj                                      # parent forms = ['oignon', 'de', 'semis', 'précoces']
                                            
            
        
        # without preposition                        
        else:
            
           # plural masculin
           if feat_noun == "Gender=Masc|Number=Plur":           # if noun has a plural form and its gender is masculin 
               parts_of_proposal[idx_noun] = noun               # we save lemmatised versions of the pair noun-adj
               parts_of_proposal[idx_adj] = adj                 # lemma = ['puceron', 'vert']
                                                                # parent form = ['pucerons', 'verts']
           
           # plural feminin 
           else:
               if feat_adj == "Gender=Fem|Number=Sing" :  # when adjectif doesn't accord with noun                        
                  parts_of_proposal[idx_adj] = parent_adj # this is an error, we save lemma of noun (sing) and parent of adj (sing)
                  parts_of_proposal[idx_noun] = noun      # for exemple: régions Gender=Fem|Number=Plur, lavalloise Gender=Fem|Number=Sing
               
                
               else:                                            # when there is no error of tagging
                  for old_end, new_end in adj_dict.items():     # we search for endings of adjectives
                     if parent_adj.endswith(old_end):           # if parent form of adjective (which is plural)
                        old_end_idx = parent_adj.rfind(old_end) # corresponds to one in the dict
                        parts_of_proposal[idx_noun] = noun      # we change it to sing and save lemma of a noun 
                        parts_of_proposal[idx_adj] = parent_adj[:old_end_idx] + new_end 
                        
    return parts_of_proposal



def correct_proposals(df):
    """
    

    Parameters
    ----------
    df : dataframe
        contains lemmas of proposals, lemmas of conjunts, morph. features of conjunts,
        parents of conjunts and POS of conjunctions

    Returns
    -------
    df : dataframe
        same with an additional column of grammatically correct proposals.

    """
    


    # load lists from dataframe of conjunctions
    proposals_lemma=df["proposal_lemma"].tolist()
    lemmas=df["conj_lemma"].tolist()
    feats=df["conj_feats"].tolist()
    parents=df["conj_parent"].tolist()
    upos=df["conj_upos"].tolist()
    
    
    correct_proposals = [] # initialise a list to store modified proposals
    
    for i, proposal in enumerate(proposals_lemma): # start parsing
        
        # split cells connected to the proposal into a list of strings
        temp_lemma = lemmas[i].split(",\n") # lemmas of the conjunt
        temp_feats=feats[i].split(",\n")    # features of the conjunt
        temp_upos=upos[i].split(",\n")      # POS of the conjunt
        temp_parents=parents[i].split(",\n")# parent forms of the conjunt
        
        
        # see if the proposal is inside the list of lemmas (of the corresponding cell)
        if proposal in temp_lemma:
            
            
            # get the index of the element in the list            
            idx_proposal = temp_lemma.index(proposal)            # get index of the proposal (which elemnt of the list)
            upos_proposal = temp_upos[idx_proposal].split()      # get POS features of the proposal by its index
            parent_proposal = temp_parents[idx_proposal].split() # get parent forms of the proposal by its index
            feat_proposal = temp_feats[idx_proposal].split()     # get morph. features of the proposal by its index

            parts_of_proposal = proposal.split()        # split proposal by space to a list of strings

            for idx, x in enumerate(upos_proposal):     # navigate through every token of the proposal
                
                #################################                                                            
                if x == "ADJ":
                ################################# 
                       
                    # NOUN ADJ
                    if (upos_proposal[idx - 1] == "NOUN" or upos_proposal[idx - 1] == "PROPN") and idx -1 >= 0:     # index of the noun should not negative,
                                                                                                                    # otherwise it would be an error
                                                                                                                    # as it would consider pairs like ADJ-NOUN as well
                                                                                                                    # where the noun has index of -1

                        idx_adj = idx       # get index of the adjective
                        idx_noun = idx - 1  # get index of the preceeding noun                       
                        parts_of_proposal = correct_adj(idx_adj,
                                                        idx_noun,
                                                        parts_of_proposal,
                                                        upos_proposal,
                                                        parent_proposal,
                                                        feat_proposal
                                                        ) # modify endings of the pair NOUN-ADJ
                        
                    
                    # ADJ NOUN
                    if  index_exists(upos_proposal, idx + 1) and upos_proposal[idx + 1] == "NOUN":  # index of the following noun should exist in the list
                                                                                                    # otherwise it would raise IndexError

                        idx_adj = idx       # get index of the adjective
                        idx_noun = idx + 1  # get index of the folllowing noun                    
                        parts_of_proposal = correct_adj(idx_adj,
                                                        idx_noun,
                                                        parts_of_proposal,
                                                        upos_proposal,
                                                        parent_proposal,
                                                        feat_proposal
                                                        ) # modify endings of the pair ADJ-NOUN
                     

                    # NOUN ADJ ADJ
                    if index_exists(upos_proposal, idx + 1) \
                                    and upos_proposal[idx + 1] == "ADJ" \
                                    and (upos_proposal[idx - 1] == "NOUN" or upos_proposal[idx - 1] == "PROPN") \
                                    and idx -1 >= 0:  # see if a new adjective can follow the adjective that we are currently considering
                                                      # and if a noun can preceed the two of them
                            
                        idx_adj = idx + 1   # get index of the second adjective
                        idx_noun = idx - 1  # get index of the preceeding noun                           
                        parts_of_proposal = correct_adj(idx_adj,
                                                        idx_noun,
                                                        parts_of_proposal,
                                                        upos_proposal,
                                                        parent_proposal,
                                                        feat_proposal
                                                        ) # modify endings of the pair NOUN-ADJ-ADJ
                            
                        
                ################################# 
                if x == "ADP":
                ################################# 
                
                    # ADP NOUN / ADP PROPN
                    if (upos_proposal[idx + 1] == "NOUN") or (upos_proposal[idx + 1] == "PROPN"): # see if a preposition can be followed by any noun

                        idx_adp = idx      # get index of the preposition
                        idx_noun = idx + 1 # get index of the following noun
                        
                        parent_adp = parent_proposal[idx_adp]       # get parent of of the proposition (par ex. : de, d', à)
                        parent_noun = parent_proposal[idx_noun]     # get parent of of the noun (par ex. : pailles, Angers, chair)                      
                        
                        parts_of_proposal[idx_adp] = parent_adp     # save parent form (par ex. : d')
                        parts_of_proposal[idx_noun] = parent_noun   # save parent form (par ex. : Angers)
                     
                    #  ADP DET NOUN
                    if upos_proposal[idx + 1] == "DET":  # see if a determinant follows preposition before the noun
                                                                        
                        idx_adp = idx      # get index of the preposition
                        idx_det = idx + 1  # get index of the determinant
                        idx_noun = idx + 2 # get index of the following noun
                        
                        parent_adp = parent_proposal[idx_adp] # get parent of of the proposition (par ex. : du, au, des, aux)
                        parent_det = parent_proposal[idx_det] # get parent of of the determinant. with stanza, it repeats the parent form of the preposition (par ex. : du, au, des, aux)
                        parent_noun = parent_proposal[idx_noun] # get parent of of the noun 
                        
                        if (parent_adp=="du" and parent_det == "du") \
                            or (parent_adp=="au" and parent_det == "au") \
                            or (parent_adp=="des" and parent_det == "des") \
                            or (parent_adp=="aux" and parent_det == "aux"): 
                        
                            parts_of_proposal[idx_adp] = parent_adp     # save preposition and noun but omit determinant , for ex:
                            parts_of_proposal[idx_det] = ""             # parent form : développement', 'du', 'du', 'colza'
                            parts_of_proposal[idx_noun] = parent_noun   # save : développement', 'du', '', 'colza'
                            
                            
                        if (parent_adp=="de" and parent_det == "la") \
                            or (parent_adp=="de" and parent_det == "l'") \
                            or (parent_adp=="à" and parent_det == "la") \
                            or (parent_adp=="à" and parent_det == "l'"): 
                        
                            parts_of_proposal[idx_adp] = parent_adp     # save preposition,determinant and noun, for ex:
                            parts_of_proposal[idx_det] = parent_det     # parent form : stade', 'de', 'la', 'culture' 
                            parts_of_proposal[idx_noun] = parent_noun   # save : stade', 'de', 'la', 'culture'                                                        
                 
                      
            
            parts_of_proposal = list(filter(None, parts_of_proposal))  # delete empty elements from the list (created by deleted determinants)          
            correct_proposals.insert(i, " ".join(parts_of_proposal)) # save proposal to a list by a corresponding index of a cell

        
    df["proposal"] = correct_proposals # save to df
    
    return df

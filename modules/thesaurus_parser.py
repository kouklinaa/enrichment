#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 23 16:39:31 2022

@author: anna chepaikina
"""
from modules.tagger import *
from modules.utils import *
import owlready2 as owl


def load_thesaurus(path):
    """
    

    Parameters
    ----------
    path : str
        local path to FCU.

    Returns
    -------
    onto : object
        structure of the thesaurus.

    """
    onto = owl.get_ontology(path).load()    
    return onto

def get_prefLabel(individual):
    """
    

    Parameters
    ----------
    individual : object
        correspondas to concept from the thesaurus.

    Returns
    -------
    pref : str
        french (preferred) label of the concept.

    """
    prefs = individual.prefLabel # get all preflabels
    pref = prefs[0] # french label is at position 0
    return pref

def get_altLabels(individual):
    """
    

    Parameters
    ----------
    individual : object
        correspondas to a concept from the thesaurus.

    Returns
    -------
    alts : list of str
        other french labels of the concept.

    """
    alts = [alt for alt in individual.altLabel]       
    return alts

def get_all_labels(individual):
    """
    

    Parameters
    ----------
    individual : object
        corresponds to a concept from the thesaurus.

    Returns
    -------
    labels : list of str
        all the labels for the individual.

    """
    labels = []
    
    # preflabel
    pref = get_prefLabel(individual)    
    labels.insert(0, pref)
    
    # other labels
    alts = get_altLabels(individual)
    labels.extend(alts)   
     
    return labels

def get_descendants(individual):
    """
    

    Parameters
    ----------
    individual : object
        corresponds to a concept from the thesaurus.

    Returns
    -------
    children : list of str
        skos:narrower values for the individual.

    """
    children = flatten([c.prefLabel for c in individual.narrower])
    return children

def get_ascendants(individual):
    """
    

    Parameters
    ----------
    individual : object
        corresponds to a concept from the thesaurus.

    Returns
    -------
    parents : list of str
        skos:broader values for the individual.

    """
    parents = flatten([c.prefLabel for c in individual.broader])
    return parents

def get_ascendants_of_descendants(children, parents):
    """
    

    Parameters
    ----------
    children : list of str
        skos:narrower values for the individual.
    parents : list of str
        skos:broader values for the individual.

    Returns
    -------
    parents_of_children : list of str
        skos:broader values of skos:narrower values if initial skos:broader value = multi usage.

    """
    parents_of_children = {}
    
    for label_x, concepts_x in children.items():
        
        # find all parents of children
        ascendants_of_descendants = [concepts_y 
                                     for x in concepts_x 
                                     for label_y, concepts_y in parents.items() 
                                     if x == label_y 
                                     if x != label_x 
                                     if x != "multi usages"] # map child concept of children dictionary (x) and a label of a concept from parent dictionary (label_y)
                                                             # if there are the same, then get parents for this child concept (concepts_y)
                                                             # do not include parents that are "multi usage" as it doesn't give anything new
                                                             # do not include parents that are equal to the label itself
        # flatten the list and remove duplicates
        ascendants_of_descendants = list(set(flatten(ascendants_of_descendants)))
        
        # save to a dict
        parents_of_children[label_x] = ascendants_of_descendants
    
    return parents_of_children

def parse_thesaurus(path):
    """
    

    Parameters
    ----------
    path : str
        local path to FCU.

    Returns
    -------
    labels : list of str
        all the labels for the individual.
    lemmatised_labels : list of str
        lemmatised labels for the individual.
    parents : list of str
        skos:broader values for the individual.
    children : list of str
        skos:narrower values for the individual.
    parents_of_children : list of str
        skos:broader values of skos:narrower values if initial skos:broader value = multi usage.

    """    
    
    # create empty dicts 
    labels = {}
    lemmatised_labels = {}
    parents = {}
    children = {}
    
    # create ontology from thesaurus
    onto = load_thesaurus(path)
    
    # parse ontology
    for i in onto.individuals():        
        if i.iri == "http://ontology.inrae.fr/frenchcropusage":
            continue
        else:
            iri = i.iri # get iri of the concept
            list_of_labels = get_all_labels(i) # get preflabel and altlabels of the concept           
            ascendants = get_ascendants(i) # get preflabels of broader elements of the concept
            descendants = get_descendants(i) # get preflabels of narrower elements of the concept

            # save all to different dictionaries                      
            for label in list_of_labels:
                # all labels dict 
                labels[label] = iri                
                # all lemmatised labels dict
                lemmatised_labels[label+"="+iri] = lemmatise(label)
                # all broader concepts dict
                parents[label] = ascendants
                # all narrower concepts dict
                children[label] = descendants                                                        
    
    # create parents of children dict
    parents_of_children=get_ascendants_of_descendants(children, parents)
    return labels,lemmatised_labels, parents, children, parents_of_children

    
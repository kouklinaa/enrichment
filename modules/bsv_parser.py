#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar  8 15:05:14 2022

@author: anna chepaikina
"""
from modules.utils import *
from bs4 import BeautifulSoup
import urllib.request
import re

#%%
#########################################################################################
#####################################LOAD CORPUS#########################################
#########################################################################################


def load_html(html):
    """
    

    Parameters
    ----------
    html : str
        url to an html page.

    Returns
    -------
    soup : object
        represents the document as a nested data structure.

    """
    soup = BeautifulSoup(urllib.request.urlopen(html), features="lxml")
    return soup

def extract_anchor_tags(soup):
    """
    

    Parameters
    ----------
    soup : object
        represents the document as a nested data structure.

    Returns
    -------
    anchor_tags : list of str
        holds extracted URLs found within a page’s <a> tags.

    """
    anchor_tags = [a for a in soup.find_all('a', href=True) 
                   if (a.text != "Name") and 
                   (a.text != "Description") and 
                   (a.text != "Size") and 
                   (a.text != "Last modified") and 
                   (a.text != "Parent Directory") and not (".csv" in a.text)]   # some pages hold information like :
                                                                                # Name, Description, Size,Last modified, Parent Directory.
                                                                                # these <a> tags don't contain html links to bsv
                                                                                # therefore we skip them
                                                                                # conserve urls like : http://ontology.inrae.fr/bsv/html/Corpus/Vespa/
    return anchor_tags

def extract_small_tags(soup):
    """
    

    Parameters
    ----------
    soup : object
        represents the document as a nested data structure.

    Returns
    -------
    small : list of str
        holds text found within a page’s <small> tags.

    """
    small = [tag.get_text() for tag in soup.findAll('small')] 
    return small

def extract_paragraph_tags(soup):
    """
    

    Parameters
    ----------
    soup : object
        represents the document as a nested data structure.

    Returns
    -------
    paragraph : list of str
        holds text found within a page’s <p> tags.

    """
    paragraph = [tag.get_text() for tag in soup.findAll('p') 
                 if tag.get_text() not in extract_small_tags(soup)] # select text from <p> tags 
                                                                    # as <small> tags usually contain picture desciptions which mix with other information
                                                                    # we skip text from <small> tags
    return paragraph



def get_bulletin(html):
    """
    

    Parameters
    ----------
    html : str
        url to an html page.

    Returns
    -------
    dico : dict
        maps url of a page to text found within this page’s <p> tags.
        key = url to an html page (bulletin)
        value = text found within this page’s <p> tags.

    """
    dico = {html+tag_html["href"]: extract_paragraph_tags(load_html(html+tag_html["href"])) 
            for tag_html in extract_anchor_tags(load_html(html))}       # search <a> tags of the html page to get urls of bulletins,
                                                                        # for ex. : http://ontology.inrae.fr/bsv/html/Corpus/Vespa/html/modification_BSV_maraichage_13-03_cle8eed1c.html'
                                                                        # then extract text from these bulletins
                                                                        # save it all to a dict
    return dico

def load_corpus(corpus):
    """
    

    Parameters
    ----------
    corpus : str
        main corpus page : http://ontology.inrae.fr/bsv/html/Corpus/  
        
        tree structure of this page :
          -  http://ontology.inrae.fr/bsv/html/Corpus/
             -   http://ontology.inrae.fr/bsv/html/Corpus/Alea/
                 -   http://ontology.inrae.fr/bsv/html/Corpus/Alea/pdf/
                 -   http://ontology.inrae.fr/bsv/html/Corpus/Alea/html/
             -   http://ontology.inrae.fr/bsv/html/Corpus/Tests/
                 -   http://ontology.inrae.fr/bsv/html/Corpus/Tests/Viticulture/html/pdf2blocks
                 -   http://ontology.inrae.fr/bsv/html/Corpus/Tests/Maraichage/html/
                 -   http://ontology.inrae.fr/bsv/html/Corpus/Tests/GrandsCultures/html/
             -   http://ontology.inrae.fr/bsv/html/Corpus/Vespa/
                 -   http://ontology.inrae.fr/bsv/html/Corpus/Vespa/pdf/
                 -   http://ontology.inrae.fr/bsv/html/Corpus/Vespa/html/
         
            we aim to parse it and extract bulletins (html pages) present in the folders: either html/ or pdf2blocks/ 

    Returns
    -------
    bsv : dict
        key = url to an html page (bulletin)
        value = text found within this page’s <p> tags.

    """    
    bsv={}
    for tag in extract_anchor_tags(load_html(corpus)):  # seacrh for <a> tags : VESPA/, TESTS/, ALEA/
        sub_corpus = corpus + tag.text                  # save full path to a test corpus , for  ex.: http://ontology.inrae.fr/bsv/html/Corpus/VESPA/
        print(sub_corpus)                                
        
        for sub_tag in extract_anchor_tags(load_html(sub_corpus)): # parse this test corpus 
            if "pdf" in sub_tag.text:                               # if <a> tag equals to pdf/
                continue                                                #  we skip it
            
            elif "html" in sub_tag.text:                               # if <a> tag equals to html/, 
                html = sub_corpus + sub_tag.text                        # we get full path to this fonder, for  ex.: http://ontology.inrae.fr/bsv/html/Corpus/VESPA/html/

            else:
                html = sub_corpus + sub_tag.text + "html/" + "pdf2blocs/" if sub_tag.text == "Viticulture" else sub_corpus + sub_tag.text + "html/"
                                                                        # get full path of bulletins (html pages) from VITICULTURE, MARAICHAGE, GRANDES CULTURES subfolders
                                                                        # in case of VITICULTURE, pages are held in  html/pdf2blocks/
                                                                        # otherwise, just html/
        
            dico = get_bulletin(html) # create a dictionary which maps path of a bulletin to its text
            bsv.update(dico) # add to the bsv dictionary
    return bsv



#%%
#########################################################################################
####################################CORRECT CORPUS#######################################
#########################################################################################

def unicode2latin1(bsv):
    """
    

    Parameters
    ----------
    bsv : dict
        key = url to an html page (bulletin)
        value = text found within this page’s <p> tags.

    Returns
    -------
    dico : dict
        key = url to an html page (bulletin)
        value = text found within this page’s <p> tags, converted from utf8 to latin1 

    """
    dico = {}
    for bulletin, text in bsv.items():
        new_text = []
        for mystring in text:
            mystring = mystring.replace("\u2019", "'") # convert unicode "RIGHT SINGLE QUOTATION MARK" to a simple apostrophe (not seen by the function .encode() used later)
            mystring = mystring.replace("\'", "'") # correct the apostrophe preceeded by a slash to simple apostrophe
            mystring = mystring.encode('latin1', 'ignore').decode('latin1') # save only latin 1 characters (delete unicode icons frequently used in html pages)
            new_text.append(mystring)
        dico[bulletin]=new_text
    
    return dico

def delete_urls(bsv):
    """
    

    Parameters
    ----------
    bsv : dict
        key = url to an html page (bulletin)
        value = text found within this page’s <p> tags.

    Returns
    -------
    dico : dict
        key = url to an html page (bulletin)
        value = text without urls found inside 

    """
    dico = {}
    with open('output/junk/deleted_urls.csv', 'w') as f:  # start writing a csv file      
        for bulletin,text in bsv.items():                      
            new_text = []           
            for mystring in text:
                result = re.findall(r'h?ttp\S+|\S+pdf',mystring)   # find all occurences of urls in text. urls can also end by .pdf        
                if result:
                    f.writelines(bulletin +";" +";".join(result)+"\n") # save them to the csv file
                new_string = re.sub(r'h?ttp\S+|\S+pdf', '',mystring) # delete these occurences from text
                new_text.append(new_string) # save new text
            dico[bulletin]=new_text # update bulletin
    
    return dico

def delete_consequtive_single_letters(bsv):
    """
    

    Parameters
    ----------
    bsv : dict
        key = url to an html page (bulletin)
        value = text found within this page’s <p> tags.

    Returns
    -------
    dico : dict
        key = url to an html page (bulletin)
        value = text without sentences containing consequtive single letters. 
                these sentences are almost always badly formed and resulted by pdf->html conversion

    """
    dico = {}
    with open('output/junk/deleted_consequtive_letters.csv', 'w') as f: # start writing a csv file 
        for bulletin,text in bsv.items():
            new_text = []
            for mystring in text:
                result = re.findall(r'\b(\w\s+){4,}\w\s*',  mystring) # find single letters in a string if they appear at more than 3 times
                if result:
                    f.writelines(bulletin+";"+mystring+"\n") # save the sentence, containing this occurence to the csv file
                else:
                    new_text.append(mystring) # save other sentences without such mistakes
            dico[bulletin]=new_text # update bulletin
    return dico

def split_by_uppercase(bsv):
    """
    

    Parameters
    ----------
    bsv : dict
        key = url to an html page (bulletin)
        value = text found within this page’s <p> tags.

    Returns
    -------
    dico : dict
        key = url to an html page (bulletin)
        value = text where strings like "endStart" are separated to "end. Start"

    """
    dico = {}
    for bulletin,text in bsv.items():
        new_text = [re.sub(r'(?<![A-Z\W])(?=[A-Z|Ç|É|È|À])', '. ', mystring) for mystring in text] # if a capital letter follows a small letter, we separte them by dot
        dico[bulletin]=new_text # update bulletin
    return dico




def split_by_dot(bsv):
    """
    

    Parameters
    ----------
    bsv : dict
        key = url to an html page (bulletin)
        value = text found within this page’s <p> tags.

    Returns
    -------
    dico : dict
        key = url to an html page (bulletin)
        value = list of str (sentences), resulted by split on dots

    """
    dico = {}
    for bulletin, text in bsv.items():
        new_text = []
        for mystring in text:
            new_list = re.split('\.\s?(?=[A-Z|0-9])', mystring) # split by dot followed by a space (or not), a Capital letter or digits . other strings like a. transiens should be remained
            new_list = [sentence.rstrip('.') for sentence in new_list] # erase dots at the beginning of a sentence
            new_list = [sentence.strip() for sentence in new_list] # delete trailing spaces
            new_list = list(filter(None, new_list)) # delete empty strings in a list
            new_list = [sentence for sentence in new_list if len(sentence)>1] # save strings which are longer than 1 character
            new_text.append(new_list) # save new text
        dico[bulletin]=flatten(new_text) # update bulletin
    return dico


def correct_corpus(bsv):
    """
    

    Parameters
    ----------
    bsv : dict
        key = url to an html page (bulletin)
        value = text found within this page’s <p> tags.

    Returns
    -------
    dico : dict
        key = url to an html page (bulletin)
        value = list of str (sentences), with some modifications 

    """
    dico = unicode2latin1(bsv) # delete unicode icons
    dico = delete_urls(dico) # delete urls
    dico = delete_consequtive_single_letters(dico) # delete sentences with consequtive letters
    dico = split_by_uppercase(dico) # correct mistakes like endStart
    dico = split_by_dot(dico) # split text into sentences
    return dico


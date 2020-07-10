import json
import re
import pandas as pd
import random
import pickle
import copy
import unicodedata
import rdflib
from rdflib import URIRef, RDFS
from sparql_builder import sparql_build
from sparql_builder import constants
from corrector import get_suggestion_property,get_correct_title,get_correct_people_name

data_path = 'pandas_data/'
graph = rdflib.Graph()
graph.parse("data/movieontology.ttl", format="ttl")


import unicodedata

def strip_accents(s):
   return ''.join(c for c in unicodedata.normalize('NFD', s)
                  if unicodedata.category(c) != 'Mn').lower()

entities_dict = pickle.load( open( "entities_dict.p", "rb" ) )
with open(data_path+"movies_df.dat", "rb") as f:
    movies = pickle.load(f)
with open(data_path+"series_df.dat", "rb") as f:
    series = pickle.load(f)
with open(data_path+"person_df.dat", "rb") as f:
    person = pickle.load(f)    
with open(data_path+"production_company_df.dat", "rb") as f:
    company = pickle.load(f)

person['birthName'] = person['birthName'].apply(strip_accents)
movies['title'] = movies['title'].apply(strip_accents)
series['title'] = series['title'].apply(strip_accents)
company['name'] = company['name'].apply(strip_accents)

def get_uri_from_movie_serie(title):
    results = movies.loc[movies['title']==strip_accents(title)]
    if not results.empty:
        return "movie", results["uri"].tolist()
    else:
        results = series.loc[series['title']==strip_accents(title)]
        return "series", results["uri"].tolist()

def get_uri_from_serie_movie(title):
  results = series.loc[series['title']==strip_accents(title)]
  if not results.empty:
        return "series", results["uri"].tolist()
  else:
    movies.loc[movies['title']==strip_accents(title)]
    return "movie", results["uri"].tolist()
     

def get_company_uri(name):
    results = company.loc[company['name']==strip_accents(name)]
    return results["uri"].tolist()


def get_person_uri(birth_name):
    df = person.loc[person["birthName"]==strip_accents(birth_name)]
    results = []
    for index, row in df.iterrows():
        staff_pos = re.search(r"\w*_*-*\w*$", row["type"], re.IGNORECASE).group()
        results.append([row["uri"], staff_pos])
    try:
      n1,n2=birth_name.split()
      birth_name2=n2+', '+n1
      df = person.loc[person["birthName"]==strip_accents(birth_name2)]
      for index, row in df.iterrows():
          staff_pos = re.search(r"\w*_*-*\w*$", row["type"], re.IGNORECASE).group()
          results.append([row["uri"], staff_pos])
    except ValueError:
      return results
    return results


def get_relations(text):
  relations = text.split('*')[1]
  #relations_list = relations.split(')')
  relations_list = re.findall('\(.*?\)',relations)
  return relations_list


def clean_word(palavra):

    # Unicode normalize transforma um caracter em seu equivalente em latin.
    nfkd = unicodedata.normalize('NFKD', palavra)
    palavraSemAcento = u"".join([c for c in nfkd if not unicodedata.combining(c)])

    # Usa expressÃ£o regular para retornar a palavra apenas com nÃºmeros, letras e espaÃ§o
    r=re.sub('[^a-zA-Z0-9 \\\]', '', palavraSemAcento)
    return r

def check_remove(val):
  exclude_list = ['data','Data']
  if(val in exclude_list):
    return True

  return False


def especify_entities(entities):
  print('Specify Entities')
  sugestions=[]
  return_sugestion=False
  to_check_cond=False
  
  c=-1
  unk_ents = []
  ambigue_ents=[]

  is_series=False


  for ent in entities:
    c+=1
    print(ent['entity'])

    #filter
    if(ent['value']=='data de'):
      continue

    if(check_remove(ent['value'])):
      print('Removing: ',ent['value'])
      unk_ents.append(c)
      continue

    print('checking what entity is this value: ',ent['value'])
    if(ent['value'] in entities_dict):
      ent['entity'] = entities_dict[ent['value']]
      print('entity is defined on entities dict!')
      if(entities_dict[ent['value']]=='series'):
        is_series=True
      print(ent['entity'])
      continue
    elif(ent['entity']=='genre_name' or ent['entity']=='staff_ent' or ent['entity']=='property_ent'):
      print(clean_word(ent['value']))
      v=clean_word(ent['value']).lower()
      if(v in entities_dict):
        ent['entity'] = entities_dict[v]
      else:
        #utilizar corrector
        a = get_suggestion_property([ent['value']])
        #sugestions.append(a)
        #return_sugestion=True
        #unk_ents.append(c)
        print('corrector suggestion: ',str(a))
        ent['entity']=a
    elif(ent['entity']=='awards'):
      ent['entity'] = entities_dict[clean_word(ent['value']).lower()]
    elif(ent['entity']=='award'):
      pass
    else:
      cond_found=False

      ###person#################################################3      

      if ent['entity']=='people_names':
        print('searching person name in database...')
        uris = get_person_uri(ent['value'])
        
        if(len(uris)>=1):
          print('entity is a person')
          print(uris)
          ent['entity']='person'
          ent['uris']=uris
          cond_found=True
        else:
          print('searching company uris in database...')
          uris = get_company_uri(ent['value'])
          #print(uris)
          if(len(uris)>=1):
            #print('entity is a movie')
            #ent['entity']='company'
            ent['uris']=uris
            cond_found=True

      ###movie series#################################################3      


      elif ent['entity']=='title':
        if(is_series==False):
          print('searching movie title in database...')
          uris = get_uri_from_movie_serie(ent['value'])
        else:
          print('searching serie title in database...')
          uris = get_uri_from_serie_movie(ent['value'])
        #print(uris)
        if(len(uris[1])>=1):
          #print('entity is a movie')
          ent['entity']=uris[0]
          ent['uris']=uris
          cond_found=True
        else:
          print('did not find movie/serie title...maybe is a company name?')
          print('searching company uris in database...')
          uris = get_company_uri(ent['value'])
          #print(uris)
          if(len(uris)>=1):
            #print('entity is a movie')
            ent['entity']='company_names'
            ent['uris']=uris
            cond_found=True


      ###company#################################################3      
      elif ent['entity']=='company_names':
        print('searching company uris in database...')
        uris = get_company_uri(ent['value'])
        #print(uris)
        if(len(uris)>=1):
          #print('entity is a movie')
          #ent['entity']='company'
          ent['uris']=uris
          cond_found=True
        else:
          print('searching person name in database...')
          uris = get_person_uri(ent['value'])
          
          if(len(uris)>=1):
            print('entity is a person')
            print(uris)
            ent['entity']='person'
            ent['uris']=uris
            cond_found=True
          else:
            print('searching movie title in database...')
            uris = get_uri_from_movie_serie(ent['value'])
            if(len(uris[1])>=1):
              #print('entity is a movie')
              ent['entity']=uris[0]
              ent['uris']=uris
              cond_found=True
            else:
              print('searching serie title in database...')
              uris = get_uri_from_serie_movie(ent['value'])
              #print(uris)
              if(len(uris[1])>=1):
                #print('entity is a movie')
                ent['entity']=uris[0]
                ent['uris']=uris
                cond_found=True




      if(cond_found==False):
        #checar se e algum filme ou nome de pessoa
        title_name_related=[]
        if ent['entity']=='people_names':
          title_name_related=get_correct_people_name(ent['value'])
          for t in title_name_related:
            sugestions.append(t)
            return_sugestion=True
          
        elif ent['entity']=='title':
          title_name_related=get_correct_title(ent['value'])
          for t in title_name_related:
            sugestions.append(t)
            return_sugestion=True
        if(len(title_name_related)==0):
          print("Entity Unknow!!")
          print('deleting the entity:')
          unk_ents.append(c)


  new_entities=[]
  for i in range(len(entities)):
    if(i not in unk_ents):
      new_entities.append(entities[i])
  return new_entities,return_sugestion,sugestions


def get_relations_queries(rasa_entities):
  relations = []
  text = rasa_entities['text']
  entities = rasa_entities['entities']
  for i in range(len(entities)):
    for j in range(len(entities)):
      if(i!=j):
        relations.append(text+'|'+entities[i]['value']+'|'+entities[j]['value'])
  return relations

def get_relations_queries2(text,entities):
  relations = []
  for i in range(len(entities)):
    for j in range(len(entities)):
      if(i!=j):
        relations.append(text+'|'+entities[i]['value']+'|'+entities[j]['value'])
  return relations


def get_rdfs_label( subject, lang="pt-br"):
    subject = URIRef(subject)
    labels = []
    # setup the language filtering
    if lang is not None:
        if lang == "":  # we only want not language-tagged literals

            def langfilter(l):
                return l.language is None

        else:

            def langfilter(l):
                return l.language == lang

    else:  # we don't care about language tags

        def langfilter(l):
            return True

    for label in graph.objects(subject, RDFS.label):
        if langfilter(label):
            #labels.append(str(label))
            return str(label)
    return labels
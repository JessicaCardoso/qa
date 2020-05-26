from utils import get_uri_from_movie_serie,clean_word,get_rdfs_label,especify_entities,get_relations_queries,get_person_uri
from pprint import pprint
from simpletransformers.classification import ClassificationModel
import copy
from sparql_builder import sparql_build,constants
from SPARQLWrapper import SPARQLWrapper, JSON
import pickle
import traceback
import context

#re_model = ClassificationModel('roberta', '/content/drive/My Drive/NLP/RE_models', args={})
re_model = ClassificationModel('roberta', 'RE_models', use_cuda=False)
entities_dict = pickle.load( open( "entities_dict.p", "rb" ) )

interest_var_dict={'movie_value':'movie'}
login = "dslab"
password = "DSLABm3d3ixa3ntrar" 

endpoint = "http://139.82.100.42:50004/fuseki/imdb-dataset/query"
sparql_wrapper = SPARQLWrapper(endpoint)
sparql_wrapper.setCredentials(login, password)


def relation_extraction(relations_queries):
  relations=[]
  #for r in relations_queries:
  #  predictions, raw_outputs = re_model.predict([r])
  #  if(predictions[0]==0):
  #    relations.append(r)
  predictions, raw_outputs = re_model.predict(relations_queries)
  print('predictions: ',predictions)
  for i in range(len(predictions)):
    if(predictions[i]==0):
      relations.append(relations_queries[i])

  return relations

def remove_duplicated_relations(relations):
  filtered_relations=[]
  for i in range(len(relations)):
    cond=True
    #remove ('actor','','actor')
    if(relations[i][0]==relations[i][2]):
      continue
    for j in range(i,len(relations)):
      if i!=j:
        if(relations[i][0]==relations[j][0] and relations[i][2]==relations[j][2]):
          cond=False
    if(cond):
      filtered_relations.append(relations[i])
  return filtered_relations

def get_relation(triple):
  if(triple[0] not in constants.PERSON and
    triple[0] not in constants.MOVIE_SERIE and
    triple[0] not in constants.OTHERS ):
    return None
  if(triple[2] not in constants.PERSON and
    triple[2] not in constants.MOVIE_SERIE and
    triple[2] not in constants.OTHERS):
    return None

  for t in constants.TRIPLES_MOVIE:
      if(triple[2] == t[2]):
        return t[1]
  for t in constants.TRIPLES_PERSON:
      if(triple[2] == t[2]):
        return t[1]

def extend_triples(tuples,entities,uris):
  print("Extending Triples")
  new_tuples=[]
  for triple in tuples:
    if(triple[2].startswith('genre_')):
      if(triple[0]!='genre'):
        new_tuples.append((triple[0],'has_genre','genre'))
      new_tuples.append(('genre','has_value',triple[2]))
    elif(triple[2].startswith('territory_')):
      if(triple[0]=='movie' or triple[0]=='serie'):
        new_tuples.append((triple[0],'has_filming_location','territory'))
        new_tuples.append(('territory','has_value',triple[2]))
      else:
        new_tuples.append((triple[0],'has_company_location','territory'))
        new_tuples.append(('territory','has_value',triple[2]))
    elif(triple[2].startswith('award_')):
        if(triple[0]=='nomination'):
            new_tuples.append(('nomination','has_value',entities_dict[triple[2]]))
        else:
            new_tuples.append(('award','has_value',entities_dict[triple[2]]))
        if(triple[0] in constants.PERSON or triple[0] in constants.MOVIE_SERIE ):
          new_tuples.append((triple[0],'has_award','award'))
    else:
      rel = get_relation(triple)

      print('relation: ',rel)
      if(rel is None):
        print('triple has person name or title')
        print(triple)
        #entidades
        for ent in entities:
          if(ent['value']==triple[0] or ent['value']==triple[2]):
            if 'uris' in ent:
              print(ent['uris'])
              if(ent['uris'][0]=='movie' or ent['uris'][0]=='serie'):
                rel = get_relation([ent['uris'][0],'',triple[2]])
                #Bugfix questao 'Indicacoes do filme El Sistema Pelegrin'
                if(rel == None):
                  pass
                else:
                  new_tuples.append((ent['uris'][0],rel,triple[2]))
                for uri in ent['uris'][1]:
                  new_tuples.append([ent['uris'][0], 'has_value', uri])
              
              elif(ent['entity']=='person'):
                print('person uris:')
                if(triple[0] not in constants.PERSON ):
                  new_tuples.append((triple[0], 'has_person', 'person'))  
                  for uri in ent['uris']:
                    new_tuples.append(('person', 'has_value', uri[0]))  
                else:
                  for uri in ent['uris']:
                    new_tuples.append((triple[0], 'has_value', uri[0]))
                  
              #else:
              #  caso [['http://www.imdb..', 'Actress'],[['http://www.imdb...', 'Producer']]
              #  new_tuples.append(('movie','has_person','person'))
              #  for uri in ent['uris']:
              #    new_tuples.append(('person', 'has_value', uri[0]))
              
            else:
              #caso que e um title ou people_names, mas
              #nao foi encontrado esse titulo no bd
              new_tuples.append([triple[0], 'has_value', triple[2]])
      else:
        if(triple[0] in constants.PERSON):
          print('Triple is some person job')
          new_tuples.append((triple[0], rel, triple[2]))
        elif(triple[0] in constants.MOVIE_SERIE):
          print('Triple is Movie or Serie')
          #rel = get_relation(triple[2])
          new_tuples.append((triple[0], rel, triple[2]))      
  return new_tuples
  
def is_entity(entity):
  if entity in constants.NER_ENTITIES_MAP:
    return True
  if(entity  in constants.GENRE_MAP):
    return True
  
  
  return False


def construct_tuples(relations,entities):
  ent_dict = {}
  tuples_relation =[]
  uris = []
  values_dict = {}
  for ent in entities:
    if('uris' in ent):
      pass 
    elif(ent['entity']=='title'):
      pass
    elif(ent['entity']=='people_names'):
      pass
    else:
      ent_dict[ent['value']] = ent['entity']
  print('ent_dict: ',ent_dict)
  for rel in relations:
    left_val = rel.split('|')[1]
    right_val = rel.split('|')[2]
    if(left_val in ent_dict):
      subj = ent_dict[left_val]
    else:
      subj = left_val
    if(right_val in ent_dict):
      obj = ent_dict[right_val]
    else:
      obj = right_val

    #substitui titulos/person name nas relacoes pela entidade
    if obj in values_dict:
      obj = values_dict[obj]

    tuples_relation.append([subj,"",obj])
  
  return tuples_relation,uris


def run_sparql(sparql_query):
  sparql_wrapper.setQuery(sparql_query)
  sparql_wrapper.setReturnFormat(JSON)
  results = sparql_wrapper.query().convert()
  print(len(results["results"]["bindings"]))
  return results

def encode(results,rec_relations):
  data=[]
  output = {
        "text": "Resultado(s) retornado(s):",
        "related": [],
        "relations":rec_relations,
        "results":[],
        "eval_options": True
    }
  
  my_dict={key:[] for key in results[0]['head']['vars']}

  for re in results:
    bindings = re['results']['bindings']
    for b in bindings:
      for name in b.keys():
        if(b[name]['value'].startswith('http')):
          my_dict[name].append(get_rdfs_label(b[name]['value']))
          #data.append(get_rdfs_label(b[name]['value']))
        else:
          my_dict[name].append(b[name]['value'])
          #data.append(b[name]['value'])
  output['results'] = my_dict
  return output

def is_domain(x,y,context):
  if(x in context.domain_dict):
    domains = context.domain_dict[x]
    if(y in domains):
      return True
  return False 

def relation_recommendation(relations):
  new_relations = []
  for triple in relations:
    new_triple = []
    for t in triple:
      if(not t.startswith("http")):
        if(t in constants.NER_ENTITIES_MAP):
          correct_entity = constants.NER_ENTITIES_MAP[t]
          if(correct_entity in constants.ENTITY_TO_URI):
            new_triple.append(constants.ENTITY_TO_URI[correct_entity])
          else:
            print("Error! Entidade n esta no dict!!")
            print(correct_entity)
            return relations
        else:
            print("Error! Entidade n esta no dict!!")
            print(t)
            return relations
      else:
        new_triple.append(t)
    new_relations.append(new_triple)
      
  return new_relations
          
def get_context_related(interest_entities,cont):
  print('get context!!!')
  print(cont.history)
  relations=[]
  cond=True
  #percorrer o historico
  for hist in cont.history:
    for ent in hist[1]:
      for interest_entity in interest_entities:
        print(interest_entity['entity'],ent['entity'])
        if is_domain(interest_entity['entity'],ent['entity'],cont):
          print('Is domain!!')
          #context_entities.append(ent['entity'])
          if(cond):#so pode receber relacoes 1 vez
            #retirar a relacao principal da questao
            #Ex: premios do filme avatar tem ((movie,'',award),(movie,'',Avatar))
            #comparamos com a interest var do historico eleito: 
            #retiramos ((movie,'',award))
            #print('history: ')
            #print(hist[0][0])
            for h in hist[2]:
              print('h: ',h)
              if(h[0]!=hist[0][0] and h[2]!=hist[0][0]):
                relations.append(h)
            cond=False
          question_triple = [ent['entity'],'',interest_entity['entity']]
          rec = get_relation(question_triple)
          relations.append((question_triple[0],rec,question_triple[2]))
  return relations

import copy
from rasa.nlu.model import Interpreter,Metadata
interpreter = Interpreter.load('models/')
cont = context.Context()


def search(text=''):

  text=clean_word(text)

  entities_rasa = interpreter.parse(text)
  print('Raw Entities:')
  pprint(entities_rasa)


  intent = entities_rasa['intent']['name']
  if(intent =='property_by_movie_series'):
    intent = 'select'
  if(intent =='movies_affirmative_simple'):
    intent = 'ask'

  entities=especify_entities(entities_rasa['entities'])
  print('Corrected Entities:')
  pprint(entities)

  #tratar intencao de contexto
  if(entities_rasa['intent']['name']=='context'):
    print('Inferir de contexto')
    relations=[]
    interest_entities = entities
    print('interest_entity: ',interest_entities)
    #no contexto simples, todas as entidades recebidas
    #sao as de interesse.
    ref=cont.search_for_numbers(text)
    print(ref)
    if(ref==-1):
      relations_tuples = get_context_related(interest_entities,cont)
      print('infered relations:',relations_tuples)

    else:
      relations=[]
      cond=True
      for hist in cont.history:
        for ent in hist[1]:
          for interest_entity in interest_entities:
            if is_domain(interest_entity['entity'],ent['entity'],cont):
              if(cond):
                print(hist)
                #print(hist[0]) 
                interest_var=hist[0][0]
                #print(hist[3]['results']) 
                results=hist[3]['results'][interest_var]
                context_interest_var = interest_var_dict[interest_var]
                relations.append([context_interest_var,'',results[ref]])
                relations.append([context_interest_var,'',interest_entity['entity']])
                print('relations: ',relations)
                cond=False

                raw_relations_tuples = copy.deepcopy(relations)
                relations_tuples =extend_triples(relations,entities,[])
                print('tuples after: ',relations_tuples)
                relations_tuples_copy = copy.deepcopy(relations_tuples)

    rec_relations = relation_recommendation(relations_tuples)
    print(rec_relations)
    
    sparql_query,interest_var = sparql_build(relations_tuples)
    print(sparql_query,interest_var)

    try:
      results = run_sparql(sparql_query)
      data= encode([results],rec_relations)
      cont.set_current_turn_results(text,data,entities_rasa['intent']['name'],entities,relations_tuples,results['head']['vars'])
      return data
    except Exception:
      traceback.print_exc()
      output = {
        "text": "Sem resultados.",
        "related": [],
        "relations":[],
        "results":[],
        "eval_options": False
        }
      return output

  queries = get_relations_queries(entities_rasa)
  print(queries)
  
  pred_relations=relation_extraction(queries)
  print(pred_relations)
  
  relations_tuples,uris=construct_tuples(pred_relations,entities)
  print('tuples before: ',relations_tuples)
  
  raw_relations_tuples = copy.deepcopy(relations_tuples)

  relations_tuples =extend_triples(relations_tuples,entities,uris)
  print('tuples after: ',relations_tuples)
  relations_tuples_copy = copy.deepcopy(relations_tuples)

  rec_relations = relation_recommendation(relations_tuples)
  print(rec_relations)
  
  sparql_query,interest_var = sparql_build(relations_tuples,spql_type=intent)
  print(sparql_query,interest_var)
  #return entities_rasa['intent']['name'],entities,relations_tuples,interest_var
  
  try:
    results = run_sparql(sparql_query)
    data= encode([results],rec_relations)
    cont.set_current_turn_results(text,data,entities_rasa['intent']['name'],entities,relations_tuples,results['head']['vars'])
    return data
  except Exception:
    traceback.print_exc()
    output = {
        "text": "Sem resultados.",
        "related": [],
        "relations":[],
        "results":[],
        "eval_options": False
        }
    return output
    
#funciona
text= 'premios do Avatar'
#text = 'atores que ganharam o oscar'
#text = 'atores que foram indicados ao oscar'
#text = 'me diga a premiacao da atriz Angelina Jolie'
#text = 'Me diga filmes da Angelina Jolie'
#text = 'Me diga filmes da atriz Angelina Jolie'
#text = 'filmes que ganharam o oscar'
#text = 'Indicações do filme El Sistema Pelegrin'
#text='O filme The Vampire obteve que premiação?'
#text = 'O Ator Geraldo Rivera do filme Volver ganhou o que.'

#text = 'me diga a premiacao do Geraldo Rivera'

#text = 'Me mande filmes de crime'
#text= 'quais os filmes do genero diversão'
#text='atrizes de avatar'

#Intent:: ask
#text = 'Seria Angelina Jolie uma atriz'
#text = 'Seria do genero diversão esse filme avatar?'

results = search(text)
print('Results: ')
print(results)
#text = 'atores desse primeiro'
#text = 'suas atrizes'
text='atrizes'

results = search(text)
print(results)

#Atores de avatar
#suas atrizes (avatar)
#seus premios (avatar)
#premio do primeiro (atrizes)
#preimio do primeiro ator (ator)

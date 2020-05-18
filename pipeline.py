from utils import get_uri_from_movie_serie,clean_word,get_rdfs_label,especify_entities,get_relations_queries,get_person_uri
from pprint import pprint
from simpletransformers.classification import ClassificationModel
import copy
from sparql_builder import sparql_build,constants
from SPARQLWrapper import SPARQLWrapper, JSON
import pickle
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


def extend_triples(tuples,entities,uris):
  new_tuples=[]
  for triple in tuples:
    if(triple[2].startswith('genre_')):
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
      if(triple[0] == 'person'):
        for uri in uris:
          new_tuples.append(('person', 'has_value', uri[0]))

      elif(triple[0] in constants.PERSON):
        cond=False
        for t in constants.TRIPLES_PERSON:
          if(triple[2]==t[2]):
            cond=True
            new_tuples.append((triple[0], t[1], triple[2]))
        if(cond==False):
          #uris = get_person_uri(triple[2])
          for uri in uris:
            if(triple[0].lower()==uri[1].lower()):
              new_tuples.append((triple[0], 'has_value', uri[0]))
      elif(triple[0] in constants.MOVIE_SERIE):
        cond=False
        for t in constants.TRIPLES_MOVIE:
          if(triple[2]==t[2]):
            cond=True
            new_tuples.append((triple[0], t[1], triple[2]))
        if(cond==False):
          #we have already found uris from movie
          if(len(uris)>0):
            #uris = get_uri_from_movie_serie(triple[2])
            print('movies uris: ')
            print(uris)
            #if(triple[0].lower()==uris[0].lower()):
              #print(uris)Estou colocando todas as uris com esse titulo
            for uri in uris:
              new_tuples.append((triple[0], 'has_value', uri[0]))
          else:
            print('finding uris in extend_triples')
            uris = get_uri_from_movie_serie(triple[2])
            print(uris)
            for uri in uris[1]:
              new_tuples.append((triple[0], 'has_value', uri))
          

      else:
        #identificar como titulo de filme,nome de empresa, ou nome de pessoa
          #bugfix: ajustar entity com  o titulo do filme
          for ent in entities:
            if(ent['entity'] == triple[0]):
              ent['entity'] = 'movie'

        #a=2/0
        #new_tuples.append(('person', 'has_value', uris[0][0]))

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
    if(ent['entity'] == 'people_names'):
      #checar nome pessoa
      uris = get_person_uri(ent['value'])
      
      #if(len(uris)>=1):
      tuples_relation.append(('person','',ent['value']))
      values_dict[ent['value']] = 'person'
        #é pessoa!
        #for uri in uris:
        #  tuples_relation.append((uri[1],'', ent['value'] ))

    elif(not is_entity(ent['entity'])):
      print('checking what entity is')
      print(ent['entity'])
      #checar nome pessoa
      uris = get_person_uri(ent['entity'])
      
      if(len(uris)>=1):
        #é pessoa!
        for uri in uris:
          tuples_relation.append((uri[1],'', ent['value'] ))
          values_dict[ent['value']] = 'person'
      
      #checar titulo filme
      uris = get_uri_from_movie_serie(ent['entity'])
      if(len(uris[1])>=1):
        print('uris: ',uris)
        ent['entity']=uris[0]
        tuples_relation.append((uris[0], '', ent['value']))
        
  for ent in entities:
    if(ent['entity']=='people_names'):
      pass 
    else:
      ent_dict[ent['value']] = ent['entity']
  
  
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
          

import copy
from rasa.nlu.model import Interpreter,Metadata
interpreter = Interpreter.load('models/')
cont = context.Context()


def search(text=''):

  text=clean_word(text)

  entities_rasa = interpreter.parse(text)
  pprint(entities_rasa)

  entities=especify_entities(entities_rasa['entities'])
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
    cond=True
    if(ref==-1):
      context_entities=[]
      #percorrer o historico
      for hist in cont.history:
        
        for ent in hist[1]:
          for interest_entity in interest_entities:
            if is_domain(interest_entity['entity'],ent['entity'],cont):
              context_entities.append(ent['entity'])
              if(cond):#so pode receber relacoes 1 vez
                #retirar a relacao principal da questao
                #Ex: premios do filme avatar tem ((movie,'',award),(movie,'',Avatar))
                #comparamos com a interest var do historico eleito: 
                #retiramos ((movie,'',award))
                #print('history: ')
                #print(hist[0][0])
                for h in hist[2]:
                  #print('h: ',h)
                  if(h[0]!=hist[0][0] and h[2]!=hist[0][0]):
                    relations.append(h)
                cond=False
              relations.append([ent['entity'],'',interest_entity['entity']])
      print(context_entities)
      print('infered relations:',relations)

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

    rec_relations = relation_recommendation(relations_tuples)
    print(rec_relations)
    
    sparql_query,interest_var = sparql_build(relations_tuples)
    print(sparql_query,interest_var)

    try:
      results = run_sparql(sparql_query)
      print(results)
      data= encode([results],rec_relations)
      print(data)

      cont.set_current_turn_results(text,data,entities_rasa['intent']['name'],entities,raw_relations_tuples,results['head']['vars'])
      return data
    except:
      output = {
        "text": "Sem resultados.",
        "related": [],
        "relations":[],
        "eval_options": True
        }
      return output

  queries = get_relations_queries(entities_rasa)
  print(queries)
  
  pred_relations=relation_extraction(queries)
  print(pred_relations)
  
  relations_tuples,uris=construct_tuples(pred_relations,entities)
  print('tuples before: ',relations_tuples)
  print('Correct entities: ')
  pprint(entities)
  
  raw_relations_tuples = copy.deepcopy(relations_tuples)

  relations_tuples =extend_triples(relations_tuples,entities,uris)
  print('tuples after: ',relations_tuples)

  rec_relations = relation_recommendation(relations_tuples)
  print(rec_relations)
  
  sparql_query,interest_var = sparql_build(relations_tuples)
  print(sparql_query,interest_var)
  #return entities_rasa['intent']['name'],entities,relations_tuples,interest_var
  
  try:
    results = run_sparql(sparql_query)
    print(results)

    data= encode([results],rec_relations)
    print(data)

    cont.set_current_turn_results(text,data,entities_rasa['intent']['name'],entities,raw_relations_tuples,results['head']['vars'])
    return data
  except:
    output = {
        "text": "Sem resultados.",
        "related": [],
        "relations":[],
        "eval_options": True
        }
    return output
    

#text = 'Indicações do filme El Sistema Pelegrin'
#text='O filme The Vampire obteve que premiação?'
#text = 'O Ator Geraldo Rivera do filme Volver ganhou o que.'
#text = 'me diga a premiacao da atriz Angelina Jolie'
#text = 'me diga a premiacao do Geraldo Rivera'
#text = 'atores que ganharam o oscar'
#text = 'atores que foram indicados ao oscar'
text = 'filmes que ganharam o oscar'
#text= 'premios do avatar'
text = 'Me diga filmes da Angelina Jolie'
#text = 'Me diga filmes da atriz Angelina Jolie'

#text = 'Me mande filmes de crime'

results = search(text)
print(results)
text = 'atores desse primeiro'
#text = 'suas atrizes'

results = search(text)
print(results)

#Atores de avatar
#suas atrizes (avatar)
#seus premios (avatar)
#premio do primeiro (atrizes)
#preimio do primeiro ator (ator)

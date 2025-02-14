from utils import get_uri_from_movie_serie,clean_word,get_rdfs_label,especify_entities,get_relations_queries,get_relations_queries2,get_person_uri
from pprint import pprint
from simpletransformers.classification import ClassificationModel
import copy
from sparql_builder import sparql_build,constants
from SPARQLWrapper import SPARQLWrapper, JSON
import pickle
import traceback
import context
import multiprocessing
import time


#re_model = ClassificationModel('roberta', '/content/drive/My Drive/NLP/RE_models', args={})
re_model = ClassificationModel('roberta', 'RE_models', use_cuda=False)
entities_dict = pickle.load( open( "entities_dict.p", "rb" ) )

#interest_var_dict={'movie_value':'movie'}
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

  if(triple[0] in constants.PERSON and 'award_' in triple[2]):
    return 'has_award'
  
  if(triple[0] not in constants.P and
    triple[0] not in constants.PERSON and
    triple[0] not in constants.MOVIE_SERIE and
    triple[0] not in constants.OTHERS ):
    return None
  if(triple[2] not in constants.P and
    triple[2] not in constants.PERSON and
    triple[2] not in constants.MOVIE_SERIE and
    triple[2] not in constants.OTHERS and
    triple[2] not in constants.GENRE_MAP ):
    return None

  for t in constants.TRIPLES_MOVIE:
      if(triple[2] == t[2]):
        return t[1]
  for t in constants.TRIPLES_PERSON:
      if(triple[2] == t[2]):
        return t[1]
  if(triple[0]=='genre' and 'genre_' in triple[2]):
    return 'has_value'

def extend_triples(tuples,entities,uris):
  print("Extending Triples")
  new_tuples=[]
  for triple in tuples:
    if(triple[2].startswith('genre_')):
      if(triple[0]!='genre'):
        new_tuples.append((triple[0],'has_genre','genre'))
      new_tuples.append(('genre','has_value',triple[2]))
    elif(triple[2].startswith('territory_')):
      if(triple[0]=='movie' or triple[0]=='series'):
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
              if(ent['uris'][0]=='movie' or ent['uris'][0]=='series'):
                print('entity is movie!')
                rel = get_relation([ent['uris'][0],'',triple[2]])
                #rel = get_relation([ent['uris'][0],'','movie'])
                #Bugfix questao 'Indicacoes do filme El Sistema Pelegrin'
                if(rel == None):
                  pass
                else:
                  new_tuples.append((ent['uris'][0],rel,triple[2]))
                for uri in ent['uris'][1]:
                  new_tuples.append([ent['uris'][0], 'has_value', uri])
                if(triple[2]=='releasedate'):
                  new_tuples.append(['movie', 'has_release_date', 'releasedate'])
              
              elif(ent['entity']=='person'):
                print('entity is person!')
                
                if(triple[2]=='award' or triple[2]=='nomination'):
                   rel = get_relation(['person','',triple[2]])
                   new_tuples.append(('person', rel, triple[2]))  
                   for uri in ent['uris']:
                    new_tuples.append(('person', 'has_value', uri[0]))  
                
                elif(triple[0] not in constants.PERSON ):
                  new_tuples.append((triple[0], 'has_person', 'person'))  
                  for uri in ent['uris']:
                    new_tuples.append(('person', 'has_value', uri[0]))  
                else:
                  for uri in ent['uris']:
                    #new_tuples.append((triple[0], 'has_value', uri[0]))
                    new_tuples.append(('person', 'has_value', uri[0]))
                  new_tuples.append(['person', 'has_value', triple[0]])

                if(triple[2]=='birthDate'):
                  new_tuples.append(('person', 'has_birth_date', 'birthDate'))
                
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
  #print(len(results["results"]["bindings"]))
  return results

def encode(results,rec_relations,entities):
  data=[]

  output = {
        "text": "Resultado(s) retornado(s):",
        "related": [],
        "relations":rec_relations,
        "results":[],
        "entities":entities,
        "suggestion_text": "",
        "success":True,
        "eval_options": True
    }
  
  if('boolean' in results[0]):
    output['results'] = {'boolean':[results[0]['boolean']]}
    return output

  my_dict={key:[] for key in results[0]['head']['vars']}

  cond = False
  for re in results:
    bindings = re['results']['bindings']
    for b in bindings:
      for name in b.keys():
        if(len(b[name])>0):
            cond=True
        if(b[name]['value'].startswith('http')):

          my_dict[name].append(get_rdfs_label(b[name]['value']))
          #data.append(get_rdfs_label(b[name]['value']))
        else:
          my_dict[name].append(b[name]['value'])
          #data.append(b[name]['value'])
  if(cond==False):
    output['text']='sem resultados encontrados.'
    output['results'] = my_dict
    return output
  output['results'] = my_dict
  print('output: ',output)
  return output

def is_domain(x,y,context):
  #print('is domain: ',str(x),str(y))
  
  if('person' == y and x in constants.PERSON_PROP):
    return False

  #bugfix person com award_... Cenario 3.3
  if(x in constants.PERSON and y == 'person'):
    return True

  if('person' == y and x in constants.PERSON_PROP):
    return False
  
  #bugfix: casos de genero
  if('genre_' in x and y in constants.MOVIE_SERIE):
    return True
  if(x in context.domain_dict):
    domains = context.domain_dict[x]
    if(y in domains):
      return True

    #tratar person
    if(x!='person'):
      if(x in constants.PERSON):
        return is_domain('person',y,context)
    if(y!='person'):
      if(y in constants.PERSON):
        return is_domain(x,'person',context)
  #tratar serie e movie
  if (x=='movie' or x == 'series') and (y=='movie' or y == 'series'):
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
        elif(t in constants.GENRE_MAP):
          correct_entity = constants.GENRE_MAP[t][0]
          new_triple.append(correct_entity)
          
        else:
            print("Error! Entidade n esta no dict!!")
            print(t)
            return relations
      else:
        new_triple.append(t)
    new_relations.append(new_triple)
      
  return new_relations

def add_relation(relations,interest_entity,ent):
    question_triple = [interest_entity['entity'],'',ent['entity']]
    print("relation triple: ",question_triple)
    rec = get_relation(question_triple)
    print(rec)
    
    if(rec!=None):
      #tratar award_..
      if('award_' in question_triple[2]):
        question_triple[2] = 'award'
        
      relations.append((question_triple[0],rec,question_triple[2]))
    return relations
  
def find_get_context_related(interest_entities,cont):
  print('find_get_context_related!!!')
  print(cont.history)
  relations=[]
  cond=True
  asked_entity=None
  hist_intent ='select' 

  #percorrer o historico invertido
  for hist in cont.history[::-1]:
    if(cond==False):
      break
    #pra cada entidade no historico
    for ent in hist[1]:
      #pra cada entidade nova de interesse
      for interest_entity in interest_entities:
        print(interest_entity['entity'],ent['entity'])
        #We have to exclude the entities that have
        #been asked before.
        #Ex: user ask award from movie. Now he ask the actors.
        #We have to exclude 'award' from the context, as
        #it does not interest us, and keep 'movie' only.
        print('hist: ',hist)
        #caso questao foi ask
        if(type(hist[0])==bool):
          asked_entity=''
        elif(type(hist[0])==dict):
          asked_entity=list(hist[0].keys())[0]
        elif('_value' in hist[0][0]): 
          asked_entity =hist[0][0][:-6] 
        else:
          asked_entity =hist[0][0]
        if('_value' in asked_entity): 
          asked_entity = asked_entity[:-6] 
        print('asked_entity: ',asked_entity)
        if is_domain(interest_entity['entity'],ent['entity'],cont):
          print('Is domain!!')
          if(type(hist[0])==bool):
            hist_intent = 'ask'
          #context_entities.append(ent['entity'])
          if(cond):#so pode receber relacoes 1 vez
            #retirar a relacao principal da questao
            #Ex: premios do filme avatar tem ((movie,'',award),(movie,'',Avatar))
            #comparamos com a interest var do historico eleito: 
            #retiramos ((movie,'',award))
            #print('history: ')
            #print(hist[0][0])
            
            #Adentrando na tupla de contexto e verificando
            for h in hist[2]:
              print('h: ',h)
              #trocar filmes por series
              #deve quebrar em perg complexa
              if((h[0]=='movie' or h[0]=='series') and (interest_entity['entity']=='movie' or interest_entity['entity']=='series')):
                relations.append((interest_entity['entity'],h[1],h[2]))
              #bugfix: 
              #h:  ('movie', 'has_genre', 'genre')
              #h:  ('genre', 'has_value', 'genre_fun')
              #onde a pergunta pede genre_logical_thrilling,
              #eliminando o  ('movie', 'has_genre', 'genre') 
              if('genre_' in interest_entity['entity']):
                if((h[0] =='movie' or h[0] =='series') and h[2]  =='genre'):
                  relations.append(h)
                if( 'genre_' not in h[0] and 'genre_' not in h[2]):
                  relations.append(h)
              else:
                #caso ask
                if asked_entity =='':
                    ents=[]
                    for enti in hist[1]:
                        ents.append(enti['entity'])
                    if h[2] in ents:
                        continue   

                if(h[0] != asked_entity and h[2] != asked_entity):
                  relations.append(h)
              

            cond=False
          
          #tratamento de erros
          if(interest_entity['entity']!=asked_entity):
            
            #bugfix: trocar filme por serie
            if((ent['entity']=='movie' or ent['entity']=='series') and (interest_entity['entity']=='movie' or interest_entity['entity']=='series')):
              pass
            else:  
              question_triple = [ent['entity'],'',interest_entity['entity']]
              print("relation triple: ",question_triple)
              
              #bugfix: questao 'filme de genero X', e 'e genero Y?' 
              if(('movie' == question_triple[0] or 'series' == question_triple[0]) 
                  and ('genre_' in question_triple[2]) ):
                question_triple[0]='genre'              
            
              rec = get_relation(question_triple)

              if('person' == question_triple[0] and question_triple[2] in constants.PERSON):
                rec= 'has_value'
              print(rec)
              if(rec!=None):
                relations.append((question_triple[0],rec,question_triple[2]))
        
        elif(is_domain(ent['entity'],interest_entity['entity'],cont)):
          print('Is counter domain!!')
          if(type(hist[0])==bool):
            hist_intent = 'ask'

          if(cond):

            for h in hist[2]:
              #bug questao: Premio de cameron diaz -> E Angelina joulie?
              #estou jogando fora as pessoas do historico em questao
              if(interest_entity['entity']=='person'):
                if(h[0]=='person' and h[1] == 'has_value'):
                    continue
                else:
                    relations.append(h)

              print('h: ',h)
              if(h[0] != asked_entity and h[2] != asked_entity):
                relations.append(h)
            cond=False
          if(ent['entity']!=asked_entity):
            relations=add_relation(relations,interest_entity,ent)

          #bug questao: Premio de cameron diaz -> E Angelina joulie?
          if(interest_entity['entity']=='person'):
            for uri in interest_entity['uris']:
                relations.append(('person','has_value',uri[0]))
            return relations
            #relations=add_relation(relations,interest_entity,ent)


  return relations,hist_intent

def get_context_related(hist,interest_entities,cont):
  print('get_context_related!!!')
  print(cont.history)
  relations=[]
  cond=True

  for ent in hist[1]:
    for interest_entity in interest_entities:
      print(interest_entity['entity'],ent['entity'])
      if('_value' in hist[0][0]): 
        asked_entity =hist[0][0][:-6] 
      else:
        asked_entity =hist[0][0]
      print('asked_entity: ',asked_entity)
      if is_domain(interest_entity['entity'],ent['entity'],cont):
        print('Is domain!!')
        if(cond):#so pode receber relacoes 1 vez
          for h in hist[2]:
            print('h: ',h)
            #eliminando o  ('movie', 'has_genre', 'genre') 
            if('genre_' in interest_entity['entity']):
              if(h[0] =='movie' and h[2]  =='genre'):
                relations.append(h)
              if( 'genre_' not in h[0] and 'genre_' not in h[2]):
                relations.append(h)
            else:
              if(h[0] != asked_entity and h[2] != asked_entity):
                relations.append(h)

          cond=False
        if(interest_entity['entity']!=asked_entity):
          question_triple = [ent['entity'],'',interest_entity['entity']]
          print("relation triple: ",question_triple)
          
          #bugfix: questao 'filme de genero X', e 'e genero Y?' 
          if(('movie' == question_triple[0]) and ('genre_' in question_triple[2]) ):
            question_triple[0]='genre'              
          
          
          rec = get_relation(question_triple)
          relations.append((question_triple[0],rec,question_triple[2]))
      
      elif(is_domain(ent['entity'],interest_entity['entity'],cont)):
        print('Is counter domain!!')
        if(cond):
          for h in hist[2]:
            print('h: ',h)
            if(h[0] != asked_entity and h[2] != asked_entity):
              relations.append(h)
          cond=False
        if(ent['entity']!=asked_entity):
          question_triple = [interest_entity['entity'],'',ent['entity']]
          print("relation triple: ",question_triple)
          rec = get_relation(question_triple)
          relations.append((question_triple[0],rec,question_triple[2]))
  return relations

def check_ref(s):
  if '[QUOTED_TEXT]' in s:
    return 'explicit_ref'
  return None

import os
import copy
from rasa.nlu.model import Interpreter,Metadata
interpreter = Interpreter.load('models/')
cont = context.Context()

def get_output():
  output = {
        "text": "Resultados não encontrados. Tente reformular sua pergunta.",
        "related": [],
        "relations":[],
        "results":[],
        "entities":[],
        "suggestion_text": "",
        "success":False,
        "eval_options": False
        }
  return output


def search(text='',id_client='0',id_hist='0',clean_context=False,save_context_in_context=False,load_context=True):
  cont = context.Context()  

  #limpar contexto
  if(clean_context):
    if os.path.exists('contexts/'+id_client+'_'+id_hist+'.p'):
      os.remove('contexts/'+id_client+'_'+id_hist+'.p')
    else:
      print("The file ",id_client+'_'+id_hist+'.p'," does not exist") 
  #load context
  if(load_context):
    if(os.path.isfile('contexts/'+id_client+'_'+id_hist+'.p')):
      print('Context Loaded!')
      print('User: ',id_client)
      print('Historic: ',id_hist)
      cont = pickle.load(open('contexts/'+id_client+'_'+id_hist+'.p','rb'))
    else:
      print("No context found")

  old_text = copy.deepcopy(text)
  text=clean_word(text)
  intent=check_ref(old_text)

  if(intent == 'explicit_ref'):
    print('#########Intent: Explicit ref')
    s1,s2= old_text.split('[QUOTED_TEXT]')
    s1,s2=clean_word(s1),clean_word(s2)

    print('searching for ',s1,' in explicit ref.')
    print(cont.history)
    hist=cont.find_context(s1)
    print('found: ',str(hist))

    entities_rasa = interpreter.parse(s2)
    print('Raw Entities:')
    pprint(entities_rasa)
    entities,do_sugestion,sugestions=especify_entities(entities_rasa['entities'])
    if(do_sugestion):
      output = get_output()
      output['results'] = sugestions
      output['related'] = sugestions
      output['text']='Resultados não encontrados. Você quis dizer: '
      output["success"]=False
      output["entities"]=entities
      print('returning suggestions (1)...')
      return output
      
    print('Corrected Entities:')
    pprint(entities)

    interest_entities=entities
    relations_tuples = get_context_related(hist,interest_entities,cont)
    relations_tuples = remove_duplicated_relations(relations_tuples)
    print('infered relations:',relations_tuples)
  
  else:
    entities_rasa = interpreter.parse(text)
    print('Raw Entities:')
    pprint(entities_rasa)

    intent = entities_rasa['intent']['name']
    print('intent: ',intent)
    if(intent =='property_by_movie_series'):
      intent = 'select'
    if(intent =='movies_affirmative_simple'):
      intent = 'ask'

    entities,do_sugestion,sugestions=especify_entities(entities_rasa['entities'])
    if(do_sugestion):
      output = get_output()
      output['results'] = {"sugestões": sugestions}
      output['related'] = sugestions
      output['text']='Resultados não encontrados. Você quis dizer: '
      output["success"]=False
      output["entities"]=entities
      print('returning suggestions (2)...')
      return output
    print('Corrected Entities:')
    pprint(entities)
    if(len(entities)==1):
      intent='context'

  #tratar intencao de contexto
  if(intent=='context'):
    print('#########Intent: Context')

    hist_intent='select'
    
    relations=[]
    interest_entities = entities
    print('interest_entity: ',interest_entities)
    #no contexto simples, todas as entidades recebidas
    #sao as de interesse.
    ref=cont.search_for_numbers(text)
    print(ref)
    if(ref==-1):
      relations_tuples,hist_intent = find_get_context_related(interest_entities,cont)
      relations_tuples = remove_duplicated_relations(relations_tuples)
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
                if(type(hist[0])==bool):
                    hist_intent = 'ask'
                #print(hist[0]) 
                interest_var=hist[0][0]
                #print(hist[3]['results']) 
                results=hist[3]['results'][interest_var]
                context_interest_var = interest_var
                relations.append([context_interest_var,'',results[ref]])
                relations.append([context_interest_var,'',interest_entity['entity']])
                print('relations: ',relations)
                cond=False

                raw_relations_tuples = copy.deepcopy(relations)
                relations_tuples =extend_triples(relations,entities,[])
                relations_tuples = remove_duplicated_relations(relations_tuples)
                print('tuples after: ',relations_tuples)
                relations_tuples_copy = copy.deepcopy(relations_tuples)
  
  if(intent=='context' or intent == 'explicit_ref' ):
    rec_relations = relation_recommendation(relations_tuples)
    print('rec_relations:',rec_relations)
    
    sparql_query,interest_var = sparql_build(relations_tuples,spql_type=hist_intent)
    print(sparql_query,interest_var)

    try:
      p = multiprocessing.Process(target=run_sparql, name="Foo", args=(sparql_query,))
      p.start()

      p.join(8)
      # If thread is active
      if p.is_alive():
          print("foo is running... let's kill it...")

          # Terminate foo
          p.terminate()
          p.join()
          a=2/0

      results = run_sparql(sparql_query)
    
      data= encode([results],rec_relations,entities)
      
      if('head' in results):
        if('vars'in results):
          res=results['head']['vars']
          res = list(res.keys())
      if 'boolean' in results:
        res = results['boolean']
      else:
        res = data['results']
        res = list(res.keys())

      #print('res:',res)
      if(save_context_in_context):
        cont.set_current_turn_results(text,data,entities_rasa['intent']['name'],entities,relations_tuples,res)
        pickle.dump(cont,open('contexts/'+id_client+'_'+id_hist+'.p','wb'))
      print('returning data: ')
      print(data)
      return data
    except Exception:
      traceback.print_exc()
      print('returning empty..')
      output = get_output()
      return output

  #queries = get_relations_queries(entities_rasa)
  queries = get_relations_queries2(entities_rasa['text'],entities)
  print(queries)
  
  pred_relations=relation_extraction(queries)
  print(pred_relations)
  
  relations_tuples,uris=construct_tuples(pred_relations,entities)
  print('tuples before: ',relations_tuples)
  
  raw_relations_tuples = copy.deepcopy(relations_tuples)

  relations_tuples =extend_triples(relations_tuples,entities,uris)
  relations_tuples = remove_duplicated_relations(relations_tuples)
  print('tuples after: ',relations_tuples)
  relations_tuples_copy = copy.deepcopy(relations_tuples)

  rec_relations = relation_recommendation(relations_tuples)
  print('Relations for recommendation:',rec_relations)
  
  sparql_query,interest_var = sparql_build(relations_tuples,spql_type=intent)
  print(sparql_query,interest_var)
  #return entities_rasa['intent']['name'],entities,relations_tuples,interest_var
  
  try:
    # Start foo as a process
    p = multiprocessing.Process(target=run_sparql, name="Foo", args=(sparql_query,))
    p.start()

    p.join(8)
    # If thread is active
    if p.is_alive():
        print ("foo is running... let's kill it...")
        # Terminate foo
        p.terminate()
        p.join()
        a=2/0

    results = run_sparql(sparql_query)
    #print('results: ',results)
    if(len(results)==0):
        a=2/0
    data= encode([results],rec_relations,entities)
    if('head' in results):
      if('vars'in results):
        res=results['head']['vars']
        res = list(res.keys())
    if 'boolean' in results:
      res = results['boolean']
    else:
      res = data['results']
      res = list(res.keys())
    cont.set_current_turn_results(text,data,entities_rasa['intent']['name'],entities,relations_tuples,res)
    pickle.dump(cont,open('contexts/'+id_client+'_'+id_hist+'.p','wb'))
    print('returning data: ')
    print(data)
    return data
  except Exception:
    traceback.print_exc()
    print('returning empty..')
    output = get_output()
    return output
    
#funciona
#text= 'premios do avatar'

#text = 'atores que foram indicados ao oscar'
#text = 'me diga a premiacao da atriz Angelina Jolie'
#text = 'Me diga filmes da Angelina Jolie'
#filtrar atriz
#text = 'Me diga filmes da atriz Angelina Jolie'
#text = 'filmes que ganharam o oscar'
#text = 'Indicações do filme El Sistema Pelegrin'
#text='O filme The Vampire obteve que premiação?'
#text = 'O Ator Geraldo Rivera do filme Volver ganhou o que.'

#bugs
#text='estreia de Avatar?' #context
#text='data de nascimento da Angeline Joulie?'


#text='quais as atrizes e atores de Avatar'
#results = search(text)
#print(results)


#text='seria Angelina Jolie uma atriz?'
#results = search(text)
#print(results)


#Cenario 6.1: ASK
"""
text='seria do genero diversao o filme Avatar?'
results = search(text)
print(results)

text='seria Angelina Jolie uma atriz?'
results = search(text)
print(results)

text='Angelina Jolie venceu algum oscar??'
results = search(text)
print(results)

text='seria Avatar um filme?'
results = search(text)
print(results)

text='quais seus atores?'
results = search(text)
print(results)

text='suas atrizes?'
results = search(text)
print(results)
"""

"""
text='voce poderia me dizer a data de nascimento da Angelina Jolie?'
results = search(text)
print(results)

text='em quais filmes ela atuou?'
results = search(text)
print(results)

text='qual o gênero desse Foxfire?'
results = search(text)
print(results)

text='quais premios ele ganhou?'
results = search(text)
print(results)
"""

"""
text='data de nascimento da Angelina Jolie?'
results = search(text)
print(results)

text='genero de Avatar?'
results = search(text)
print(results)

text='atores?'
results = search(text)
print(results)
"""

"""
text='me diga os filmes de Ação?'
results = search(text)
print(results)

text='e series?'
results = search(text)
print(results)
"""
"""
text='premios de Avatar'
results = search(text)
print(results)
"""
#Cenario 5.1: Corrector
"""
text='premios da Angeline Joulie?'
results = search(text)
print(results)
"""

"""
#Cenario 4.1: Referencia explicita
text='Quais os atores de Avatar?'
results = search(text)
print(results)

text='Quais os atores de Avatar?[QUOTED_TEXT]E suas atrizes?'
results = search(text)
print(results)
"""

"""
#Cenario 1.1: Data properties
text='qual a data de nascimento de Angelina Jolie'
results = search(text)
print(results)
text='qual o orcamento de Avatar'
results = search(text)
print(results)
text='qual a receita de Avatar'
results = search(text)
print(results)
text='qual a nota de Avatar'
results = search(text)
print(results)
text='qual a estreia de Avatar'
results = search(text)
print(results)
text='qual a duração de Avatar'
results = search(text)
print(results)
"""


#text = 'me diga a premiacao do Geraldo Rivera'

#text = 'Me mande filmes de crime'
#text= 'quais os filmes do genero diversão'
#text='atrizes de avatar'

#Intent:: ask
#text = 'Seria Angelina Jolie uma atriz'
#text = 'Seria do genero diversão esse filme avatar?'

"""
#Cenario 3.1: Contexto 
text= 'Filmes de comédia.'
results = search(text)
#print(results)

text= 'e de violencia.'
results = search(text)
print(results)

text= 'me mostre de ação.'
results = search(text)
print(results) 

text= 'e tambem de fantasia.'
results = search(text)
print(results) 

"""

"""
#Cenario 3.3: Contexto

text = 'atores que ganharam o oscar'

results = search(text)
print(results)

text = 'atrizes'
results = search(text)
print(results)

text = 'diretores'
results = search(text)
print(results)

text = 'editores'
results = search(text)
print(results)
"""

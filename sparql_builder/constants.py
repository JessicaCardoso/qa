from operator import itemgetter
from copy import deepcopy

from .constants import (
    ONTOLOGY_CLASS,
    OBJ_PROPERTIES,
    DATA_PROPERTIES,
    GENRE_MAP,
    DATA_PROPERTIES_RANGE_MAP,
    OPERATOR_MAP,
    NER_ENTITIES_MAP,
    VALUES_TO,
    FILTER_BY,
    SELECT_SKELETON,
    ASK_SKELETON,
    TRIPLES,
    PERSON
)


def genre_to_respective_uri(question_triples, current_triple, curr):
  first, middle, _ = current_triple
  uri, rest = GENRE_MAP[curr]
  question_triples.append((first, middle, uri))
  for value in rest:
    genre_to_respective_uri(question_triples, current_triple, value)

def build_continent_sparql(first, last):
  sparql = ""
  sparql += f"?{first} a ?temp_{first}_ref. "
  first = f"temp_{first}_ref"
  if last == "territory_africa":
    sparql += VALUES_TO.format(first,
                               """<http://www.movieontology.org/2009/10/01/movieontology.owl#Eastern_Africa>
                               <http://www.movieontology.org/2009/10/01/movieontology.owl#Middle_Africa>
                               <http://www.movieontology.org/2009/10/01/movieontology.owl#Northern_Africa>
                               <http://www.movieontology.org/2009/10/01/movieontology.owl#Southern_Africa>
                               <http://www.movieontology.org/2009/10/01/movieontology.owl#Western_Africa>
                               """)
  elif last == "territory_america":
    sparql += VALUES_TO.format(first,
                               """<http://www.movieontology.org/2009/10/01/movieontology.owl#Caribbean>
                               <http://www.movieontology.org/2009/10/01/movieontology.owl#Central_America>
                               <http://www.movieontology.org/2009/10/01/movieontology.owl#South_America>
                               <http://www.movieontology.org/2009/10/01/movieontology.owl#Northern_America>
                               """)
  elif last == "territory_latin_america":
    sparql += VALUES_TO.format(first,
                               """<http://www.movieontology.org/2009/10/01/movieontology.owl#Central_America>
                               <http://www.movieontology.org/2009/10/01/movieontology.owl#South_America>
                               """)
  elif last == "territory_asia":
    sparql += VALUES_TO.format(first,
                               """<http://www.movieontology.org/2009/10/01/movieontology.owl#Central_Asia>
                               <http://www.movieontology.org/2009/10/01/movieontology.owl#Eastern_Asia>
                               <http://www.movieontology.org/2009/10/01/movieontology.owl#Southeastern_Asia>
                               <http://www.movieontology.org/2009/10/01/movieontology.owl#Southern_Asia>
                               <http://www.movieontology.org/2009/10/01/movieontology.owl#Western_Asia>
                               """)
  elif last == "territory_europe":
    sparql += VALUES_TO.format(first,
                               """<http://www.movieontology.org/2009/10/01/movieontology.owl#Eastern_Europe>
                               <http://www.movieontology.org/2009/10/01/movieontology.owl#Northern_Europe>
                               <http://www.movieontology.org/2009/10/01/movieontology.owl#Southern_Europe>
                               <http://www.movieontology.org/2009/10/01/movieontology.owl#Western_Europe>
                               """)
  elif last == "territory_oceania":
    sparql += VALUES_TO.format(first,
                               """<http://www.movieontology.org/2009/10/01/movieontology.owl#Australia_and_New_Zealand>
                               <http://www.movieontology.org/2009/10/01/movieontology.owl#Melanesia>
                               <http://www.movieontology.org/2009/10/01/movieontology.owl#Micronesia>
                               <http://www.movieontology.org/2009/10/01/movieontology.owl#Polynesia>
                               """)

  return sparql

def part1(triples):
  question_triples_filtered = []
  for first, middle, last in triples:
    if last in GENRE_MAP:
      current_triple = first, middle, last
      genre_to_respective_uri(question_triples_filtered, current_triple, last)
    else:
      question_triples_filtered.append((first, middle, last))
  return question_triples_filtered
  

def part3(question_triples, variables = None, sep="\n"):
  if variables == None:
    variables = {}
  sparql_body = []
  question_triples.sort(key=itemgetter(0, 1))
  question_triples_filtered = []
  values_temp = {}

  for first, middle, last in question_triples:
    if last.startswith("http"):
      if first in values_temp:
        values_temp[first].append(f"<{last}>")
      else:
        values_temp[first] = [f"<{last}>"]
    else:
      question_triples_filtered.append((first, middle, last))

  for key, value in values_temp.items():
    sparql_body.append(VALUES_TO.format(key, " ".join(value)))
    variables[key] = False
    # diff
    class_key = NER_ENTITIES_MAP[key]
    #bugfix
    if class_key != "Genre" : 
      sparql_body.append(ONTOLOGY_CLASS[class_key].format(f"?{key}"))
  
  for first, middle, last in question_triples_filtered:
    first_var = f"?{first}"
    class_key = None
    if first in NER_ENTITIES_MAP:
      class_key = NER_ENTITIES_MAP[first]
    elif "territory" in last:
      variables[first] = False
      if (last == "territory_africa" or last == "territory_america" or
          last == "territory_asia" or last == "territory_europe" or 
          last == "territory_oceania" or last == "territory_latin_america" 
          ):
        sparql_body.append((build_continent_sparql(first, last)))
      else:
        class_key = NER_ENTITIES_MAP[last]

    if class_key and class_key in ONTOLOGY_CLASS:
      sparql_body.append(ONTOLOGY_CLASS[class_key].format(f"?{first}"))

      if first not in variables:
        variables[first] = True

      if middle in NER_ENTITIES_MAP:
        prop = NER_ENTITIES_MAP[middle]
        last_var = f"?{last}"
        if prop in OBJ_PROPERTIES:
          sparql_body.append(OBJ_PROPERTIES[prop].format(first_var, last_var))
        elif prop in DATA_PROPERTIES:
          sparql_body.append(DATA_PROPERTIES[prop].format(first_var, last_var))
        if last not in variables:
          variables[last] = True

  sparql_body = sep.join(set(sparql_body))
  return sparql_body


def part2(question_triples, variables = None, sep="\n"):
  if variables == None:
    variables = {}

  question_triples_filtered = []
  values_temp = {}
  indices = {}

  # Trocar between por greater_than e less_than
  question_triples2 = []
  temp = {}
  for first, middle, last in question_triples:
    if last == "between":
      temp[first] = True
      question_triples2.append((first, middle, "greater_than"))
    else:
      question_triples2.append((first, middle, last))
      if first in temp and temp[first]:
        temp[first] = False
        question_triples2.append((first, "has_relation_operator", "less_than"))     
      
  for first, middle, last in question_triples2:
    if middle is not "has_literal_value" and middle is not "has_relation_operator":
       question_triples_filtered.append((first, middle, last))
    else:
      variables[first] = False
      if first not in values_temp:
        values_temp[first] = []
        indices[first] = 0
        if middle is "has_relation_operator":
          values_temp[first].append({"operator": last})
        else:
          values_temp[first].append({"value": last})
      else:
        if middle is "has_relation_operator":
          if "operator" not in values_temp[first][indices[first]]:
            values_temp[first][indices[first]]["operator"] =  last
          else:
            indices[first] += 1
            values_temp[first].append({"operator": last})   
        else:
          if "value" not in values_temp[first][indices[first]]:
            values_temp[first][indices[first]]["value"] =  last
          else:
            indices[first] += 1
            values_temp[first].append({"value": last})

  sparql_body = []
  for key, items in values_temp.items():
    prop = DATA_PROPERTIES_RANGE_MAP[key]
    for it in items:
      value = it['value']
      if prop.endswith("#int") or prop.endswith("#double"):
        if "operator" in it: 
          if it['operator'] in OPERATOR_MAP:
            operator = OPERATOR_MAP[it['operator']]
        else:
          operator = OPERATOR_MAP['equal_to']
        
        sparql_body.append(FILTER_BY.format(f"?{key} {operator} {value}"))
      elif prop.endswith("#string"):
        sparql_body.append(FILTER_BY.format(f"contains(lcase(?{key}), lcase('{value}'))"))
      elif prop.endswith("#dateTime"):
        if "operator" in it: 
          if it['operator'] in OPERATOR_MAP:
            operator = OPERATOR_MAP[it['operator']]
        else:
          operator = OPERATOR_MAP['equal_to']
        sparql_body.append(FILTER_BY.format(f"<http://www.w3.org/2001/XMLSchema#date>(?indicationDate) {operator} '{value}'^^<http://www.w3.org/2001/XMLSchema#date>"
))
        
  sparql_body = sep.join(sparql_body)
  return question_triples_filtered, sparql_body


def sparql_label_body(variables, sep):
  data_properties_values = {
      "movie": "title",
      "series": "title",
      "person": "birthName",
      "actor": "birthName",
      "actress": "birthName",
      "director": "birthName",
      "writer": "birthName",
      "editor": "birthName",
      "costume_designer": "birthName",
      "producer": "birthName",
      "company": "companyName"
  }

  variables2 = deepcopy(variables)
  ontology_labels = ["genre", "award", "nomination", "territory"]
  unknown = []
  label_body = []
  for key, value in variables.items():
    if value:
      if key in data_properties_values:
        variables2[key] = False
        variables2[f"{key}_value"] = True
        label_body.append(DATA_PROPERTIES[data_properties_values[key]].format(f"?{key}", f"?{key}_value"))
      elif key in ontology_labels:
        unknown.append(key)
  return variables2, sep.join(label_body), unknown

def sparql_build(question_triples, sep="\n", spql_type="select"):
  variables = {}
  #question_triples = preprocess(question_triples)
  question_triples = part1(question_triples)
  question_triples, sparql_body = part2(question_triples,variables, sep=sep)
  sparql = part3(question_triples,variables, sep=sep)
  variables, sparql_body_label, unknown = sparql_label_body(variables, sep=sep)
  sparql_body = sep.join([sparql, sparql_body, sparql_body_label])
  if spql_type == "select":
    variables = [f"?{var_name}" for var_name, value in variables.items() if value]
    variables = " ".join(variables)
    sparql_query = SELECT_SKELETON.format(variables, sparql_body)
  else:
    sparql_query = ASK_SKELETON.format(sparql_body)
  return sparql_query, unknown 


def get_relation(first, last):
  for triple in TRIPLES:
    if triple[0] == "person" and first in PERSON:
      if last == triple[2]:
        return triple[1]
    elif first == triple[0]:
      if last == triple[2]:
        return triple[1]
  return "has_value"


def preprocess(question_triples):
  question_triples_2 = []
  for first, _, last in question_triples:
     if last.startswith("http") or last.startswith("genre_"):
       middle = "has_value"
     else:
       middle = get_relation(first, last)
     question_triples_2.append((first, middle, last))
  return question_triples_2

import pickle
import difflib

model = pickle.load(open('corrector/corrector_prop_model.b','rb'))
inv_areas = pickle.load(open('corrector/inv_areas.b','rb'))
count_vect = pickle.load(open('corrector/count_vect.b','rb'))
entities_dict = pickle.load(open('entities_dict.p','rb'))

movie_data = pickle.load(open('pandas_data/movies_df.dat','rb'))
people_data = pickle.load(open('pandas_data/person_df.dat','rb'))
print("Corrector data loaded!!!")

def get_suggestion_property(text):
  x = count_vect.transform(text)
  pred = model.predict(x)
  print(model.decision_function(x))
  print(pred)
  score = model.decision_function(x)[0][pred[0]]
  print('corretor confidence: ',score)
  area = inv_areas[pred[0]]
  a=entities_dict[area[0]]
  print("corrector prediction: ",a)
  return a

def filter_results(res):
  f_res={}
  for i in range(len(res)):
    f_res[res[i]]=1
  return f_res.keys()

def get_correct_title(text):
  titles =[]
  bindings = movie_data['results']['bindings']
  for b in bindings:
    title = b['title']['value']
    titles.append(title)
  titles_results = difflib.get_close_matches(text, titles,n=4,cutoff=0.7)
  return filter_results(titles_results)

def get_correct_people_name(text):
  names =[]
  bindings = people_data['results']['bindings']
  for b in bindings:
    name = b['birthName']['value']
    if ',' in name:
      n = name.split(',')
      name = n[1][1:]+' '+n[0]
    names.append(name)
  names_results = difflib.get_close_matches(text, names,n=4,cutoff=0.7)
  return filter_results(names_results)


 
#s=get_suggestion_property(['prmio'])
#s=get_correct_people_name('Angeline Jouli')
#s=get_correct_title('Avtar')
#print(s)
#a=2/0


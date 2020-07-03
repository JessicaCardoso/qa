import pickle
class Context():
    def __init__(self):
        self.history = []
        self.prop_by_movie_history = []
        self.turn = -1
        self.words = {'primeiro':1,'segundo':2,'terceiro':3,'quarto':4,'quinto':5,'sexto':6,'setimo':7,'oitavo':8,'nono':9,'decimo':10}
        #self.history_index ={'movie_value':'search'}
        self.domain_dict = {'actor': ['series', 'movie'],
                        'actress': ['movie', 'series'],
                        'award': ['person', 'movie', 'series'],
                        'nomination': ['person', 'movie', 'series'],
                        'certification': ['movie', 'series'],
                        'colorinfo': ['series', 'movie'],
                        'companycountry': ['territory'],
                        'consumable_product': ['series', 'movie'],
                        'costume_designer': ['series', 'movie'],
                        'editor': ['movie', 'series'],
                        'director': ['movie', 'series'],
                        'genre': ['movie', 'series'],
                        'language': ['movie', 'series'],
                        'location_company': ['movie'],
                        'movie': ['sound_mix'],
                        'musical_artist': ['movie', 'series'],
                        'person': ['movie'],
                        'place': ['movie'],
                        'production_company': ['location_company', 'territory'],
                        'sound_mix': ['series', 'movie'],
                        'territory': ['company_country'],
                        'tvseries': ['sound_mix'],
                        'writer': ['series', 'movie'],
                        'imdbrating': ['series', 'movie'],
                        'releasedate': ['series', 'movie'],
                        'runtime': ['series', 'movie'],
                        'budget': ['series', 'movie'],
                        'gross': ['series', 'movie'],
                        'birthDate':['person']

                        }


    def set_current_turn_results(self,text,data_results,intent,entities,relations,interest_var):
        print("Set in Context")
        self.turn+=1
        
        #A interest var nao consegue decidir as entidades
        #que devemos eliminar.
        #Em 'Atores de filme X' e 'filmes de genero y'
        #devemos considerar a entidade buscada pelo usuario
        #ex: pro caso 2 poderia ser 'e de genero z' ou
        #'series agora'. Devemos tratar isso em
        #get_context_related
        #retirado data results
        self.history.append((interest_var,entities,relations,text,intent))
        

        """
        #A interest var deve ser todas as entidades que
        #NAO foram definidas com valores. 
        #Em atores de avatar, seria "atores".
        #Assim, o contexto leva os fatos que conhecemos
        #para as proximas perguntas.
        
        print('relations:',relations)
        tuples_dict={}
        know_ents =[]
        for re in relations:
            if(re[1]=='has_value'):
              tuples_dict[re[0]]=1
            else:
              if(re[0] not in tuples_dict):
                tuples_dict[re[0]]=0
              if(re[2] not in tuples_dict):
                tuples_dict[re[2]]=0
        for t in tuples_dict.keys():
            if(tuples_dict[t]==0):
              know_ents.append(t)
        print('know entities: ',know_ents)

        self.history.append((know_ents,entities,relations,data_results))
        """

        print("History: ")
        print(self.history[self.turn])


    def search_for_numbers(self,text):
        ref_number = -1
        #Case1
        #check if there is a number
        #para casos como: atores desse primeiro...genero desse 2...
        nums = [int(s) for s in text.split() if s.isdigit()]
        if(len(nums)>0):
            ref_number = nums[0]
        else:
            for word in self.words.keys():
                if word in text.split():
                    ref_number = self.words[word]
        return ref_number

    def find_context(self,text):
      for hist in self.history:
        print('comparing: ',str(hist[3]),' with ',str(text))
        if(hist[3]==text):
          return hist
      return None
      


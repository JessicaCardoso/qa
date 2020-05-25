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
                        'certification': ['movie', 'series'],
                        'colorinfo': ['series', 'movie'],
                        'companycountry': ['territory'],
                        'consumable_product': ['series', 'movie'],
                        'costume_designer': ['series', 'movie'],
                        'editor': ['movie', 'series'],
                        'film_director': ['movie', 'series'],
                        'genre': ['movie', 'series'],
                        'language': ['movie', 'series'],
                        'location_company': ['movie'],
                        'movie': ['sound_mix'],
                        'musical_artist': ['movie', 'series'],
                        'person': ['award'],
                        'place': ['movie'],
                        'production_company': ['location_company', 'territory'],
                        'sound_mix': ['series', 'movie'],
                        'territory': ['company_country'],
                        'tvseries': ['sound_mix'],
                        'writer': ['series', 'movie']}

	def set_current_turn_results(self,text,data_results,intent,entities,relations,interest_var):
		self.turn+=1

		#'atores desse primeiro'
		#ou originalmente: Os atores de Avatar
		#if(intent=='context'):
		#	pass

		#if(intent=='property_by_movie_series'):
		self.history.append((interest_var,entities,relations,data_results))
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

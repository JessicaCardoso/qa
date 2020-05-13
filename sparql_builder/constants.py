SELECT_SKELETON = "SELECT DISTINCT {} WHERE {{{}}}"
ASK_SKELETON = "ASK WHERE {{ {} }}"
VALUES_TO = "VALUES ?{}{{{}}}. "
COUNT = "COUNT({})"
FILTER_BY = "FILTER({}). "

OBJ_PROPERTIES ={
    "belongsToGenre": ("{0} <http://www.movieontology.org/2009/10/01/movieontology.owl#belongsToGenre> ?temp_genre_uri. "
                       "?temp_genre_uri a {1}. {1} a <http://www.w3.org/2002/07/owl#Class>. "),
    "hasActress": "{} <http://www.movieontology.org/2009/10/01/movieontology.owl#hasActress> {}. ",
    "hasMaleActor": "{} <http://www.movieontology.org/2009/10/01/movieontology.owl#hasMaleActor> {}. ",
    "hasCompanyLocation": "{} <http://www.movieontology.org/2009/11/09/movieontology.owl#hasCompanyLocation> {}. ",
    "hasCostumeDesigner": "{} <http://www.movieontology.org/2009/10/01/movieontology.owl#hasCostumeDesigner> {}. ",
    "hasDirector": "{} <http://www.movieontology.org/2009/10/01/movieontology.owl#hasDirector> {}. ",
    "hasEditor": "{} <http://www.movieontology.org/2009/10/01/movieontology.owl#hasEditor> {}. ",
    "hasFilmLocation": "{} <http://www.movieontology.org/2009/10/01/movieontology.owl#hasFilmLocation> {}. ",
    "hasProducer": "{} <http://www.movieontology.org/2009/10/01/movieontology.owl#hasProducer> {}. ",
    "isAwardedWith": "{} <http://www.movieontology.org/2009/10/01/movieontology.owl#isAwardedWith> {}. ",
    "isAwardOf": "{} <http://www.movieontology.org/2009/11/09/movieontology.owl#isAwardOf> {}. ",
    "isCostumeDesignerIn": "{} <http://www.movieontology.org/2009/10/01/movieontology.owl#isCostumeDesignerIn> {}. ",
    "isProducedBy": "{} <http://www.movieontology.org/2009/10/01/movieontology.owl#isProducedBy> {}. ",
    "nominatedFor": "{} <http://www.movieontology.org/2009/10/01/movieontology.owl#nominatedFor> {}. ",
    "writtenBy": "{} <http://www.movieontology.org/2009/11/09/movieontology.owl#writtenBy> {}. ",
    "wrote": "{} <http://www.movieontology.org/2009/11/09/movieontology.owl#wrote> {}. ",
    # specials
    "hasActor": "{} ?has_actor {}. FILTER(?has_actor IN (<http://www.movieontology.org/2009/10/01/movieontology.owl#hasActress>, <http://www.movieontology.org/2009/10/01/movieontology.owl#hasMaleActor>))."
}

DATA_PROPERTIES={
    "productionStartYear": "{} <http://dbpedia.org/ontology/productionStartYear> {}. ",
    "birthDate": "{} <http://dbpedia.org/ontology/birthDate> {}. ",
    "birthName": "{} <http://dbpedia.org/ontology/birthName> {}. ",
    "budget": "{} <http://dbpedia.org/ontology/budget> {}. ",
    "companyName": "{} <http://www.movieontology.org/2009/11/09/movieontology.owl#companyName> {}. ",
    "gross": "{} <http://dbpedia.org/ontology/gross> {}. ",
    "imdbrating": "{} <http://www.movieontology.org/2009/10/01/movieontology.owl#imdbrating> {}. ",
    "indicationDate": "{} <http://www.movieontology.org/2009/11/09/movieontology.owl#indicationDate> {}. ",
    "releasedate": "{} <http://www.movieontology.org/2009/10/01/movieontology.owl#releasedate> {}. ",
    "runtime": "{} <http://www.movieontology.org/2009/10/01/movieontology.owl#runtime> {}. ",
    "title": "{} <http://www.movieontology.org/2009/10/01/movieontology.owl#title> {}. ",
    "rdfs:label": "{} <http://www.w3.org/2000/01/rdf-schema#label> {}. "
}

ONTOLOGY_CLASS = {
    "Award": "{} a <http://www.movieontology.org/2009/10/01/movieontology.owl#Award>. ",
    "Person": "{} a ?person_classes. FILTER (?person_classes IN (<http://www.movieontology.org/2009/11/09/movieontology.owl#Actress>, <http://www.movieontology.org/2009/10/01/movieontology.owl#Costume_Designer>, <http://dbpedia.org/ontology/Actor>, <http://dbpedia.org/ontology/Musical_Artist>, <http://dbpedia.org/ontology/Writer>, <http://www.movieontology.org/2009/10/01/movieontology.owl#Editor>, <http://dbpedia.org/page/Film_Director>, <http://www.movieontology.org/2009/10/01/movieontology.owl#Producer>)).",
    # subclasses de pessoas
    "Actress": "{} a <http://www.movieontology.org/2009/11/09/movieontology.owl#Actress>. ",
    "Costume_Designer": "{} a <http://www.movieontology.org/2009/10/01/movieontology.owl#Costume_Designer>. ",
    "Actor": "{} a <http://dbpedia.org/ontology/Actor>. ",
    "Writer": "{} a <http://dbpedia.org/ontology/Writer>. ",
    "Editor": "{} a <http://www.movieontology.org/2009/10/01/movieontology.owl#Editor>. ",
    "Film_Director": "{} a <http://dbpedia.org/page/Film_Director>. ",
    "Producer": "{} a <http://www.movieontology.org/2009/10/01/movieontology.owl#Producer>. ",
    # gêneros
    "Genre": "{} a <http://www.movieontology.org/2009/10/01/movieontology.owl#Genre>. ",
    ## Entretenimento
    "Actionreach": "{} a <http://www.movieontology.org/2009/10/01/movieontology.owl#Actionreach>. ", 
    "Brute_Action": "{} a <http://www.movieontology.org/2009/10/01/movieontology.owl#Brute_Action>. ",
    "Old_Action": "{} a <http://www.movieontology.org/2009/10/01/movieontology.owl#Old_Action>. ",
    "Entertaining_Information": "{} a <http://www.movieontology.org/2009/10/01/movieontology.owl#Entertaining_Information>. ",
    "Experience": "{} a <http://www.movieontology.org/2009/10/01/movieontology.owl#Imaginational_Entertainment>. ", # sem resultados :(
    "Intelectual_Entertainment": "{} a <http://www.movieontology.org/2009/10/01/movieontology.owl#Intelectual_Entertainment>. ", # sem resultados
    "Musical_Entertainment": "{} a <http://www.movieontology.org/2009/10/01/movieontology.owl#Musical_Entertainment>. ",
    "Porn": "{} a <http://www.movieontology.org/2009/10/01/movieontology.owl#Porn>. ",
    "TV-Entertainment": "{} a <http://www.movieontology.org/2009/10/01/movieontology.owl#TV-Entertainment>. ",
    "Imaginational_Entertainment": "{} a <http://www.movieontology.org/2009/10/01/movieontology.owl#Imaginational_Entertainment>. ",
    "SciFi_and_Fantasy": "{} a <http://www.movieontology.org/2009/10/01/movieontology.owl#SciFi_and_Fantasy>. ",
    "Thrilling": "{} a <http://www.movieontology.org/2009/10/01/movieontology.owl#Thrilling>. ", # sem resultados :(
    "Logical_Thrilling": "{} a <http://www.movieontology.org/2009/10/01/movieontology.owl#Logical_Thrilling>. ",
    "Sensible_Thrilling": "{} a <http://www.movieontology.org/2009/10/01/movieontology.owl#Sensible_Thrilling>. ",
    "Sensible": "{} a <http://www.movieontology.org/2009/10/01/movieontology.owl#Sensible>. ", # sem resultados :(
    "Heavy_Sensible": "{} a <http://www.movieontology.org/2009/10/01/movieontology.owl#Heavy_Sensible>. ",
    "Love": "{} a <http://www.movieontology.org/2009/10/01/movieontology.owl#Love>. ",
    "SocialActive": "{} a <http://www.movieontology.org/2009/10/01/movieontology.owl#SocialActive>. ", # sem resultados :(
    "Fun": "{} a <http://www.movieontology.org/2009/10/01/movieontology.owl#Fun>. ",
    "Kids": "{} a <http://www.movieontology.org/2009/10/01/movieontology.owl#Kids>. ", # sem resultado :(
    "Information": "{} a <http://www.movieontology.org/2009/10/01/movieontology.owl#Information>. ", # sem resultado
    "Fast-Info": "{} a <http://www.movieontology.org/2009/10/01/movieontology.owl#Fast-Info>. ", # sem resultado
    "Info-TV": "{} a <http://www.movieontology.org/2009/10/01/movieontology.owl#Info-TV>. ",
    "Special-Info": "{} a <http://www.movieontology.org/2009/10/01/movieontology.owl#Special-Info>. ", # sem resultado
    "Documentarial_Information": "{} a <http://www.movieontology.org/2009/10/01/movieontology.owl#Documentarial_Information>. ",
    "Historical_Information": "{} a <http://www.movieontology.org/2009/10/01/movieontology.owl#Historical_Information>. ",
    # Companhias
    "Center_American_Company": "{} a <http://www.movieontology.org/2009/10/01/movieontology.owl#Center_American_Company>. ",
    "East_Asian_Company": "{} a <http://www.movieontology.org/2009/10/01/movieontology.owl#East_Asian_Company>. ",
    "North_American_Company": "{} a <http://www.movieontology.org/2009/10/01/movieontology.owl#North_American_Company>. ",
    "North_European_Company": "{} a <http://www.movieontology.org/2009/10/01/movieontology.owl#North_European_Company>. ",
    "Oceanian_Company": "{} a <http://www.movieontology.org/2009/10/01/movieontology.owl#Oceanian_Company>. ",
    "South_American_Company": "{} a <http://www.movieontology.org/2009/10/01/movieontology.owl#South_American_Company>. ",
    "South_Asian_Company": "{} a  <http://www.movieontology.org/2009/10/01/movieontology.owl#South_Asian_Company>. ",
    "South_European_Company": "{} a <http://www.movieontology.org/2009/10/01/movieontology.owl#South_European_Company>. ",
    "SouthEast_Asian_Company": "{} a <http://www.movieontology.org/2009/10/01/movieontology.owl#SouthEast_Asian_Company>. ",
    "West_European_Company": "{} a <http://www.movieontology.org/2009/10/01/movieontology.owl#West_European_Company>. ",
    # Filme
    "Movie": "{} a <http://www.movieontology.org/2009/10/01/movieontology.owl#Movie>. ",
    # Companhia de produção
    "Production_Company": "{} a <http://www.movieontology.org/2009/10/01/movieontology.owl#Production_Company>. ",
    # Território
    ## - Africa
    "Eastern_Africa": "{} a <http://www.movieontology.org/2009/10/01/movieontology.owl#Eastern_Africa>. ",
    "Middle_Africa": "{} a <http://www.movieontology.org/2009/10/01/movieontology.owl#Middle_Africa>. ",
    "Northern_Africa": "{} a <http://www.movieontology.org/2009/10/01/movieontology.owl#Northern_Africa>. ",
    "Southern_Africa": "{} a <http://www.movieontology.org/2009/10/01/movieontology.owl#Southern_Africa>. ",
    "Western_Africa": "{} a <http://www.movieontology.org/2009/10/01/movieontology.owl#Western_Africa>. ",
    ## - América
    "Caribbean": "{} a <http://www.movieontology.org/2009/10/01/movieontology.owl#Caribbean>. ",
    ### - América latina
    "Central_America": "{} a <http://www.movieontology.org/2009/10/01/movieontology.owl#Central_America>. ",
    "South_America": "{} a <http://www.movieontology.org/2009/10/01/movieontology.owl#South_America>. ",
    ### - América do norte
    "Northern_America": "{} a <http://www.movieontology.org/2009/10/01/movieontology.owl#Northern_America>. ",
    ## - Ásia
    "Central_Asia": "{} a <http://www.movieontology.org/2009/10/01/movieontology.owl#Central_Asia>. ",
    "Eastern_Asia": "{} a <http://www.movieontology.org/2009/10/01/movieontology.owl#Eastern_Asia>. ",
    "Southeastern_Asia": "{} a <http://www.movieontology.org/2009/10/01/movieontology.owl#Southeastern_Asia>. ",
    "Southern_Asia": "{} a <http://www.movieontology.org/2009/10/01/movieontology.owl#Southern_Asia>. ",
    "Western_Asia": "{} a <http://www.movieontology.org/2009/10/01/movieontology.owl#Western_Asia>. ",
    ## - Europa
    "Eastern_Europe": "{} a <http://www.movieontology.org/2009/10/01/movieontology.owl#Eastern_Europe>. ",
    "Northern_Europe": "{} a <http://www.movieontology.org/2009/10/01/movieontology.owl#Northern_Europe>. ",
    "Southern_Europe": "{} a <http://www.movieontology.org/2009/10/01/movieontology.owl#Southern_Europe>. ",
    "Western_Europe": "{} a <http://www.movieontology.org/2009/10/01/movieontology.owl#Western_Europe>. ",
    ## - Oceania
    "Australia_and_New_Zealand": "{} a <http://www.movieontology.org/2009/10/01/movieontology.owl#Australia_and_New_Zealand>. ",
    "Melanesia": "{} a <http://www.movieontology.org/2009/10/01/movieontology.owl#Melanesia>. ",
    "Micronesia": "{} a <http://www.movieontology.org/2009/10/01/movieontology.owl#Micronesia>. ",
    "Polynesia": "{} a <http://www.movieontology.org/2009/10/01/movieontology.owl#Polynesia>. ",
    # Série de TV
    "TVSeries": "{} a <http://www.movieontology.org/2009/10/01/movieontology.owl#TVSeries>. "
}


DATA_PROPERTIES_RANGE_MAP = {
    "runtime":"http://www.w3.org/2001/XMLSchema#int", # basic
    "title":"http://www.w3.org/2001/XMLSchema#dateTime", 
    "releasedate":"http://www.w3.org/2001/XMLSchema#string", # contains
    "productionStartYear":"http://www.w3.org/2001/XMLSchema#int", # basic
    "indicationDate":"http://www.w3.org/2001/XMLSchema#dateTime",
    "imdbrating":"http://www.w3.org/2001/XMLSchema#double", # basic
    "gross":"http://www.w3.org/2001/XMLSchema#string", # contains
    "countryCode":"http://www.w3.org/2001/XMLSchema#string", # contains
    "companyName":"http://www.w3.org/2001/XMLSchema#string", # contains
    "budget":"http://www.w3.org/2001/XMLSchema#string", # contains
    "birthName":"http://www.w3.org/2001/XMLSchema#string", # # contains
    "birthDate":"http://www.w3.org/2001/XMLSchema#dateTime",

}

OPERATOR_MAP = {
    "greater_than": ">",
    "less_than": "<",
    "equal_to": "==",
    "less_than_or_equal_to": "<=",
    "greater_than_or_equal_to": ">="

}


GENRE_MAP = {
      "genre_entertainment": ("http://www.movieontology.org/2009/10/01/movieontology.owl#Entertainment",
                                [
                                 "genre_actionreach",
                                 "genre_entertaining_information",
                                 "genre_experience",
                                 "genre_imaginational_entertainment",
                                 "genre_sensible",
                                 "genre_social_active"])
                        ,
      "genre_actionreach":("http://www.movieontology.org/2009/10/01/movieontology.owl#Actionreach",
                           [
                            "genre_brute_Action",
                            "genre_old_action",
                      ]),
      "genre_brute_Action": ("http://www.movieontology.org/2009/10/01/movieontology.owl#Brute_Action", []),
      "genre_old_action": ("http://www.movieontology.org/2009/10/01/movieontology.owl#Old_Action", []),
      "genre_entertaining_Information": ("http://www.movieontology.org/2009/10/01/movieontology.owl#Entertaining_Information", []),
      "genre_experience": ("http://www.movieontology.org/2009/10/01/movieontology.owl#Experience",
                           [
                            "genre_intelectual_entertainment",
                            "genre_porn",
                            "genre_tv_entertainment"
                            ]),
      "genre_intelectual_entertainment": ("http://www.movieontology.org/2009/10/01/movieontology.owl#Intelectual_Entertainment",
                                          [
                                           "genre_musical_entertainment"
                                          ]),
      "genre_musical_entertainment": ("http://www.movieontology.org/2009/10/01/movieontology.owl#Musical_Entertainment", []),
      "genre_porn": ("http://www.movieontology.org/2009/10/01/movieontology.owl#Porn",[]),
      "genre_tv_entertainment": ("http://www.movieontology.org/2009/10/01/movieontology.owl#TV-Entertainment", []),
      "genre_imaginational_entertainment": ("http://www.movieontology.org/2009/10/01/movieontology.owl#Imaginational_Entertainment",
                                            ["genre_scifi_and_fantasy",
                                             "genre_thrilling"
                                             ]),
      "genre_scifi_and_fantasy": ("http://www.movieontology.org/2009/10/01/movieontology.owl#SciFi_and_Fantasy", []),
      "genre_thrilling": ("http://www.movieontology.org/2009/10/01/movieontology.owl#Thrilling",
                          ["genre_logical_thrilling",
                          "genre_sensible_thrilling"]),
      "genre_logical_thrilling": ("http://www.movieontology.org/2009/10/01/movieontology.owl#Logical_Thrilling", []),
      "genre_sensible_thrilling": ("http://www.movieontology.org/2009/10/01/movieontology.owl#Sensible_Thrilling", []),
      "genre_sensible": ("http://www.movieontology.org/2009/10/01/movieontology.owl#Sensible",
                         ["genre_heavy_sensible",
                          "genre_love"]),
      "genre_heavy_sensible": ("http://www.movieontology.org/2009/10/01/movieontology.owl#Heavy_Sensible", []),
      "genre_love": ("http://www.movieontology.org/2009/10/01/movieontology.owl#Love", []),
      "genre_social_active": ("http://www.movieontology.org/2009/10/01/movieontology.owl#SocialActive",
                              ["genre_fun",
                               "genre_kids"]),
      "genre_fun": ("http://www.movieontology.org/2009/10/01/movieontology.owl#Fun", []),
      "genre_kids": ("http://www.movieontology.org/2009/10/01/movieontology.owl#Kids", []),
      "genre_information": ("http://www.movieontology.org/2009/10/01/movieontology.owl#Information",
                            [
                             "genre_fast_info",
                             "genre_special_info"
                             ]),
      "genre_fast_info": ("http://www.movieontology.org/2009/10/01/movieontology.owl#Fast-Info",
                          ["genre_info_tv"]),
      "genre_info_tv": ("http://www.movieontology.org/2009/10/01/movieontology.owl#Info-TV", []),
      "genre_special_info": ("http://www.movieontology.org/2009/10/01/movieontology.owl#Special-Info",
                             ["genre_documentarial_information"]
                             ),
      "genre_documentarial_information": ("http://www.movieontology.org/2009/10/01/movieontology.owl#Documentarial_Information",
                                          ["genre_historical_information"]),
      "genre_historical_information": ("http://www.movieontology.org/2009/10/01/movieontology.owl#Historical_Information", [])

}

NER_ENTITIES_MAP = {
    "actor": "Actor",
    "genre": "Genre",
    "award": "Award",
    "actress": "Actress",
    "movie": "Movie",
    "person": "Person",
    "company": "Production_Company",
    "series": "TVSeries",
    "director":"Film_Director",
    "writer":"Writer",
    "editor":"Editor",
    "costume_designer":"Costume_Designer",
    "producer":"Producer",

    # Africa
    "territory_eastern_africa": "Eastern_Africa",
    "territory_middle_Africa": "Middle_Africa",
    "territory_northern_Africa": "Northern_Africa",
    "territory_southern_Africa": "Southern_Africa",
    "territory_western_Africa": "western_Africa",
    # America
    "territory_caribbean": "Caribbean",
    "territory_central_america": "Central_America",
    "territory_south_america": "South_America",
    "territory_northern_America": "Northern_America",
    #Asia
    "territory_central_asia": "Central_Asia",
    "territory_eastern_asia": "Eastern_Asia",
    "territory_southeastern_asia": "Southeastern_Asia",
    "territory_southern_asia": "Southern_Asia",
    "territory_western_asia": "Western_Asia",
    # Europa
    "territory_eastern_europe": "Eastern_Europe",
    "territory_northern_europe": "Northern_Europe",
    "territory_southern_europe": "Southern_Europe",
    "territory_western_europe": "Western_Europe",
    # Oceania
    "territory_australia_and_new_zealand": "Australia_and_New_Zealand",
    "territory_melanesia": "Melanesia",
    "territory_micronesia": "micronesia",
    "territory_polynesia": "polynesia",
    # object_properties
    "has_actor": "hasActor",
    "has_actress": "hasActress",
    "has_male_actor": "hasMaleActor",
    "has_award": "isAwardedWith",
    "has_genre": "belongsToGenre",
    "has_filming_location": "hasFilmLocation",
    "has_company_location": "hasCompanyLocation",
    "has_designer": "hasCostumeDesigner",
    "has_director": "hasDirector",
    "has_editor": "has_editor",
    "has_producer": "hasProducer",
    "has_company": "isProducedBy",
    "has_nomination": "nominatedFor",
    "has_writer": "writtenBy",
    "is_award_of": "isAwardOf",
    "is_costume_designer_in": "isCostumeDesignerIn",
    "is_writer_in": "wrote",
    # Data properties
    "has_runtime": "runtime",
    "has_birth_date": "birthDate",
    "has_birth_name": "birthName",
    "has_budget": "budget",
    "has_company_name": "companyName",
    "has_country_code": "countryCode",
    "has_gross": "gross",
    "has_imdbrating": "imdbrating",
    "has_indication_date": "indicationDate",
    "has_production_start_year": "productionStartYear",
    "has_release_date": "releasedate",
    "has_title": "title",
    "has_value": "has_value",

}

TRIPLES  = [('series', 'has_award', 'award'),
 ('series', 'has_writer', 'writer'),
 ('series', 'has_indication_date', 'indication_date'),
 ('series', 'has_male_actor', 'actor'),
 ('series', 'has_nomination', 'nomination'),
 ('series', 'has_production_start_year', 'start_year'),
 ('series', 'has_director', 'film_director'),
 ('series', 'has_genre', 'genre'),
 ('series', 'has_actress', 'actress'),
 ('series', 'has_designer', 'costume_designer'),
 ('series', 'has_imdbrating', 'imdbrating'),
 ('series', 'has_producer', 'producer'),
 ('series', 'has_gross', 'gross'),
 ('series', 'has_editor', 'editor'),
 ('series', 'has_budget', 'budget'),
 ('series', 'has_company', 'company'),
 ('series', 'has_filming_location', 'location'),
 ('award', 'is_award_of', 'series'),
 ('award', 'is_award_of', 'person'),
 ('award', 'is_award_of', 'movie'),
 ('series', 'has_runtime', 'runtime'),
 ('series', 'has_release_date', 'release_date'),
 ('costume_designer', 'is_costume_designer_in', 'series'),
 ('costume_designer', 'is_costume_designer_in', 'movie'),
 ('writer', 'is_writer_in', 'series'),
 ('writer', 'is_writer_in', 'movie'),
 ('company', 'has_company_location', 'location'),
]

TRIPLES_MOVIE = [
('movie', 'has_award', 'award'),
 ('movie', 'has_writer', 'writer'),
 ('movie', 'has_indication_date', 'indication_date'),
 ('movie', 'has_male_actor', 'actor'),
 ('movie', 'has_nomination', 'nomination'),
 ('movie', 'has_production_start_year', 'start_year'),
 ('movie', 'has_director', 'film_director'),
 ('movie', 'has_genre', 'genre'),
 ('movie', 'has_actress', 'actress'),
 ('movie', 'has_designer', 'costume_designer'),
 ('movie', 'has_imdbrating', 'imdbrating'),
 ('movie', 'has_producer', 'producer'),
 ('movie', 'has_gross', 'gross'),
 ('movie', 'has_editor', 'editor'),
 ('movie', 'has_budget', 'budget'),
 ('movie', 'has_company', 'company'),
 ('movie', 'has_filming_location', 'location'),
 ('movie', 'has_runtime', 'runtime'),
 ('movie', 'has_release_date', 'release_date'),
 

]
TRIPLES_PERSON = [
('person', 'has_award', 'award'),
 ('person', 'has_indication_date', 'indication_date'),
 ('person', 'has_nomination', 'nomination'),
 ('person', 'has_birth_date', 'birth_date'),

]

PERSON = [
          "actor", "actress", "writer", "costume_designer", "diretor", 'editor'
]

MOVIE_SERIE = [
        "movie","series"
]

ENTITY_TO_URI={
  "Award": "http://www.movieontology.org/2009/10/01/movieontology.owl#Award",
    "Actress": "http://www.movieontology.org/2009/11/09/movieontology.owl#Actress",
    "Costume_Designer": "http://www.movieontology.org/2009/10/01/movieontology.owl#Costume_Designer",
    "Actor": "http://dbpedia.org/ontology/Actor",
    "Writer": "http://dbpedia.org/ontology/Writer",
    "Editor": "http://www.movieontology.org/2009/10/01/movieontology.owl#Editor",
    "Film_Director": "http://dbpedia.org/page/Film_Director",
    "Producer": "http://www.movieontology.org/2009/10/01/movieontology.owl#Producer",
    "Genre": "http://www.movieontology.org/2009/10/01/movieontology.owl#Genre",
    "Actionreach": "http://www.movieontology.org/2009/10/01/movieontology.owl#Actionreach", 
    "Brute_Action": "http://www.movieontology.org/2009/10/01/movieontology.owl#Brute_Action",
    "Old_Action": "http://www.movieontology.org/2009/10/01/movieontology.owl#Old_Action",
    "Entertaining_Information": "http://www.movieontology.org/2009/10/01/movieontology.owl#Entertaining_Information",
    "Experience": "http://www.movieontology.org/2009/10/01/movieontology.owl#Imaginational_Entertainment", 
    "Intelectual_Entertainment": "http://www.movieontology.org/2009/10/01/movieontology.owl#Intelectual_Entertainment", 
    "Musical_Entertainment": "http://www.movieontology.org/2009/10/01/movieontology.owl#Musical_Entertainment",
    "Porn": "http://www.movieontology.org/2009/10/01/movieontology.owl#Porn",
    "TV-Entertainment": "http://www.movieontology.org/2009/10/01/movieontology.owl#TV-Entertainment",
    "Imaginational_Entertainment": "http://www.movieontology.org/2009/10/01/movieontology.owl#Imaginational_Entertainment",
    "SciFi_and_Fantasy": "http://www.movieontology.org/2009/10/01/movieontology.owl#SciFi_and_Fantasy",
    "Thrilling": "http://www.movieontology.org/2009/10/01/movieontology.owl#Thrilling", 
    "Logical_Thrilling": "http://www.movieontology.org/2009/10/01/movieontology.owl#Logical_Thrilling",
    "Sensible_Thrilling": "http://www.movieontology.org/2009/10/01/movieontology.owl#Sensible_Thrilling",
    "Sensible": "http://www.movieontology.org/2009/10/01/movieontology.owl#Sensible", 
    "Heavy_Sensible": "http://www.movieontology.org/2009/10/01/movieontology.owl#Heavy_Sensible",
    "Love": "http://www.movieontology.org/2009/10/01/movieontology.owl#Love",
    "SocialActive": "http://www.movieontology.org/2009/10/01/movieontology.owl#SocialActive", 
    "Fun": "http://www.movieontology.org/2009/10/01/movieontology.owl#Fun",
    "Kids": "http://www.movieontology.org/2009/10/01/movieontology.owl#Kids", 
    "Information": "http://www.movieontology.org/2009/10/01/movieontology.owl#Information", 
    "Fast-Info": "http://www.movieontology.org/2009/10/01/movieontology.owl#Fast-Info", 
    "Info-TV": "http://www.movieontology.org/2009/10/01/movieontology.owl#Info-TV",
    "Special-Info": "http://www.movieontology.org/2009/10/01/movieontology.owl#Special-Info", 
    "Documentarial_Information": "http://www.movieontology.org/2009/10/01/movieontology.owl#Documentarial_Information",
    "Historical_Information": "http://www.movieontology.org/2009/10/01/movieontology.owl#Historical_Information",
    "Center_American_Company": "http://www.movieontology.org/2009/10/01/movieontology.owl#Center_American_Company",
    "East_Asian_Company": "http://www.movieontology.org/2009/10/01/movieontology.owl#East_Asian_Company",
    "North_American_Company": "http://www.movieontology.org/2009/10/01/movieontology.owl#North_American_Company",
    "North_European_Company": "http://www.movieontology.org/2009/10/01/movieontology.owl#North_European_Company",
    "Oceanian_Company": "http://www.movieontology.org/2009/10/01/movieontology.owl#Oceanian_Company",
    "South_American_Company": "http://www.movieontology.org/2009/10/01/movieontology.owl#South_American_Company",
    "South_Asian_Company": " http://www.movieontology.org/2009/10/01/movieontology.owl#South_Asian_Company",
    "South_European_Company": "http://www.movieontology.org/2009/10/01/movieontology.owl#South_European_Company",
    "SouthEast_Asian_Company": "http://www.movieontology.org/2009/10/01/movieontology.owl#SouthEast_Asian_Company",
    "West_European_Company": "http://www.movieontology.org/2009/10/01/movieontology.owl#West_European_Company",
    "Movie": "http://www.movieontology.org/2009/10/01/movieontology.owl#Movie",
    "Production_Company": "http://www.movieontology.org/2009/10/01/movieontology.owl#Production_Company",
    "Eastern_Africa": "http://www.movieontology.org/2009/10/01/movieontology.owl#Eastern_Africa",
    "Middle_Africa": "http://www.movieontology.org/2009/10/01/movieontology.owl#Middle_Africa",
    "Northern_Africa": "http://www.movieontology.org/2009/10/01/movieontology.owl#Northern_Africa",
    "Southern_Africa": "http://www.movieontology.org/2009/10/01/movieontology.owl#Southern_Africa",
    "Western_Africa": "http://www.movieontology.org/2009/10/01/movieontology.owl#Western_Africa",
    "Caribbean": "http://www.movieontology.org/2009/10/01/movieontology.owl#Caribbean",
    "Central_America": "http://www.movieontology.org/2009/10/01/movieontology.owl#Central_America",
    "South_America": "http://www.movieontology.org/2009/10/01/movieontology.owl#South_America",
    "Northern_America": "http://www.movieontology.org/2009/10/01/movieontology.owl#Northern_America",
    "Central_Asia": "http://www.movieontology.org/2009/10/01/movieontology.owl#Central_Asia",
    "Eastern_Asia": "http://www.movieontology.org/2009/10/01/movieontology.owl#Eastern_Asia",
    "Southeastern_Asia": "http://www.movieontology.org/2009/10/01/movieontology.owl#Southeastern_Asia",
    "Southern_Asia": "http://www.movieontology.org/2009/10/01/movieontology.owl#Southern_Asia",
    "Western_Asia": "http://www.movieontology.org/2009/10/01/movieontology.owl#Western_Asia",
    "Eastern_Europe": "http://www.movieontology.org/2009/10/01/movieontology.owl#Eastern_Europe",
    "Northern_Europe": "http://www.movieontology.org/2009/10/01/movieontology.owl#Northern_Europe",
    "Southern_Europe": "http://www.movieontology.org/2009/10/01/movieontology.owl#Southern_Europe",
    "Western_Europe": "http://www.movieontology.org/2009/10/01/movieontology.owl#Western_Europe",
    "Australia_and_New_Zealand": "http://www.movieontology.org/2009/10/01/movieontology.owl#Australia_and_New_Zealand",
    "Melanesia": "http://www.movieontology.org/2009/10/01/movieontology.owl#Melanesia",
    "Micronesia": "http://www.movieontology.org/2009/10/01/movieontology.owl#Micronesia",
    "Polynesia": "http://www.movieontology.org/2009/10/01/movieontology.owl#Polynesia",
    "TVSeries": "http://www.movieontology.org/2009/10/01/movieontology.owl#TVSeries",

    "belongsToGenre": "http://www.movieontology.org/2009/10/01/movieontology.owl#belongsToGenre",
    "hasActress": "http://www.movieontology.org/2009/10/01/movieontology.owl#hasActress",
    "hasMaleActor": "http://www.movieontology.org/2009/10/01/movieontology.owl#hasMaleActor",
    "hasCompanyLocation": "http://www.movieontology.org/2009/11/09/movieontology.owl#hasCompanyLocation",
    "hasCostumeDesigner": "http://www.movieontology.org/2009/10/01/movieontology.owl#hasCostumeDesigner",
    "hasDirector": "http://www.movieontology.org/2009/10/01/movieontology.owl#hasDirector",
    "hasEditor": "http://www.movieontology.org/2009/10/01/movieontology.owl#hasEditor",
    "hasFilmLocation": "http://www.movieontology.org/2009/10/01/movieontology.owl#hasFilmLocation",
    "hasProducer": "http://www.movieontology.org/2009/10/01/movieontology.owl#hasProducer",
    "isAwardedWith": "http://www.movieontology.org/2009/10/01/movieontology.owl#isAwardedWith",
    "isAwardOf": "http://www.movieontology.org/2009/11/09/movieontology.owl#isAwardOf",
    "isCostumeDesignerIn": "http://www.movieontology.org/2009/10/01/movieontology.owl#isCostumeDesignerIn",
    "isProducedBy": "http://www.movieontology.org/2009/10/01/movieontology.owl#isProducedBy",
    "nominatedFor": "http://www.movieontology.org/2009/10/01/movieontology.owl#nominatedFor",
    "writtenBy": "http://www.movieontology.org/2009/11/09/movieontology.owl#writtenBy",
    "wrote": "http://www.movieontology.org/2009/11/09/movieontology.owl#wrote",

    "productionStartYear": "http://dbpedia.org/ontology/productionStartYear",
    "birthDate": "http://dbpedia.org/ontology/birthDate",
    "birthName": "http://dbpedia.org/ontology/birthName",
    "budget": "http://dbpedia.org/ontology/budget",
    "companyName": "http://www.movieontology.org/2009/11/09/movieontology.owl#companyName",
    "gross": "http://dbpedia.org/ontology/gross",
    "imdbrating": "http://www.movieontology.org/2009/10/01/movieontology.owl#imdbrating",
    "indicationDate": "http://www.movieontology.org/2009/11/09/movieontology.owl#indicationDate",
    "releasedate": "http://www.movieontology.org/2009/10/01/movieontology.owl#releasedate",
    "runtime": "http://www.movieontology.org/2009/10/01/movieontology.owl#runtime",
    "title": "http://www.movieontology.org/2009/10/01/movieontology.owl#title",
    "has_value": "has_value",
}

# p1 = OBJ_PROPERTIES["hasDirector"].format("<uri_filme_x>", "?diretor")
# p2 =  OBJ_PROPERTIES["isAwardedWith"].format("?diretor", "<uri_award>")
# p3 = COUNT.format("?diretor")
# sparql_query = SELECT_SKELETON.format(p3, p1 + p2)

# print(sparql_query)
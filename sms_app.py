from flask import Flask, request, jsonify #without s is incoming
import requests #with S is for outgoing
import json
import random




app = Flask('bootcamp')

def call_api_by_name(body):
  body = body.lower()
  

  error_msg = "Pokemon Not Found"
  opening = '''<?xml version="1.0" encoding="UTF-8"?><Response> <Message>'''
  closing = '</Message> </Response>'

  exception = False
  exceptions = {'farfetch\'d':'farfetched',
    "mr. mime":['mr-mime','Mr. Mime'],
    "mr mime":['mr-mime','Mr. Mime'],
    "mr-mime":['mr-mime','Mr. Mime'],

    "ho-oh":['ho-oh','Ho-Oh'],
    "porygon-z": ["porygon-z",'Porygon-Z'], 
    'mime jr.':["mime-jr","Mime Jr."],
    'mime jr':["mime-jr","Mime Jr."],
    'mime-jr':["mime-jr","Mime Jr."],
    'jangmo-o':["jangmo-o","Jangmo-o"],
    "type: null":["type-null","Type: Null"],
    "type null":["type-null","Type: Null"],
    "typenull":["type-null","Type: Null"],
    "type-null":["type-null","Type: Null"],

    'hakamo-o':["hakamo-o","Hakamo-o"],
    'kommo-o':["kommo-o","Kommo-o"], 
    "jangmo-o":["jangmo-o","Jangmo-o"],

    'tapu koko': ['tapu-koko','Tapu Koko'], 
    'tapu-koko': ['tapu-koko','Tapu Koko'], 
    'tapu-lele': ['tapu-lele','Tapu Lele'], 
    'tapu lele': ['tapu-lele','Tapu Lele'], 
    'tapu bulu': ['tapu-bulu','Tapu Bulu'], 
    'tapu-bulu': ['tapu-bulu','Tapu Bulu'], 
    'tapu fini': ['tapu-fini','Tapu Fini'], 
    'tapu-fini': ['tapu-fini','Tapu Fini'], 

    "nidoran♀": ["nidoran-f","Nidoran♀"], 
    "nidoran-f": ["nidoran-f","Nidoran♀"], 

    "nidoran female": ["nidoran-f","Nidoran♀"], 
    "nidoran f": ["nidoran-f","Nidoran♀"], 
    "nidoran♂":["nidoran-m","Nidoran♂"],
    "nidoran male":["nidoran-m","Nidoran♂"],
    "nidoran m":["nidoran-m","Nidoran♂"],
    "nidoran-m":["nidoran-m","Nidoran♂"],

    "flabébé":["flabebe","Flabébé"],
    "flabebe":["flabebe","Flabébé"],

    "oricorio pa\'u":["oricorio-pau","Oricorio Pa\'u"],
    "oricorio pau":["oricorio-pau","Oricorio Pa\'u"],
    "oricorio-pau":["oricorio-pau","Oricorio Pa\'u"],

    'oricorio pom-pom':['oricorio-pom-pom',"Oricorio Pom-Pom"],
    'oricorio-pom-pom':['oricorio-pom-pom',"Oricorio Pom-Pom"],
    'oricorio pom pom':['oricorio-pom-pom',"Oricorio Pom-Pom"]

    }
  # santizes the user input (removes non search_term characters)
  if body in exceptions: 
    print("exception detected")
    exception = True

    user_input_search_term = exceptions[body][0]
  else:
    user_input_search_term =  ''.join(ch for ch in body if ch.isalnum())
  # print("user_input_search_term: " + user_input_search_term)
  
  POKEMON_API_URL = 'https://pokeapi.co/api/v2/'
  url = POKEMON_API_URL + '/pokemon/' + user_input_search_term.lower()

  # calls the API
  r = requests.get(url)

  # returns an error if pokemon not found
  if r.status_code == 404:
    return opening + error_msg + closing

  api_response = json.loads(r.content)
  # print(api_response.keys())

  name = (api_response['name']).title()


  # sprite
  sprite = api_response['sprites']['front_default']
  # print(sprite)
  # error handling: Names with special characters
  if exception:
    name = exceptions[user_input_search_term][1]
  

  # generates a list of pokedex entries
  species_url = api_response['species']['url']
  r = requests.get(species_url)
  species_api_response = json.loads(r.content)
  dex_entries_en = []
  for entry in (species_api_response["flavor_text_entries"]):
    dex_desc = entry['flavor_text']
    dex_desc = dex_desc.replace('\n',' ')
    dex_desc = dex_desc.replace('\f',' ')

    if entry['language']['name'] == 'en':
      dex_entries_en.append(dex_desc) 



  
  pokedex_desc = random.choice(dex_entries_en)
  print(pokedex_desc)
  # print(list(pokedex_desc))

  type_1 = api_response['types'][0]['type']['name'].title()
  types = type_1 + ' type'
  print(type_1)
  if len(api_response['types']) > 1:
    type_2 = api_response['types'][1]['type']['name']
    types = type_1.title() + ' and ' + type_2.title() + ' type'

  height_in = api_response['height'] * 4
  height_ft = height_in // 12
  remaining_in = height_in % 12
  height = str(height_ft) + "\'" +  str(remaining_in) + "\""
  
  weight = api_response['weight']
  # 4.53563714903
  weight = round(float(weight) / 4.53563714903, 1)
  # + weight

  print(height, weight)

  pokemon_dex = "<Media>" + sprite + "</Media>" + name + """ 
""" + types + """
""" + 'Height: ' + height + ", Weight: " + str(weight) + " lbs " + """

""" + pokedex_desc
  print(pokemon_dex)

  response = opening + pokemon_dex + closing
  # print(response)

  return response 


call_api_by_name('oddish')

@app.route('/')
def index():
  return "welcome to the index"





@app.route('/weather', methods=['GET', 'POST'])
def weather():

  city = request.values['Body']
  # city = 'Denver'
  response = requests.get('http://api.openweathermap.org/data/2.5/weather', params={
  'appid': '972498aee47cf8cee7487e742cd1bc15',
  'q': city
  })
  weather_data = json.loads(response.content)
  print(weather_data)

  temperature = (float(weather_data['main']['temp']) - 273.15 ) * (9 / 5) + 32
  temperature = round(temperature, 1)
  returned_string = "The weather in " + city + " is " + str(temperature) + "F!"

  return """<?xml version="1.0" encoding="UTF-8"?>
  <Response>
    <Message>""" + returned_string + """</Message>
  </Response>"""












@app.route('/pokedex',methods=['GET','POST'])
def pokedex():

  body = request.values['Body']
  response = call_api_by_name(body)

#   error_msg = "Pokemon Not Found"
#   opening = '''<?xml version="1.0" encoding="UTF-8"?><Response> <Message>'''
#   closing = '</Message> </Response>'

#   user_input_search_term =  ''.join(ch for ch in body if ch.issearch_term())
#   print("user_input_search_term: " + user_input_search_term)
  
#   POKEMON_API_URL = 'https://pokeapi.co/api/v2/'

#   url = POKEMON_API_URL + '/pokemon/' + user_input_search_term.lower()
#   r = requests.get(url)
#   if r.status_code == 404:

#     return opening + error_msg + closing

#   api_response = json.loads(r.content)


#   print(api_response.keys())

#   name = (api_response['name']).title()
#   if name in exceptions:
#     name = exceptions[name]

#   species_url = api_response['species']['url']


#   r = requests.get(species_url)
#   species_api_response = json.loads(r.content)
#   dex_entries_en = []
#   for entry in (species_api_response["flavor_text_entries"]):
#     if entry['language']['name'] == 'en':
#       dex_entries_en.append(entry['flavor_text']) 

# # new_list = [expression(i) for i in old_list if filter(i)]

  
#   pokedex_desc = random.choice(dex_entries_en)
#   print(len(pokedex_desc))
#   pokedex_desc = pokedex_desc.replace('\n',' ')
#   print(pokedex_desc)
#   print(len(pokedex_desc))

#   type_1 = api_response['types'][0]['type']['name'].title()
#   types = type_1 + ' type'
#   print(type_1)
#   if len(api_response['types']) > 1:
#     type_2 = api_response['types'][1]['type']['name']
#     types = type_1.title() + ' and ' + type_2.title() + ' type'

#   height_in = api_response['height'] * 4
#   height_ft = height_in // 12
#   remaining_in = height_in % 12
#   height = str(height_ft) + "\'" +  str(remaining_in) + "\""
#   print(height)
#   weight = api_response['weight']
#   # 4.53563714903
#   weight = round(float(weight) / 4.53563714903, 1)
#   # + weight

#   print(weight)

#   pokemon_dex = name + """ 
# """ + types + """
# """ + 'Height: ' + height + ", Weight: " + str(weight) + " lbs " + """

# """ + pokedex_desc


#   response = opening + pokemon_dex + closing
  # print(response)

  return response 

app.run(debug=True, host='0.0.0.0', port=8080)

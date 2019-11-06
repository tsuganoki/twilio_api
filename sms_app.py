from flask import Flask, request, jsonify #without s is incoming
import requests #with S is for outgoing
import json
import random

app = Flask('bootcamp')



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
  ret_string = "The weather in " + city + " is " + str(temperature) + "F!"

  return """<?xml version="1.0" encoding="UTF-8"?>
  <Response>
    <Message>""" + ret_string + """</Message>
  </Response>"""





@app.route('/pokedex',methods=['GET','POST'])
def pokedex():

  body = request.values['Body']

  error_msg = "Pokemon Not Found"
  opening = '''<?xml version="1.0" encoding="UTF-8"?><Response> <Message>'''
  closing = '</Message> </Response>'

  user_input_alpha =  ''.join(ch for ch in body if ch.isalpha())
  print("user_input_alpha: " + user_input_alpha)
  
  POKEMON_API_URL = 'https://pokeapi.co/api/v2/'

  url = POKEMON_API_URL + '/pokemon/' + user_input_alpha.lower()
  r = requests.get(url)
  if r.status_code == 404:

    return opening + error_msg + closing

  api_response = json.loads(r.content)


  print(api_response.keys())

  name = (api_response['name']).title()

  species_url = api_response['species']['url']


  r = requests.get(species_url)
  species_api_response = json.loads(r.content)
  dex_entries_en = []
  for entry in (species_api_response["flavor_text_entries"]):
    if entry['language']['name'] == 'en':
      dex_entries_en.append(entry['flavor_text']) 

# new_list = [expression(i) for i in old_list if filter(i)]

  
  pokedex_desc = random.choice(dex_entries_en)
  print(len(pokedex_desc))
  pokedex_desc = pokedex_desc.replace('\n',' ')
  print(pokedex_desc)
  print(len(pokedex_desc))

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
  print(height)
  weight = api_response['weight']
  # 4.53563714903
  weight = round(weight / 4.53563714903, 1)
  # + weight

  print(weight)

  pokemon_dex = name + """ 
""" + types + """
""" + 'Height: ' + height + ", Weight: " + str(weight) + " lbs " + """

""" + pokedex_desc


  response = opening + pokemon_dex + closing
  # print(response)

  return response 

app.run(debug=True, host='0.0.0.0', port=8080)

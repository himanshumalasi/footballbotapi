import apiai
import json
import requests
from pprint import pprint
# api.ai client 
APIAI_ACCESS_TOKEN = "ef4ddbe4120d45ee99b53c35afa97a62"
ai = apiai.ApiAI(APIAI_ACCESS_TOKEN)


HELP_MSG = """
Hey! I am ScoreBot. 
I can provide you score,result,table from all around the worlds leagues :)
This app will show you today result and fixture.
"""
def livescore(params):
    url = 'https://footballbotapi.herokuapp.com/api/fetch/'
    header = {'query':'livescore'}
    r = requests.get(url,params=header)
    return r.content

def worldRanking(params):
    url = 'https://footballbotapi.herokuapp.com/api/fetch/'
    header = {'query':'worldranking'}
    r = requests.get(url,params=header)
    return r.content

def fixture(params):
    url = 'https://footballbotapi.herokuapp.com/api/fetch/'
    header = {'query':'fixture',
             'league':params.get('league')}
    r = requests.get(url,params=header)
    return r.content

def playerRanking(params):
    url = 'https://footballbotapi.herokuapp.com/api/fetch/'
    header = {'query':'playerranking'}
    r = requests.get(url,params=header)
    return r.content

def topScorer(params):
    url = 'https://footballbotapi.herokuapp.com/api/fetch/'
    header = {'query':'scorer',
             'league':params.get('league')}
    r = requests.get(url,params=header)
    return r.content

def pointsTable(params):
    url = 'https://footballbotapi.herokuapp.com/api/fetch'
    league = params.get('league')
    header = {'query':'pointsTable',
             'league':params.get('league')}
    r = requests.get(url,params=header)
    return r.content

def resultstoday(params):
    url = 'https://footballbotapi.herokuapp.com/api/fetch'
    league = params.get('league')
    header = {'query':'todayresult',
             'league':params.get('league')}
    r = requests.get(url,params=header)
    return r.content

def apiai_response(query, session_id):
	"""
	function to fetch api.ai response
	"""
	request = ai.text_request()
	request.lang = 'en'
	request.session_id = session_id
	request.query = query
	response = request.getresponse()
	return json.loads(response.read().decode('utf8'))


def parse_response(response):
	"""
	function to parse response and 
	return intent and its parameters
	"""
	result = response['result']
	params = result.get('parameters')
	intent = result['metadata'].get('intentName')
	return intent, params

	
def fetch_reply(query, session_id):
    response = apiai_response(query, session_id)
    intent, params = parse_response(response)
    reply = {}
#    print('RESPONSE')
#    pprint(response)
    if response['result']['action'].startswith('smalltalk'):
        reply['type'] = 'smalltalk'
        if response['result']['resolvedQuery'] == 'help' or response['result']['resolvedQuery'] == 'HELP':
            reply['data'] = HELP_MSG
        else:
            reply['data'] = response['result']['fulfillment']['speech']
    if response['result']['action'] == 'input.unknown':
        reply['type'] = 'unknown'
        reply['data'] = response['result']['fulfillment']['speech']
    if intent == 'playerranking':
        reply['type']='playerranking'
        # make a api call
        reply['data'] = playerRanking(params)
    if intent == 'scorer':
        reply['type'] = 'scorer'
        reply['data'] = topScorer(params)
    if intent == 'points_table':
        reply['type'] = 'points_table'
        reply['data'] = pointsTable(params)
    if intent=='result_today':
        reply['type']='resulttoday'
        reply['data']= resultstoday(params)
    if intent == 'fixture':
        reply['type'] = 'fixture'
        reply['data'] = fixture(params)
    if intent == 'world_ranking':
        reply['type'] = 'world_ranking'
        reply['data'] = worldRanking(params)
    if intent == 'live_score':
        reply['type'] = 'live_score'
        reply['data'] = livescore(params)
    return reply

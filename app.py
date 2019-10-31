from flask import (
    Flask,
    request,
    jsonify
)
from utils import (
    find_ranking,
    top_scorer,
    point_table,
    today_result,
    today_fixture,
    world_ranking,
    livescore
)
from utility import fetch_reply
import json

app = Flask('__name__')
random_id = 'cd785760-4812-4292-bbc1-f7b3efce58c7'

@app.route('/api/fetch',methods=['GET'])
def api_for_result():
    if request.method == 'GET':
        query = request.args.get('query')
        if query == 'playerranking':
            return find_ranking()
        if query == 'scorer':
            league = request.args.get('league')
            return top_scorer(league)
        if query == 'pointsTable':
            league = request.args.get('league')
            return point_table(league)
        if query == 'todayresult':
            league = request.args.get('league')
            return today_result(league)
        if query == 'fixture':
            league = request.args.get('league')
            return today_fixture(league)
        if query == 'worldranking':
            return world_ranking()
        if query == 'livescore':
            return livescore()
        
@app.route('/api/',methods=['GET'])
def api_for_query():
    if request.method == 'GET':
        query = request.args.get('text')
        print(query)
        reply = fetch_reply(query,random_id)
        return json.dumps(reply)
    
if __name__ == '__main__':
    app.run(debug=True,port=8000)
import requests
from bs4 import BeautifulSoup
import json

def livescore():
    url="https://www.theguardian.com/football/live"
    r=requests.get(url)
    soup=BeautifulSoup(r.content,"html5lib")

    allleague=soup.findAll("div",{"class":"football-table__container"})
    l={}
    for i in range(len(allleague)):
        pleague=allleague[i].findAll("table",{"class":"table table--football football-matches table--responsive-font"})
        leaguename=pleague[0].findAll("caption",{"class":"table__caption table__caption--top"})

        l[leaguename[0].findAll('a')[0].text] = []
        for j in range(len(pleague)):
            allmatches=pleague[j].findAll("tr",{"class":"football-match football-match--live"})
            s={}
            for k in range(len(allmatches)):
                match=allmatches[k].findAll('span',{"class":"team-name__long"})
                score=allmatches[k].findAll('div',{"class":"football-team__score"})
                s["match"]=match[0].text+" "+score[0].text+"-"+score[1].text+" "+match[1].text
                s['link']=allmatches[k]['data-link-to']
                l[leaguename[0].findAll('a')[0].text].append(s)
                s={}
    matches = []
    for leag in l:
        if len(l[leag]) > 0:
            for match in l[leag]:
                matches.append(match)
    data = {}
    data['result'] = 'success'
    data['content'] = matches
    return json.dumps(data)

def world_ranking():
    url='http://www.fifa.com/fifa-world-ranking/ranking-table/men/index.html'
    r=requests.get(url)
    soup=BeautifulSoup(r.content,'html5lib')
    body=soup.findAll('tbody')
    teams = body[0].findAll('div',{'class':'fi-t__n'})
    i = 1
    ranking = {}
    for team in teams:
        rank = i
        name = team.findAll('span',{'class':'fi-t__nText'})[0].text
        ranking[rank] = {}
        ranking[rank]['name'] = name
        i += 1
    images = body[0].findAll('img',{'class':'fi-flag--4'})
    points = body[0].findAll('td',{'class':'fi-table__td fi-table__points'})
    for i in range(1,len(teams)):
        ranking[i]['img'] = images[i]['src']
    for i in range(1,len(teams)):
        ranking[i]['points'] = points[i].text
    data = {}
    data['result'] = 'success'
    data['content'] = ranking
    return json.dumps(data)

def today_fixture(league):
    url="https://www.theguardian.com/football/live"
    r=requests.get(url)
    soup=BeautifulSoup(r.content,"html5lib")
    allleague=soup.findAll('div',{'class':'football-table__container'})
    allleagues=[]
    l={}
    for i in range(len(allleague)):
        xyz=allleague[i].findAll('tr',{'class':'football-match football-match--fixture'})
        name=allleague[i].findAll('caption',{'class':'table__caption table__caption--top'})[0].findAll('a')[0].text
        l[name] = {}
        l[name]['matches'] = []
        for j in range(len(xyz)):
            abc=xyz[j].findAll('td',{'class':'football-match__teams table-column--main'})
            s={}
            for k in range(len(abc)):
                match=abc[k].findAll('span',{'class':'team-name__long'})
                link=abc[k].findAll('a')[0]['href']
                s['match']=match[0].text+"  VS  "+match[1].text
                s['link']=link
                l[name]['matches'].append(s)
                s={}
    data = {}
    for leag in l:
        if league.lower() in leag.lower():
            data['result'] = 'success'
            data['content'] = l[leag]['matches']
            break
    else:
        data['result'] = 'error'
    return json.dumps(data)


"""
This function is used to find the result of various leagues
"""
def today_result(league):
    url="https://www.theguardian.com/football/results"
    r=requests.get(url)
    soup=BeautifulSoup(r.content,"html5lib")
    alltables=soup.findAll("div",{"football-matches__day"})
    p={}
    for i in range(1):
        pleaguetable=alltables[i].findAll('div',{"class":"football-table__container"})
        for j in range(len(pleaguetable)):
            leaguename=pleaguetable[j].findAll("caption",{"class":"table__caption table__caption--top"})
            p[leaguename[0].findAll('a')[0].text] = {}
            p[leaguename[0].findAll('a')[0].text]['matches'] = []
            #print(leaguename[0].findAll('a')[0].text)
            body=pleaguetable[j].findAll('tbody')
            for k in range(len(body)):
                rows=body[k].findAll('tr',{"class":"football-match football-match--result"})
                for l in range(len(rows)):
                    s={}
                    s["match"]=rows[l].findAll('span',{"class":"team-name__long"})[0].text+" "+rows[l].findAll('div',{"class":"football-team__score"})[0].text+"-"+rows[l].findAll('div',{"class":"football-team__score"})[1].text+" "+rows[l].findAll('span',{"class":"team-name__long"})[1].text
                    s['link']=rows[l].findAll('a')[0]['href']
                    #p.append(s)
                    #print(s)
                    p[leaguename[0].findAll('a')[0].text]['matches'].append(s)
    data = {}
    for leag in p:
        if league.lower() in leag.lower():
            data['result'] = 'success'
            data['content'] = p[leag]['matches']
            break
    else:
        data['result'] = 'error'
    return json.dumps(data)

def point_table(league):
    url="http://www.skysports.com/football/tables"
    r=requests.get(url)
    soup=BeautifulSoup(r.content,'html5lib')
    allleagues=soup.findAll('div',{"class":"page-filters__offset"})
    alltables={}
    p=[]
    for i in range(len(allleagues)):
        pleague=allleagues[i].findAll('a',{"class":"standing-table block"})
        for j in range(len(pleague)):
            name = pleague[j].findAll('caption',{"class":"standing-table__caption"})[0].text.replace('\n','').strip()
            alltables[name] = {}
            alltables[name]['table'] = []
            body=pleague[j].findAll('tbody')
            for k in range(len(body)):
                rows=body[k].findAll('tr',{"class":"standing-table__row"})
                for l in range(len(rows)):
                    q=[]
                    q.append(rows[l].findAll("td",{"class":"standing-table__cell"})[0].text)
                    q.append(rows[l].findAll("td",{"class":"standing-table__cell"})[1].text)
                    q.append(rows[l].findAll("td",{"class":"standing-table__cell"})[2].text)
                    q.append(rows[l].findAll("td",{"class":"standing-table__cell"})[3].text)
                    q.append(rows[l].findAll("td",{"class":"standing-table__cell"})[4].text)
                    alltables[name]['table'].append(q)
    #print(alltables)
    data = {}
    for leag in alltables:
        #print(leag)
        if league.lower() in leag.lower():
            data['result'] = 'success'
            table = alltables[leag]['table']
            data['content'] = table
            break
    else:
        data['result'] = 'error'
    return json.dumps(data)

def find_ranking():
    url='https://www.ranker.com/list/best-current-soccer-players/ranker-sports'
    r=requests.get(url)
    soup=BeautifulSoup(r.content,'html5lib')
    players = soup.findAll('div',{'class':'listItem listItem__h2 listItem__h2--grid listItem__h2--popUp pointer flex relative robotoC'})
    ranker = []
    for player in players[:15]:
        rank = player.findAll('strong',{'class':'listItem__rank block center instapaper_ignore'})[0].text
        name = player.findAll('a')[0].text
        ranker.append([rank,name])
    return json.dumps(ranker)

def top_scorer(league):
    d = {'la liga':'spanish-la-liga',
    'bundesliga':'german-bundesliga',
     'fa cup':'fa-cup',
     'Serie A':'italian-serie-a',
     'Scottish premiership':'scottish-premiership',
     'Scottish Championship':'scottish-championship',
     'premier league':'premier-league',
     'ligue 1':'french-ligue-one',
     'League One':'league-one',
    }
    nl = d.get(league)
    if nl == None:
        data = {}
        data['result'] = 'error'
        return json.dumps(data)
    url = 'http://www.bbc.com/sport/football/'+nl + '/top-scorers'
    r=requests.get(url)
    if r.status_code == 200:
        soup=BeautifulSoup(r.content,"html5lib")
        alltables=soup.findAll("div",{'class':'top-player-stats__body'})
        l=[]
        topscorerlaliga=[]
        # topscorerlaliga.append('http://www.bbc.com/sport/football/spanish-la-liga/top-scorers')
        for i in range(len(alltables)):
            name=alltables[i].findAll('h2',{'class':'top-player-stats__name gel-double-pica'})[0].text
            team=alltables[i].findAll('span',{'class':'gel-long-primer team-short-name'})[0].text
            goal=alltables[i].findAll('span',{'class':'top-player-stats__goals-scored-number'})[0].text
            assist=alltables[i].findAll('span',{'class':'top-player-stats__assists-number gel-double-pica'})[0].text
            topscorerlaliga.append([name,team,goal,assist])
        data = {}
        data['result'] = 'success'
        data['content'] = topscorerlaliga[:5]
        return json.dumps(data)
    else:
        data = {}
        data['result'] = 'error'
        return json.dumps(data)
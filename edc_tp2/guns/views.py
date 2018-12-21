from django.shortcuts import render
from django.http import HttpRequest,HttpResponse,Http404
import requests
import json
from django.views.decorators.csrf import csrf_exempt
from s4api.graphdb_api import GraphDBApi
from s4api.swagger import ApiClient
url = 'https://query.wikidata.org/sparql'
endpoint = "http://localhost:7200"

def home(request):


    
    #query to retrieve the 9 guns with the most stock in the store with their correspondent image
    
    query = """         
        PREFIX prop: <http://www.wikidata.org/wiki/Property/>
        PREFIX entity: <http://www.wikidata.org/entity/>
        select DISTINCT ?item ?image ?name ?count ?price  where { 
            ?item prop:P18 ?image .
            ?item prop:P2561 ?name .
            ?item prop:P1114 ?count .
            ?item prop:P2284 ?price .
        }
        ORDER BY DESC(?count)
        limit 9
    """

   
    bindings = executeQuery(query)
    items = [{
        'name':i['name']['value'], 
        'image':i['image']['value'], 
        'count':i['count']['value'],
        'price':i['price']['value']} for i in bindings ]

    # objective: [['a1','a2','a3'],['b1','b2','b3'],['c1','c2','c3']]

    
    gunlist = [items[i:i + 3] for i in range(0, len(items), 3)]
    
    
    #get all types of weapons (instance of firearms)
    query = """             
        SELECT ?weapon ?weaponLabel
        WHERE { 
        ?weapon wdt:P31 wd:Q12796 .
        SERVICE wikibase:label { bd:serviceParam wikibase:language "en". }
}
    """
    r = requests.get(url, params = {'format': 'json', 'query': query})
    bindings = r.json()['results']['bindings']
    types_of_weapons = [{'weapon':i['weapon']['value'], 'label': i['weaponLabel']['value']} for i in bindings]
    print(types_of_weapons)

    tparams = {
        'gunlist': gunlist,
        'types': types_of_weapons
    }
    return render(request, 'index.html', tparams)


def search(request):
    rg = request.GET

    filter = ''         #default filter option --> no filter
    setting = 'sd'      #default search option
    if 'filter' in rg:
        filter = rg['filter']
    
    filterstr='FILTER regex(?label, "{}", "i" ) .'.format(filter)

    if 'setting' in rg:
        setting = rg['setting']


    if setting=='sd':   #stock desc
            
        query = """         
            PREFIX prop: <http://www.wikidata.org/wiki/Property/>
            PREFIX entity: <http://www.wikidata.org/entity/>
            select DISTINCT ?item ?img ?label ?count ?price  where { 
                ?item prop:P18 ?img .
                ?item prop:P2561 ?label .
                ?item prop:P1114 ?count .
                ?item prop:P2284 ?price .""" + filterstr + """
            }
            ORDER BY DESC(?count)
        """
    elif setting=='sc':   #stock cres
        query = """         
            PREFIX prop: <http://www.wikidata.org/wiki/Property/>
            PREFIX entity: <http://www.wikidata.org/entity/>
            select DISTINCT ?item ?img ?label ?count ?price  where { 
                ?item prop:P18 ?img .
                ?item prop:P2561 ?label .
                ?item prop:P1114 ?count .
                ?item prop:P2284 ?price .""" + filterstr + """
            }
            ORDER BY (?count)
        """
    elif setting=='pc':   #price cres
        query = """         
            PREFIX prop: <http://www.wikidata.org/wiki/Property/>
            PREFIX entity: <http://www.wikidata.org/entity/>
            select DISTINCT ?item ?img ?label ?count ?price  where { 
                ?item prop:P18 ?img .
                ?item prop:P2561 ?label .
                ?item prop:P1114 ?count .
                ?item prop:P2284 ?price .""" + filterstr + """
            }
            ORDER BY (?price)
        """
    elif setting=='pd':   #price desc
        query = """         
            PREFIX prop: <http://www.wikidata.org/wiki/Property/>
            PREFIX entity: <http://www.wikidata.org/entity/>
            select DISTINCT ?item ?img ?label ?count ?price  where { 
                ?item prop:P18 ?img .
                ?item prop:P2561 ?label .
                ?item prop:P1114 ?count .
                ?item prop:P2284 ?price .""" + filterstr + """
            }
            ORDER BY DESC(?price)
        """
    elif setting=='nc':   #name cres
        query = """         
            PREFIX prop: <http://www.wikidata.org/wiki/Property/>
            PREFIX entity: <http://www.wikidata.org/entity/>
            select DISTINCT ?item ?img ?label ?count ?price  where { 
                ?item prop:P18 ?img .
                ?item prop:P2561 ?label .
                ?item prop:P1114 ?count .
                ?item prop:P2284 ?price .""" + filterstr + """
            }
            ORDER BY (?label)
        """
    elif setting=='nd':   #name desc
        query = """         
            PREFIX prop: <http://www.wikidata.org/wiki/Property/>
            PREFIX entity: <http://www.wikidata.org/entity/>
            select DISTINCT ?item ?img ?label ?count ?price  where { 
                ?item prop:P18 ?img .
                ?item prop:P2561 ?label .
                ?item prop:P1114 ?count .
                ?item prop:P2284 ?price .""" + filterstr + """
            }
            ORDER BY DESC(?label)
        """

    elif setting=='wiki': #wikidata query
        query = '''
        SELECT DISTINCT ?item ?name2 ?label ?image 
        WHERE {
            ?item wdt:P31 wd:Q12796.
            ?name2 wdt:P279* ?item.
            ?name2 wdt:P18 ?image;
                rdfs:label ?label. ''' + filterstr + '''
                FILTER(LANGMATCHES(LANG(?label), "en"))
            SERVICE wikibase:label { bd:serviceParam wikibase:language "en". }
        }ORDER BY(?label)
        limit 50
        '''

    wiki = setting=='wiki'

    if wiki:
        bindings = executeWikiQuery(query)    
        print(len(set([i['name2']['value'] for i in bindings])))
        data = { i['name2']['value']:(i['label']['value'],i['image']['value'])  for i in bindings  }  #img id label
        print('query',query)
        items = [{
            'id':k.split('/')[-1],
            'label':v[0],
            'img':v[1]
        } for k,v in data.items() ]
        
 
    else:
        bindings = executeQuery(query)
        items = [{
            'id':i['item']['value'],
            'label':i['label']['value'], 
            'labelid':i['label']['value'].replace(' ','_').replace('&','!'),
            'img':i['img']['value'], 
            'count':i['count']['value'],
            'price':i['price']['value']} for i in bindings ]


    controls = [
        { 'label': 'stock', 'setting': [ 'sc','sd'] },
        { 'label': 'price', 'setting': ['pc','pd'] },
        { 'label': 'name', 'setting': ['nc','nd'] }
    ]

    tparams = {
        'guns': items,
        'controls': controls,
        'wiki': wiki,
        'filter': filter
    }
    return render(request, 'search.html', tparams)


def remove(request):
    rg = request.POST
    name,stock = rg['name'],rg['price']
    return render(request, 'ok', {})


@csrf_exempt
def increase(request,name):
    rg = request.POST
    print(rg)
    print(name)
    name = name.replace('_',' ').replace('!','&')
    update = '''         
        PREFIX prop: <http://www.wikidata.org/wiki/Property/>
        PREFIX entity: <http://www.wikidata.org/entity/>


        DELETE {
            ?item prop:P1114 ?count .
        }  
        INSERT {
            ?item prop:P1114 ?cc.
        }
        WHERE{
            ?item prop:P2561 "''' + name + '''".
            ?item prop:P1114 ?count .
            BIND((?count+1) as ?cc)
        }

        '''
    executeUpdate(update)
    return render(request,'ok.html',{})


@csrf_exempt
def decrease(request,name):

    name = name.replace('_',' ').replace('!','&')
    update = '''         
        PREFIX prop: <http://www.wikidata.org/wiki/Property/>
        PREFIX entity: <http://www.wikidata.org/entity/>


        DELETE {
            ?item prop:P1114 ?count .
        }  
        INSERT {
            ?item prop:P1114 ?cc.
        }
        WHERE{
            FILTER(?count != 0 )
            ?item prop:P2561 "''' + name +'''".
            ?item prop:P1114 ?count .
            BIND((?count-1) as ?cc)
        }

        '''
    executeUpdate(update)
    return render(request,'ok.html',{})

@csrf_exempt
def add(request,id,price):



    #wikidata query
    query = '''
        select distinct ?image ?label
        where {
            wd:'''+ id +''' wdt:P18 ?image.
            wd:'''+ id +''' rdfs:label ?label.
            FILTER (langMatches( lang(?label), "en" ) )
        }
    '''
    data = executeWikiQuery(query)[0]
    name = data['label']['value']
    image = data['image']['value']


    #insert new weapon
    update = '''
        PREFIX prop: <http://www.wikidata.org/wiki/Property/>
        PREFIX entity: <http://www.wikidata.org/entity/>
        INSERT DATA
        {
            entity:''' + id + ''' prop:P2561 "''' + name + '''".
            entity:''' + id + ''' prop:P2284 ''' + str(price) + '''.
            entity:''' + id + ''' prop:P18 "''' + image + '''".
            entity:''' + id + ''' prop:P1114 0.
        }
    '''
    
    executeUpdate(update)
    print(update)
    return render(request,'ok.html',{})



def executeQuery(query):   #function to avoid repeating code
    repo_name = "Guns"
    client = ApiClient(endpoint=endpoint)
    accessor = GraphDBApi(client)
    payload_query = {"query": query}
    res = accessor.sparql_select(body=payload_query,repo_name=repo_name)
    res = json.loads(res)
    bindings = res['results']['bindings']
    return bindings




def executeWikiQuery(query):   #function to avoid repeating code
    r = requests.get(url, params = {'format': 'json', 'query': query})
    return r.json()['results']['bindings']




def executeUpdate(update):   #function to avoid repeating code
    repo_name = "Guns"
    client = ApiClient(endpoint=endpoint)
    accessor = GraphDBApi(client)
    payload_update = {"update": update}
    print(payload_update)
    res = accessor.sparql_update(body=payload_update,repo_name=repo_name)

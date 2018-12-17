from django.shortcuts import render
from django.http import HttpRequest,HttpResponse,Http404
import requests
import json
from s4api.graphdb_api import GraphDBApi
from s4api.swagger import ApiClient
url = 'https://query.wikidata.org/sparql'
endpoint = "http://localhost:7200"

def home(request):


    
    #query to retrieve the 9 guns with the most stock in the store with their correspondent image
    query = """         
        PREFIX prop: <http://www.wikidata.org/wiki/Property/>
        PREFIX entity: <http://www.wikidata.org/entity/>
        select DISTINCT ?item ?image ?name ?count  where { 
            ?item prop:P18 ?image .
            ?item prop:P2561 ?name .
            ?item prop:P1114 ?count .
        }

        ORDER BY DESC(?count)
        
        limit 9
    """

   
    bindings = executeQuery(query)
    items = [{'name':i['name']['value'], 'image':i['image']['value'], 'count':i['count']['value'] } for i in bindings ]

    # objective: [['a1','a2','a3'],['b1','b2','b3'],['c1','c2','c3']]

    gunlist = [items[i:i + 3] for i in range(0, len(items), 3)]
    tparams = {
        'gunlist': gunlist
    }
    return render(request, 'index.html', tparams)


def weapontype(request):
    rg = request.GET
    print('rg',rg)
    type = rg['type']
    print('type',type)
    tparams = {
        
    }
    return render(request, 'weapontype.html', tparams)



def executeQuery(query):   #function to avoid repeating code
    repo_name = "Guns"
    client = ApiClient(endpoint=endpoint)
    accessor = GraphDBApi(client)
    payload_query = {"query": query}
    res = accessor.sparql_select(body=payload_query,repo_name=repo_name)
    res = json.loads(res)
    bindings = res['results']['bindings']
    return bindings

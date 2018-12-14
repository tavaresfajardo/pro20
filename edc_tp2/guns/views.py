from django.shortcuts import render
from django.http import HttpRequest,HttpResponse,Http404
import requests
url = 'https://query.wikidata.org/sparql'

def home(request):
    
    query = 'SELECT ?name ?nameLabel ?image WHERE { ?name wdt:P31 wd:Q12796. SERVICE wikibase:label { bd:serviceParam wikibase:language "en". } OPTIONAL { ?name wdt:P18 ?image. } }'
    r = requests.get(url, params = {'format': 'json', 'query': query})
    data = r.json()
    data = [{   'name': v['name']['value'], 'nameLabel': v['nameLabel']['value'] } for v in data['results']['bindings'] ]   
    print(data)


    tparams = {
        
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
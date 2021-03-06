import json
import requests
import random
url = 'https://query.wikidata.org/sparql'
wikiurl_entity = '<http://www.wikidata.org/entity/'
wikiurl_prop = '<http://www.wikidata.org/wiki/Property/'


newDB = []
newDB +=  [(wikiurl_prop+'P2561>', wikiurl_prop+'P2561>' , '"name"')]
newDB +=  [(wikiurl_prop+'P1114>', wikiurl_prop+'P2561>' , '"count"')]
newDB +=  [(wikiurl_prop+'P18>', wikiurl_prop+'P2561>' , '"image"')]
newDB +=  [(wikiurl_prop+'P2284>', wikiurl_prop+'P2561>' , '"price"')]

query =('''SELECT ?name ?nameLabel ?name2 ?label ?image WHERE {
       ?name wdt:P31 wd:Q12796.
       ?name2 wdt:P279* ?name.
        ?name2 rdfs:label ?label.
       ?name2 wdt:P18 ?image.
             
       filter langMatches(lang(?label), "en")
       FILTER NOT EXISTS{
       FILTER regex(?label, "/", "i")
         }
       SERVICE wikibase:label { bd:serviceParam wikibase:language "en". }
       }
       ''' )

print(query)
r = requests.get(url, params = {'format': 'json', 'query': query})
data = r.json()

R = []
#print('data',data)
R=[{   'name': '<'+v['name2']['value']+'>' , 'nameLabel': '"'+v['label']['value']+'"' , 'image' : '"'+v['image']['value']+'"' }for v in data['results']['bindings'] if v['label']['value'] not in v['name2']['value'] ]

dataset = [0,0]
while len(set(dataset))<50:
      
       dataset = [i['nameLabel'] for i in random.sample(R, 50)]
       print(len(set(dataset)),len(dataset))

newR = [(i,random.randint(1,20),random.randint(16,40)) for i in random.sample(R, 50)]

#generate random dataset, price is multiple of 50   ->  (entity,stock,price//50)

for i in newR:
       newDB +=  [(i[0]['name'],wikiurl_prop+'P2561>', i[0]['nameLabel'])]
       newDB +=  [(i[0]['name'],wikiurl_prop+'P1114>',i[1])]
       newDB +=  [(i[0]['name'],wikiurl_prop+'P2284>',i[2]*50)]
       newDB +=  [(i[0]['name'],wikiurl_prop+'P18>',i[0]['image'])]
       #print([(i[0]['name'],i[1]) for i in newR])


writeData = '\n'.join([' '.join([str(j) for j in list(i)]) + ' .' for i in newDB])
with open('storage.nt','w') as f:
       print('OK')
       f.write(writeData)

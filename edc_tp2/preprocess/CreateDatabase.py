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

query =('SELECT DISTINCT ?name ?nameLabel ?name2 ?name2Label ?image WHERE {'
      ' ?name wdt:P31 wd:Q12796.'
       '?name2 wdt:P279* ?name.'
       '?name2 wdt:P18 ?image.'
        'FILTER NOT EXISTS { '
       ' FILTER regex(?name2Label, "/", "i")'
          
      '}'
       'SERVICE wikibase:label { bd:serviceParam wikibase:language "en". }'
       
"}")

print(query)
r = requests.get(url, params = {'format': 'json', 'query': query})
data = r.json()

R = []
#print('data',data)
R=[{   'name': '<'+v['name2']['value']+'>' , 'nameLabel': '"'+v['name2Label']['value']+'"' , 'image' : '"'+v['image']['value']+'"' }for v in data['results']['bindings'] if v['name2Label']['value'] not in v['name2']['value'] ]

newR = [(i,random.randint(1,20),random.randint(800,2000)) for i in random.sample(R, 50)]
for i in newR:
       newDB +=  [(i[0]['name'],wikiurl_prop+'P2561>', i[0]['nameLabel'])]
       newDB +=  [(i[0]['name'],wikiurl_prop+'P1114>',i[1])]
       newDB +=  [(i[0]['name'],wikiurl_prop+'P2284>',i[2])]
       newDB +=  [(i[0]['name'],wikiurl_prop+'P18>',i[0]['image'])]
       print([(i[0]['name'],i[1]) for i in newR])


writeData = '\n'.join([' '.join([str(j) for j in list(i)]) + ' .' for i in newDB])
with open('storage.nt','w') as f:
       print('OK')
       f.write(writeData)

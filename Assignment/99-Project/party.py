import json

with open('party.json') as json_file:  
    data = json.load(json_file)

    for p in data['party']:
        print('U: ' + p['id'])
        print('P: ' + p['boss'])
        print('S: ' + p['name']["th"])
        print('P: ' + p['name']["en"])
        print('P: ' + p['name']["short"])
        print('')
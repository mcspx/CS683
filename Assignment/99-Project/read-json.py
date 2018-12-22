import json

with open('test.json') as json_file:  
    data = json.load(json_file)

    for p in data['medical']:
        print('U: ' + p['use'])
        print('S: ' + p['sq-ft'])
        print('P: ' + p['price'])
        print('')
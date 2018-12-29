import asyncio
import aiohttp
import json
import queue
import os

from flask  import Flask, render_template, make_response
from redis  import Redis
from time   import time
from random import random
from bs4    import BeautifulSoup

app = Flask(__name__)

REDIS_HOST = os.environ['REDIS_HOST']
REDIS_PORT = os.environ['REDIS_PORT']

redis = Redis(host=REDIS_HOST, port=REDIS_PORT)

async def party():
    partyList = []

    with open('party.json') as json_file:
        data = json.load(json_file)

        for p in data['party']:
            partyList.append(p['name']["th"])
            print('U: ' + p['id'])
            print('S: ' + p['name']["th"])
            print('P: ' + p['name']["short"])
            print('')

async def visit(client, queue, sites):
    try:
        urls = queue.pop(0)

        async with client.get(urls, timeout=30) as response:
            if response.status == 200:
                html = await response.text()
                soup = BeautifulSoup(html, 'html.parser')

                for href in soup.findAll('a'):
                    link = str(href.get('href'))

                    if link.startswith('http'):
                        if link in sites:
                            pass
                            #print('Dup - ', link)
                        else:
                            queue.append(link)
                            #print('new - ', link)

                sites.append(urls)

                return urls
            else:
                print("Request error ...")

                return ''
    except:
        print("Exception error ...")

        return ''

async def main(queue, sites):
    limit = 100
    count = 0

    while len(queue) > 0 and count < limit:
        count = count + 1

        async with aiohttp.ClientSession() as client:
            urls = await visit(client, queue, sites)

            if urls:
                print('Visit OK - %04d : %s' % (count, urls))
            else:
                print("Visit error !")

@app.route('/')
def hello():
    redis.incr('hits')
    return 'Redis ({}) hit counter: {}'.format(REDIS_HOST, redis.get('hits'))

@app.route('/live')
def hello_world():
    return render_template('index.html', data='test')

@app.route('/live-data')
def live_data():
    data = [time() * 1000, random() * 100]
    
    response = make_response(json.dumps(data))
    response.content_type = 'application/json'
    return response

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)

    elapsed_start = time.time()

    #queue = ['https://en.wikipedia.org/wiki/Main_Page']
    #sites = []

    #loop = asyncio.get_event_loop()
    #loop.run_until_complete(main(queue, sites))

    elapsed_finish = time.time()

    print('Elapsed :', (elapsed_finish - elapsed_start), 'seconds.')

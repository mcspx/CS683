import asyncio
import aiohttp
import time

from bs4 import BeautifulSoup

#----------------------------------------

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
                            #print('New - ', link)

                sites.append(urls)

                return urls
            else:
                print('Request error ...')

                return ''
    except:
        print('Exception error ...')

        return ''

# ----------------------------------------

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
                print('Visit error !')

# ----------------------------------------

if __name__ == '__main__':
    elapsed_start = time.time()

    queue = ['https://en.wikipedia.org/wiki/Main_Page']
    sites = []

    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(queue, sites))

    elapsed_finish = time.time()

    print('Elapsed :', (elapsed_finish - elapsed_start), 'seconds.')
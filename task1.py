# Реализовать в потоках проверку списка прокси серверов. https://awmproxy.net/freeproxy.php
# Нужно использовать очередь. Один поток заполняет очередь.
# Еще несколько берут прокси из очереди и пробуют по ней перейти. http://httpbin.org/anything
# Для выполнения запросов используйте requests. https://requests.readthedocs.io/en/master/

import asyncio
import aiohttp
import requests

proxy_list = ['https://49.88.210.188:38801', 'https://195.154.63.169:5836', 'https://162.244.83.192:3128',
              'https://113.218.232.161:38801', 'https://103.103.212.222:53281']


async def worker(queue):
    while True:
        try:
            proxy = queue.get_nowait()
        except Exception:
            await asyncio.sleep(0)
            continue
        proxies = {'http': proxy}
        async with aiohttp.ClientSession() as session:
            async with session.get('http://httpbin.org/anything') as resp:
                for pr in proxies:
                    sg = session.get(pr)
                print('coroutine status: ', resp.status)
                htm = await resp.text()
                print(htm)
        return sg


async def gener(q):
    for proxy in proxy_list:
        await q.put(proxy)


loop = asyncio.get_event_loop()
q2 = asyncio.Queue()
task_worker = [worker(q2) for i in range(5)]
fut = asyncio.gather(*[gener(q2)], *task_worker)
tmp = loop.run_until_complete(fut)
print(tmp)

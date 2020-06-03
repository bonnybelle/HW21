# Реализовать задачу с подбором пароля для архива. Использовать асинхронность.
# Тоже нужно использовать очередь, генератор задач и исполнителей.

import asyncio
import itertools
import string
from zipfile import ZipFile

zip_object = ZipFile('lesson6.zip', 'r')
pwd_list = []


async def pwd_generator(q, alphabet=string.ascii_lowercase):
    for pwd in itertools.product(alphabet, repeat=3):
        current_pwd = ''.join(pwd)
        await q.put(pwd_list.append(current_pwd))


async def worker(q):
    for password in pwd_list:
        try:
            await q.put(zip_object.extractall(pwd=password.encode('utf-8')))
            print('PASSWORD FOUND: {}'.format(password))
            break
        except Exception:
            await asyncio.sleep(0)


loop = asyncio.get_event_loop()
q2 = asyncio.Queue()
fut = asyncio.gather(*[pwd_generator(q2), worker(q2)])
tmp = loop.run_until_complete(fut)

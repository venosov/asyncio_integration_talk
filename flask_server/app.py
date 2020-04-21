import asyncio
from pathlib import Path

import aiohttp_jinja2
import jinja2
from aiohttp import web

from flask_server.utils import json_payload


routes = web.RouteTableDef()

app = web.Application()
messages_list = []


@aiohttp_jinja2.template('index.html')
async def index(request):
    return {}


@aiohttp_jinja2.template('messages.html')
async def reset(request):
    messages_list.clear()
    return dict(messages=['Cleaned'])


@routes.post('/messages')
async def add_messages(request):

    raw_data = await request.read()  # Raises 400 if malformed data is passed
    data = json_payload(raw_data)

    import random

    messages_list.extend([data] * random.randint(1,3))

    print(messages_list)

    return "OK"


@aiohttp_jinja2.template('messages.html')
def get_messages(request):
    return dict(messages=messages_list)


async def sleep():
    for i in range(0, 30):
        await asyncio.sleep(1)
        print(f"Waited {i}s")


def start_sleep_server():
    loop = asyncio.get_event_loop()
    coro = sleep()
    task = loop.create_task(coro)

    return task


if __name__ == '__main__':
    templates_folder = Path(__file__).parent / 'templates'
    aiohttp_jinja2.setup(app, loader=jinja2.FileSystemLoader(templates_folder))
    app.add_routes([
        web.get('/', index),
        web.get('/reset', reset),
        web.get('/messages', get_messages),
        web.post('/messages', add_messages),
    ])

    start_sleep_server()
    web.run_app(app)


import asyncio
import re
from bs4 import BeautifulSoup
import aiohttp
from aiohttp import web
from model import Temperature, session as db_session, Resource
import aiohttp_jinja2
import jinja2


async def parser(session, title, url, element, attribute, value):
    async with session.get(url, ssl=False) as response:
        if response.status == 200:
            html = await response.text()
            soup = BeautifulSoup(html, 'lxml')
            temp = soup.find(element, attrs={attribute: value})
            try:
                temp = re.sub(r'[^0-9+-]+', r'', temp.text)
            except AttributeError:
                temp = 'no data'
            qs = db_session.query(Temperature).filter(Temperature.name == title).update({'degree': temp})
            if not qs:
                db_session.add(Temperature(name=title, degree=temp))
            db_session.commit()
        else:
            qs = db_session.query(Temperature).filter(Temperature.name == title).update({'degree': 'no response'})
            if not qs:
                db_session.add(Temperature(name=title, degree='no response'))
            db_session.commit()


@aiohttp_jinja2.template('index.html')
async def main(request):
    qs_res = db_session.query(Resource).all()
    tasks = []
    async with aiohttp.ClientSession() as session:
        for i in qs_res:
            tasks.append(parser(session, i.title, i.url, i.element, i.attribute, i.value))
        await asyncio.gather(*tasks)
    qs = db_session.query(Temperature).all()
    return {'qs': qs}


@aiohttp_jinja2.template('resource_list.html')
async def resource_list(request):
    qs = db_session.query(Resource).all()
    return {'qs': qs}


@aiohttp_jinja2.template('create_resource.html')
async def create_resource(request):
    if request.method == 'POST':
        form = await request.post()
        db_session.add(Resource(title=form['title'], url=form['url'], element=form['element'], attribute=form['attribute'],
                                value=form['value']))
        db_session.commit()
        raise web.HTTPFound('/')
    return {}


app = web.Application()
aiohttp_jinja2.setup(app,
    loader=jinja2.FileSystemLoader('templates'))

app.add_routes([web.get('/', main),
                web.get('/create_resource', create_resource),
                web.post('/create_resource', create_resource),
                web.get('/resource_list', resource_list),
                ])

if __name__ == '__main__':
    web.run_app(app)
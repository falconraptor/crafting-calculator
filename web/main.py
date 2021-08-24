from typing import Any, Dict

from litespeed import render, route, start_with_args, serve
from litespeed.utils import Request

from web import game, version
from web.db import DB


@route(methods='GET')
def index(request: Request):
    return render(request, 'html/index.html', {'games': DB.execute('SELECT name, released, id FROM Games ORDER BY name').fetchall()})


@route(r'/static/([\s\w./%-]+)', 'GET', no_end_slash=True)
def static(_: Request, file: str):
    if file.startswith('game') or file.startswith('mod'):
        file, id = file.split('/', 1)
        return DB.execute(f'SELECT image FROM {file} WHERE id=?', (id,)).fetchone()['image']
    return serve(f'static/{file}')


if __name__ == '__main__':
    game.add_routes()
    version.add_routes()
    start_with_args()

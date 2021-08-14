from typing import Any, Dict

from litespeed import render, route, start_with_args, serve
from litespeed.utils import Request

from web import game
from web.db import DB


@route(methods='GET')
def index(request: Request):
    return render(request, 'html/index.html', {'games': DB.execute('SELECT name, released, id FROM Games ORDER BY name').fetchall()})


@route(r'/([\s\w%-]+)/mods/([\s\w%-]+)/', 'GET')
@require_mod
def versions(request: Request, game: Dict[str, Any]):
    return render(request, 'html/game.html', {'game': game, 'versions': DB.execute('SELECT version, released FROM ModVersions WHERE game=? ORDER BY released DESC', (game['id'],)).fetchall(), 'mods': DB.execute('SELECT Mods.* FROM Mods INNER JOIN ModVersions ON Mods.id=ModVersions.mod WHERE game_version IN (SELECT id FROM GameVersions WHERE game=?)', (game['id'],)).fetchall()})


# @route(r'/([\s\w%-]+)/mods/', 'GET')
# @require_game
# def game_mods(request: Request, game: Dict[str, Any]):
#     return render(request, 'html/game_mods.html', {'game': game, 'mods': DB.execute('SELECT Mods.* FROM Mods INNER JOIN ModVersions ON Mods.id=ModVersions.mod WHERE game_version IN (SELECT id FROM GameVersions WHERE game=?)', (game['id'],)).fetchall()})


@route(r'/static/([\s\w./%-]+)', ['GET'], no_end_slash=True)
def static(_: Request, file: str):
    if file.startswith('game') or file.startswith('mod'):
        file, id = file.split('/', 1)
        return DB.execute(f'SELECT image FROM {file} WHERE id=?', (id,)).fetchone()['image']
    return serve(f'static/{file}')


if __name__ == '__main__':
    game.add_routes()
    start_with_args()

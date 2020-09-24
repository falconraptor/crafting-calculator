from litespeed import render, route, start_with_args
from litespeed.utils import Request

from db import fetchall


@route(methods='GET')
def index(request: Request):
    return render(request, 'html/index.html', {'games': fetchall('SELECT name, released, image FROM Games ORDER BY name ASC')})


@route(r'/(\w+)/', methods='GET')
def games(request: Request, game: str):
    if not (game := fetchall('SELECT name, released, image, id FROM Games WHERE name=?', game)):
        return '', 307, {'Location': '/add_game/'}
    game = game[0]
    return render(request, 'html/game.html', {'game': game, 'versions': fetchall('SELECT version, released FROM GameVersions WHERE game=? ORDER BY released DESC', game['id'])})


@route(r'/(\w+)/(\w+)/')
def versions(request: Request, game: str, version: str):
    if not (game := fetchall('SELECT name, released, image, id FROM Games WHERE name=?', game)):
        return '', 307, {'Location': '/add_game/'}
    game = game[0]
    if not (version := fetchall('SELECT version, released FROM GameVersions WHERE game=? and version=?', game['id'], version)):
        return '', 307, {'Location': f'/{game}/add_version/'}
    version = version[0]
    return render(request, 'html/game.html', {'game': game, 'version': version})


if __name__ == '__main__':
    start_with_args()

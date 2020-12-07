from typing import Any, Dict

from litespeed import render, route, start_with_args
from litespeed.utils import Request

from web.db import DB


@route(methods='GET')
def index(request: Request):
    return render(request, 'html/index.html', {'games': DB.execute('SELECT name, released, image FROM Games ORDER BY name')})


@route(methods=['GET', 'POST'])
def add_game(request: Request):
    if request.POST:
        # TODO
        return '', 307, {'Location': f'/{game}'}
    return render(request, 'html/add_game.html')


def require_game(f):
    def wrapped(*args, **kwargs):
        game_kwargs = kwargs.get('game', None)
        game_args = args[0] if len(args) >= 1 else None
        if not (game := DB.execute('SELECT name, released, image, id FROM Games WHERE name=?', game_kwargs or game_args)):
            return '', 307, {'Location': '/add_game/'}
        if game_kwargs:
            kwargs['game'] = game
        if game_args:
            args = [game] + args[1:]
        return f(*args, **kwargs)
    return wrapped


def require_version(f):
    @require_game
    def wrapped(*args, **kwargs):
        game = kwargs.get('game', args[0] if len(args) >= 1 else '')
        version_kwargs = kwargs.get('version', None)
        version_args = args[1] if len(args) >= 2 else None
        if not (version := DB.execute('SELECT version, released FROM GameVersions WHERE game=? and version=?', game['id'], version_kwargs or version_args)):
            return '', 307, {'Location': f'/{game["name"]}/add_version/'}
        if version_kwargs:
            kwargs['version'] = version
        if version_args:
            args = args[0] + [version] + args[2:]
        return f(*args, **kwargs)
    return wrapped


@route(r'/(\w+)/add_version/', ['GET', 'POST'])
@require_game
def add_version(request: Request, game: Dict[str, Any]):
    if request.POST:
        # TODO
        return '', 307, {'Location': f'/{game}/{version}/'}
    return render(request, 'html/add_version.html', {'game': game})


@route(r'/(\w+)/', 'GET')
@require_game
def versions(request: Request, game: Dict[str, Any]):
    return render(request, 'html/game.html', {'game': game, 'versions': DB.execute('SELECT version, released FROM GameVersions WHERE game=? ORDER BY released DESC', game['id'])})


@route(r'/(\w+)/mods/', 'GET')
@require_game
def game_mods(request: Request, game: Dict[str, Any]):
    return render(request, 'html/game_mods.html', {'game': game, 'mods': DB.execute('SELECT Mods.* FROM Mods INNER JOIN ModVersions ON Mods.id=ModVersions.mod WHERE game_version IN (SELECT id FROM GameVersions WHERE game=?)', game)})


@route(r'/(\w+)/(\w+)/', 'GET')
@require_version
def game_version(request: Request, game: Dict[str, Any], version: Dict[str, Any]):
    return render(request, 'html/game_version.html', {'game': game, 'version': version})


@route(r'/(\w+)/(\w+)/items/', 'GET')
@require_version
def game_version_items(request: Request, game: Dict[str, Any], version: Dict[str, Any]):
    return render(request, 'html/game_version_items.html', {'game': game, 'version': version, 'items': DB.execute('SELECT GameItems.* FROM GameItems INNER JOIN GameVersionItemMap ON GameItems.id=GameVersionItemMap.item WHERE version=?', version['id'])})


@route(r'/(\w+)/(\w+)/mods/', 'GET')
@require_version
def game_version_mods(request: Request, game: Dict[str, Any], version: Dict[str, Any]):
    return render(request, 'html/game_version_mods.html', {'game': game, 'version': version, 'mods': DB.execute('SELECT Mods.* FROM Mods INNER JOIN ModVersions ON Mods.id=ModVersions.mod WHERE game_version=?', version['id'])})


if __name__ == '__main__':
    start_with_args()

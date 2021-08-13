from typing import Any, Dict

from litespeed import render, route, start_with_args, serve
from litespeed.utils import Request

from web.db import DB


@route(methods='GET')
def index(request: Request):
    return render(request, 'html/index.html', {'games': DB.execute('SELECT name, released, id FROM Games ORDER BY name').fetchall()})


@route(methods=['GET', 'POST'])
def add_game(request: Request):
    if request.POST:
        DB.execute('INSERT INTO Games (name, released, image) VALUES (?, ?, ?)', (request.POST['name'], request.POST['released'], request.POST['icon']))
        DB.commit()
        return '', 307, {'Location': f'/{request.POST["name"]}/'}
    return render(request, 'html/add_game.html')


def require_game(f):
    def wrapped(*args, **kwargs):
        game_kwargs = kwargs.get('game', None)
        game_args = args[1] if len(args) > 1 else None
        if not (game := DB.execute('SELECT name, released, id FROM Games WHERE name=?', (game_kwargs or game_args,)).fetchone()):
            return '', 307, {'Location': '/add_game/'}
        if game_kwargs:
            kwargs['game'] = game
        if game_args:
            args = args[:1] + (game,) + args[2:]
        return f(*args, **kwargs)
    return wrapped


def require_version(f):
    @require_game
    def wrapped(*args, **kwargs):
        game = kwargs.get('game', args[1] if len(args) > 1 else '')
        version_kwargs = kwargs.get('version', None)
        version_args = args[2] if len(args) > 2 else None
        if not (version := DB.execute('SELECT version, released FROM GameVersions WHERE game=? and version=?', (game['id'], version_kwargs or version_args)).fetchone()):
            return '', 307, {'Location': f'/{game["name"]}/add_version/'}
        if version_kwargs:
            kwargs['version'] = version
        if version_args:
            args = args[:2] + (version,) + args[3:]
        return f(*args, **kwargs)
    return wrapped


@route(r'/([\s\w%-]+)/add_version/', ['GET', 'POST'])
@require_game
def add_version(request: Request, game: Dict[str, Any]):
    if request.POST:
        DB.execute('INSERT INTO GameVersions (game, version, released) VALUES (?, ?, ?)', (game['id'], request.POST['version'], request.POST['released']))
        DB.commit()
        return '', 307, {'Location': f'/{game["name"]}/{request.POST["version"]}/'}
    return render(request, 'html/add_version.html', {'game': game})


@route(r'/([\s\w%-]+)/', 'GET')
@require_game
def versions(request: Request, game: Dict[str, Any]):
    return render(request, 'html/game.html', {'game': game, 'versions': DB.execute('SELECT version, released FROM GameVersions WHERE game=? ORDER BY released DESC', (game['id'],)).fetchall(), 'mods': DB.execute('SELECT Mods.* FROM Mods INNER JOIN ModVersions ON Mods.id=ModVersions.mod WHERE game_version IN (SELECT id FROM GameVersions WHERE game=?)', (game['id'],)).fetchall()})


# @route(r'/([\s\w%-]+)/mods/', 'GET')
# @require_game
# def game_mods(request: Request, game: Dict[str, Any]):
#     return render(request, 'html/game_mods.html', {'game': game, 'mods': DB.execute('SELECT Mods.* FROM Mods INNER JOIN ModVersions ON Mods.id=ModVersions.mod WHERE game_version IN (SELECT id FROM GameVersions WHERE game=?)', (game['id'],)).fetchall()})


@route(r'/([\s\w%-]+)/([\s\w.%-]+)/', 'GET')
@require_version
def game_version(request: Request, game: Dict[str, Any], version: Dict[str, Any]):
    return render(request, 'html/game_version.html', {'game': game, 'version': version})


@route(r'/([\s\w%-]+)/([\s\w.%-]+)/items/', 'GET')
@require_version
def game_version_items(request: Request, game: Dict[str, Any], version: Dict[str, Any]):
    return render(request, 'html/game_version_items.html', {'game': game, 'version': version, 'items': DB.execute('SELECT GameItems.* FROM GameItems INNER JOIN GameVersionItemMap ON GameItems.id=GameVersionItemMap.item WHERE version=?', (version['id'],)).fetchall()})


@route(r'/([\s\w%-]+)/([\s\w.%-]+)/mods/', 'GET')
@require_version
def game_version_mods(request: Request, game: Dict[str, Any], version: Dict[str, Any]):
    return render(request, 'html/game_version_mods.html', {'game': game, 'version': version, 'mods': DB.execute('SELECT Mods.* FROM Mods INNER JOIN ModVersions ON Mods.id=ModVersions.mod WHERE game_version=?', (version['id'],)).fetchall()})


@route(r'/static/([\s\w./%-]+)', ['GET'], no_end_slash=True)
def static(_: Request, file: str):
    if file.startswith('game') or file.startswith('mod'):
        file, id = file.split('/', 1)
        return DB.execute(f'SELECT image FROM {file} WHERE id=?', (id,)).fetchone()['image']
    return serve(f'static/{file}')


if __name__ == '__main__':
    start_with_args()

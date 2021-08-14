from typing import Any

from litespeed import render, route
from litespeed.utils import Request

from web.db import DB
from web.utils import require_game


def add_routes():
    route('add_game/', ['GET', 'POST'], add_game)
    route(r'/([\s\w%-]+)/add_version/', ['GET', 'POST'], add_version)
    route(r'/([\s\w%-]+)/', 'GET', versions)


def add_game(request: Request):
    if request.POST:
        DB.execute('INSERT INTO Games (name, released, image) VALUES (?, ?, ?)', (request.POST['name'], request.POST['released'], list(request.FILES['icon'].values())[0].read()))
        DB.commit()
        return '', 307, {'Location': f'/{request.POST["name"]}/'}
    return render(request, 'html/add_game.html')


@require_game
def add_version(request: Request, game: dict[str, Any]):
    if request.POST:
        DB.execute('INSERT INTO GameVersions (game, version, released) VALUES (?, ?, ?)', (game['id'], request.POST['version'], request.POST['released']))
        DB.commit()
        return '', 307, {'Location': f'/{game["name"]}/{request.POST["version"]}/'}
    return render(request, 'html/add_version.html', {'game': game})


@require_game
def versions(request: Request, game: dict[str, Any]):
    return render(request, 'html/game.html', {'game': game, 'versions': DB.execute('SELECT version, released FROM GameVersions WHERE game=? ORDER BY released DESC', (game['id'],)).fetchall(), 'mods': DB.execute('SELECT Mods.* FROM Mods INNER JOIN ModVersions ON Mods.id=ModVersions.mod WHERE game_version IN (SELECT id FROM GameVersions WHERE game=?)', (game['id'],)).fetchall()})

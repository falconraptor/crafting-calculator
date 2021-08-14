from typing import Any

from litespeed import render, route
from litespeed.utils import Request

from web.db import DB
from web.utils import require_version


def add_routes():
    route(r'/([\s\w%-]+)/([\s\w.%-]+)/', 'GET', game_version)
    route(r'/([\s\w%-]+)/([\s\w.%-]+)/items/', 'GET', game_version_items)
    route(r'/([\s\w%-]+)/([\s\w.%-]+)/mods/', 'GET', game_version_mods)
    route(r'/([\s\w%-]+)/([\s\w.%-]+)/add_mod/', ['GET', 'POST'], add_mod)


@require_version
def game_version(request: Request, game: dict[str, Any], version: dict[str, Any]):
    return render(request, 'html/game_version.html', {'game': game, 'version': version})


@require_version
def game_version_items(request: Request, game: dict[str, Any], version: dict[str, Any]):
    return render(request, 'html/game_version_items.html', {'game': game, 'version': version, 'items': DB.execute('SELECT GameItems.* FROM GameItems INNER JOIN GameVersionItemMap ON GameItems.id=GameVersionItemMap.item WHERE version=?', (version['id'],)).fetchall()})


@require_version
def game_version_mods(request: Request, game: dict[str, Any], version: dict[str, Any]):
    return render(request, 'html/game_version_mods.html', {'game': game, 'version': version, 'mods': DB.execute('SELECT Mods.* FROM Mods INNER JOIN ModVersions ON Mods.id=ModVersions.mod WHERE game_version=?', (version['id'],)).fetchall()})


@require_version
def add_mod(request: Request, game: dict[str, Any], version: dict[str, Any]):
    if request.POST:  # TODO check if mod exists already
        DB.execute('INSERT INTO Mods (game, name, description, created, image) VALUES (?, ?, ?, ?, ?)', (game['id'], request.POST['name'], request.POST['description'], request.POST['created'], list(request.FILES['icon'].values())[0].read()))
        DB.commit()
        return '', 307, {'Location': f'/{game["name"]}/mods/{request.POST["name"]}/'}
    return render(request, 'html/add_mod.html', {'game': game, 'version': version})

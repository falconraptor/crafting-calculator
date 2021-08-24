from typing import Any

from litespeed import render, route
from litespeed.utils import Request

from web.db import DB
from web.utils import require_version


def add_routes():
    route(r'/([\s\w%-]+)/([\s\w.%-]+)/', 'GET', game_version)
    route(r'/([\s\w%-]+)/([\s\w.%-]+)/add_mod/', ['GET', 'POST'], add_mod)
    route(r'/([\s\w%-]+)/([\s\w.%-]+)/add_item/', ['GET', 'POST'], add_item)


@require_version
def game_version(request: Request, game: dict[str, Any], version: dict[str, Any]):
    return render(request, 'html/game_version.html', {'game': game, 'version': version, 'items': DB.execute('SELECT GameItems.* FROM GameItems INNER JOIN GameVersionItemMap ON GameItems.id=GameVersionItemMap.item WHERE version=? ORDER BY name', (version['id'],)).fetchall(), 'mods': DB.execute('SELECT Mods.* FROM Mods INNER JOIN ModVersions ON Mods.id=ModVersions.mod WHERE game_version=? ORDER BY name', (version['id'],)).fetchall()})


@require_version
def add_mod(request: Request, game: dict[str, Any], version: dict[str, Any]):
    if request.POST:
        if not request.POST.get('id', True):
            DB.execute('INSERT INTO Mods (game, name, description, created, image) VALUES (?, ?, ?, ?, ?)', (game['id'], request.POST['name'], request.POST['description'], request.POST['created'], list(request.FILES['icon'].values())[0].read()))
            request.POST['id'] = DB.execute('SELECT last_insert_rowid() as row').fetchone()['row']
        DB.execute('INSERT INTO ModVersions (mod, version, game_version, released) VALUES (?, ?, ?, ?)', (request.POST['id'], request.POST['version'], version['id'], request.POST['released']))
        DB.commit()
        return '', 307, {'Location': f'/{game["name"]}/mods/{request.POST["name"]}/{request.POST["version"]}/'}
    return render(request, 'html/add_mod.html', {'game': game, 'version': version, 'mods': DB.execute('SELECT name, created, id FROM Mods WHERE game=? AND id NOT IN (SELECT mod FROM ModVersions WHERE game_version=?) ORDER BY name', (game['id'], version['id'])).fetchall()})


@require_version
def add_item(request: Request, game: dict[str, Any], version: dict[str, Any]):
    if request.POST:
        if not request.POST.get('id', True):
            DB.execute('INSERT INTO GameItems (name, image) VALUES (?, ?)', (request.POST['name'], list(request.FILES['icon'].values())[0].read()))
            request.POST['id'] = DB.execute('SELECT last_insert_rowid() as row').fetchone()['row']
        DB.execute('INSERT INTO GameVersionItemMap VALUES (?, ?)', (version['id'], request.POST['id']))
        DB.commit()
        return '', 307, {'Location': f'/{game["name"]}/{version["version"]}/items/{request.POST["name"]}/'}
    return render(request, 'html/add_item.html', {'game': game, 'version': version, 'items': DB.execute('SELECT name, GameItems.id FROM GameItems INNER JOIN GameVersionItemMap GVIM ON GameItems.id = GVIM.item INNER JOIN GameVersions GV ON GV.id = GVIM.version WHERE game=? AND GameItems.id NOT IN (SELECT item FROM GameVersionItemMap WHERE version=?) ORDER BY name', (game['id'], version['id'])).fetchall()})

from web.db import DB


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
        if not (version := DB.execute('SELECT version, released, id FROM GameVersions WHERE game=? and version=?', (game['id'], version_kwargs or version_args)).fetchone()):
            return '', 307, {'Location': f'/{game["name"]}/add_version/'}
        if version_kwargs:
            kwargs['version'] = version
        if version_args:
            args = args[:2] + (version,) + args[3:]
        return f(*args, **kwargs)
    return wrapped


def require_mod(f):
    @require_version
    def wrapped(*args, **kwargs):
        game = kwargs.get('game', args[1] if len(args) > 1 else '')
        mod_kwargs = kwargs.get('mod', None)
        mod_args = args[2] if len(args) > 2 else None
        if not (mod := DB.execute('SELECT name, description, created FROM Mods WHERE game=? AND name=?', (game['id'], mod_kwargs or mod_args)).fetchone()):
            return '', 307, {'Location': f'/{game["name"]}/add_version/'}
        if mod_kwargs:
            kwargs['mod'] = mod
        if mod_args:
            args = args[:2] + (mod,) + args[3:]
        return f(*args, **kwargs)
    return wrapped


# def require_mod_version(f):
#     @require_mod
#     def wrapped(*args, **kwargs):
#         game = kwargs.get('game', args[1] if len(args) > 1 else '')
#         mod = kwargs.get('mod', args[2] if len(args) > 2 else '')
#         version_kwargs = kwargs.get('version', None)
#         version_args = args[3] if len(args) > 3 else None
#         if not (version := DB.execute('SELECT version, `release` FROM ModVersions WHERE game=? and version=?', (game['id'], version_kwargs or version_args)).fetchone()):
#             return '', 307, {'Location': f'/{game["name"]}/add_version/'}
#         if version_kwargs:
#             kwargs['version'] = version
#         if version_args:
#             args = args[:2] + (version,) + args[3:]
#         return f(*args, **kwargs)
#     return wrapped

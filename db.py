from os.path import exists
from sqlite3 import connect


def setup_db():
    create = not exists('crafting.db')
    db = connect('crafting.db')
    db.row_factory = lambda cursor, row: {col[0]: row[idx] for idx, col in enumerate(cursor.description)}
    if create:
        db.execute('CREATE TABLE Games (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL, released DATE NOT NULL, item_unit TEXT NOT NULL DEFAULT "", fluid_unit TEXT NOT NULL DEFAULT "", image BLOB)')
        db.execute('CREATE TABLE GameVersions (id INTEGER PRIMARY KEY AUTOINCREMENT, game INT NOT NULL, version TEXT NOT NULL, released DATE NOT NULL, FOREIGN KEY (game) REFERENCES Games(id))')
        db.execute('CREATE TABLE GameItems (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL, image BLOB)')
        db.execute('CREATE TABLE GameMechanics (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL, image BLOB)')
        db.execute('CREATE TABLE GameVersionItemMap (version INT NOT NULL, item INT NOT NULL, FOREIGN KEY (version) REFERENCES GameVersions(id), FOREIGN KEY (item) REFERENCES GameItems(id))')
        db.execute('CREATE TABLE GameVersionMechanicMap (version INT NOT NULL, mechanic INT NOT NULL, FOREIGN KEY (version) REFERENCES GameVersions(id), FOREIGN KEY (mechanic) REFERENCES GameMechanics(id))')
        db.execute('CREATE TABLE GameVersionRecipeMap (version INT NOT NULL, recipe INT NOT NULL, FOREIGN KEY (version) REFERENCES GameVersions(id), FOREIGN KEY (recipe) REFERENCES GameRecipes(id))')
        db.execute('CREATE TABLE GameRecipes (id INTEGER PRIMARY KEY AUTOINCREMENT, mechanic INT NOT NULL, FOREIGN KEY (mechanic) REFERENCES GameMechanics(id))')
        db.execute('CREATE TABLE GameRecipeItems (recipe INT NOT NULL, type TEXT NOT NULL, item INT NOT NULL, amount FLOAT NOT NULL DEFAULT 1, FOREIGN KEY (recipe) REFERENCES GameRecipes(id), FOREIGN KEY (item) REFERENCES GameItems(id))')
        db.execute('CREATE TABLE Mods (id INTEGER PRIMARY KEY AUTOINCREMENT, game INT NOT NULL, name TEXT NOT NULL, description TEXT NOT NULL, created DATE NOT NULL, image BLOB, FOREIGN KEY (game) REFERENCES Game(id))')
        db.execute('CREATE TABLE ModVersions (id INTEGER PRIMARY KEY AUTOINCREMENT, mod INT NOT NULL, version TEXT NOT NULL, game_version INT NOT NULL, release DATE NOT NULL, FOREIGN KEY (game_version) REFERENCES GameVersions(id))')
        db.execute('CREATE TABLE ModItems (id INTEGER PRIMARY KEY AUTOINCREMENT, mod INT NOT NULL, name TEXT NOT NULL, image BLOB, FOREIGN KEY (mod) REFERENCES Mods(id))')
        db.execute('CREATE TABLE ModMechanics (id INTEGER PRIMARY KEY AUTOINCREMENT, mod INT NOT NULL, name TEXT NOT NULL, image BLOB, FOREIGN KEY (mod) REFERENCES Mods(id))')
        db.execute('CREATE TABLE ModVersionItemMap (version INT NOT NULL, item INT NOT NULL, FOREIGN KEY (version) REFERENCES ModVersions(id), FOREIGN KEY (item) REFERENCES ModItems(id))')
        db.execute('CREATE TABLE ModVersionMechanicMap (version INT NOT NULL, mechanic INT NOT NULL, FOREIGN KEY (version) REFERENCES ModVersions(id), FOREIGN KEY (mechanic) REFERENCES ModMechanics(id))')
        db.execute('CREATE TABLE ModVersionRecipeMap (version INT NOT NULL, recipe INT NOT NULL, FOREIGN KEY (version) REFERENCES ModVersions(id), FOREIGN KEY (recipe) REFERENCES ModRecipes(id))')
        db.execute('CREATE TABLE ModVersionRequirements (version INT NULL, requires INT NOT NULL, FOREIGN KEY (version) REFERENCES ModVersions(id), FOREIGN KEY (requires) REFERENCES ModVersions(id))')
        db.execute('CREATE TABLE ModRecipes (id INTEGER PRIMARY KEY AUTOINCREMENT, mod_mechanic INT, game_mechanic INT, FOREIGN KEY (mod_mechanic) REFERENCES ModMechanic(id), FOREIGN KEY (game_mechanic) REFERENCES GameMechanic(id))')
        db.execute('CREATE TABLE ModRecipeItems (recipe INT NOT NULL, type TEXT NOT NULL, mod_item INT, game_item INT, amount FLOAT NOT NULL DEFAULT 1, FOREIGN KEY (recipe) REFERENCES ModRecipes(id), FOREIGN KEY (mod_item) REFERENCES ModItems(id), FOREIGN KEY (game_item) REFERENCES GameItems(id))')
        db.execute('CREATE TABLE Modpack (id INTEGER PRIMARY KEY AUTOINCREMENT, game INT NOT NULL, name TEXT NOT NULL, description TEXT NULL NOT, created DATE NOT NULL, image BLOB, FOREIGN KEY (game) REFERENCES Games(id))')
        db.execute('CREATE TABLE ModpackVerions (id INTEGER PRIMARY KEY AUTOINCREMENT, modpack INT NOT NULL, version TEXT NOT NULL, game_version INT NOT NULL, release DATE NOT NULL, FOREIGN KEY (modpack) REFERENCES Modpacks(id), FOREIGN KEY (game_version) REFERENCES GameVersions(id))')
        db.execute('CREATE TABLE ModpackMods (modpack_version INT NOT NULL, mod_version INT NOT NULL, FOREIGN KEY (modpack_version) REFERENCES ModpackVersions(id), FOREIGN KEY (mod_version) REFERENCES ModVersions(id))')
        db.execute('CREATE TABLE ModpackRecipes (id PRIMARY KEY AUTOINCREMENT, modpack_version INT NOT NULL, mod_recipe INT, game_recipe INT, FOREIGN KEY (mod_recipe) REFERENCES ModRecipes(id), FOREIGN KEY (game_recipe) REFERENCES GameRecipes(id))')
        db.execute('CREATE TABLE ModpackRecipeItems (recipe INT NOT NULL, type TEXT NOT NULL, mod_item INT, game_item INT, amount FLOAT NOT NULL DEFAULT 1, FOREIGN KEY (recipe) REFERENCES ModpackRecipes(id), FOREIGN KEY (mod_item) REFERENCES ModItems(id), FOREIGN KEY (game_item) REFERENCES GameItems(id))')
    return db


def fetchall(sql, *params):
    with DB.cursor() as cursor:
        cursor.execute(sql, params)
        return cursor.fetchall()


DB = setup_db()

from gridworld.direction import Direction
from gridworld.game_repo import GameRepo
from gridworld.database import Database
from gridworld.game import Game


def _insert_game(conn, game_json_str):
    sql = r"""
    INSERT INTO games (data) VALUES (?)
    """
    cursor = conn.cursor()
    cursor.execute(sql, (game_json_str,))
    conn.commit()
    cursor.close()


def _select_games(conn):
    sql = r"""
    SELECT id, data FROM games ORDER BY id
    """
    results = []
    cursor = conn.cursor()
    for game_id, game_data in cursor.execute(sql):
        results.append((game_id, game_data))
    conn.commit()
    cursor.close()
    return results


def test_game_repo_init():
    db = Database()
    repo = GameRepo(db)
    assert repo.db is db


def test_game_repo_get_all_games():
    db = Database()
    game1 = Game.from_dimensions((2, 5))
    game2 = Game.from_dimensions((3, 4))
    _insert_game(db.conn, game1.to_json_str())
    _insert_game(db.conn, game2.to_json_str())
    repo = GameRepo(db)
    games_with_ids = repo.get_all_games()
    assert len(games_with_ids) == 2
    assert [game_id for game_id, _game in games_with_ids] == [1, 2]
    assert [game for _game_id, game in games_with_ids] == [game1, game2]


def test_game_repo_get_game_by_id():
    db = Database()
    game1 = Game.from_dimensions((2, 5))
    game2 = Game.from_dimensions((3, 4))
    _insert_game(db.conn, game1.to_json_str())
    _insert_game(db.conn, game2.to_json_str())
    repo = GameRepo(db)
    got = repo.get_game_by_id(2)
    assert got == game2
    got = repo.get_game_by_id(42)
    assert got is None


def test_game_repo_create_game():
    db = Database()
    game1 = Game.from_dimensions((2, 5))
    game2 = Game.from_dimensions((3, 4))
    _insert_game(db.conn, game1.to_json_str())
    _insert_game(db.conn, game2.to_json_str())
    repo = GameRepo(db)
    games = _select_games(db.conn)
    # preconditions:
    assert [game_id for game_id, _game_data in games] == [1, 2]
    assert [
        Game.from_json_str(game_data) for _game_id, game_data in games
    ] == [game1, game2]
    got = repo.create_game((1, 2))
    # postconditions:
    games = _select_games(db.conn)
    assert got == 3
    assert [game_id for game_id, _game_data in games] == [1, 2, 3]
    assert [
        Game.from_json_str(game_data).grid.dimensions
        for _game_id, game_data in games
    ] == [(2, 5), (3, 4), (1, 2)]


def test_game_repo_update_game_by_id():
    db = Database()
    game1 = Game.from_dimensions((2, 5))
    game2 = Game.from_dimensions((3, 4))
    old_game2 = Game.from_json_str(game2.to_json_str())
    assert game2 == old_game2
    _insert_game(db.conn, game1.to_json_str())
    _insert_game(db.conn, game2.to_json_str())
    repo = GameRepo(db)
    moved = game2.move(Direction.RIGHT)
    assert moved is True
    assert game2 != old_game2
    got = repo.update_game_by_id(2, game2)
    assert got is True
    games = _select_games(db.conn)
    assert [game_id for game_id, _game_data in games] == [1, 2]
    assert [
        Game.from_json_str(game_data) for _game_id, game_data in games
    ] == [game1, game2]

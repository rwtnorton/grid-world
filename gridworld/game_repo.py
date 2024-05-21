from typing import Iterable, Tuple, Optional

from gridworld.game import Game
from gridworld.database import Database


class GameRepo:
    def __init__(self, db: Database):
        self.db = db

    def get_all_games(self) -> Iterable[Tuple[int, Game]]:
        select_all_games_sql = r"""
        SELECT id, data FROM games ORDER BY id
        """
        result = []
        cursor = self.db.conn.cursor()
        for game_id, game_json_str in cursor.execute(select_all_games_sql):
            result.append((game_id, Game.from_json_str(game_json_str)))
        cursor.close()
        return result

    def get_game_by_id(self, game_id: int) -> Optional[Game]:
        select_game_by_id_sql = r"""
        SELECT data FROM games WHERE id = ? LIMIT 1
        """
        cursor = self.db.conn.cursor()
        res = cursor.execute(select_game_by_id_sql, (game_id,))
        got = res.fetchone()
        cursor.close()
        if got is not None:
            data = got[0]
            return Game.from_json_str(data)
        return None

    def create_game(self, dimensions: Tuple[int, int]) -> int:
        insert_game_sql = r"""
        INSERT INTO games (data) VALUES (?) RETURNING id
        """
        new_game = Game.from_dimensions(dimensions)
        json_str = new_game.to_json_str()
        cursor = self.db.conn.cursor()
        res = cursor.execute(insert_game_sql, (json_str,))
        (game_id,) = res.fetchone()
        self.db.conn.commit()
        cursor.close()
        return game_id

    def update_game_by_id(self, game_id: int, game: Game) -> bool:
        update_game_sql = r"""
        UPDATE games SET data = ? WHERE id = ?
        """
        json_str = game.to_json_str()
        cursor = self.db.conn.cursor()
        res = cursor.execute(update_game_sql, (json_str, game_id))
        self.db.conn.commit()
        cursor.close()
        return res.rowcount == 1

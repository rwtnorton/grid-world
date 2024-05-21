from gridworld.database import Database


def test_database_init():
    db = Database()
    assert db._db_path == ":memory:"
    assert db.conn.execute(r"select 42").fetchone()[0] == 42


def test_database_ensure_migrations_ran():
    db = Database()
    table_names = []
    cur = db.conn.cursor()
    for res in cur.execute(
        r"select name from sqlite_master where type='table'"
    ):
        table_names.append(res[0])
    cur.close()
    assert "games" in table_names

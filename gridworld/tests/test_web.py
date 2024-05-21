import json

from fastapi.testclient import TestClient
from unittest.mock import patch

from gridworld.database import Database
from gridworld.direction import Direction
from gridworld.game import Game
from gridworld.web import app

client = TestClient(app)


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


@patch("gridworld.web.get_db")
@patch("gridworld.game_repo.GameRepo.get_all_games")
def test_get_all_games(get_all_games_mock, get_db_mock):
    get_db_mock.return_value = Database()
    game1 = Game.from_dimensions((1, 1))
    game2 = Game.from_dimensions((2, 2))
    get_all_games_mock.return_value = [
        (1, game1),
        (2, game2),
    ]
    response = client.get("/games")
    assert response.status_code == 200
    assert response.json() == {
        "games": {
            "1": json.loads(game1.to_json_str()),
            "2": json.loads(game2.to_json_str()),
        }
    }


@patch("gridworld.web.get_db")
@patch("gridworld.game_repo.GameRepo.get_game_by_id")
def test_get_game_by_id_found(get_game_by_id_mock, get_db_mock):
    get_db_mock.return_value = Database()
    game1 = Game.from_dimensions((1, 1))
    get_game_by_id_mock.return_value = game1
    response = client.get("/games/1")
    assert response.status_code == 200
    assert response.json() == json.loads(game1.to_json_str())


@patch("gridworld.web.get_db")
@patch("gridworld.game_repo.GameRepo.get_game_by_id")
def test_get_game_by_id_not_found(get_game_by_id_mock, get_db_mock):
    get_db_mock.return_value = Database()
    get_game_by_id_mock.return_value = None
    response = client.get("/games/42")
    assert response.status_code == 404
    assert response.json() == {"detail": "game not found"}


@patch("gridworld.web.get_db")
@patch("gridworld.game_repo.GameRepo.create_game")
def test_create_game_happy(create_game_mock, get_db_mock):
    get_db_mock.return_value = Database()
    create_game_mock.return_value = 17
    response = client.post("/games", json={"dimensions": (2, 3)})
    assert response.status_code == 201
    assert response.json() == {"game_id": 17}


@patch("gridworld.web.get_db")
@patch("gridworld.game_repo.GameRepo.create_game")
def test_create_game_bad_param(create_game_mock, get_db_mock):
    get_db_mock.return_value = Database()
    create_game_mock.return_value = "whatever"
    response = client.post("/games", json={"foo": "bar"})
    assert response.status_code == 422
    assert response.json() == {
        "detail": [
            {
                "input": {
                    "foo": "bar",
                },
                "loc": [
                    "body",
                    "dimensions",
                ],
                "msg": "Field required",
                "type": "missing",
            }
        ]
    }


@patch("gridworld.web.get_db")
@patch("gridworld.game_repo.GameRepo.get_game_by_id")
def test_get_game_status_by_id_not_found(get_game_by_id_mock, get_db_mock):
    get_db_mock.return_value = Database()
    get_game_by_id_mock.return_value = None
    response = client.get("/games/42/status")
    assert response.status_code == 404
    assert response.json() == {"detail": "game not found"}


@patch("gridworld.web.get_db")
@patch("gridworld.game_repo.GameRepo.get_game_by_id")
def test_get_game_status_by_id_found_win(get_game_by_id_mock, get_db_mock):
    get_db_mock.return_value = Database()
    game1 = Game.from_dimensions((1, 2))
    game1.agent.position = game1.goal_position
    assert game1.is_win() is True
    get_game_by_id_mock.return_value = game1
    response = client.get("/games/1/status")
    assert response.status_code == 200
    assert response.json() == {"status": "win"}


@patch("gridworld.web.get_db")
@patch("gridworld.game_repo.GameRepo.get_game_by_id")
def test_get_game_status_by_id_found_loss(get_game_by_id_mock, get_db_mock):
    get_db_mock.return_value = Database()
    game1 = Game.from_dimensions((1, 2))
    game1.agent.health = 0
    assert game1.is_loss() is True
    get_game_by_id_mock.return_value = game1
    response = client.get("/games/2/status")
    assert response.status_code == 200
    assert response.json() == {"status": "loss"}


@patch("gridworld.web.get_db")
@patch("gridworld.game_repo.GameRepo.get_game_by_id")
def test_get_game_status_by_id_found_ongoing(get_game_by_id_mock, get_db_mock):
    get_db_mock.return_value = Database()
    game1 = Game.from_dimensions((1, 2))
    assert game1.is_win() is False
    assert game1.is_loss() is False
    get_game_by_id_mock.return_value = game1
    response = client.get("/games/3/status")
    assert response.status_code == 200
    assert response.json() == {"status": "ongoing"}


@patch("gridworld.web.get_db")
@patch("gridworld.game_repo.GameRepo.get_game_by_id")
@patch("gridworld.game_repo.GameRepo.update_game_by_id")
def test_update_game_by_id_happy(
    update_game_by_id_mock, get_game_by_id_mock, get_db_mock
):
    get_db_mock.return_value = Database()
    game1 = Game.from_dimensions((1, 2))
    old_game1 = Game.from_json_str(game1.to_json_str())
    assert game1 == old_game1
    get_game_by_id_mock.return_value = game1
    update_game_by_id_mock.return_value = "whatever"
    response = client.put("/games/1/direction", json={"direction": "R"})
    # Verify that the PUT mutated game1.
    assert game1 != old_game1
    # Verify that we can perform the same mutation with the same results.
    assert old_game1.move(Direction.RIGHT) is True
    assert game1 == old_game1
    assert response.status_code == 200
    assert response.json() == json.loads(game1.to_json_str())


@patch("gridworld.web.get_db")
@patch("gridworld.game_repo.GameRepo.get_game_by_id")
@patch("gridworld.game_repo.GameRepo.update_game_by_id")
def test_update_game_by_id_not_found(
    update_game_by_id_mock, get_game_by_id_mock, get_db_mock
):
    get_db_mock.return_value = Database()
    get_game_by_id_mock.return_value = None
    update_game_by_id_mock.return_value = "whatever"
    response = client.put("/games/42/direction", json={"direction": "R"})
    assert response.status_code == 404
    assert response.json() == {"detail": "game not found"}


@patch("gridworld.web.get_db")
@patch("gridworld.game_repo.GameRepo.get_game_by_id")
@patch("gridworld.game_repo.GameRepo.update_game_by_id")
def test_update_game_by_id_invalid_params(
    update_game_by_id_mock, get_game_by_id_mock, get_db_mock
):
    get_db_mock.return_value = Database()
    game1 = Game.from_dimensions((1, 2))
    old_game1 = Game.from_json_str(game1.to_json_str())
    assert game1 == old_game1
    get_game_by_id_mock.return_value = game1
    update_game_by_id_mock.return_value = "whatever"
    response = client.put("/games/1/direction", json={"foo": "bar"})
    assert response.status_code == 422
    assert response.json() == {
        "detail": [
            {
                "input": {
                    "foo": "bar",
                },
                "loc": [
                    "body",
                    "direction",
                ],
                "msg": "Field required",
                "type": "missing",
            }
        ]
    }
    # Verify that no mutation occurred.
    assert game1 == old_game1


@patch("gridworld.web.get_db")
@patch("gridworld.game_repo.GameRepo.get_game_by_id")
@patch("gridworld.game_repo.GameRepo.update_game_by_id")
def test_update_game_by_id_bump_into_wall(
    update_game_by_id_mock, get_game_by_id_mock, get_db_mock
):
    get_db_mock.return_value = Database()
    game1 = Game.from_dimensions((1, 2))
    old_game1 = Game.from_json_str(game1.to_json_str())
    assert game1 == old_game1
    get_game_by_id_mock.return_value = game1
    update_game_by_id_mock.return_value = "whatever"
    response = client.put("/games/1/direction", json={"direction": "U"})
    assert response.status_code == 200
    assert response.json() == {"message": "direction had no effect: U"}
    # Verify that no mutation occurred.
    assert game1 == old_game1

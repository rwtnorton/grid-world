import json
import os
from typing import Tuple

from fastapi import FastAPI, Depends, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from gridworld.database import Database
from gridworld.direction import Direction
from gridworld.game import Game
from gridworld.game_repo import GameRepo

app = FastAPI()

db: Database | None = None


def get_db():
    db_name = os.getenv("DB_NAME", None)
    global db
    if db_name is None or db_name == ":memory:":
        db = Database()
    else:
        db = Database(f"{db_name}.sqlite3")
    return db


def get_game_repo():
    game_repo = GameRepo(db=get_db())
    yield game_repo


@app.get("/health")
async def health():
    return {"status": "ok"}


#
# Note:  Much of the JSON awkwardness of my approach below comes down to how
#        much FastAPI expects users to lean into pydantic models, which
#        I have avoided unless absolutely necessary.
#        Modeling requests and responses is fine, but I very much did
#        not want to pollute my internal models (e.g., Game) with
#        the peculiarities of pydantic.  Core business logic should be
#        fully modular, pluggable into web (and other) interfaces, and
#        independent of the details of clients, IMHO.  The dependency graph
#        should be acyclic.
#
#        Guess I will chalk this experience up to my first time using
#        FastAPI in anger.
#


@app.get("/games")
async def get_all_games(repo: GameRepo = Depends(get_game_repo)):
    id_game_pairs = repo.get_all_games()
    # Kludgy
    json_str = f"""
    {{
      "games": {{
        {', '.join(
          f'"{g_id}": {g.to_json_str()}' for g_id, g in id_game_pairs)}
      }}
    }}
    """
    return JSONResponse(content=json.loads(json_str))


@app.get("/games/{game_id}")
async def get_game_by_id(
    game_id: int, repo: GameRepo = Depends(get_game_repo)
):
    game_maybe = repo.get_game_by_id(game_id)
    if game_maybe is None:
        raise HTTPException(status_code=404, detail="game not found")
    return JSONResponse(content=json.loads(game_maybe.to_json_str()))


class GridDimensions(BaseModel):
    dimensions: Tuple[int, int]


@app.post("/games")
async def create_game(
    dims: GridDimensions, repo: GameRepo = Depends(get_game_repo)
):
    game_id = repo.create_game(dims.dimensions)
    return {"game_id": game_id}


class AgentDirection(BaseModel):
    direction: str


@app.put("/games/{game_id}/direction")
async def update_agent_direction(
    game_id: int,
    agent_dir: AgentDirection,
    repo: GameRepo = Depends(get_game_repo),
):
    game_maybe = repo.get_game_by_id(game_id)
    if game_maybe is None:
        raise HTTPException(status_code=404, detail="game not found")
    game: Game = game_maybe  # better name, no maybe
    try:
        d = Direction.from_str(agent_dir.direction)
    except ValueError:
        raise HTTPException(
            status_code=400,
            detail=f"invalid direction: {agent_dir.direction}",
        )
    if game.move(d):
        repo.update_game_by_id(game_id, game)
        return JSONResponse(content=json.loads(game.to_json_str()))
    return {"message": f"direction had no effect: {agent_dir.direction}"}


@app.get("/games/{game_id}/status")
async def get_game_status_by_id(
    game_id: int, repo: GameRepo = Depends(get_game_repo)
):
    game_maybe = repo.get_game_by_id(game_id)
    if game_maybe is None:
        raise HTTPException(status_code=404, detail="game not found")
    game: Game = game_maybe
    if game.is_win():
        return {"status": "win"}
    elif game.is_loss():
        return {"status": "loss"}
    else:
        return {"status": "ongoing"}

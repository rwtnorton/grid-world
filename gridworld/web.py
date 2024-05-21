import json
from typing import Tuple

from fastapi import FastAPI, Depends, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from gridworld.database import Database
from gridworld.game_repo import GameRepo

app = FastAPI()


# TODO: How to provide the db file name from main.py?
def get_db():
    db = Database("some_db.sqlite3")
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
        raise HTTPException(status_code=404, detail="Game not found")
    return JSONResponse(content=json.loads(game_maybe.to_json_str()))


class GridDimensions(BaseModel):
    dimensions: Tuple[int, int]


@app.post("/games")
async def create_game(
    dims: GridDimensions, repo: GameRepo = Depends(get_game_repo)
):
    game_id = repo.create_game(dims.dimensions)
    return {"game_id": game_id}


#
# @app.put("/games/{game_id}")
# async def create_game(
#     dims: GridDimensions, repo: GameRepo = Depends(get_game_repo)
# ):
#     game_id = repo.create_game(dims.dimensions)
#     return {"game_id": game_id}

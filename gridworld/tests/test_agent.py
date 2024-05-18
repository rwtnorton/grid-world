import pytest

from gridworld.agent import Agent
import gridworld.agent as agent


def test_agent_init():
    pos = (1, 2)
    h, mh = 10, 100
    m, mm = 20, 200
    ag = Agent(pos, health=h, max_health=mh, moves=m, max_moves=mm)
    assert ag.position == pos
    assert ag.health == h
    assert ag.max_health == mh
    assert ag.moves == m
    assert ag.max_moves == mm


def test_agent_init_defaults():
    pos = (1, 2)
    ag = Agent(pos)
    assert ag.position == pos
    assert ag.health == agent.DEFAULT_HEALTH
    assert ag.max_health == agent.DEFAULT_HEALTH
    assert ag.moves == agent.DEFAULT_MOVES
    assert ag.max_moves == agent.DEFAULT_MOVES


def test_agent_init_bad_args():
    pos = (1, 2)
    with pytest.raises(ValueError) as max_h_err:
        Agent(pos, max_health=0)
    assert "non-positive max_health: 0" in str(max_h_err.value)
    #
    with pytest.raises(ValueError) as max_m_err:
        Agent(pos, max_moves=0)
    assert "non-positive max_moves: 0" in str(max_m_err.value)
    #
    with pytest.raises(ValueError) as too_lil_health_err:
        Agent(pos, health=0, max_health=10)
    assert "invalid health: 0, max=10" in str(too_lil_health_err.value)
    #
    with pytest.raises(ValueError) as too_big_health_err:
        Agent(pos, health=11, max_health=10)
    assert "invalid health: 11, max=10" in str(too_big_health_err.value)
    #
    with pytest.raises(ValueError) as too_lil_moves_err:
        Agent(pos, moves=0, max_moves=10)
    assert "invalid moves: 0, max=10" in str(too_lil_moves_err.value)
    #
    with pytest.raises(ValueError) as too_big_moves_err:
        Agent(pos, moves=11, max_moves=10)
    assert "invalid moves: 11, max=10" in str(too_big_moves_err.value)


def test_agent_to_json_str():
    pos = (1, 2)
    h, mh = 10, 100
    m, mm = 20, 200
    ag = Agent(pos, health=h, max_health=mh, moves=m, max_moves=mm)
    assert ag.to_json_str() == (
        '{"position": [1, 2],'
        + ' "health": 10, "max_health": 100,'
        + ' "moves": 20, "max_moves": 200}'
    )


def test_agent_from_json_str():
    pos = (1, 2)
    h, mh = 10, 100
    m, mm = 20, 200
    ag = Agent(pos, health=h, max_health=mh, moves=m, max_moves=mm)
    s = (
        '{"position": [1, 2],'
        + ' "health": 10, "max_health": 100,'
        + ' "moves": 20, "max_moves": 200}'
    )
    assert Agent.from_json_str(s) == ag


def test_agent_is_healthy():
    pos = (1, 2)
    h, mh = 10, 100
    m, mm = 20, 200
    ag = Agent(pos, health=h, max_health=mh, moves=m, max_moves=mm)
    assert ag.is_healthy() is True
    ag.health = 0
    assert ag.is_healthy() is False


def test_agent_is_motive():
    pos = (1, 2)
    h, mh = 10, 100
    m, mm = 20, 200
    ag = Agent(pos, health=h, max_health=mh, moves=m, max_moves=mm)
    assert ag.is_motive() is True
    ag.moves = 0
    assert ag.is_motive() is False


def test_agent_is_alive():
    pos = (1, 2)
    h, mh = 10, 100
    m, mm = 20, 200
    ag = Agent(pos, health=h, max_health=mh, moves=m, max_moves=mm)
    assert ag.is_alive() is True
    ag.health = 0
    assert ag.is_alive() is False
    ag.health = h
    assert ag.is_alive() is True
    ag.moves = 0
    assert ag.is_alive() is False


def test_agent_is_dead():
    pos = (1, 2)
    h, mh = 10, 100
    m, mm = 20, 200
    ag = Agent(pos, health=h, max_health=mh, moves=m, max_moves=mm)
    assert ag.is_dead() is False
    ag.health = 0
    assert ag.is_dead() is True
    ag.health = h
    assert ag.is_dead() is False
    ag.moves = 0
    assert ag.is_dead() is True

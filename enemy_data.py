ENEMY_SPAWN_DATA = [
    {
        # 1
        "fly": 5,
        "ant": 0,
        "mosquito": 0,
        "cockroach": 0
    },
    {
        # 2
        "fly": 30,
        "ant": 0,
        "mosquito": 0,
        "cockroach": 0
    },
    {
        # 3
        "fly": 20,
        "ant": 10,
        "mosquito": 0,
        "cockroach": 0
    },
    {
        # 4
        "fly": 15,
        "ant": 15,
        "mosquito": 0,
        "cockroach": 0
    },
    {
        # 5
        "fly": 0,
        "ant": 15,
        "mosquito": 10,
        "cockroach": 0
    },
    {
        # 6
        "fly": 10,
        "ant": 15,
        "mosquito": 15,
        "cockroach": 1
    },
    {
        # 7
        "fly": 10,
        "ant": 15,
        "mosquito": 10,
        "cockroach": 5
    },

]

ENEMY_DATA = {
    "fly": {
        "flying": True,
        "health": 5,
        "speed": 2,
        "reward": 1
    },
    "ant": {
        "flying": False,
        "health": 15,
        "speed": 1,
        "reward": 5
    },
    "mosquito": {
        "flying": True,
        "health": 20,
        "speed": 4,
        "reward": 15
    },
    "cockroach": {
        "flying": False,
        "health": 30,
        "speed": 6,
        "reward": 50
    }

}

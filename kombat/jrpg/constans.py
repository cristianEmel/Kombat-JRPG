from typing import Dict

HITS: Dict[str, Dict[str, str]] = {
    "player1": [
        {
            "energy": 3,
            "name": "Taladoken",
            "combination": "DSDP"
        },
        {
            "energy": 2,
            "name": "Remuyuken",
            "combination": "SDK"
        },
        {
            "energy": 1,
            "name": "Puño",
            "combination": "P"
        },
        {
            "energy": 1,
            "name": "Patada",
            "combination": "K"
        },
    ],
    "player2": [
        {
            "energy": 3,
            "name": "Remuyuken",
            "combination": "SAK"
        },
        {
            "energy": 2,
            "name": "Taladoken",
            "combination": "ASAP"
        },
        {
            "energy": 1,
            "name": "Puño",
            "combination": "P"
        },
        {
            "energy": 1,
            "name": "Patada",
            "combination": "K"
        },
    ]
}

MESSAGE: Dict[str, str] = {
    "player1-dsdp": "Tonyn usa un Taladoken",
    "player1-sdk": "Tonyn usa un Remuyuken",
    "player1-p": "Tonyn le da un puñetazo al pobre Arnaldor",
    "player1-k": "Tonyn avanza y da una patada",
    "player1": "Tonyn se mueve",
    "player1-win": "Tonyn gana la pelea",
    "player2-sak": "Arnaldor usa un Remuyuke",
    "player2-asap": "Arnaldor usa un Taladoken",
    "player2-p": "Arnaldor le da un puñetazo al pobre Tonyn",
    "player2-k": "Arnaldor avanza y da una patada",
    "player2": "Arnaldor se mueve",
    "player2-win": "Arnaldor gana la pelea",
}
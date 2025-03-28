import random
import json

from src.cfg.game_settings import GameSettings


class EnemySettings:

    def __init__(self) -> None:
        self.enemy_path = "assets/cfg/enemies.json"
        self.enemies_config = json.load(open(self.enemy_path))

    def get_enemies(self) -> dict:
        return self.enemies_config

    

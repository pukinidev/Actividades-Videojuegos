import random
import json

from src.cfg.game_settings import GameSettings


class EnemySettings:

    def __init__(self) -> None:
        self.enemy_path = "assets/cfg/enemies.json"
        self.window_size = GameSettings().get_window_size()
        self._load_settings()

    def _load_settings(self) -> None:
        self.check_settings()

    def _create_enemies(self) -> dict:
        enemies = {}
        n_enemies = random.randint(0, 4)
        for i in range(n_enemies):
            enemy = {
                "color": {
                    "r": random.randint(0, 255),
                    "g": random.randint(0, 255),
                    "b": random.randint(0, 255),
                },
                "size": {
                    "x": random.randint(10, 50),
                    "y": random.randint(10, 50),
                },
                "velocity_min": random.randint(40, 100),
                "velocity_max": random.randint(100, 200),
            }
            enemies[f"Type_{i}"] = enemy
            
        with open(self.enemy_path, "w") as file:
            json.dump(enemies, file, indent=4)

        return enemies

    def _create_level_enemies(self, enemies: dict) -> None:
        level_enemies = {}
        for i, enemy in enumerate(enemies):
            level_enemy = {
                "time": random.randint(0, 10),
                "enemy_type": enemy,
                "position": {
                    "x": random.randint(0, self.window_size[0]),
                    "y": random.randint(0, self.window_size[1]),
                },
            }
            level_enemies[f"{i}"] = level_enemy
            
        with open("assets/cfg/level_01.json", "w") as file:
            json.dump({"enemy_spawn_events": level_enemies}, file, indent=4)

    def get_settings(self) -> dict:
        return json.load(open(self.enemy_path))

    def check_settings(self) -> None:
        try:
            self.get_settings()
        except FileNotFoundError:
            enemies = self._create_enemies()
            self._create_level_enemies(enemies)
            print("Enemies settings created")

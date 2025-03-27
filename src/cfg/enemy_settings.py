import random
import json


class EnemySettings:

    def __init__(self) -> None:
        self.enemy_path = "assets/cfg/enemies.json"
        self._load_settings()

    def _load_settings(self) -> None:
        self.check_settings()

    def _create_enemies(self) -> list:
        enemies = []
        n_enemies = random.randint(4, 8)
        for enemy in range(n_enemies):
            enemy = {
                "name": f"enemy_{enemy}",
                "color": {
                    "r": random.randint(0, 255),
                    "g": random.randint(0, 255),
                    "b": random.randint(0, 255),
                },
                "size": {
                    "x": random.randint(10, 50),
                    "y": random.randint(10, 50),
                },
                "vmin": random.randint(40, 100),
                "vmax": random.randint(100, 200),
            }
            enemies.append(enemy)

        with open(self.enemy_path, "w") as file:
            json.dump({"enemies": enemies}, file, indent=4)

        return enemies

    def _create_level_enemies(self, enemies: list) -> None:
        level_enemies = []
        for enemy in enemies:
            level = {
                "type": enemy["name"],
                "time": random.randint(1, 10),
                "position": {
                    "x": random.randint(0, 800),
                    "y": random.randint(0, 600),
                },
            }
            level_enemies.append(level)

        with open("assets/cfg/level_01.json", "w") as file:
            json.dump({"level_enemies": level_enemies}, file, indent=4)

    def get_settings(self) -> dict:
        return json.load(open(self.enemy_path))

    def check_settings(self) -> None:
        try:
            self.get_settings()
        except FileNotFoundError:
            enemies = self._create_enemies()
            self._create_level_enemies(enemies)
            print("Enemies settings created")

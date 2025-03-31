
import json


class PlayerSettings:

    def __init__(self):
        self.player_path = "assets/cfg/player.json"
        self.player_config = json.load(open(self.player_path))

    def get_player(self) -> dict:
        return self.player_config
    
    
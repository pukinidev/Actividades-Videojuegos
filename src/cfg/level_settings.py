import json
    
class LevelSettings:
    
    def __init__(self):
        self.config_json = json.load(open('assets/cfg/level_01.json'))
        self.spawn_events = self.config_json['enemy_spawn_events']
        self.player_spawn = self.config_json['player_spawn']
        
    def get_spawn_events(self) -> dict:
        return self.spawn_events
    
    def get_spawn_player(self) -> dict:
        return self.player_spawn
import json
    
class LevelSettings:
    
    def __init__(self):
        self.level_config = json.load(open('assets/cfg/level_01.json'))['enemy_spawn_events']
        
    def get_level_enemies(self) -> dict:
        return self.level_config
import json
    
class LevelSettings:
    
    def __init__(self):
        self.spawn_events = json.load(open('assets/cfg/level_01.json'))['enemy_spawn_events']
        
    def get_spawn_events(self) -> dict:
        return self.spawn_events
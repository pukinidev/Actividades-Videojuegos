
from src.cfg.level_settings import LevelSettings


class CEnemySpawner:
    
    def __init__(self):
        self.spawn_events = LevelSettings().get_spawn_events()
        self.time_accumulator = 0.0
        
        
        
    


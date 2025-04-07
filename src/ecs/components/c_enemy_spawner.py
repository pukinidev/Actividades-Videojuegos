

class CEnemySpawner:

    def __init__(self, spawn_events: dict) -> None:
        self.spawn_events = spawn_events
        self.spawned_flags = [False] * len(self.spawn_events)
        self.time_accumulator = 0.0

import esper
import pygame

from src.create.prefab_create import create_enemy_entity
from src.ecs.components.c_enemy_spawner import CEnemySpawner


def system_enemy_spawner(world: esper.World, delta_time: float, enemies_config: dict):
    components = world.get_components(CEnemySpawner)
    c_e: CEnemySpawner
    
    for entity, (c_e,) in components:
        c_e.time_accumulator += delta_time
        for i, event in enumerate(c_e.spawn_events):
            if not c_e.spawned_flags[i] and c_e.time_accumulator >= event["time"]:
                c_e.spawned_flags[i] = True  
                position = pygame.Vector2(event["position"]["x"], event["position"]["y"])
                create_enemy_entity(world, event["enemy_type"], position, enemies_config)
                print(f"[SPAWN] {event["enemy_type"]} at t={c_e.time_accumulator:.2f}s pos={position}")
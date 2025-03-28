import esper
import pygame

from src.create.prefab_create import crear_enemy
from src.ecs.components.c_enemy_spawner import CEnemySpawner


def system_enemy_spawner(world: esper.World, delta_time: float, enemies_config: dict):
    components = world.get_components(CEnemySpawner)
    c_e: CEnemySpawner
    
    for entity, (c_e,) in components:
        c_e.time_accumulator += delta_time

        to_spawn = [event for event in c_e.spawn_events if c_e.time_accumulator >= event["time"]]

        for event in to_spawn:
            # TODO: Check why the position or velocity is affecting the bounce
            position = pygame.Vector2(event["position"]["x"], event["position"]["y"])
            enemy_type = event["enemy_type"]
            crear_enemy(world, enemy_type, position, enemies_config)
            print(f"[SPAWN] {enemy_type} at t={c_e.time_accumulator:.2f}s pos={position}")

        c_e.spawn_events = [event for event in c_e.spawn_events if event not in to_spawn]
import math
import random
import esper
import pygame

from src.ecs.components.c_enemy_spawner import CEnemySpawner
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_velocity import CVelocity

def get_entity_config(config: dict) -> dict:
    return {
        "size": pygame.Vector2(config["size"]["x"], config["size"]["y"]),
        "color": pygame.Color(config["color"]["r"], config["color"]["g"], config["color"]["b"]),
    }

def create_square(world: esper.World, size: pygame.Vector2, pos: pygame.Vector2, vel: pygame.Vector2, col: pygame.Color):
    cuad_entity = world.create_entity()
    world.add_component(cuad_entity, CSurface(
        size=size, color=col
    ))
    world.add_component(cuad_entity, CTransform(
        pos=pos
    ))
    world.add_component(cuad_entity, CVelocity(
        vel=vel
    ))
    
def create_enemy_square(world: esper.World, enemy_type: str, position: pygame.Vector2, enemies_config: dict) -> int:
    cfg = enemies_config[enemy_type]
    settings = get_entity_config(cfg)
    speed = random.uniform(cfg["velocity_min"], cfg["velocity_max"])
    angle = random.uniform(0, 2 * math.pi)
    direction = pygame.Vector2(math.cos(angle), math.sin(angle)) * speed
    return create_square(world, settings["size"], position, direction, settings["color"])

def create_player_square(world: esper.World, player_config:dict, player_lvl_config:dict) -> int:
    settings = get_entity_config(player_config)
    pos = pygame.Vector2(player_lvl_config["position"]["x"] - settings["size"].x / 2, player_lvl_config["position"]["y"] - settings["size"].y / 2)
    vel = pygame.Vector2(0, 0)
    return create_square(world, settings["size"], pos, vel, settings["color"])
    
def create_spawner_entity(world: esper.World, spawn_events: dict) -> int:
    spawner_entity = world.create_entity()
    world.add_component(spawner_entity, CEnemySpawner(spawn_events=spawn_events))
    return spawner_entity
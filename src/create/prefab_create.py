import math
import random
import esper
import pygame

from src.ecs.components.c_enemy_spawner import CEnemySpawner
from src.ecs.components.c_input_command import CInputCommand
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_velocity import CVelocity
from src.ecs.components.tags.c_tag_bullet import CTagBullet
from src.ecs.components.tags.c_tag_enemy import CTagEnemy
from src.ecs.components.tags.c_tag_player import CTagPlayer

def get_entity_config(config: dict) -> dict:
    return {
        "size": pygame.Vector2(config["size"]["x"], config["size"]["y"]),
        "color": pygame.Color(config["color"]["r"], config["color"]["g"], config["color"]["b"]),
    }

def create_square(world: esper.World, size: pygame.Vector2, pos: pygame.Vector2, vel: pygame.Vector2, col: pygame.Color) -> int:
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
    return cuad_entity
    
def create_enemy_square(world: esper.World, enemy_type: str, position: pygame.Vector2, enemies_config: dict) -> int:
    cfg = enemies_config[enemy_type]
    settings = get_entity_config(cfg)
    speed = random.uniform(cfg["velocity_min"], cfg["velocity_max"])
    angle = random.uniform(0, 2 * math.pi)
    direction = pygame.Vector2(math.cos(angle), math.sin(angle)) * speed
    enemy_entity = create_square(world, settings["size"], position, direction, settings["color"])
    world.add_component(enemy_entity, CTagEnemy())

def create_player_square(world: esper.World, player_config:dict, player_lvl_config:dict) -> int:
    settings = get_entity_config(player_config)
    pos = pygame.Vector2(player_lvl_config["position"]["x"] - settings["size"].x / 2, player_lvl_config["position"]["y"] - settings["size"].y / 2)
    vel = pygame.Vector2(0, 0)
    player_entity = create_square(world, settings["size"], pos, vel, settings["color"])
    world.add_component(player_entity, CTagPlayer())
    return player_entity
    
def create_spawner_entity(world: esper.World, spawn_events: dict) -> int:
    spawner_entity = world.create_entity()
    world.add_component(spawner_entity, CEnemySpawner(spawn_events=spawn_events))
    return spawner_entity

def create_input_player(world: esper.World) -> int:
    input_left = world.create_entity()
    input_right = world.create_entity()
    input_up = world.create_entity()
    input_down = world.create_entity()
    input_fire = world.create_entity()
    world.add_component(input_left, CInputCommand(
        "PLAYER_LEFT", pygame.K_LEFT
    ))
    world.add_component(input_right, CInputCommand(
        "PLAYER_RIGHT", pygame.K_RIGHT
    ))
    world.add_component(input_up, CInputCommand(
        "PLAYER_UP", pygame.K_UP
    ))
    world.add_component(input_down, CInputCommand(
        "PLAYER_DOWN", pygame.K_DOWN
    ))
    world.add_component(input_fire, CInputCommand(
        "PLAYER_FIRE", pygame.BUTTON_LEFT
    ))
    
def create_bullet(world: esper.World, mouse_pos: pygame.Vector2, player_pos: pygame.Vector2, player_size: pygame.Vector2, bullet_config: dict) -> int:
    settings = get_entity_config(bullet_config)
    pos = pygame.Vector2(player_pos.x + player_size[0] / 2, player_pos.y + player_size[1] / 2)
    vel = (mouse_pos - player_pos)
    vel = vel.normalize() * bullet_config["velocity"]
    bullet_entity = create_square(world, settings["size"], pos, vel, settings["color"])
    world.add_component(bullet_entity, CTagBullet())
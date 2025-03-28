import math
import random
import esper
import pygame

from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_velocity import CVelocity


def crear_cuadrado(world: esper.World, size: pygame.Vector2, pos: pygame.Vector2, vel: pygame.Vector2, col: pygame.Color):
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
    
def crear_enemy(world: esper.World, enemy_type: str, position: pygame.Vector2, enemies_config: dict) -> int:
    cfg = enemies_config[enemy_type]
    size = pygame.Vector2(cfg["size"]["x"], cfg["size"]["y"])
    color = pygame.Color(cfg["color"]["r"], cfg["color"]["g"], cfg["color"]["b"])
    speed = random.uniform(cfg["velocity_min"], cfg["velocity_max"])
    angle = random.uniform(0, 2 * math.pi)
    direction = pygame.Vector2(math.cos(angle), math.sin(angle)) * speed

    return crear_cuadrado(world, size, position, direction, color)

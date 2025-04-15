import math
import random
import esper
import pygame

from src.ecs.components.c_animation import CAnimation
from src.ecs.components.c_enemy_hunter_state import CEnemyHunterState
from src.ecs.components.c_enemy_spawner import CEnemySpawner
from src.ecs.components.c_input_command import CInputCommand
from src.ecs.components.c_player_state import CPlayerState
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_velocity import CVelocity
from src.ecs.components.tags.c_tag_bullet import CTagBullet
from src.ecs.components.tags.c_tag_enemy import CTagEnemy
from src.ecs.components.tags.c_tag_explosion import CTagExplosion
from src.ecs.components.tags.c_tag_player import CTagPlayer



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

def create_sprite(world: esper.World, pos: pygame.Vector2, vel: pygame.Vector2, surface: pygame.Surface) -> int:
    sprite_entity = world.create_entity()
    world.add_component(sprite_entity, CTransform(
        pos=pos
    ))
    world.add_component(sprite_entity, CVelocity(
        vel=vel
    ))
    world.add_component(sprite_entity, CSurface.from_surface(surface = surface))
    return sprite_entity
    
    
def create_enemy_square(world: esper.World, position: pygame.Vector2, enemies_config: dict) -> int:
    enemy_surface = pygame.image.load(enemies_config["image"]).convert_alpha()
    speed = random.uniform(enemies_config["velocity_min"], enemies_config["velocity_max"])
    angle = random.uniform(0, 2 * math.pi)
    direction = pygame.Vector2(math.cos(angle), math.sin(angle)) * speed
    enemy_entity = create_sprite(world, position, direction, enemy_surface)
    world.add_component(enemy_entity, CTagEnemy("Normal"))
    
def create_enemy_hunter(world: esper.World, position: pygame.Vector2, hunter_config: dict) -> int:
    enemy_surface = pygame.image.load(hunter_config["image"]).convert_alpha()
    enemy_entity = create_sprite(world, position, pygame.Vector2(0, 0), enemy_surface)
    world.add_component(enemy_entity, CEnemyHunterState(
        start_pos=position
    ))
    world.add_component(enemy_entity, CAnimation(
        hunter_config["animations"]
    ))
    world.add_component(enemy_entity, CTagEnemy("Hunter"))


def create_player_square(world: esper.World, player_config:dict, player_lvl_config:dict) -> int:
    player_sprite = pygame.image.load(player_config["image"]).convert_alpha()
    size = player_sprite.get_size()
    size = (size[0] / player_config["animations"]["number_frames"], size[1])
    pos = pygame.Vector2(player_lvl_config["position"]["x"] - size[0] / 2, player_lvl_config["position"]["y"] - size[1] / 2)
    vel = pygame.Vector2(0, 0)
    player_entity = create_sprite(world, pos, vel, player_sprite)
    world.add_component(player_entity, CTagPlayer())
    world.add_component(player_entity, CAnimation(
        player_config["animations"]
    ))
    world.add_component(player_entity, CPlayerState())
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
    bullet_surface = pygame.image.load(bullet_config["image"]).convert_alpha()
    bullet_size = bullet_surface.get_rect().size
    pos = pygame.Vector2(player_pos.x + (player_size[0] / 2) - (bullet_size[0] / 2), player_pos.y + (player_size[1] / 2) - (bullet_size[1] / 2))
    vel = (mouse_pos - player_pos)
    vel = vel.normalize() * bullet_config["velocity"]
    bullet_entity = create_sprite(world, pos, vel, bullet_surface)
    world.add_component(bullet_entity, CTagBullet())
    
def create_explosion(world: esper.World, position: pygame.Vector2, explosion_config: dict) -> int:
    explosion_surface = pygame.image.load(explosion_config["image"]).convert_alpha()
    explosion_entity = create_sprite(world, position, pygame.Vector2(0, 0), explosion_surface)
    world.add_component(explosion_entity, CTagExplosion())
    world.add_component(explosion_entity, CAnimation(
        explosion_config["animations"]
    ))
    return explosion_entity
import esper
import pygame

from src.cfg.load_settings import ConfigLoader
from src.create.prefab_create import create_bullet, create_explosion, create_input_player, create_spawner_entity, create_player_square
from src.ecs.components.c_input_command import CInputCommand, CommandPhase
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_velocity import CVelocity
from src.ecs.components.tags.c_tag_bullet import CTagBullet
from src.ecs.systems.s_animation import system_animation
from src.ecs.systems.s_collision_enemy_bullet import system_collision_enemy_bullet
from src.ecs.systems.s_collision_player_enemy import system_collision_player_enemy
from src.ecs.systems.s_explosion import system_explosion
from src.ecs.systems.s_input_player import system_player_input
from src.ecs.systems.s_movement import system_movement
from src.ecs.systems.s_player_state import system_player_state
from src.ecs.systems.s_rendering import system_rendering
from src.ecs.systems.s_screen_bounce import system_screen_bounce
from src.ecs.systems.s_enemy_spawner import system_enemy_spawner
from src.ecs.systems.s_screen_bullet import system_screen_bullet
from src.ecs.systems.s_screen_player import system_screen_player


class GameEngine:
    def __init__(self) -> None:
        pygame.init()
        self.loader = ConfigLoader()
        self.config = self.loader.get_window_config()
        self.enemies = self.loader.get_enemies_config()
        self.level = self.loader.get_level_01_config()
        self.player = self.loader.get_player_config()
        self.bullet = self.loader.get_bullet_config()
        self.explosion = self.loader.get_explosion_config()
        self.screen = pygame.display.set_mode((
            self.config["size"]["w"],
            self.config["size"]["h"]
        ), pygame.SCALED)
        self.title = pygame.display.set_caption(self.config["title"])
        self.clock = pygame.time.Clock()
        self.is_running = False
        self.framerate = self.config["framerate"]
        self.delta_time = 0
        self.ecs_world = esper.World()

    def run(self) -> None:
        self._create()
        self.is_running = True
        while self.is_running:
            self._calculate_time()
            self._process_events()
            self._update()
            self._draw()
        self._clean()

    def _create(self):
        self.player_entity = create_player_square(
            self.ecs_world, self.player, self.level["player_spawn"])
        self.player_c_v = self.ecs_world.component_for_entity(
            self.player_entity, CVelocity)
        self.player_c_t = self.ecs_world.component_for_entity(
            self.player_entity, CTransform)
        self.player_c_s = self.ecs_world.component_for_entity(
            self.player_entity, CSurface)
        create_spawner_entity(self.ecs_world, self.level["enemy_spawn_events"])
        create_input_player(self.ecs_world)
        
            

    def _calculate_time(self):
        self.clock.tick(self.framerate)
        self.delta_time = self.clock.get_time() / 1000.0

    def _process_events(self):
        for event in pygame.event.get():
            system_player_input(self.ecs_world, event, self._do_action)
            if event.type == pygame.QUIT:
                self.is_running = False

    def _update(self):
        system_enemy_spawner(self.ecs_world, self.delta_time, self.enemies)
        system_movement(self.ecs_world, self.delta_time)
        
        system_player_state(self.ecs_world)
        
        system_screen_bounce(self.ecs_world, self.screen)
        system_screen_player(self.ecs_world, self.screen)
        system_screen_bullet(self.ecs_world, self.screen)
        system_collision_enemy_bullet(self.ecs_world, self.explosion)
        system_collision_player_enemy(self.ecs_world, self.player_entity, self.level["player_spawn"], self.explosion)
        
        
        system_animation(self.ecs_world, self.delta_time)
        system_explosion(self.ecs_world)
        
        self.ecs_world._clear_dead_entities()
        self.num_bullets = len(self.ecs_world.get_component(CTagBullet))
        
        

    def _draw(self):
        self.screen.fill((
            self.config["bg_color"]["r"],
            self.config["bg_color"]["g"],
            self.config["bg_color"]["b"]
        ))
        system_rendering(self.ecs_world, self.screen)
        pygame.display.flip()

    def _clean(self):
        self.ecs_world.clear_database()
        pygame.quit()

    def _do_action(self, c_input: CInputCommand):
        if c_input.name in ["PLAYER_LEFT", "PLAYER_RIGHT"]:
            self._handle_horizontal_movement(c_input)
        elif c_input.name in ["PLAYER_UP", "PLAYER_DOWN"]:
            self._handle_vertical_movement(c_input)
        elif c_input.name == "PLAYER_FIRE":
            self._handle_fire_action(c_input)

    def _handle_horizontal_movement(self, c_input: CInputCommand):
        velocity_change = self.player["input_velocity"]
        if c_input.name == "PLAYER_LEFT":
            velocity_change = -velocity_change
        if c_input.phase == CommandPhase.START:
            self.player_c_v.vel.x += velocity_change
        elif c_input.phase == CommandPhase.END:
            self.player_c_v.vel.x -= velocity_change

    def _handle_vertical_movement(self, c_input: CInputCommand):
        velocity_change = self.player["input_velocity"]
        if c_input.name == "PLAYER_UP":
            velocity_change = -velocity_change
        if c_input.phase == CommandPhase.START:
            self.player_c_v.vel.y += velocity_change
        elif c_input.phase == CommandPhase.END:
            self.player_c_v.vel.y -= velocity_change

    def _handle_fire_action(self, c_input: CInputCommand):
        if self.num_bullets < self.level["player_spawn"]["max_bullets"]:
            create_bullet(
                self.ecs_world,
                c_input.mouse_pos,
                self.player_c_t.pos,
                self.player_c_s.area.size,
                self.bullet
            )

import esper
import pygame

from src.cfg.load_settings import ConfigLoader
from src.create.prefab_create import create_input_player, create_spawner_entity, create_player_square
from src.ecs.components.c_input_command import CInputCommand, CommandPhase
from src.ecs.components.c_velocity import CVelocity
from src.ecs.systems.s_collision_player_enemy import system_collision_player_enemy
from src.ecs.systems.s_input_player import system_player_input
from src.ecs.systems.s_movement import system_movement
from src.ecs.systems.s_rendering import system_rendering
from src.ecs.systems.s_screen_bounce import system_screen_bounce
from src.ecs.systems.s_enemy_spawner import system_enemy_spawner


class GameEngine:
    def __init__(self) -> None:
        pygame.init()
        self.loader = ConfigLoader()
        self.config = self.loader.get_window_config()
        self.enemies = self.loader.get_enemies_config()
        self.level = self.loader.get_level_01_config()
        self.player = self.loader.get_player_config()
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
        system_screen_bounce(self.ecs_world, self.screen)
        system_collision_player_enemy(self.ecs_world, self.player_entity, self.level["player_spawn"])
        self.ecs_world._clear_dead_entities()

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
        if c_input.name == "PLAYER_LEFT":
            if c_input.phase == CommandPhase.START:
                self.player_c_v.vel.x -= self.player["input_velocity"]
            elif c_input.phase == CommandPhase.END:
                self.player_c_v.vel.x += self.player[
                    "input_velocity"]
        if c_input.name == "PLAYER_RIGHT":
            if c_input.phase == CommandPhase.START:
                self.player_c_v.vel.x += self.player[
                    "input_velocity"]
            elif c_input.phase == CommandPhase.END:
                self.player_c_v.vel.x -= self.player[
                    "input_velocity"]

        if c_input.name == "PLAYER_UP":
            if c_input.phase == CommandPhase.START:
                self.player_c_v.vel.y -= self.player[
                    "input_velocity"]
            elif c_input.phase == CommandPhase.END:
                self.player_c_v.vel.y += self.player[
                    "input_velocity"]

        if c_input.name == "PLAYER_DOWN":
            if c_input.phase == CommandPhase.START:
                self.player_c_v.vel.y += self.player[
                    "input_velocity"]
            elif c_input.phase == CommandPhase.END:
                self.player_c_v.vel.y -= self.player[
                    "input_velocity"]

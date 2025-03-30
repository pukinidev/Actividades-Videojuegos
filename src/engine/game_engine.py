import esper
import pygame

from src.cfg.enemy_settings import EnemySettings
from src.cfg.level_settings import LevelSettings
from src.create.prefab_create import create_spawner_entity
from src.ecs.systems.s_movement import system_movement
from src.ecs.systems.s_rendering import system_rendering
from src.ecs.systems.s_screen_bounce import system_screen_bounce
from src.ecs.systems.s_enemy_spawner import system_enemy_spawner
from src.cfg.game_settings import GameSettings


class GameEngine:
    def __init__(self) -> None:
        pygame.init()
        self.config = GameSettings()
        self.enemies = EnemySettings()
        self.level = LevelSettings()
        self.screen = pygame.display.set_mode(self.config.get_window_size(), pygame.SCALED)
        self.title = pygame.display.set_caption(self.config.get_window_title())
        self.clock = pygame.time.Clock()
        self.is_running = False
        self.framerate = self.config.get_window_framerate()
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
        create_spawner_entity(self.ecs_world, self.level.get_spawn_events())

    def _calculate_time(self):
        self.clock.tick(self.framerate)
        self.delta_time = self.clock.get_time() / 1000.0

    def _process_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.is_running = False

    def _update(self):
        system_enemy_spawner(self.ecs_world, self.delta_time, self.enemies.get_enemies())
        system_movement(self.ecs_world, self.delta_time)
        system_screen_bounce(self.ecs_world, self.screen)

    def _draw(self):
        self.screen.fill(self.config.get_window_background_color())
        system_rendering(self.ecs_world, self.screen)
        pygame.display.flip()

    def _clean(self):
        pygame.quit()

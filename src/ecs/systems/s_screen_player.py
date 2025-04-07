

import esper
import pygame

from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_velocity import CVelocity
from src.ecs.components.tags.c_tag_player import CTagPlayer


def system_screen_player(world: esper.World, screen: pygame.Surface) -> None:
    scr_rect = screen.get_rect()
    components = world.get_components(CTransform, CSurface, CVelocity, CTagPlayer)
    for _, (c_t, c_s, c_v, _) in components:
        player_rect = c_s.surf.get_rect(topleft=c_t.pos)
        if not scr_rect.contains(player_rect):
            player_rect.clamp_ip(scr_rect)
            c_t.pos.xy = player_rect.topleft
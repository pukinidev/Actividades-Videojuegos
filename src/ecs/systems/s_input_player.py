from typing import Callable
import esper
import pygame

from src.ecs.components.c_input_command import CInputCommand, CommandPhase

def system_player_input(world: esper.World, event: pygame.Event, do_action:Callable[[CInputCommand], None]):
    
    components = world.get_component(CInputCommand)
    for _, c_i in components:
        if event.type == pygame.KEYDOWN and c_i.key == event.key:
            c_i.phase = CommandPhase.START
            do_action(c_i)
            
        elif event.type == pygame.KEYUP and c_i.key == event.key:
            c_i.phase = CommandPhase.END
            do_action(c_i)
        
        
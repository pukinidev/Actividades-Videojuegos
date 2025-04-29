import esper

from src.create.prefab_create import create_dynamic_text
from src.ecs.components.tags.c_tag_pause import CTagPause

def system_render_pause_text(world: esper.World, is_paused: bool, font, text_config) -> None:
    pause_entities = [entity for entity, _ in world.get_component(CTagPause)]
    if is_paused:
        if not pause_entities:
            entity = create_dynamic_text(
                world,
                font=font,
                text_config=text_config,
                name="PAUSE",
            )
            world.add_component(entity, CTagPause())
    else:
        for entity in pause_entities:
            world.delete_entity(entity)
import esper

from src.create.prefab_create import create_explosion
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.tags.c_tag_bullet import CTagBullet
from src.ecs.components.tags.c_tag_enemy import CTagEnemy

def system_collision_enemy_bullet(world: esper.World, explosion_config: dict):
    component_enemy = world.get_components(CSurface, CTransform, CTagEnemy)
    components_bullet = world.get_components(CSurface, CTransform, CTagBullet)
    for enemy_entity, (c_s, c_t, _) in component_enemy:
        ene_rect = CSurface.get_area_relative(c_s.area, c_t.pos)
        for bullet_entity, (c_b_s, c_b_t, _) in components_bullet:
            bul_rect = CSurface.get_area_relative(c_b_s.area, c_b_t.pos)
            if ene_rect.colliderect(bul_rect):
                world.delete_entity(enemy_entity)
                world.delete_entity(bullet_entity)
                create_explosion(world, c_t.pos, explosion_config)
                
    
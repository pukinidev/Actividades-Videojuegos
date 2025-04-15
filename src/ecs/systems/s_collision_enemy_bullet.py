import esper

from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.tags.c_tag_bullet import CTagBullet
from src.ecs.components.tags.c_tag_enemy import CTagEnemy

def system_collision_enemy_bullet(world: esper.World) -> None:
    component_enemy = world.get_components(CSurface, CTransform, CTagEnemy)
    components_bullet = world.get_components(CSurface, CTransform, CTagBullet)
    for enemy_entity, (c_s, c_t, _) in component_enemy:
        ene_rect = c_s.area.copy()
        ene_rect.topleft = c_t.pos
        for bullet_entity, (c_b_s, c_b_t, _) in components_bullet:
            bul_rect = c_b_s.area.copy()
            bul_rect.topleft = c_b_t.pos
            if ene_rect.colliderect(bul_rect):
                world.delete_entity(enemy_entity)
                world.delete_entity(bullet_entity)
                
    
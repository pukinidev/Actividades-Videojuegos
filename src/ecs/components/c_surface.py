import pygame

class CSurface:
    
    def __init__(self, size: pygame.Vector2, color: pygame.Color) -> None:
        self.surf = pygame.Surface(size)
        self.surf.fill(color)
        self.area = self.surf.get_rect()
        
    @classmethod
    def from_surface(cls, surface: pygame.Surface) -> None:
        c_surf = cls(pygame.Vector2(0, 0), pygame.Color(0, 0, 0))
        c_surf.surf = surface
        c_surf.area = surface.get_rect()
        return c_surf
    
    @classmethod
    def from_text(cls, font: pygame.font.Font, config: dict) -> None:
        c_surf = cls(pygame.Vector2(0, 0), pygame.Color(0, 0, 0))
        c_surf.surf = font.render(config["text"], True, pygame.Color(config["color"]["r"], config["color"]["g"], config["color"]["b"]))
        c_surf.area = c_surf.surf.get_rect()
        return c_surf
    
    
    def get_area_relative(area: pygame.Rect, pos_top_left: pygame.Vector2) -> pygame.Rect:
        new_rect = area.copy()
        new_rect.topleft = pos_top_left.copy()
        return new_rect
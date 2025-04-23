import pygame 

class TextService:
    def __init__(self):
        self._fonts = {}
        
    def load_font(self, path: str, size: int):
        if path not in self._fonts:
            self._fonts[path] = pygame.font.Font(path, size)
        return self._fonts[path]
        
    
import json



class GameSettings:
    def __init__(self):
        self.window_config = json.load(open('assets/cfg/window.json'))

    def get_window_size(self) -> tuple:
        size = self.window_config['size']
        return (size['w'], size['h'])
    
    def get_window_title(self) -> str:
        return self.window_config['title']
    
    def get_window_background_color(self) -> tuple:
        color = self.window_config['bg_color']
        return (color['r'], color['g'], color['b'])
    
    def get_window_framerate(self) -> int:
        return self.window_config['framerate']
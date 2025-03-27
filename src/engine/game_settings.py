import json
import os


class GameSettings:
    def __init__(self):
        config_path = os.path.join(os.path.dirname(
            __file__), "../../assets/cfg/window.json")
        self.window_config = json.load(open(config_path))['window']

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
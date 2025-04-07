import os
import json
from types import MethodType
from typing import Dict, Any

class ConfigLoader:
    def __init__(self, config_path: str = "assets/cfg/"):
        self.config_path = config_path
        self.configs: Dict[str, Dict[str, Any]] = {}
        self.load_configs()
        self.create_custom_functions()

    def load_configs(self):
        try:
            for filename in os.listdir(self.config_path):
                if filename.endswith(".json"):
                    file_path = os.path.join(self.config_path, filename)
                    with open(file_path, 'r') as file:
                        config_name = os.path.splitext(filename)[0]  
                        self.configs[config_name] = json.load(file)
        except Exception as e:
            print(f"Error loading configs: {e}")

    def create_custom_functions(self):
        for config_name in self.configs:
            def custom_function(self, config_name=config_name) -> Dict[str, Any]:
                return self.configs[config_name]
            setattr(self, f"get_{config_name}_config", MethodType(custom_function, self))



import os
import json

class StateManager:
    preset_base_dir = "/home/jona/.jearig/"

    def __init__(self):
        os.makedirs(StateManager.preset_base_dir, exist_ok=True)        

        self.presets = {}

    def get_effect_state_path(effect, name):
        base = os.path.join(StateManager.preset_base_dir, f"{effect.plugin.name}")
        os.makdirs(base)
        return os.path.join(base, f"{name}.json")
    
    def get_state_path(name):
        return os.path.join(StateManager.preset_base_dir, f"{name}.json")

    def save_effect_state(self, effect, name):
        s = effect.get_state()
        f = StateManager.get_effect_state_path(effect, name)
        with open(f, 'w') as json_file:
            json.dump(s, json_file, indent=2)

    def load_effect_state(self, effect, name):
        f = StateManager.get_effect_state_path(effect, name)
        with open(f, 'r') as json_file:
            s = json.load(json_file)
            self.set_state(s)

    def save_effects_state(self, effects, name):
        s = dict([(e.plugin.name, e.get_state()) for e in effects])
        f = StateManager.get_state_path(name)
        with open(f, 'w') as json_file:
            json.dump(s, json_file, indent=2)

    def load_effects_state(self, effects, name):
        f = StateManager.get_state_path(name)
        with open(f, 'r') as json_file:
            s = json.load(json_file)
            
            for e in effects:
                e.set_state(s[e.plugin.name])


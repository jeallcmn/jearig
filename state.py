import os
import json

from effect import Effect
from pedalboard import Pedalboard

class StateManager:
    preset_base_dir = "/home/jona/.jearig/"
    pedalboard_base_dir = "/home/jona/.jearig/pedalboards"

    def __init__(self):
        pass

    def save_state(self, state, file):
        d = os.path.dirname(file)
        os.makedirs(d, exist_ok=True)
        with open(file, 'w') as f:
            json.dump(state, f, indent=2)

    def load_state(self, file):
        if os.path.exists(file):
            with open(file, 'r') as f:
                state = json.load(f)
                return state;
        else:
            return []
        
    def save_pedalboard(self, pedalboard):
        file = os.path.join(StateManager.pedalboard_base_dir, pedalboard.name+'.json')
        os.makedirs(StateManager.pedalboard_base_dir, exist_ok=True)
        state = pedalboard.get_state()
        self.save_state(state, file)

    def load_pedalboard(self, name: str, pedalboard: Pedalboard):
        pedalboard.reset()
        file = os.path.join(StateManager.pedalboard_base_dir, name+'.json')
        os.makedirs(StateManager.pedalboard_base_dir, exist_ok=True)
        state = self.load_state(file)
        pedalboard.set_state(state)

    # def __init__(self):
    #     os.makedirs(StateManager.preset_base_dir, exist_ok=True)
    #     self.presets = {}

    # def get_effect_state_path(effect: Effect, name: str):
    #     base = os.path.join(StateManager.preset_base_dir, f"{effect.plugin.name}")
    #     os.makedirs(base, exist_ok=True)
    #     return os.path.join(base, f"{name}.json")
    
    # def get_state_path(name):
    #     return os.path.join(StateManager.preset_base_dir, f"{name}.json")

    # def save_effect_state(self, effect: Effect, name: str):
    #     s = effect.get_state()
    #     f = StateManager.get_effect_state_path(effect, name)
    #     with open(f, 'w') as json_file:
    #         json.dump(s, json_file, indent=2)

    # def load_effect_state(self, effect: Effect, name: str):
    #     f = StateManager.get_effect_state_path(effect, name)
    #     with open(f, 'r') as json_file:
    #         s = json.load(json_file)
    #         # apply the loaded state to the effect
    #         effect.set_state(s)

    # def save_effects_state(self, effects: list[Effect], name: str):
    #     s = dict([(e.plugin.name, e.get_state()) for e in effects])
    #     f = StateManager.get_state_path(name)
    #     with open(f, 'w') as json_file:
    #         json.dump(s, json_file, indent=2)

    # def load_effects_state(self, effects: list[Effect], name: str):
    #     f = StateManager.get_state_path(name)
    #     with open(f, 'r') as json_file:
    #         s = json.load(json_file)
            
    #         for e in effects:
    #             if e.plugin.name in s:
    #                 e.set_state(s[e.plugin.name])

    # def save_rig(self, effects: list[Effect], name: str, connections: bool=None):
    #     """Save full rig: effects state plus logical connections.
    #     effects: list of Effect instances
    #     connections: optional list of connection dicts; if None, gathered from effects
    #     """
    #     eff_states = dict([(e.plugin.name, e.get_state()) for e in effects])
    #     if connections is None:
    #         # gather from effect.connections
    #         connections = []
    #         for e in effects:
    #             for c in e.connections:
    #                 # normalize to include source and dest effect names
    #                 if c.get('src'):
    #                     connections.append(c)
    #                 elif c.get('dst'):
    #                     connections.append({'type': c.get('type'), 'src': e.name, 'dst': c.get('dst')})

    #     payload = {"effects": eff_states, "connections": connections}
    #     f = StateManager.get_state_path(name)
    #     with open(f, 'w') as json_file:
    #         json.dump(payload, json_file, indent=2)

    # def load_rig(self, effects: list[Effect], name: str, host=None):
    #     """Load rig file and apply effect states and recreate logical connections.
    #     If host is provided it will attempt to connect JACK ports using effect names to find instances in `effects` list.
    #     """
    #     f = StateManager.get_state_path(name)
    #     if not os.path.exists(f):
    #         raise FileNotFoundError(f"Rig preset not found: {f}")
    #     with open(f, 'r') as json_file:
    #         payload = json.load(json_file)
    #         effs = payload.get('effects', {})
    #         conns = payload.get('connections', [])
    #         # apply states
    #         for e in effects:
    #             if e.plugin.name in effs:
    #                 e.set_state(effs[e.plugin.name])
    #         # clear existing logical connections
    #         for e in effects:
    #             e.connections = []
    #         # recreate logical connections and attempt JACK connections if host provided
    #         name_to_effect = {e.name: e for e in effects}
    #         for c in conns:
    #             src = c.get('src')
    #             dst = c.get('dst')
    #             t = c.get('type')
    #             if src in name_to_effect and dst in name_to_effect:
    #                 s_eff = name_to_effect[src]
    #                 d_eff = name_to_effect[dst]
    #                 if t == 'audio':
    #                     s_eff.connect(d_eff)
    #                 elif t == 'midi':
    #                     s_eff.connect_midi(d_eff)

    # def list_presets(self):
    #     """Return available rig preset filenames (top-level)"""
    #     entries = []
    #     for fn in os.listdir(StateManager.preset_base_dir):
    #         path = os.path.join(StateManager.preset_base_dir, fn)
    #         if os.path.isfile(path) and fn.endswith('.json'):
    #             entries.append(fn[:-5])
    #     return entries


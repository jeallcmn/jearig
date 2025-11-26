from host import Host
import lv2plugin
from effect import Effect, SystemEffect
import os
# Encapsulates connecting/disconnecting and managing effects
class Pedalboard():

    plugin_directory = "./plugins"
    plugin_files = sorted([x for x in os.listdir(plugin_directory) if x.endswith(".json")])
    plugins = [lv2plugin.Plugin.load(f"plugins/{f}") for f in plugin_files]

    def find_plugin(name):
        for p in Pedalboard.plugins:
            
            if p.name == name:
                return p
        print(f"Could not find plugin {name}")
        return None

    def __init__(self, host: Host):
        self.effects: list[Effect] = []

        # Create the Audio input and output device
        self.device = SystemEffect(host)
        self.host = host
        
        # Use only second input
        self.device.audio_outputs = self.device.audio_outputs[1:]

        self.lastEffect = self.device
        #Midi
        self.host.transport(1, 4, 134)
        self.host.transport_sync('midi')

    def set_bpm(self, beats_per_measure: int, beats_per_minute: int):
        self.host.transport(1, beats_per_measure, beats_per_minute)


    def get_effect(self, name: str):
        return self.effects[name]
    
    def create_effect(self, pluginName: str, autoConnect: bool=False):
        effect = Pedalboard.find_plugin(pluginName).create_effect(self.host)
        self.effects.append(effect)

        if autoConnect:
            self.lastEffect.connect(effect)
        self.lastEffect = effect
        return effect
    
    def remove_all(self):
        for e in self.effects:
            e.remove()
        self.effects.clear()

    # def remove_effect(self, name: str):
    #     # effect = self.effects.pop(name)
    #     # disconnect and remove the effect
    #     effect.remove()
    #     return effect
    
    def get_state(self):
        return {
            "effects": [e.get_state() for e in self.effects]
        }
    
    def set_state(self, state):
        for s in state["effects"]:
            e = self.create_effect(s["name"])
            e.set_state(s)


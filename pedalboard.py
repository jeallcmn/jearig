from host import Host
import lv2plugin
from effect import Effect, SystemEffect
import os
import jack

# Encapsulates connecting/disconnecting and managing effects
class Pedalboard():

    plugin_directory = "./plugins"
    plugin_files = sorted([x for x in os.listdir(plugin_directory) if x.endswith(".json")])
    plugins = [lv2plugin.Plugin.load(f"plugins/{f}") for f in plugin_files]

    def find_plugin(name) -> lv2plugin.Plugin:
        for p in Pedalboard.plugins:
            
            if p.name == name:
                return p
        print(f"Could not find plugin {name}")
        return None

    def __init__(self, name, host: Host):
        self.name = name
        self.effects: list[Effect] = []

        # Create the Audio input and output device
        self.device = SystemEffect(host)
        self.host = host
        
        # Use only second input
        self.device.audio_outputs = self.device.audio_outputs[1:]

        # self.lastEffect = self.device
        # pass through by default
        # self.lastEffect.connect(self.device)
        
        #Midi
        self.host.transport(1, 4, 134)
        self.host.transport_sync('midi')

    def set_bpm(self, beats_per_measure: int, beats_per_minute: int):
        self.host.transport(1, beats_per_measure, beats_per_minute)


    def get_effect(self, name: str):
        return self.effects[name]
    
    def create_effect(self, pluginName: str, id: int = None, autoConnect: bool=True):
        effect = Pedalboard.find_plugin(pluginName).create_effect(self.host, id)
        self.effects.append(effect)

        # if self.lastEffect and autoConnect:
        #     self.lastEffect.disconnect(self.device)

        #     self.lastEffect.connect(effect)
        #     # connect this to output automatically
        #     effect.connect(self.device)

        # self.lastEffect = effect
        return effect
    
    # def insert_effect(self, pluginName: str, before:Effect, after: Effect, id:int = None):
    #     """ Inserts a new effect between two effects"""
    #     effect = Pedalboard.find_plugin(pluginName).create_effect(self.host, id)
    #     self.effects.append(effect)

    #     before.disconnect(after)
    #     before.connect(effect)
    #     effect.connect(after)

    def reset(self):
        for e in self.effects:
            e.remove()
        self.effects.clear()
        # self.lastEffect = None
        # self.lastEffect.connect(self.device)
        

    # def remove_effect(self, name: str):
    #     # effect = self.effects.pop(name)
    #     # disconnect and remove the effect
    #     effect.remove()
    #     return effect
    
    def get_state(self):
        state = {
            "name": self.name,
            "effects": [e.get_state() for e in self.effects],
        }

        connections = {}
        for e in self.effects:
            connections.update(e.get_output_connection_state())
                
        connections.update(self.device.get_output_connection_state())
        state["connections"] = connections
        return state
    
    def set_state(self, state):
        self.name = state["name"]
        for s in state["effects"]:
            e = self.create_effect(s["name"], s["id"], False)
            e.set_state(s)
        for k,v in state["connections"].items():
            for o in v:
                try:
                    self.host.jack.connect(k, o)
                except jack.JackError as e :
                    print(f"Unable to connect: {k} -> {o}: {e.codemessage}")
                    pass

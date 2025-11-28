from host import Host
import lv2plugin
from effect import Effect, SystemEffect
import os
import jack
import state

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
        self.name: str = name
        self.effects: list[Effect] = []

        # Create the Audio input and output device
        self.device: SystemEffect = SystemEffect(host)
        self.host: Host = host
        
        # Use only second input
        self.device.audio_outputs = self.device.audio_outputs[1:]

        #Midi
        self.host.transport(1, 4, 134)
        self.host.transport_sync('midi')

        self.state_manager = state.StateManager()

    def set_bpm(self, beats_per_measure: int, beats_per_minute: int):
        self.host.transport(1, beats_per_measure, beats_per_minute)


    def get_effect(self, name: str):
        return self.effects[name]
    
    def create_effect(self, pluginName: str, id: int = None):
        effect = Pedalboard.find_plugin(pluginName).create_effect(self.host, id)
        self.effects.append(effect)

        return effect
    
    def reset(self):
        for e in self.effects:
            e.remove()
        self.effects.clear()
        

    def remove_effect(self, effect: Effect):
        effect.remove()
    
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
    def save(self, name: None):
        if name:
            self.name = name
        self.state_manager.save_pedalboard(self)
    def load(self, name: str):
        self.state_manager.load_pedalboard(name, self)



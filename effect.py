
from host import Host
from lv2plugin import Plugin
import util
import os
import json
import jack

INPUT_JACK = 0
OUTPUT_JACK = 1


# class EffectJack:

#     def __initj__(self, effect: 'Effect', port: jack.Port):
#         self.effect: 'Effect' = effect
#         self.port = port
#         self.cable = None
#     def is_input(self):
#         return self.port.is_input
#     def is_audio(self):
#         return self.port.is
       

# class Cable:
#     def __init__(self, source: EffectJack, target: EffectJack):
#         self.source = source
#         self.target = target
#         self.source.conn
#     def is_midi(self):
#         return self.source.is_midi
#     def is_audio(self):
#         return self.source.is_audio

        
# class ConnectionManager():
#     def __init__(self, jack: jack.Client):
#         self.connections = []
#         self.jack = jack
#     def connect(self, src: jack.Port, tgt: jack.Port):
#         jack.connect(src, tgt)
#         self.connections.append(Connection(src, tgt))
    


class BaseEffect:
    def __init__(self, plugin: Plugin, host: Host, name:str):
        self.plugin = plugin
        self.host: Host = host
        self.name = name
        self.audio_inputs = self.host.jack.get_ports(name_pattern=f"{self.name}:*", is_audio=True, is_physical=False, is_input=True, is_output=False)
        self.audio_outputs = self.host.jack.get_ports(name_pattern=f"{self.name}:*", is_audio=True, is_physical=False, is_input=False, is_output=True)
        self.midi_inputs = self.host.jack.get_ports(name_pattern=f"{self.name}:*", is_midi=True, is_physical=False, is_input=True, is_output=False)
        self.midi_outputs = self.host.jack.get_ports(name_pattern=f"{self.name}:*", is_midi=True, is_physical=False, is_input=False, is_output=True)

    def get_connected_effect_names(self, ports:list[jack.Port]):
        effects = []
        for s in ports:
            for x in self.host.jack.get_all_connections(s):
                effects.append(x.split(":")[0])
        return sorted(list(set((effects))))
    

    def get_output_connection_state(self):
        """ Connections are owned by the source, which is effect that owns the audio outputs"""
        state = {}
        for s in self.audio_outputs:
            state[s.name] = [x.name for x in self.host.jack.get_all_connections(s)]
        for s in self.midi_outputs:
            state[s.name] = [x.name for x in self.host.jack.get_all_connections(s)]            
        return state

    def disconnect_ports(self, ports, target:'BaseEffect' = None):
        for s in ports:
            for t in self.host.jack.get_all_connections(s):
                if (not target) or t.name.startswith(target.name):
                    print(f"Disconnecting port {s.name} from {None if t is None else t.name}")
                    if s.is_output:
                        self.host.jack.disconnect(s, t)
                    else:
                        self.host.jack.disconnect(t, s)

    def disconnect_all(self, target:'BaseEffect' = None):
        print(f"Disconnection {self.name} from {target and target.name}")
        if not target:
            self.disconnect_ports(self.audio_inputs, target)
        
        self.disconnect_ports(self.audio_outputs, target)

        if not target:
            self.disconnect_ports(self.midi_inputs, target)
        
        self.disconnect_ports(self.midi_outputs, target)

    def disconnect_all_audio(self, target:'BaseEffect' = None):
        self.disconnect_ports(self.audio_inputs, target)
        self.disconnect_ports(self.audio_outputs, target)

    def disconnect_all_midi(self, target:'BaseEffect' = None):
        self.disconnect_ports(self.midi_inputs, target)
        self.disconnect_ports(self.midi_outputs, target)    


    def connect(self, target: 'BaseEffect'):
        print (f"Conenction {self.name} to {target.name}")
        for connection in util.outer_join(self.audio_outputs, target.audio_inputs):
            # connect actual JACK ports
            try:
                print(f"Connecting {connection[0].name} to {connection[1].name}")
                self.host.jack.connect(connection[0], connection[1])
            except jack.JackError as e :
                print(f"Unable to connect: {connection[0].name} -> {connection[1].name}: {e.message}")
                pass
            
    def connect_midi(self, target: 'BaseEffect'):
        for connection in util.outer_join(self.midi_outputs, target.midi_inputs):
            self.host.jack.connect(connection[0], connection[1])

class SystemEffect(BaseEffect):
    def __init__(self, host: Host):
        BaseEffect.__init__(self, None, host, "system")

class Effect(BaseEffect):
    
    def __init__(self, plugin: Plugin, host: Host, uri: str, id: int = None, globalEffect:bool=False):
        self.id: int = host.add(uri, id)
        BaseEffect.__init__(self, plugin, host, f"effect_{self.id}")
        self.enabled:bool = True
        self.uri:str = uri
        self.globalEffect:bool = globalEffect
        self.patchValue:str = None
    
    def remove(self):
        self.disconnect_all()
        self.host.remove(self.id)


    def set_enabled(self, b):
        self.enabled = b
        if(self.enabled):
            self.host.bypass(self.id, 0)
        else:
            self.host.bypass(self.id, 1)
    def toggle(self):
        if(self.enabled):
            self.set_enabled(False)
        else:
            self.set_enabled(True)
    def param(self, name, value):
        self.host.param_set(self.id, name, value)
    def get_param(self, name):
        return self.host.param_get(self.id, name)
    def patch(self, value):
        self.patchValue = value
        self.host.patch_set(self.id, self.plugin.get_patch_controls(), value)
    def get_patch(self):
        return self.patchValue

    def get_parameter_names(self):
        return [x.symbol for x in self.plugin.get_input_controls()]
    
    def parameter_map(self):
        return dict([(f, self.get_param(f.symbol)) for f in self.plugin.get_input_controls()])
    
    def get_state(self):
        return {
            "id": self.id,
            "name": self.plugin.name,
            "uri": self.uri,
            "enabled": self.enabled,
            "parameters": self.parameter_map(),
            "patch": self.patchValue
        }
    
    def set_state(self,state):
        """ id, state, uri are used for creating the effect, this only applies the state"""
        if self.plugin.patch and state["patch"]:
            self.patch(state["patch"])
        for k,v in state["parameters"].items():
            self.param(k,v)
        self.set_enabled(state["enabled"])

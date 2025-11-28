
from host import Host
from lv2plugin import Plugin
import util
import os
import json
import jack

class BaseEffect:
    def __init__(self, plugin: Plugin, host: Host, name:str):
        self.plugin = plugin
        self.host: Host = host
        self.name = name
        self.audio_inputs = self.host.jack.get_ports(name_pattern=f"{self.name}:*", is_audio=True, is_physical=False, is_input=True, is_output=False)
        self.audio_outputs = self.host.jack.get_ports(name_pattern=f"{self.name}:*", is_audio=True, is_physical=False, is_input=False, is_output=True)
        self.midi_inputs = self.host.jack.get_ports(name_pattern=f"{self.name}:*", is_midi=True, is_physical=False, is_input=True, is_output=False)
        self.midi_outputs = self.host.jack.get_ports(name_pattern=f"{self.name}:*", is_midi=True, is_physical=False, is_input=False, is_output=True)

    def get_output_connection_state(self):
        """ Connections are owned by the source, which is effect that owns the audio outputs"""
        state = {}
        for s in self.audio_outputs:
            state[s.name] = [x.name for x in self.host.jack.get_all_connections(s)]
        for s in self.midi_outputs:
            state[s.name] = [x.name for x in self.host.jack.get_all_connections(s)]            
        return state

    def _disconnect_port(self, p):
        try:
            p.disconnect()
        except jack.JackError as e:
            print(f"Unabled to disconnect {p.name}")
            pass 

    def disconnect_all(self):
        for c in self.audio_inputs:
            self._disconnect_port(c)
        for c in self.audio_outputs:
            self._disconnect_port(c)
        for c in self.midi_inputs:
            self._disconnect_port(c)
        for c in self.midi_inputs:
            self._disconnect_port(c)
            
    def disconnect(self, target: 'BaseEffect'):
        for connection in util.outer_join(self.audio_outputs, target.audio_inputs):
            self._disconnect_port(connection)
    

    def connect(self, target: 'BaseEffect'):
        for connection in util.outer_join(self.audio_outputs, target.audio_inputs):
            # connect actual JACK ports
            try:
                self.host.jack.connect(connection[0], connection[1])
            except jack.JackError as e :
                print(f"Unable to connect: {connection[0].name} -> {connection[1].name}: {e.message}")
                pass
            # # record logical connection (use effect instance names which are unique in this app)
            # self.connections.append({"type": "audio", "dst": target.name})
            # target.connections.append({"type": "audio", "src": self.name})
            
    def connect_midi(self, target: 'BaseEffect'):
        for connection in util.outer_join(self.midi_outputs, target.midi_inputs):
            self.host.jack.connect(connection[0], connection[1])
            # self.connections.append({"type": "midi", "dst": target.name})
            # target.connections.append({"type": "midi", "src": self.name})

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
        self.host.remove(self.id)

    def disconnect_all(self):
        """ Disconnect all connections with the prefix "effect" """


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
       

    def parameter_map(self):
        return dict([(f, self.get_param(f)) for f in self.plugin.get_input_controls()])
    
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

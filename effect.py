
import util
import os
import json
class BaseEffect:
    def __init__(self, plugin, host, name):
        self.plugin = plugin
        self.host = host
        self.name = name
        
    
        self.audio_inputs = self.host.jack.get_ports(name_pattern=f"{self.name}:*", is_audio=True, is_physical=False, is_input=True, is_output=False)
        self.audio_outputs = self.host.jack.get_ports(name_pattern=f"{self.name}:*", is_audio=True, is_physical=False, is_input=False, is_output=True)
        self.midi_inputs = self.host.jack.get_ports(name_pattern=f"{self.name}:*", is_midi=True, is_physical=False, is_input=True, is_output=False)
        self.midi_outputs = self.host.jack.get_ports(name_pattern=f"{self.name}:*", is_midi=True, is_physical=False, is_input=False, is_output=True)

    def connect(self, target):
        for connection in util.outer_join(self.audio_outputs, target.audio_inputs):
            self.host.jack.connect(connection[0], connection[1])
    def connect_midi(self, target):
        for connection in util.outer_join(self.midi_outputs, target.midi_inputs):
            self.host.jack.connect(connection[0], connection[1])
class SystemEffect(BaseEffect):
    def __init__(self, host):
        BaseEffect.__init__(self, None, host, "system")

class Effect(BaseEffect):
    
    
    def __init__(self, plugin, host, uri, globalEffect=False):
        self.id = host.add(uri)
        BaseEffect.__init__(self, plugin, host, f"effect_{self.id}")
        self.enabled = True
        self.uri = uri
        self.globalEffect = globalEffect
        self.patchValue = None
    
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
            "enabled": self.enabled,
            "parameters": self.parameter_map(),
            "patch": self.patchValue
        }
    
    def set_state(self,state):
        if self.plugin.patch and state["patch"]:
            self.patch(state["patch"])
        for k,v in state["parameters"].items():
            self.param(k,v)
        self.set_enabled(state["enabled"])

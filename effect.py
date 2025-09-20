
import util

class BaseEffect:
    def __init__(self, host, name):
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
        BaseEffect.__init__(self, host, "system")

class Effect(BaseEffect):
    def __init__(self,  host, uri):
        self.id = host.add(uri)
        BaseEffect.__init__(self, host, f"effect_{self.id}")
        self.enabled = True
        self.uri = uri
    
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
    def patch(self, name, value):
        self.host.patch_set(self.id, f"{self.uri}#{name}", value)
        
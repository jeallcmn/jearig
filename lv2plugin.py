import json
from host import Host

class Port:
    def __init__(self, json: dict):
        self.name = json['lv2:name']
        self.symbol = json['lv2:symbol']
        self.types = json['@type']

        self.is_output = 'lv2:OutputPort' in self.types
        self.is_input = 'lv2:InputPort' in self.types
        self.is_audio = 'lv2:AudioPort' in self.types
        self.is_control = 'lv2:ControlPort' in self.types

        if self.is_control and self.is_input:
            self.default = json['lv2:default']
            if not isinstance(self.default, (int)):
                self.default = json['lv2:default']['@value']

            self.maximum = json['lv2:maximum']
            if not isinstance(self.maximum, (int)):
                self.maximum = json['lv2:maximum']['@value']
            
            self.minimum = json['lv2:minimum']
            if not isinstance(self.minimum, (int)):
                self.minimum = json['lv2:minimum']['@value']

    def __str__(self):
        desc = f"Port: {self.symbol}, Output:{self.is_output}, Input:{self.is_input}, Control:{self.is_control}, Audio:{self.is_audio}"
        if(self.is_control):
            desc += f", Default:{self.default}, Max:{self.maximum}, Min:{self.minimum}"
        return desc

class Plugin:
    def load(file: str):
        print(f"Loading {file}")
        with open(file) as jsonFile:
            return Plugin(json.load(jsonFile))
        
    def __init__(self, json: dict):
        self.uri = json.get('@id')
        self.name = json.get('doap:name') or 'Unknown Effect'
        self.ports = []
        # if json.get('lv2:port'):
        self.ports = [Port(p) for p in json['lv2:port']]
        self.patch = json.get('http://lv2plug.in/ns/ext/patch#writable')
    def __str__(self):
        ports = "\n\t\t".join([str(p) for p in self.ports])
        return f"{self.name} ({self.uri})\n\tPorts:\n\t\t{ports}\n\tPatch:{self.patch}"
    def create_global_effect(self, host: Host):
        import effect
        e = effect.Effect(self, host, self.uri, globalEffect=True)
        return e
    def create_effect(self, host: Host, id: int = None):
        import effect
        e = effect.Effect(self, host, self.uri, id)
        return e
    def get_input_controls(self):
        return [p.symbol for p in self.ports if p.is_control and p.is_input]
    
    def get_patch_controls(self):
        return self.patch['@id']


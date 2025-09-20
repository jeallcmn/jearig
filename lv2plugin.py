import json
import effect

class Port:
    def __init__(self, json):
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
    def load(file):
        print(f"Loading {file}")
        with open(file) as jsonFile:
            return Plugin(json.load(jsonFile))
        
    def __init__(self, json):
        self.uri = json.get('@id')
        self.name = json.get('doap:name') or 'Unknown Effect'
        self.ports = []
        # if json.get('lv2:port'):
        self.ports = [Port(p) for p in json['lv2:port']]
        self.patch = json.get('http://lv2plug.in/ns/ext/patch#writable')
    def __str__(self):
        ports = "\n\t\t".join([str(p) for p in self.ports])
        return f"{self.name} ({self.uri})\n\tPorts:\n\t\t{ports}\n\tPatch:{self.patch}"
    def create_effect(self, host):
        e = effect.Effect(host, self.uri)
        # if self.patch:
        #     patchId = self.patch['@id']
        #     p = patchId.split["#"][1]
        #     setattr(e, p, lambda x: e.patch(patchId, x))
        return e


if __name__=="__main__":
    import sys
    plugin = Plugin.load(sys.argv[1])
    # with open(sys.argv[1]) as file:
    #     plugin = Plugin(json.load(file))
    #     print(plugin)

# class Entry:
#     def __init__(self, indent, name, children=[]):
#         self.indent = indent
#         self.name = name
#         self.children = children

#     def get_indents(line):
#         return len(line) - len(lin.lstrip())
     
#     def read_from_lines(indent, lines):

        

# lines = []

# with open('plugins/nam.plugin') as file:
#     lines = [line for line in file]

# #print (lines)
# uri = lines[0].strip()

# lines = lines[2:]

# print(lines)


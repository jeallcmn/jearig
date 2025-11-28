import socket
import atexit
import signal
import time
import jack

class ModProtocol:
    def add(self, uri: str, id: str):
        return f"add {uri} {id}"
    def remove(self, id):
        return f"remove {id}"
    def connect(self, src: str, dst: str):
        return f"connect {src} {dst}"
    def disconnect(self, src: str, dst: str):
        return f"disconnnect {src} {dst}"
    def set_bpm(self, num:int):
        return f"set_bpm {num}"
    def set_bpb(self, num: int):
        return f"set_bpb {num}"        
    def transport(self, rolling: int, bpb: int, bpm: int):
        return 'transport {} {} {}'.format(rolling, bpb, bpm)
    def transport_sync(self, mode: str):
        return 'transport_sync {}'.format(mode)
    def preset_load(self, id: int, uri: str):
        return 'preset_load {} {}'.format(id, uri)
    def preset_save(self, id: int, name: str, dir: str, file: str):
        return 'preset_save {} {} {} {}'.format(id, name, dir, file)
    def preset_show(self, uri: str):
        return 'preset_show {}'.format(uri)
    def param_set(self, id: int, symbol: str, value: str):
        return 'param_set {} {} {}'.format(id, symbol, value)
    def param_get(self, id: int, symbol: str):
        return 'param_get {} {}'.format(id, symbol)
    def param_monitor():
        pass
    def patch_set(self, id: int, uri: str, value: str):
        return 'patch_set {} {} "{}"'.format(id, uri, value)  
    def patch_get(self, id: int, uri: str):
        return 'patch_get {} {}'.format(id, uri)      
    def monitor():
        pass
    def midi_learn(self, plugin: str, param: str):
        pass
    def midi_map(self,plugin, param: str, midi_chanel:int, midi_cc:int):
        pass
    def midi_unmap(self,plugin: str, param: str):
        pass
    def bypass(self, id: int, active: bool):
        return 'bypass {} {}'.format( id,
            1 if active else 0
        )
    def load(self, filename: str):
        return 'load {}'.format(filename)
    def save(self, filename: str):
        return 'save {}'.format(filename)
    def help(self):
        return 'help'
    def quit(self):
        return 'quit'

class ModConnection(object):
    client = None

    def __init__(self, socket_port: int=5555, address: str='localhost'):
        self.client = socket.socket()
        self.client.connect((address, socket_port))
        self.client.settimeout(5)

    def send(self, message: str):
        # print(message.encode('utf-8'))
        self.client.send(message.encode('utf-8'))
        received = self.client.recv(1024)
        return received
        # time.sleep(0.1)
        # return None

    def close(self):
        self.client.close()

class Host():
    
    def __init__(self, socket_port:int=5555, address: str='localhost'):
        self.connection = ModConnection(socket_port, address)
        self.protocol = ModProtocol()
        self.jack = jack.Client(name='Jack client', no_start_server=True)
        self.set_xrun_callback(Host.print_xrun)
        self.jack.activate()

        self.ids = []
        #register shutdown hooks
        @atexit.register
        def cleanup():
            self.remove_all()
        def terminate(arg1, arg2):
            self.remove_all()
        signal.signal(signal.SIGTERM, terminate)

    def get_random_id(self):
        import random
        id = random.randint(0, 9000)
        while id in self.ids:
            id = random.randint(0, 9000)
        self.ids.append(id)
        return id

    def print_xrun(msg: str):
        # print(f"XRun: {msg}")
        pass
    def cpu_load(self):
        return self.jack.cpu_load()
    def set_xrun_callback(self, callback):
        return self.jack.set_xrun_callback(callback)

    def add(self, uri: str, id: int = None):
        if not id:
            id = self.get_random_id()
        self.ids.append(id)
        self.connection.send(self.protocol.add(uri, id))
        return id
    def remove(self, id:int):
        self.ids.remove(id)
        return self.connection.send(self.protocol.remove(id))
    def connect(self, src: str, dst: str):
        return self.connection.send(self.protocol.connect(src, dst))
    def disconnect(self, src: str, dst: str):
        return self.connection.send(self.protocol.disconnect(src, dst))
    def set_bpm(self, num:int):
        return self.connection.send(self.protocol.set_bpm(num))
    def set_bpb(self, num:int):
        return self.connection.send(self.protocol.set_bpb(num))
    def transport(self, rolling:int, bpb:int, bpm:int):
        return self.connection.send(self.protocol.transport(rolling, bpb, bpm))
    def transport_sync(self, mode:int):
        return self.connection.send(self.protocol.transport_sync(mode))
    def preset_load(self, id:int, uri: str):
        return self.connection.send(self.protocol.preset_load(id, uri))
    def preset_save(self, id: int, name: str, dir: str, file: str):
        return self.connection.send(self.protocol.preset_save(id, name, dir, file))
    def preset_show(self, uri: str):
        return self.connection.send(self.protocol.preset_show(uri))
    def param_set(self, id: int, symbol: str, value: str):
        return self.connection.send(self.protocol.param_set(id, symbol, value))
    def param_get(self, id: int, symbol: str):
        response = str(self.connection.send(self.protocol.param_get(id, symbol)))
        return float(response.split(' ')[2].split('\\')[0])
    def param_monitor(self):
        return self.connection.send(self.protocol.param_monitor(id))
    def patch_set(self, id: int,  uri: str, value: str):
        return self.connection.send(self.protocol.patch_set(id, uri, value))
    def patch_get(self, id: int,  uri: str):
        return self.connection.send(self.protocol.patch_get(id, uri))    
    def monitor(self):
        return self.connection.send(self.protocol.monitor())
    def midi_learn(self, id: int, param: str):
        return self.connection.send(self.protocol.midi_learn(id, param))
    def midi_map(self,id: int, param: str, midi_channel: int, midi_cc: int):
        return self.connection.send(self.protocol.midi_map(id, param, midi_channel, midi_cc))
    def midi_unmap(self,id: int, param: str):
        return self.connection.send(self.protocol.midi_unmap(id, param))
    def bypass(self, id: int, active: bool):
        return self.connection.send(self.protocol.bypass(id, active))
    def load(self, filename: str):
        return self.connection.send(self.protocol.load(filename))
    def save(self, filename: str):
        return self.connection.send(self.protocol.save(filename))
    def help(self):
        return self.connection.send(self.protocol.help())
    def quit(self):
        return self.connection.send(self.protocol.quit())
    def remove_all(self):
        for i in self.ids:
            self.remove(i)   

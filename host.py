import socket
import atexit
import signal
import time
import jack

class ModProtocol:
    def add(self, uri, id):
        return f"add {uri} {id}"
    def remove(self, id):
        return f"remove {id}"
    def connect(self, src, dst):
        return f"connect {src} {dst}"
    def disconnect(self, src, dst):
        return f"disconnnect {src} {dst}"
    def set_bpm(self, num):
        return f"set_bpm {num}"
    def set_bpb(self, num):
        return f"set_bpb {num}"        
    def transport(self, rolling, bpb, bpm):
        return 'transport {} {} {}'.format(rolling, bpb, bpm)
    def transport_sync(self, mode):
        return 'transport_sync {}'.format(mode)
    def preset_load(self, id, uri):
        return 'preset_load {} {}'.format(id, uri)
    def preset_save(self, id, name, dir, uri):
        return 'preset_save {} {} {} {}'.format(id, name, dir, uri)
    def preset_show(self, id, uri):
        return 'preset_show {} {}'.format(id, uri)
    def param_set(self, id, symbol, value):
        return 'param_set {} {} {}'.format(id, symbol, value)
    def param_get(self, id, symbol):
        return 'param_get {} {}'.format(id, symbol)
    def param_monitor():
        pass
    def patch_set(self, id, uri, value):
        return 'patch_set {} {} "{}"'.format(id, uri, value)  
    def monitor():
        pass
    def midi_learn(self, plugin, param):
        pass
    def midi_map(self,plugin, param, midi_chanel, midi_cc):
        pass
    def midi_unmap(self,plugin, param):
        pass
    def bypass(self, id, active):
        return 'bypass {} {}'.format( id,
            1 if active else 0
        )
    def load(self, filename):
        return 'load {}'.format(filename)
    def save(self, filename):
        return 'save {}'.format(filename)
    def help(self):
        return 'help'
    def quit(self):
        return 'quit'

class ModConnection(object):
    client = None

    def __init__(self, socket_port=5555, address='localhost'):
        self.client = socket.socket()
        self.client.connect((address, socket_port))
        self.client.settimeout(5)

    def send(self, message):
        # print(message.encode('utf-8'))
        self.client.send(message.encode('utf-8'))
        received = self.client.recv(1024)
        return received
        # time.sleep(0.1)
        # return None

    def close(self):
        self.client.close()

class Host():
    
    def __init__(self, socket_port=5555, address='localhost'):
        self.connection = ModConnection(socket_port, address)
        self.protocol = ModProtocol()
        self.jack = jack.Client(name='Jack client', no_start_server=True)
        self.set_xrun_callback(Host.print_xrun)
        self.jack.activate()

        self.effects = []
        #register shutdown hooks
        @atexit.register
        def cleanup():
            self.remove_all()
        def terminate(arg1, arg2):
            self.remove_all()
        signal.signal(signal.SIGTERM, terminate)

    def print_xrun(msg):
        # print(f"XRun: {msg}")
        pass
    def cpu_load(self):
        return self.jack.cpu_load()
    def set_xrun_callback(self, callback):
        return self.jack.set_xrun_callback(callback)

    def add(self, uri):
        id = len(self.effects)
        self.effects.append(id)
        self.connection.send(self.protocol.add(uri, id))
        return id
    def remove(self, id):
        return self.connection.send(self.protocol.remove(id))
    def connect(self, src, dst):
        return self.connection.send(self.protocol.connect(src, dst))
    def disconnect(self, src, dst):
        return self.connection.send(self.protocol.disconnect(src, dst))
    def set_bpm(self, num):
        return self.connection.send(self.protocol.set_bpm(num))
    def set_bpb(self, num):
        return self.connection.send(self.protocol.set_bpb(num))
    def transport(self, rolling, bpb, bpm):
        return self.connection.send(self.protocol.transport(rolling, bpb, bpm))
    def transport_sync(self, mode):
        return self.connection.send(self.protocol.transport_sync(mode))
    def preset_load(self, id, uri):
        return self.connection.send(self.protocol.preset_load(id, uri))
    def preset_save(self, id, name, dir, uri):
        return self.connection.send(self.protocol.preset_save(id, name, dir, uri))
    def preset_show(self, id, uri):
        return self.connection.send(self.protocol.preset_show(id, uri))
    def param_set(self, id, symbol, value):
        return self.connection.send(self.protocol.param_set(id, symbol, value))
    def param_get(self, id, symbol):
        return self.connection.send(self.protocol.param_get(id, symbol))
    def param_monitor(self):
        return self.connection.send(self.protocol.param_monitor(id))
    def patch_set(self, id,  uri, value):
        return self.connection.send(self.protocol.patch_set(id, uri, value))
    def monitor(self):
        return self.connection.send(self.protocol.monitor())
    def midi_learn(self, id, param):
        return self.connection.send(self.protocol.midi_learn(id, param))
    def midi_map(self,id, param, midi_channel, midi_cc):
        return self.connection.send(self.protocol.midi_map(id, param, midi_channel, midi_cc))
    def midi_unmap(self,id, param):
        return self.connection.send(self.protocol.midi_unmap(id, param))
    def bypass(self, id, active):
        return self.connection.send(self.protocol.bypass(id, active))
    def load(self, filename):
        return self.connection.send(self.protocol.load(filename))
    def save(self, filename):
        return self.connection.send(self.protocol.save(filename))
    def help(self):
        return self.connection.send(self.protocol.help())
    def quit(self):
        return self.connection.send(self.protocol.quit())
    def remove_all(self):
        for i in self.effects:
            self.remove(i)        


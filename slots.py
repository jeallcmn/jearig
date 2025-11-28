
from pedalboard import Pedalboard

class SlotManager:
    def __init__(self, pedalboard: Pedalboard):
        self.slots = [None, None, None, None]
        self.pedalboard: Pedalboard = pedalboard

    def clear_slot(self, index):
        if self.slots[index]:
            self.slots[index].disconnect_all()
            self.slots[index].remove()
        self.slots[index] = None

    def set_slot(self, index:int, plugin_name: str):



    def reconnect_all(self):
        if len(self.slots) <= 0:
            return
        
        self.device.disconnect_all()



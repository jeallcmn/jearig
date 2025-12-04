from chain import EffectChain
from host import Host
from effect import Effect

class Pedalboard():
    """
    A fixed length effect chain with set order.
    """
    def __init__(self, host):
        self.chain: EffectChain = EffectChain("pedalboard", host)
        self.slots = 10

    def find_effect_after(self, index) -> Effect:
        for i in range(index+1, self.slots):
            e = self.chain.get_effect(f"effect_{i}")
            if e:
                return e
        # No effects are before this one, so return the system device 
        return self.chain.device
            
    def find_effect_before(self, index) -> Effect:
        """ Returns the closest effect _before_ the index"""
        for i in reversed(range(0, index)):
            e = self.chain.get_effect(f"effect_{i}")
            if e:
                return e
        return self.chain.device
                
    def get_effect(self, index) -> Effect:
        return self.chain.get_effect(f"effect_{index}")

    def remove_effect(self, index):
        """
        Removes and disconnects an effect in the given slot
        """
        effect = self.get_effect(index)
        if effect:
            print(f"Removing effect: {effect.name}")
            effect.remove()

        

    def insert_effect(self, index, name) -> Effect:
        """ 
        Inserts an effect at the given slot.  Effects are named for the slot they occupy.  If an effect is there already, remove it first
        If possible, automatically connect the effects closeds before and after the inserted effect.
        """
        self.remove_effect(index)

        prev = self.find_effect_before(index)
        next = self.find_effect_after(index)
        
        print(f"Inserting effect {index} between {prev.name} & {next.name}")
        # Break the old connections between the prev & next
        prev.disconnect_all(next)

        effect = self.chain.create_effect(name, index)

        prev.connect(effect)
        effect.connect(next)
        return effect

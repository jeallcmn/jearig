import os

# manages available patches in a set folder:
# <set>/<patch>.<extension>
class PatchManager:
    def __init__(self, effect, extension, input_dir, output_dir):
        self.sets = []
        self.patches =[]
        self.setIndex = 0
        self.patchIndex = 0
        self.sets = sorted([x for x in os.listdir(input_dir)])
        self.input_dir = input_dir
        self.output_dir = output_dir
        self.effect = effect
        self.extension = extension

        # self.audition_current()

    def get_current_patch(self):
        set = self.sets[self.setIndex]
        patch = self.patches[self.patchIndex]
        return os.path.join(self.input_dir, set, patch)
    
    def load_patch_options(self):
        self.patches = sorted([x for x in os.listdir(os.path.join(self.input_dir, self.sets[self.setIndex])) if x.endswith(self.extension   )])

    def next_set(self):
        self.setIndex += 1
        if(self.setIndex >= len(self.sets)):
            self.setIndex = 0
        self.patchIndex = 0
        self.load_patch_options()
        self.load_current_patch()

    def prev_set(self):
        self.setIndex -= 1
        if(self.setIndex < 0):
            self.setIndex = len(self.sets) - 1
        self.patchIndex = 0 
        self.load_current_patch()

    def load_current_patch(self):
        self.load_patch_options()
        current = self.get_current_patch()
        print(f"Auditioning: {current}")
        self.effect.patch(current)

    def prev_patch(self):
        self.patchIndex -= 1
        if(self.patchIndex < 0):
            self.patchIndex = len(self.patches) - 1
        self.load_current_patch()

    def next_patch(self):
        self.patchIndex += 1
        if(self.patchIndex >= len(self.patches)):
            self.patchIndex = 0
        self.load_current_patch()


import lv2plugin
from host import Host
from effect import Effect,SystemEffect
from drumkit import DrumKit
from state import StateManager
from patch import PatchManager
from chain import EffectChain
host = Host()

chain = EffectChain("sequencer", host)


stateManager = StateManager()

amp       = chain.create_effect("Neural Amp Modeler")
tonestack = chain.create_effect("3 Band EQ")
cab       = chain.create_effect("IR loader cabsim")
eq        = chain.create_effect("EQ4Q Stereo")
reverb    = chain.create_effect("Dragonfly Hall Reverb")
sequencer    = chain.create_effect("MIDI Step Sequencer8x8")
drumkit    = chain.create_effect("Red Zeppelin Drumkit")


device = chain.device

device.connect(amp)
amp.connect(tonestack)
tonestack.connect(cab)
cab.connect(eq)
eq.connect(reverb)
reverb.connect(device)

drumkit.connect(reverb)
sequencer.connect_midi(drumkit)

#Configure ToneStack
tonestack.param('low', 0)
tonestack.param('mid', 0)
tonestack.param('high', 0)
tonestack.param('master', '-3')
tonestack.param('low_mid', 120)
tonestack.param('mid_high', 2300)

# # Set a low pass filter for global EQ
eq.param('filter4_enable', 1)
eq.param('filter4_gain', -12)
eq.param('filter4_type', 10)
eq.param('filter4_freq', 8000)
eq.param('filter4_q', .7)

amp.patch('/home/jona/Desktop/5150-2.nam')
cab.patch('/home/jona/m25.wav')

reverb.param('size', 40)
reverb.param('decay', 1.1)
reverb.param('early_send', 10)


kit = DrumKit(sequencer)

kit.set_kick([120,0,0,0,120,0,0,0])
kit.set_snare([0,0,120,0,0,0,120,0])
kit.set_hihat([120,120,120,120,120,120,120,120])

stateManager.save_chain(chain)

# def patch1():
#     amp.patch('model', '/home/jona/Desktop/5150-2.nam')
#     cab.patch('ir', '/home/jona/v30-7.wav')
#     tonestack.param('master', '-3')

# def patch2():
#     amp.patch('model', '/home/jona/Desktop/NAM/Dual Recto RED + Mudkiller.nam')
#     cab.patch('ir', '/home/jona/v30-7.wav')
#     tonestack.param('master', '3')

# sequencer.toggle()
# drumkit.toggle()

# ampManager = PatchManager(amp, '.nam', '/home/jona/work/nam', '/home/jona/work/test')
# cabManager = PatchManager(cab, '.wav', '/home/jona/work/irs', '/home/jona/work/test')
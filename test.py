import lv2plugin
from host import Host
from effect import Effect,SystemEffect
from drumkit import DrumKit
from state import StateManager
from patch import PatchManager
from pedalboard import Pedalboard
host = Host()

# pluginNames = ['amp', 'cab', 'globalEq', 'hallReverb', 'tonestack', 'sequencer', 'drumkit']
# plugins = dict([(name,lv2plugin.Plugin.load(f"plugins/{name}.json")) for name in pluginNames])

# device = SystemEffect(host)
# # Use only second input
# device.audio_outputs = device.audio_outputs[1:]

pedalboard = Pedalboard(host)

# amp         = plugins['amp'].create_effect(host)
# tonestack   = plugins['tonestack'].create_effect(host)
# cab         = plugins['cab'].create_effect(host)
# hallReverb  = plugins['hallReverb'].create_effect(host)
# globalEq    = plugins['globalEq'].create_effect(host)

# sequencer  = plugins['sequencer'].create_global_effect(host)
# drumkit  = plugins['drumkit'].create_global_effect(host)

# stateManager = StateManager()

amp       = pedalboard.create_effect("Neural Amp Modeler", True)
tonestack = pedalboard.create_effect("3 Band EQ", True)
cab       = pedalboard.create_effect("IR loader cabsim", True)
eq        = pedalboard.create_effect("EQ4Q Stereo", True)
reverb    = pedalboard.create_effect("Dragonfly Hall Reverb", True)

s1 = pedalboard.get_state()

# pedalboard.remove_all()

# pedalboard.set_state(s1)


# device.connect(amp)
# amp.connect(cab) 
# cab.connect(tonestack)
# tonestack.connect(hallReverb)
# hallReverb.connect(globalEq)
# globalEq.connect(device)

# drumkit.connect(hallReverb)

# sequencer.connect_midi(drumkit)

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
cab.patch('/home/jona/v30-7.wav')

reverb.param('size', 40)
reverb.param('decay', 1.1)
reverb.param('early_send', 10)


# kit = DrumKit(sequencer)

# kit.set_kick([120,0,0,0,120,0,0,0])
# kit.set_snare([0,0,120,0,0,0,120,0])
# kit.set_hihat([120,120,120,120,120,120,120,120])

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
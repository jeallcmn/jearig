import lv2plugin
from host import Host
from effect import Effect,SystemEffect

host = Host()

pluginNames = ['amp', 'cab', 'globalEq', 'hallReverb', 'tonestack', 'sequencer', 'drumkit']
plugins = dict([(name,lv2plugin.Plugin.load(f"plugins/{name}.json")) for name in pluginNames])

device = SystemEffect(host)
# Use only second input
device.audio_outputs = device.audio_outputs[1:]


amp         = plugins['amp'].create_effect(host)
tonestack   = plugins['tonestack'].create_effect(host)
cab         = plugins['cab'].create_effect(host)
hallReverb  = plugins['hallReverb'].create_effect(host)
globalEq    = plugins['globalEq'].create_effect(host)
sequencer  = plugins['sequencer'].create_effect(host)
drumkit  = plugins['drumkit'].create_effect(host)


device.connect(amp)
amp.connect(cab) 
cab.connect(tonestack)
tonestack.connect(hallReverb)
hallReverb.connect(globalEq)
globalEq.connect(device)

drumkit.connect(hallReverb)

sequencer.connect_midi(drumkit)

#Configure ToneStack
tonestack.param('low', 0)
tonestack.param('mid', 0)
tonestack.param('high', 0)
tonestack.param('master', '-3')
tonestack.param('low_mid', 120)
tonestack.param('mid_high', 2300)

# Set a low pass filter for global EQ
globalEq.param('filter4_enable', 1)
globalEq.param('filter4_gain', -12)
globalEq.param('filter4_type', 10)
globalEq.param('filter4_freq', 6000)
globalEq.param('filter4_q', .7)

amp.patch('model', '/home/jona/Desktop/5150-2.nam')
cab.patch('ir', '/home/jona/v30-7.wav')

#Midi
host.transport(1, 4, 134)
host.transport_sync('midi')

# Sequencery / Drum Track
sequencer.param('drummode', 1) # change to drum sequencing, otherwise not all events are fired
sequencer.param('sync', 1) # Sync to host (mod)
sequencer.param('div', 2) # 8th

#Instruments
sequencer.param('note1', 36)
sequencer.param('note2', 38)
sequencer.param('note3', 42)


# #Kick
sequencer.param('grid_1_1', 120)
sequencer.param('grid_5_1', 120)
sequencer.param('grid_8_1', 120)
# # Snare
sequencer.param('grid_3_2', 120)
sequencer.param('grid_7_2', 120)


for i in range(1,9):
    sequencer.param(f"grid_{i}_3", 120)

#host.transport(True, 128, 128)
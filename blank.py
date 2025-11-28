import host
import pedalboard
import state

h = host.Host()
p = pedalboard.Pedalboard("default", h)
sm = state.StateManager()


sm.load_pedalboard("sequencer", p)
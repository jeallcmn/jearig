import host
import chain
import state

h = host.Host()
p = chain.EffectChain("default", h)
sm = state.StateManager()


sm.load_chain("sequencer", p)
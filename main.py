from ui import JEARigUI

import host
import chain

h = host.Host()
p = chain.EffectChain("default", h)


app = JEARigUI(chain)
app.run()
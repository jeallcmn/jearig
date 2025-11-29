from ui import JEARigUI

import host
import pedalboard

h = host.Host()
p = pedalboard.Pedalboard("default", h)


app = JEARigUI(pedalboard)
app.run()
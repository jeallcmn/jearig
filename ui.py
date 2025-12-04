from textual.app import App, ComposeResult
from textual.widgets import Footer, Header, Button, ContentSwitcher, OptionList, Label,DirectoryTree
from textual.containers import Horizontal, Vertical
from textual.screen import Screen
from textual.widget import Widget
from textual import on
from textual.screen import ModalScreen
from textual_slider import Slider

import host
import pedalboard
import state
from patch import PatchManager

host = host.Host()
pedalboard = pedalboard.Pedalboard(host)
state = state.StateManager()
amp = pedalboard.insert_effect(2, "Neural Amp Modeler")
tonestack = pedalboard.insert_effect(3, "3 Band EQ")
cab = pedalboard.insert_effect(4, "IR loader cabsim")
eq = pedalboard.insert_effect(5, "EQ4Q Stereo")
reverb = pedalboard.insert_effect(6, "Dragonfly Hall Reverb")
pedalboard.get_effect(2).patch('/home/jona/Desktop/5150-2.nam')
pedalboard.get_effect(4).patch('/home/jona/m25.wav')

tonestack.param('master', -6)

eq.param('filter4_enable', 1)
eq.param('filter4_gain', -12)
eq.param('filter4_type', 10)
eq.param('filter4_freq', 8000)
eq.param('filter4_q', .7)
reverb.param('size', 40)
reverb.param('decay', 1.1)
reverb.param('early_level', 5)
reverb.param('late_level', 10)

#ampManager = PatchManager(amp, ".nam", "/home/jona/work/nam", "./")

# class PluginPicker(Widget):
#     def __init__(self, num_slots):
#         self.num_slots = num_slots

#     def compose(self) -> ComposeResult:
#         with Horizontal()


# class PluginPicker(ModalScreen):
#     def compose(self) -> ComposeResult:
#         with Vertical():
#             yield OptionList(*[x.name for x in pedalboard.chain.plugins])
#             yield Button("Done", id="done")
#     def on_button_pressed(self, event: Button.Pressed) -> None:
#         self.app.pop_screen()

# class PatchPicker(ModalScreen):
#     """ Screen for choosing patches"""
#     def __init__(self, slot, dir):
#         self.slot = slot
#         self.dir = dir
#         ModalScreen.__init__(self)
#     def compose(self) -> ComposeResult:
#         with Vertical():
#             yield DirectoryTree(self.dir)
#             yield Button("Done", id="done")

#     def on_directory_tree_file_selected(self, event: DirectoryTree.FileSelected) -> None:
#         pedalboard.get_effect(self.slot).patch(event.path)

#     def on_button_pressed(self, event: Button.Pressed) -> None:
#         if event.button.id == "done":
#             self.app.pop_screen()

    # @on(OptionList.OptionSelected, "#amp-selection")
    # def handle_amp_selected(self, event: OptionList.OptionSelected) -> None:
    #     i = event.option_index
    #     ampManager.select_set(i)
    #     self.query_one("#capture-selection").set_options(ampManager.patches)

    # @on(OptionList.OptionSelected, "#capture-selection")
    # def handle_patch_selected(self, event: OptionList.OptionSelected) -> None:
    #     i = event.option_index
    #     ampManager.select_patch(i)

    # def on_mount(self) -> None:
    #     self.query_one("#amp-selection").border_title = "Amp"
# class EffectBlock(Widget):
#     def __init__(self, slot, id):
#         self.slot = slot
#         Widget.__init__(self, id)
#     def compose(self) -> ComposeResult:
# #         yield Label(self.slot)

# class AmpApp(App[None]):
#     CSS_PATH = "ui.tcss"
#     BINDINGS = [
#         # ("a", "choose_amp", "Amp"),
#         # ("p", "choose_plugin", "Plugin")
#                 ]

#     def compose(self) -> ComposeResult:
#         yield Header()
#         with Horizontal(id="effect_chain"):
#             yield Button("1", id="effect1")           
#             yield Button("2", id="effect2")
#             yield Button("3", id="effect3")
#             yield Button("4", id="effect4")
#             yield Button("5", id="effect5")
#             yield Button("6", id="effect6")
#         with ContentSwitcher(initial="effect1"):
#             yield Label("1", id="effect1")
#             yield Label("2", id="effect2")
#             yield Label("3", id="effect3")
#             yield Label("4", id="effect4")
#             yield Label("5", id="effect5")
#             yield Label("6", id="effect6")
#         yield Footer()
#     def on_button_pressed(self, event: Button.Pressed) -> None:
#         self.query_one(ContentSwitcher).current = event.button.id
    # def on_button_pressed(self, event: Button.Pressed) -> None:
    #     if event.button.id == "amp":
    #         self.push_screen(PatchPicker(2, "/home/jona/work/nam"))
    #     if event.button.id == "cab":
    #         self.push_screen(PatchPicker(4,"/home/jona/work/irs"))            
    #     if event.button.id == "plugin":
    #         self.push_screen(PluginPicker())
    # # def action_choose_amp(self) -> None:
    

    # def on_option_list_option_selected(self, event: OptionList.OptionSelected) -> None:
    #     print(f"here: {event.option_index}")




    # @on(OptionList.OptionHighlighted, "#amp-selection")
    # def handle_amp_highlighted(self, event: OptionList.OptionHighlighted) -> None:
    #     i = event.option_index
    #     print(f"Highlighted {i}")
    #     # ampManager.select_set(i)
    #     # print(ampManager.patches)
    #     # self.query_one("#capture-selection").set_options(ampManager.patches)

from textual.widgets import ProgressBar, Static
from textual.containers import Center
from effect import Effect

class ParamSlider(Vertical):
    def __init__(self,
        effect: Effect,
        param_name: str,
        name: str | None = None,
        id: str | None = None,
        classes: str | None = None,
        disabled: bool = False,
        markup: bool = True):
        super().__init__( 
                         name=name,
                         id=id, 
                         classes=classes,
                         disabled=disabled,
                         markup=markup
        )
        self.effect = effect
        self.control = effect.plugin.get_input_control_map()[param_name]
        # Control values are scaled to 0 to 100 for consistency
        self.min = 0.0
        self.max = 100.0
    def scale_number(self, value, source_range_min, source_range_max, target_range_min, target_range_max):
        normalized_value = (value - source_range_min) / (source_range_max - source_range_min)
        scaled_value = normalized_value * (target_range_max - target_range_min) + target_range_min
        return scaled_value
    
    def to_control_value(self, value) -> int:
        return self.scale_number(value, self.min, self.max, self.control.minimum, self.control.maximum)
    
    def from_control_value(self, value) -> int:
        return self.scale_number(value, self.control.minimum, self.control.maximum, self.min, self.max)
    
    def compose(self) -> ComposeResult:
        v = self.effect.get_param(self.control.symbol)
        sv = self.from_control_value(v)
        print(f"Value: {v} -> {sv}")
        yield Static(self.name)
        with Horizontal():
            yield Label(f"{self.min}")
            yield Slider(min=0, max=100, value=sv, step=1, id=f"{self.id}_slider")
            yield Label(f"{self.max}")
        yield Static(f"{sv}", id=f"{self.id}_current_value")
    def on_slider_changed(self, event: Slider.Changed) -> None:
        self.query_one(f"#{self.id}_current_value", Static).update(f"{event.value}")
        dv = self.to_control_value(event.value)
        self.effect.param(self.control.symbol, dv)

class AmpApp(App[None]):
    CSS_PATH = "ui.tcss"
    BINDINGS = [
        # ("a", "choose_amp", "Amp"),
        # ("p", "choose_plugin", "Plugin")
                ]

    def compose(self) -> ComposeResult:
        with Center():
            yield ParamSlider(effect=tonestack, param_name="master",id="volume", name="Volume")
            yield ParamSlider(effect=tonestack, param_name="high", id="treble", name="Treble")
            yield ParamSlider(effect=tonestack, param_name="mid", id="middle", name="Mid")
            yield ParamSlider(effect=tonestack, param_name="low", id="low", name="Bass")
            # with Vertical():
            #     yield Static("Volume", id="slider_name")
            #     yield Slider(min=0, max=100, value=50, step=5, id="slider")
            #     yield Static("50", id="current_value")

    
    # def on_slider_changed(self, event: Slider.Changed) -> None:
    #         """Handles slider value changes."""
    #         self.query_one("#slider_value_display", Static).update(
    #             f"Current value: {event.value}"
    #         )

if __name__ == "__main__":
    AmpApp().run()

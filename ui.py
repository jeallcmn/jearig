from textual.app import ComposeResult, App
from textual.containers import Container, Horizontal, Vertical, Grid
from textual.widgets import Button, Static, Label, ListItem, ListView
from textual.screen import Screen
from pedalboard import Pedalboard
from effect import Effect
import lv2plugin

class PedalboardScreen(Screen):
    """Screen displaying the pedalboard with 8 effect slots."""
    
    BINDINGS = [("q", "quit", "Quit")]
    
    def __init__(self, pedalboard: Pedalboard):
        super().__init__()
        self.pedalboard = pedalboard
        self.effect_buttons = []
    
    def compose(self) -> ComposeResult:
        yield Vertical(
            Label("Pedalboard - 8 Effect Slots", id="header"),
            Horizontal(*[self._create_effect_button(i) for i in range(8)], id="effects-grid"),
            id="pedalboard-container"
        )
    
    def _create_effect_button(self, slot: int) -> Button:
        """Create a button for an effect slot."""
        effect = self.pedalboard.effects[slot] if slot < len(self.pedalboard.effects) else None
        label = effect.plugin.name if effect else f"Slot {slot + 1}"
        button = Button(label, id=f"effect-{slot}", variant="primary" if effect else "default")
        self.effect_buttons.append(button)
        return button
    
    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button clicks for effect slots."""
        button = event.button
        slot = int(button.id.split("-")[1])
        
        if slot < len(self.pedalboard.effects):
            # Edit existing effect
            self.app.push_screen(EditEffectScreen(self.pedalboard, self.pedalboard.effects[slot]))
        else:
            # Choose a new effect
            self.app.push_screen(ChooseEffectScreen(self.pedalboard, slot))
    
    def on_screen_resume(self) -> None:
        """Refresh the display when returning from another screen."""
        self._refresh_buttons()
    
    def _refresh_buttons(self) -> None:
        """Update button labels to reflect current pedalboard state."""
        for i in range(8):
            button = self.effect_buttons[i]
            effect = self.pedalboard.effects[i] if i < len(self.pedalboard.effects) else None
            if effect:
                button.label = effect.plugin.name
                button.variant = "primary"
            else:
                button.label = f"Slot {i + 1}"
                button.variant = "default"


class ChooseEffectScreen(Screen):
    """Screen for choosing an effect to add to a slot."""
    
    BINDINGS = [("escape", "back", "Back")]
    
    def __init__(self, pedalboard: Pedalboard, slot: int):
        super().__init__()
        self.pedalboard = pedalboard
        self.slot = slot
    
    def compose(self) -> ComposeResult:
        plugins = [p.name for p in self.pedalboard.plugins]
        yield Vertical(
            Label(f"Choose Effect for Slot {self.slot + 1}", id="header"),
            ListView(
                *[ListItem(Label(plugin), id=f"plugin-{i}") for i, plugin in enumerate(plugins)],
                id="plugin-list"
            ),
            id="choose-effect-container"
        )
    
    def on_list_view_selected(self, event: ListView.Selected) -> None:
        """Handle selecting a plugin from the list."""
        plugin_index = int(event.item.id.split("-")[1])
        plugin_name = self.pedalboard.plugins[plugin_index].name
        
        # Create the effect
        self.pedalboard.create_effect(plugin_name)
        
        # Return to pedalboard screen
        self.app.pop_screen()


class EditEffectScreen(Screen):
    """Screen for editing an effect's parameters."""
    
    BINDINGS = [("escape", "back", "Back"), ("t", "toggle", "Toggle")]
    
    def __init__(self, pedalboard: Pedalboard, effect: Effect):
        super().__init__()
        self.pedalboard = pedalboard
        self.effect = effect
    
    def compose(self) -> ComposeResult:
        params = self.effect.plugin.get_input_controls()
        
        yield Vertical(
            Label(f"Edit: {self.effect.plugin.name}", id="header"),
            Label(f"Enabled: {self.effect.enabled}", id="enabled-label"),
            Horizontal(
                Button("Toggle", id="toggle-btn", variant="success"),
                Button("Remove", id="remove-btn", variant="error"),
                id="effect-controls"
            ),
            Vertical(
                *[self._create_param_control(param) for param in params],
                id="parameters"
            ),
            id="edit-effect-container"
        )
    
    def _create_param_control(self, param_name: str) -> Container:
        """Create a control for a parameter."""
        value = self.effect.get_param(param_name)
        return Container(
            Label(f"{param_name}: {value:.2f}", id=f"param-{param_name}"),
            id=f"param-container-{param_name}"
        )
    
    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button clicks."""
        if event.button.id == "toggle-btn":
            self.effect.toggle()
            self._update_enabled_label()
        elif event.button.id == "remove-btn":
            self.pedalboard.remove_effect(self.effect)
            self.app.pop_screen()
    
    def _update_enabled_label(self) -> None:
        """Update the enabled status label."""
        label = self.query_one("#enabled-label", Label)
        label.update(f"Enabled: {self.effect.enabled}")
    
    def action_toggle(self) -> None:
        """Action to toggle the effect."""
        self.effect.toggle()
        self._update_enabled_label()
    
    def action_back(self) -> None:
        """Return to pedalboard screen."""
        self.app.pop_screen()


class SettingsScreen(Screen):
    """Screen for global settings."""
    
    BINDINGS = [("escape", "back", "Back")]
    
    def __init__(self, pedalboard: Pedalboard):
        super().__init__()
        self.pedalboard = pedalboard
    
    def compose(self) -> ComposeResult:
        yield Vertical(
            Label("Settings", id="header"),
            Label(f"Pedalboard: {self.pedalboard.name}"),
            Horizontal(
                Button("Save", id="save-btn", variant="success"),
                Button("Load", id="load-btn", variant="primary"),
                Button("Reset", id="reset-btn", variant="error"),
                id="settings-controls"
            ),
            id="settings-container"
        )
    
    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button clicks."""
        if event.button.id == "save-btn":
            self.pedalboard.save(None)
        elif event.button.id == "load-btn":
            pass  # Implement load logic
        elif event.button.id == "reset-btn":
            self.pedalboard.reset()
    
    def action_back(self) -> None:
        """Return to pedalboard screen."""
        self.app.pop_screen()


class JEARigUI(App):
    """Main Textual application for JEARig pedalboard."""
    
    CSS = """
    Screen {
        layout: vertical;
        background: $surface;
        color: $text;
    }
    
    #header {
        width: 100%;
        text-align: center;
        background: $accent;
        color: $text;
        border: solid $primary;
        padding: 1;
    }
    
    #pedalboard-container {
        width: 100%;
        height: 100%;
        border: solid $primary;
    }
    
    #effects-grid {
        width: 100%;
        height: auto;
        border: solid $secondary;
        padding: 1;
    }
    
    Button {
        width: 1fr;
        margin: 0 1;
    }
    
    #choose-effect-container, #edit-effect-container, #settings-container {
        width: 100%;
        height: 100%;
        border: solid $primary;
        padding: 1;
    }
    
    ListView {
        width: 100%;
        height: 1fr;
        border: solid $secondary;
    }
    
    #effect-controls, #settings-controls {
        width: auto;
        height: auto;
        margin: 1;
    }
    
    #parameters {
        width: 100%;
        height: auto;
        border: solid $secondary;
        padding: 1;
    }
    
    Label {
        margin: 0 1;
    }
    """
    
    BINDINGS = [
        ("1", "pedalboard", "Pedalboard"),
        ("2", "settings", "Settings"),
        ("q", "quit", "Quit"),
    ]
    
    def __init__(self, pedalboard: Pedalboard):
        super().__init__()
        self.pedalboard = pedalboard
    
    def on_mount(self) -> None:
        """Initialize the app with the pedalboard screen."""
        self.push_screen(PedalboardScreen(self.pedalboard))
    
    def action_pedalboard(self) -> None:
        """Switch to pedalboard mode."""
        self.push_screen(PedalboardScreen(self.pedalboard))
    
    def action_settings(self) -> None:
        """Switch to settings mode."""
        self.push_screen(SettingsScreen(self.pedalboard))

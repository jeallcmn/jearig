
sudo npm install -g @frogcat/ttl2jsonld

```bash
# Generate a ttl file from plugin
lv2info -p nam.ttl http://github.com/mikeoliphant/neural-amp-modeler-lv2
# Convert to json
ttl2jsonld nam.ttl > plugins/nam.json
# OR
cd plugins
./generate.sh
```


```bash
Running the Textual effects-chain UI

1. Install requirements:

```bash
pip install -r requirements.txt
```

2. Run the UI:

```bash
python textual_ui.py
```

Controls:
- `Ctrl-A`: add an effect after the currently selected effect (or at end when none selected)
- `Ctrl-I`: add an effect before the currently selected effect (or at front when none selected)
- Click an effect to select it. Drag from one effect and move onto another to create a connection (source -> target).

pip3 install textual
pip3 install textual-dev
pip3 install textural[syntax]
sudo apt-get install xclip

pip3 install "kivy[base]"
pip3 install kivymd2
```


# VSB
## Overview
A soundboard software that:
 - Doesn't need any proprietary hardware
 - Hosts a website accessible from virually any device
 - Can automatically change to Push-To-Talk mode on discord for better sound quality over calls
 - Can automatically mute a discord call after playing
---
## Installation
For basic functionality, VSB only needs Python 3.8 or higher with Pip.
```
git clone https://github.com/Snapwhiz914/VirtualSoundboard
cd VirtualSoundboard
pip3 install -r requirements.txt
```
In order to be able to play sound as if it was coming from your microphone (ie. discord use), you'll need to install a software for your OS that can do this. I use (VB Cabke)[https://vb-audio.com/Cable/] for Windows.
---
## Configuration
To add sounds, change sound outputs and edit discord keybinds, use the configuration UI:
```
cd VirtualSoundboard
python3 conf_ui.py
```
Sounds must be in the .wav format.
For the Keybinds section, I recommend using a keybind that won't interfere with games or other software. For example, I use:
 - Toggle Input Mode: <kbd>alt</kbd> + <kbd>[</kbd>
 - Toggle Mute: <kbd>ctrl</kbd> + <kbd>shift</kbd> + <kbd>m</kbd> (Note this one cannot be changed in discord)
 - Push to Talk: <kbd>alt</kbd> + <kbd>]</kbd>
Whatever you change in this menu you must also change in the discord menu. Note that Toggle Voice Input mode (Toggle VAD) needs to be added manually in the Keybinds menu. 

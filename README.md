# VSB
## Overview
A soundboard software that:
 - Doesn't need any proprietary hardware
 - Hosts a website accessible from virtually any device
 - Can automatically change to Push-To-Talk mode on Discord for better sound quality over calls
 - Can automatically mute a discord call after playing

## Installation
For basic functionality, VSB only needs Python 3.8 or higher with Pip.
```
git clone https://github.com/Snapwhiz914/VirtualSoundboard
cd VirtualSoundboard
pip3 install -r requirements.txt
```
To play sound as if it was coming from your microphone (ie. discord use), you'll need to install a software for your OS that can do this. I use [VB Cable](https://vb-audio.com/Cable/) for Windows.

## Usage
Open a Command Prompt or Terminal in the VirtualSoundboard directory
```
uvicorn main:app --host 0.0.0.0 --port 80
```
It will print your device's LAN address, which your trigger device must connect to. Make sure that both devices are on the same network. See notes and recommendations for more information.

## Configuration
To add sounds, change sound outputs and edit discord keybinds, use the configuration UI:
```
cd VirtualSoundboard
python3 conf_ui.py
```
 - Sounds must be in the .wav format.
 - Make sure to select your virtual audio device as an output if you wish to use it
 - For the Keybinds section, I recommend using a keybind that won't interfere with games or other software. For example, I use:
   - Toggle Input Mode: <kbd>alt</kbd> + <kbd>[</kbd>
   - Toggle Mute: <kbd>ctrl</kbd> + <kbd>shift</kbd> + <kbd>m</kbd> (Note this one cannot be changed in discord)
   - Push to Talk: <kbd>alt</kbd> + <kbd>]</kbd>
 - (These keybinds are also the default options)
 - Whatever you change in the keybinds menu you must also change in the discord menus to be the same. Note that Toggle Voice Input mode (Toggle VAD) needs to be added manually in the Keybinds menu.

## Notes & Recommendations
 - This software was made on a Python 3.9 environment running on a Windows 10 PC. It uses FastAPI to host the website, pynput to automatically press keybinds, and pyaudio & wav to play sound files
 - I use an old Kindle Fire (3rd gen) as my trigger device. Theoretically, any device with a web browser should work.
 - I recommend making your trigger device's display always on.

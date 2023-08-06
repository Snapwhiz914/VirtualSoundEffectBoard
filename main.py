from key_presser import KeyPresser
from player import SoundPlayer
import json
import threading
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
import os
import time
import socket

def get_confblock(block_name):
    j = json.load(open("conf.json", 'r'))
    return j[block_name]

sp = SoundPlayer(out_names=get_confblock("outputs"))
presser = KeyPresser()
app = FastAPI()

is_playing = ""

@app.get("/play", status_code=200)
def playsound(filename: str):
    global is_playing
    if filename == is_playing:
        sp.stop_current()
        return
    if len(is_playing) > 0: #Another file is playing
        print(f"{is_playing} is already playing")
        return
    mute = False
    rp = ""
    for sound in get_confblock("sounds"):
        if os.path.basename(sound["fp"]) == filename:
            mute = sound["mute"]
            rp = sound["fp"]
    print(f"Playing {filename} which is at {rp}")
    kbs = get_confblock("keybinds")
    presser.singlepress_combo(kbs["toggle_vc_mode"])
    time.sleep(0.5) # so discord can change modes
    hold_i = presser.hold(kbs["ptt"])
    def cb(hi, m):
        global is_playing
        presser.release(hi)
        presser.singlepress_combo(kbs["toggle_vc_mode"])
        if m: presser.singlepress_combo(kbs["mute"])
        is_playing = ""
    threading.Thread(target=sp.play_sound_t, args=(rp, cb, (hold_i, mute))).start()
    is_playing = filename

@app.get("/", status_code=200, response_class=HTMLResponse)
def give_site():
    buttons_html = ""
    for sound in get_confblock("sounds"):
        buttons_html += f'''<button class='gi' onclick="sendRequest(\'play?filename={os.path.basename(sound["fp"])}\')">{os.path.basename(sound["fp"]).replace(".wav", "")}</button>\n'''

    # HTML template with JavaScript function to handle button clicks
    html_content = open("templates/soundboard.html").read()
    html_content = html_content.replace("{buttons}", buttons_html)

    return HTMLResponse(content=html_content)

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 80))
print(f"Connect other device to: http://{s.getsockname()[0]} (Make sure both devices are on the same network)")
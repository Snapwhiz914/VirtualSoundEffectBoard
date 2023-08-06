import pynput
import time
import threading
from pynput.keyboard import Key

class KeyPresser():
    def __init__(self):
        self.cont = pynput.keyboard.Controller()
        self.strreps_to_objs = {
            "alt": Key.alt, "ctrl": Key.ctrl, "shift": Key.shift
        }
        self.holds = {}
    
    def singlepress_combo(self, combo_names):
        def t(cont, cnames, strreps):
            for key in cnames:
                if len(key) > 1:
                    cont.press(strreps[key])
                else:
                    cont.press(key)
                time.sleep(0.05)
            time.sleep(0.2)
            for key in cnames:
                if len(key) > 1:
                    cont.release(strreps[key])
                else:
                    cont.release(key)
                time.sleep(0.05)
        threading.Thread(target=t, args=(self.cont, combo_names, self.strreps_to_objs)).start()
    
    def hold(self, combo_names):
        for key in combo_names:
            if len(key) > 1:
                self.cont.press(self.strreps_to_objs[key])
            else:
                self.cont.press(key)
        holds_i = len(self.holds.keys())
        self.holds[holds_i] = combo_names
        return holds_i
    
    def release(self, hold_i):
        for key in self.holds.get(hold_i, []):
            if len(key) > 1:
                self.cont.release(self.strreps_to_objs[key])
            else:
                self.cont.release(key)
        self.holds.pop(hold_i)
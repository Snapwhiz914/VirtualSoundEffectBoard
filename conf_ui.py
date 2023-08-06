import wx
import json
import os
import pyaudio
from pynput.keyboard import Listener, Key, KeyCode

app = wx.App()
window = wx.Frame(None, title="VSB", size=(500, 250))
nb = wx.Notebook(window)

def get_confblock(block_name):
    j = json.load(open("conf.json", 'r'))
    return j[block_name]

def set_confblock(block_name, block):
    j = json.load(open("conf.json", 'r'))
    j[block_name] = block
    json.dump(j, open("conf.json", 'w'))

try:
    open('conf.json')
except FileNotFoundError:
    f = open('conf.json', 'w')
    f.write('''{"sounds": [], "outputs": [], "keybinds": {"toggle_vc_mode": [ "alt", "[" ], "mute": [ "ctrl", "shift", "m" ], "ptt": [ "alt", "]" ]}}''')
    f.close()

class SoundsEditor(wx.Panel):
    def __init__(self, parent): 
        super(SoundsEditor, self).__init__(parent)

        self.list = wx.ListBox(self, size=(300, 150))
        self.list.Bind(wx.EVT_LISTBOX, self.on_click)

        self.current_sounds = get_confblock("sounds")
        i = 0
        for sound in self.current_sounds:
            self.list.Insert(os.path.basename(sound["fp"]), i, sound)
        
        self.remove_b = wx.Button(self, label="Remove", pos=(310, 10))
        self.remove_b.Bind(wx.EVT_BUTTON, self.on_remove)

        self.mute_chkbx = wx.CheckBox(self, label="Mute discord after playing?", pos=(310, 40))
        self.mute_chkbx.Bind(wx.EVT_CHECKBOX, self.on_mute_chkbx)

        self.path = wx.TextCtrl(self, pos=(310, 70), size=(150, 150), style=wx.TE_READONLY|wx.TE_MULTILINE|wx.TE_NO_VSCROLL|wx.BORDER_NONE)

        self.add_b = wx.Button(self, label="Add", pos=(1, 155))
        self.add_b.Bind(wx.EVT_BUTTON, self.on_add_b)
    
    def on_click(self, event):
        sound = event.GetClientData()
        self.path.SetLabelText('\\'.join(sound["fp"].split('\\')[0:-1]))
        self.mute_chkbx.SetValue(sound["mute"])
    
    def on_mute_chkbx(self, event):
        label = self.list.GetString(self.list.GetSelection())
        i = 0
        for sound in self.current_sounds:
            if os.path.basename(sound["fp"]) == label:
                self.current_sounds[i]["mute"] = self.mute_chkbx.GetValue()
                break
            i += 1
        set_confblock("sounds", self.current_sounds)
    
    def on_remove(self, event):
        label = self.list.GetString(self.list.GetSelection())
        self.list.Delete(self.list.GetSelection())
        for sound in self.current_sounds:
            if os.path.basename(sound["fp"]) == label:
                self.current_sounds.remove(sound)
                break
        set_confblock("sounds", self.current_sounds)
    
    def on_add_b(self, event):
        with wx.FileDialog(self, "Choose an Audio File", style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST, wildcard="WAV Audio files (*.wav)|*.wav") as fileDialog:
            if fileDialog.ShowModal() == wx.ID_CANCEL:
                return
            sound = {
                "fp": fileDialog.GetPath(),
                "mute": False
            }
            self.list.Insert(os.path.basename(sound["fp"]), self.list.GetCount(), sound)
            self.current_sounds.append(sound)
            set_confblock("sounds", self.current_sounds)

class OutputsManager(wx.Panel):
    def __init__(self, parent): 
        super(OutputsManager, self).__init__(parent)

        self.list = wx.CheckListBox(self, size=(300, 150))
        self.list.Bind(wx.EVT_CHECKLISTBOX, self.on_check)

        self.current_devices = get_confblock("outputs")

        self.pa = pyaudio.PyAudio()
        info = self.pa.get_host_api_info_by_index(0)
        numdevices = info.get('deviceCount')

        posi = 0
        for i in range(0, numdevices):
            if (self.pa.get_device_info_by_host_api_device_index(0, i).get('maxOutputChannels')) > 0:
                name = self.pa.get_device_info_by_host_api_device_index(0, i).get('name')
                self.list.Insert(name, posi)
                posi += 1
        
        self.list.SetCheckedStrings(self.current_devices)

    def on_check(self, event):
        self.current_devices = list(self.list.GetCheckedStrings())
        set_confblock("outputs", self.current_devices)

class KeybindsEditor(wx.Panel):
    def _display_kb(self, kb_arr):
        fs = ""
        for i in range(len(kb_arr)-1):
            fs = fs + kb_arr[i] + ' + '
        fs = fs + kb_arr[len(kb_arr)-1]
        return fs

    def _change_kb(self, callback):
        if self.current_listener != None:
            self.current_listener.stop()
            self.current_listener = None
        if len(self.current_keys_pressed) > 0: self.current_keys_pressed = []
        def on_press(key):
            if type(key) == Key: #special key 
                if key == Key.alt or key == Key.alt_l or key == Key.alt_r or key == Key.alt_gr:
                    if 'alt' not in self.current_keys_pressed: self.current_keys_pressed.append('alt')
                if key == Key.ctrl or key == Key.ctrl_l or key == Key.ctrl_r:
                    if 'ctrl' not in self.current_keys_pressed: self.current_keys_pressed.append('ctrl')
                if key == Key.shift or key == Key.shift_l or key == Key.shift_r:
                    if 'shift' not in self.current_keys_pressed: self.current_keys_pressed.append('shift')
            else:
                self.current_keys_pressed.append(key.char)
                callback()
                self.current_listener.stop()
        self.current_listener = Listener(on_press=on_press)
        self.current_listener.start()

    def __init__(self, parent):
        super(KeybindsEditor, self).__init__(parent)

        self.current_keybinds = get_confblock("keybinds")

        self.kb1_label = wx.StaticText(self, label="Toggle Voice Input Mode:", pos=(5, 5))
        self.kb1 = wx.TextCtrl(self, value=self._display_kb(self.current_keybinds["toggle_vc_mode"]), size=(100, 20), pos=(145, 5), style=wx.TE_READONLY)
        self.kb1_change = wx.Button(self, label="Change", pos=(250, 4))
        self.kb1_change.Bind(wx.EVT_BUTTON, self.on_toggle_vc)

        self.kb2_label = wx.StaticText(self, label="Toggle Mute:", pos=(5, 30))
        self.kb2 = wx.TextCtrl(self, value=self._display_kb(self.current_keybinds["mute"]), size=(100, 20), pos=(85, 28), style=wx.TE_READONLY)
        self.kb2_change = wx.Button(self, label="Change", pos=(190, 27))
        self.kb2_change.Bind(wx.EVT_BUTTON, self.on_mute)

        self.kb3_label = wx.StaticText(self, label="Push to Talk:", pos=(5, 55))
        self.kb3 = wx.TextCtrl(self, value=self._display_kb(self.current_keybinds["ptt"]), size=(100, 20), pos=(85, 52), style=wx.TE_READONLY)
        self.kb3_change = wx.Button(self, label="Change", pos=(190, 51))
        self.kb3_change.Bind(wx.EVT_BUTTON, self.on_ptt)

        self.current_listener = None
        self.current_keys_pressed = []
    
    def _enable_change_buttons(self, enable: bool):
        if enable:
            self.kb1_change.Enable()
            self.kb2_change.Enable()
            self.kb3_change.Enable()
        else:
            self.kb1_change.Disable()
            self.kb2_change.Disable()
            self.kb3_change.Disable()
    
    def on_toggle_vc(self, event: wx.CommandEvent):
        def cb():
            self.current_keybinds["toggle_vc_mode"] = self.current_keys_pressed
            print(self.current_keys_pressed)
            self.kb1.SetValue(self._display_kb(self.current_keys_pressed))
            self._enable_change_buttons(True)
            set_confblock("keybinds", self.current_keybinds)
        self._change_kb(cb)
        self._enable_change_buttons(False)
    
    def on_mute(self, event: wx.CommandEvent):
        def cb():
            self.current_keybinds["mute"] = self.current_keys_pressed
            print(self.current_keys_pressed)
            self.kb2.SetValue(self._display_kb(self.current_keys_pressed))
            self._enable_change_buttons(True)
            set_confblock("keybinds", self.current_keybinds)
        self._change_kb(cb)
        self._enable_change_buttons(False)

    def on_ptt(self, event: wx.CommandEvent):
        def cb():
            self.current_keybinds["ptt"] = self.current_keys_pressed
            print(self.current_keys_pressed)
            self.kb3.SetValue(self._display_kb(self.current_keys_pressed))
            self._enable_change_buttons(True)
            set_confblock("keybinds", self.current_keybinds)
        self._change_kb(cb)
        self._enable_change_buttons(False)

nb.AddPage(SoundsEditor(nb), "Sounds")
nb.AddPage(OutputsManager(nb), "Output Devices")
nb.AddPage(KeybindsEditor(nb), "Keybinds")

window.Show()
app.MainLoop()
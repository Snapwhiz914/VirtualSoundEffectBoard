import pyaudio
import wave

CHUNK = 1024

class SoundPlayer():
    def __init__(self, out_names):
        self.out_names = out_names
        self.pa = pyaudio.PyAudio()
        self._is_stopped = False
    
    def _names_to_indexes(self, names):
        info = self.pa.get_host_api_info_by_index(0)
        numdevices = info.get('deviceCount')
        indexes = []

        for i in range(0, numdevices):
            if (self.pa.get_device_info_by_host_api_device_index(0, i).get('maxOutputChannels')) > 0:
                name = self.pa.get_device_info_by_host_api_device_index(0, i).get('name')
                for target in names:
                    if target in name:
                        indexes.append(i)
                        print(f"[MP] Selecting {i} for {name}")
        
        return indexes
    
    def stop_current(self):
        self._is_stopped = True
    
    def play_sound_t(self, path: str, cb, cb_args):
        wf = wave.open(path, "rb")
        streams = []
        for i in self._names_to_indexes(self.out_names):
            streams.append(self.pa.open(format=self.pa.get_format_from_width(wf.getsampwidth()),
                channels=wf.getnchannels(),
                rate=wf.getframerate(),
                output=True,
                output_device_index=i))
            
        while len(data := wf.readframes(CHUNK)):  # Requires Python 3.8+ for :=
            if self._is_stopped:
                self._is_stopped = False
                break
            for s in streams: s.write(data)
        
        for s in streams: s.close()
        cb(*cb_args)
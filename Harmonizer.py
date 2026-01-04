import sounddevice as sd
import numpy as np
import tkinter as tk
import threading

buttonOn = False
volume = 5
pitch = 5

#Harmonizer
class Harmonizer:
    
    sample_rate = 48000     # Hz
    channels = 1            # mono
    blocksize = 1024     # frames per block (latency control)
            
    buffer_size = 32768
    buffer = np.zeros(buffer_size, dtype=np.float32)
    write_pos = 0
    read_pos = 0.0

    def callback(indata, outdata, frames, time_info, status):
        global volume, pitch

        pitch_ratio = 2 ** (pitch / 12)

        input_signal = indata[:, 0]

        # Write incoming audio to circular buffer
        for sample in input_signal:
            Harmonizer.buffer[Harmonizer.write_pos] = sample
            Harmonizer.write_pos = (Harmonizer.write_pos + 1) % Harmonizer.buffer_size

        # Read pitched audio
        output = np.zeros(frames, dtype=np.float32)
        for i in range(frames):
            idx = int(Harmonizer.read_pos) % Harmonizer.buffer_size
            output[i] = Harmonizer.buffer[idx]
            Harmonizer.read_pos += pitch_ratio

        outdata[:, 0] = (input_signal + output) * 0.5 * volume


    def monitor():
        global buttonOn
        while True:
            while not buttonOn:
                pass
            while buttonOn:
                with sd.Stream(samplerate=Harmonizer.sample_rate,
                            blocksize=Harmonizer.blocksize,
                            channels=Harmonizer.channels,
                            dtype='float32',
                            callback=Harmonizer.callback):
                    try:
                        while buttonOn:
                            pass
                    except KeyboardInterrupt:
                        pass

#GUI 
class GUI:
    

    def __init__(self):
        global volume
        global pitch


        self.root = tk.Tk()
        self.root.geometry("800x500")

        self.Title = tk.Label(self.root, text = "Harmonizer", font=('Arial', 25))
        self.Title.pack(padx=20, pady=10)

        self.btn_On = tk.Button(self.root, text="Off", font=('Arial', 20), command=self.turnOn)
        self.btn_On.pack(padx=10, pady=10)

        self.Volume = tk.Label(self.root, text = "Volume", font=('Arial', 25))
        self.Volume.pack(padx=10, pady=10)

        self.vol_dwn = tk.Button(self.root, text="down", font=('Arial', 20), command=self.volumeDown)
        self.vol_dwn.place(x=220, y = 210)
        
        self.Vol_num = tk.Label(self.root, text = volume, font=('Arial', 25))
        self.Vol_num.place(x=388, y=215)

        self.vol_up = tk.Button(self.root, text="  up  ", font=('Arial', 20), command=self.volumeUp)
        self.vol_up.place(x=490, y=210)

        self.Pitch = tk.Label(self.root, text = "Pitch", font=('Arial', 25))
        self.Pitch.place(x=360, y=285)

        self.pch_dwn = tk.Button(self.root, text="down", font=('Arial', 20), command=self.pitchDown)
        self.pch_dwn.place(x=220, y = 350)
        
        self.Pch_num = tk.Label(self.root, text = pitch, font=('Arial', 25))
        self.Pch_num.place(x=388, y=355)

        self.pch_up = tk.Button(self.root, text="  up  ", font=('Arial', 20), command=self.pitchUp)
        self.pch_up.place(x=490, y=350)

        self.Pch_num = tk.Label(self.root, text = "WARNING: Use Headphones", font=('Arial', 25))
        self.Pch_num.place(x=180, y=430)

        self.root.mainloop()
    
    def turnOn(self):
        global buttonOn
        global volume

        if(buttonOn):
            self.btn_On.config(text="Off")
            buttonOn = False
            
        else:
            self.btn_On.config(text="On") 
            buttonOn = True

    def volumeUp(self):
            global volume
            volume += 1
            self.Vol_num.config(text=volume)
        
    
    def volumeDown(self):
        global volume
        if volume > 0:
            volume -= 1
            self.Vol_num.config(text=volume)

    def pitchUp(self):
            global pitch
            pitch += 1
            self.Pch_num.config(text=pitch)
    
    def pitchDown(self):
            global pitch
            pitch -= 1
            self.Pch_num.config(text=pitch)

threading.Thread(target = Harmonizer.monitor, daemon=True).start()
GUI()
import tkinter as tk
import time
import threading
import random
import os
import webbrowser
from sentences import underrepresented_women_scientists_dict

DEFAULT_PATH = "path/to/main"
BG_IMAGE_PATH = DEFAULT_PATH + "bg.png"

os.chdir(DEFAULT_PATH)

background_image = BG_IMAGE_PATH

class WomenSci:
    def __init__(self):
        # base
        self.base = tk.Tk()
        self.base.title(f"Underrepresented Women Scientists - a simple speed typing game")
        self.base.geometry("800x500")
        self.frame = tk.Frame(self.base)

        self.bgimg = tk.PhotoImage(file = background_image)
        self.background_label = tk.Label(self.frame, image = self.bgimg)
        self.background_label.place(x = 0, y = 0, relheight = 1, relwidth = 1)

        self.typing_complete = True

        # sentences
        self.sample_label = tk.Label(self.frame, text = random.choice(list(underrepresented_women_scientists_dict.keys())), font = ("Arial", 18, 'bold'), justify = 'center', wraplength = 600)
        self.sample_label.grid(row = 0, column = 0, padx = 20, pady = 30)
    
        # text box 
        self.input_entry = tk.Entry(self.frame, width = 60, font = ("Arial", 16), bd = 0)
        self.input_entry.grid(row = 1, column = 0, padx = 20, pady = 10)
            
        # start if a key is pressed
        self.input_entry.bind("<KeyPress>", self.start)

        # timer
        self.speed_label = tk.Label(self.frame, text = "0.00 WPM", font = ("Arial", 20), bg = "black", fg = "white", width = 20)
        self.speed_label.grid(row = 2, column = 0, columnspan = 2, padx = 20, pady = 10)

        # replay
        self.reset_button = tk.Button(self.frame, text = "Replay?", command = self.reset, font = ("Arial", 24), bg = 'white', bd = 0, activebackground = '#EEEEEE', activeforeground = 'black')
        self.reset_button.grid(row = 3, column = 0, columnspan = 2, padx = 5, pady = 10)

        self.frame.pack(expand = True)

        # wikipedia
        self.wikipedia_button = tk.Button(self.frame, text = "Read about her!", command = self.wikipedia, font = ("Arial", 15), bg = 'white', bd = 0, activebackground = '#EEEEEE', activeforeground = 'black')
        self.wikipedia_button.grid(row = 5, column = 0, columnspan = 1, padx = 10, pady = 5)

        # adding the boolean to know that the app is started or not
        self.counter = 0
        self.running = False

        """
        Closing the mainloop
        """
        self.base.mainloop()


    
    def start(self, event):
        if not self.running:
            # These keycodes represent the Shift, Ctrl, and Alt keys, respectively. I made an exception here because they may be needed to write the first letter.
            if not event.keycode in [16, 17, 18]:
                self.running = True
                time_thred = threading.Thread(target = self.time_thread)
                time_thred.start()
        if not self.sample_label.cget('text').startswith(self.input_entry.get()):
            self.input_entry.config(fg = "#FF9800")
        else:
            self.input_entry.config(fg = "#4CAF50")
        if self.input_entry.get() == self.sample_label.cget('text')[:]:
            self.running = False
            self.input_entry.config(fg = "white", bg = "#4CAF50")
            self.background_label.place(x = 0, y = 0)
            return 'break'

    def time_thread(self):
        while self.running:
            time.sleep(0.1)
            self.counter += 0.1
            wps = len(self.input_entry.get().split(" ")) / self.counter
            wpm = wps * 60

            self.speed_label.config(text=f"{wpm:.1f} Words per min.")

    def reset(self):
        self.input_entry.delete(0, 'end')
        self.sample_label.config(text = random.choice(list(underrepresented_women_scientists_dict.keys())), font = ("Arial", 18, 'bold') , justify = 'center', wraplength = 600)
        self.input_entry.config(state = 'normal', bg = "white")
        self.typing_complete = False
        if self.typing_complete == False:
            self.speed_label.config(text ="0.00 WPM")
            self.running = False
        self.start_time = time.time()

    def wikipedia(self):
        url = underrepresented_women_scientists_dict[self.sample_label.cget('text')]
        webbrowser.open(url)



WomenSci()
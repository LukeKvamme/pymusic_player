import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
from tinytag import TinyTag
import pygame
import sv_ttk
import os



class MusicPlayerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("PYMusic Player")
        
        self.mp3_files = []
        self.current_file_index = -1
        self.playing = False
        
        # Create GUI elements
        self.create_widgets()
        
    def create_widgets(self):
        # Left frame for displaying MP3 files
        self.left_frame = tk.Frame(self.root, padx=10, pady=10)
        self.left_frame.grid(row=0, column=0, sticky="nsew")
        
        self.mp3_listbox = tk.Listbox(self.left_frame, width=40, height=20)
        self.mp3_listbox.pack(fill=tk.BOTH, expand=True)
        self.load_mp3_files()
        self.mp3_listbox.bind("<<ListboxSelect>>", self.on_file_select)
        
        # Right frame for play button and progress bar
        self.right_frame = tk.Frame(self.root, padx=10, pady=10)
        self.right_frame.grid(row=0, column=1, sticky="nsew")
        
        self.play_button = tk.Button(self.right_frame, text="Play", command=self.toggle_play)
        self.play_button.pack(pady=10)
        
        self.progress_bar = ttk.Progressbar(self.right_frame, orient="horizontal", length=200, mode="determinate")
        self.progress_bar.pack(pady=10)
        
    def load_mp3_files(self):
        # Fetch all MP3 files in the current directory
        for file in os.listdir(os.path.expanduser('~') + "\Music"):
            if file.endswith(".mp3"):
                self.mp3_files.append(file)
                self.mp3_listbox.insert(tk.END, file[:-4])
                
    def on_file_select(self, event):
        # Get the index of the selected item in the listbox
        selection = event.widget.curselection()
        if selection:
            self.current_song_index = selection[0]
    
    def toggle_play(self):
        if self.playing:
            pygame.mixer.music.pause()
            self.play_button.config(text="Play")
        else:
            if self.current_song_index != -1:
                file_path = self.mp3_files[self.current_song_index]
                pygame.mixer.music.load(os.path.expanduser('~') + "\Music\\" + file_path)
                pygame.mixer.music.play()
                self.play_button.config(text="Stop")
                self.update_progress()

        self.playing = not self.playing
    
    def update_progress(self):
        if pygame.mixer.music.get_busy():
            position = pygame.mixer.music.get_pos() / 1000  # Convert to seconds
            self.progress_bar['value'] = position
            self.root.after(100, self.update_progress)
        else:
            self.play_button.config(text="Play")
            self.progress_bar['value'] = 0
            self.playing = False
    
def main():
    pygame.mixer.init()
    root = tk.Tk()
    sv_ttk.set_theme("dark")

    app = MusicPlayerApp(root)
    
    root.mainloop()

if __name__ == "__main__":
    main()

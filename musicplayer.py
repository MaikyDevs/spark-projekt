import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "1"

import sys
import pygame
import tkinter as tk
from tkinter import ttk
import tempfile
import shutil

class MusicPlayer:
    def __init__(self, root):
        self.root = root
        self.root.title("Musik Player")
        self.root.geometry("400x200")
        
        # Lade Musikdatei aus temp-Datei
        temp_dir = os.path.join(tempfile.gettempdir(), "musicplayer")
        song_file = os.path.join(temp_dir, "current_song.txt")
        
        try:
            with open(song_file, 'r') as f:
                self.music_file = f.read().strip()
        except:
            self.music_file = None
            print("Fehler beim Lesen der Temp-Datei")
            self.root.destroy()
            return
            
        # Initialisiere Pygame Mixer
        pygame.mixer.init()
        
        try:
            pygame.mixer.music.load(self.music_file)
            self.current_file = os.path.basename(self.music_file)
        except Exception as e:
            print(f"Fehler beim Laden: {str(e)}")
            self.current_file = "Fehler beim Laden der Datei"
        
        self.playing = False
        self.volume = 0.5
        
        # Titel der Musik
        self.title_label = ttk.Label(
            root, 
            text=f"Spielt: {self.current_file}",
            wraplength=350,
            justify="center"
        )
        self.title_label.pack(pady=20)
        
        # Buttons
        control_frame = ttk.Frame(root)
        control_frame.pack(pady=20)
        
        self.play_button = ttk.Button(
            control_frame,
            text="▶ Play",
            command=self.play_pause,
            width=15
        )
        self.play_button.pack(side=tk.LEFT, padx=5)
        
        self.stop_button = ttk.Button(
            control_frame,
            text="⏹ Stop",
            command=self.stop,
            width=15
        )
        self.stop_button.pack(side=tk.LEFT, padx=5)
        
        # Lautstärke-Bereich
        volume_frame = ttk.Frame(root)
        volume_frame.pack(pady=20, fill=tk.X)
        
        volume_label = ttk.Label(volume_frame, text="Lautstärke:")
        volume_label.pack(side=tk.LEFT, padx=5)
        
        self.volume_slider = ttk.Scale(
            volume_frame,
            from_=0,
            to=100,
            orient=tk.HORIZONTAL,
            command=self.set_volume
        )
        self.volume_slider.set(50)
        self.volume_slider.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        
        pygame.mixer.music.set_volume(0.5)
        
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
    
    def play_pause(self):
        try:
            if not self.playing:
                pygame.mixer.music.play()
                self.play_button.configure(text="⏸ Pause")
                self.playing = True
            else:
                pygame.mixer.music.pause()
                self.play_button.configure(text="▶ Play")
                self.playing = False
        except Exception as e:
            print(f"Fehler beim Abspielen: {e}")
    
    def stop(self):
        try:
            pygame.mixer.music.stop()
            self.play_button.configure(text="▶ Play")
            self.playing = False
        except Exception as e:
            print(f"Fehler beim Stoppen: {e}")
    
    def set_volume(self, val):
        try:
            volume = float(val) / 100
            pygame.mixer.music.set_volume(volume)
        except Exception as e:
            print(f"Fehler bei Lautstärkeänderung: {e}")
    
    def on_closing(self):
        try:
            pygame.mixer.music.stop()
            pygame.mixer.quit()
            # Lösche temp Ordner
            temp_dir = os.path.join(tempfile.gettempdir(), "musicplayer")
            shutil.rmtree(temp_dir, ignore_errors=True)
        except:
            pass
        self.root.destroy()

def main():
    root = tk.Tk()
    app = MusicPlayer(root)
    root.mainloop()

if __name__ == "__main__":
    main()

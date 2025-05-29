import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "1"

import pygame
import tkinter as tk
from tkinter import ttk, filedialog
from tkinter.scrolledtext import ScrolledText
import json
import threading
import time
from pathlib import Path

class ModernMusicPlayer:
    def __init__(self, root):
        self.root = root
        self.root.title("Spark Musikplayer")
        self.root.geometry("600x400")
        self.root.configure(bg='#2c2c2c')
        
        # Style konfigurieren
        self.style = ttk.Style()
        self.style.configure('Custom.TFrame', background='#2c2c2c')
        self.style.configure('Custom.TButton', padding=5)
        self.style.configure('Custom.TLabel', background='#2c2c2c', foreground='white')
        
        # Hauptcontainer
        self.main_frame = ttk.Frame(root, style='Custom.TFrame')
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Playlist Frame
        self.playlist_frame = ttk.Frame(self.main_frame, style='Custom.TFrame')
        self.playlist_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        # Playlist Label
        self.playlist_label = ttk.Label(self.playlist_frame, text="Playlist", style='Custom.TLabel')
        self.playlist_label.pack(pady=(0, 5))
        
        # Playlist
        self.playlist = ScrolledText(self.playlist_frame, width=40, height=15, bg='#3c3c3c', fg='white')
        self.playlist.pack(fill=tk.BOTH, expand=True)
        
        # Control Frame
        self.control_frame = ttk.Frame(self.main_frame, style='Custom.TFrame')
        self.control_frame.pack(side=tk.RIGHT, fill=tk.BOTH)
        
        # Aktueller Song
        self.current_song_label = ttk.Label(
            self.control_frame,
            text="Kein Song ausgewählt",
            style='Custom.TLabel',
            wraplength=200
        )
        self.current_song_label.pack(pady=10)
        
        # Buttons
        self.create_buttons()
        
        # Progress Bar
        self.progress_frame = ttk.Frame(self.control_frame, style='Custom.TFrame')
        self.progress_frame.pack(fill=tk.X, pady=10)
        
        self.progress_bar = ttk.Progressbar(
            self.progress_frame,
            orient=tk.HORIZONTAL,
            length=200,
            mode='determinate'
        )
        self.progress_bar.pack(fill=tk.X)
        
        self.time_label = ttk.Label(
            self.progress_frame,
            text="0:00 / 0:00",
            style='Custom.TLabel'
        )
        self.time_label.pack(pady=5)
        
        # Lautstärke
        self.volume_frame = ttk.Frame(self.control_frame, style='Custom.TFrame')
        self.volume_frame.pack(fill=tk.X, pady=10)
        
        self.volume_label = ttk.Label(
            self.volume_frame,
            text="Lautstärke:",
            style='Custom.TLabel'
        )
        self.volume_label.pack(side=tk.LEFT)
        
        self.volume_slider = ttk.Scale(
            self.volume_frame,
            from_=0,
            to=100,
            orient=tk.HORIZONTAL,
            command=self.set_volume
        )
        self.volume_slider.set(50)
        self.volume_slider.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        
        # Initialisierung
        pygame.mixer.init()
        self.playing = False
        self.current_song = None
        self.songs = []
        self.load_playlist()
        
        # Progress Update Thread
        self.update_thread = threading.Thread(target=self.update_progress, daemon=True)
        self.update_thread.start()
        
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
    
    def create_buttons(self):
        button_frame = ttk.Frame(self.control_frame, style='Custom.TFrame')
        button_frame.pack(pady=10)
        
        # Ordner hinzufügen
        self.add_folder_btn = ttk.Button(
            button_frame,
            text="📁 Ordner hinzufügen",
            command=self.add_folder,
            style='Custom.TButton'
        )
        self.add_folder_btn.pack(fill=tk.X, pady=2)
        
        # Play/Pause Button
        self.play_button = ttk.Button(
            button_frame,
            text="▶ Play",
            command=self.play_pause,
            style='Custom.TButton'
        )
        self.play_button.pack(fill=tk.X, pady=2)
        
        # Stop Button
        self.stop_button = ttk.Button(
            button_frame,
            text="⏹ Stop",
            command=self.stop,
            style='Custom.TButton'
        )
        self.stop_button.pack(fill=tk.X, pady=2)
        
        # Previous/Next Buttons
        nav_frame = ttk.Frame(button_frame, style='Custom.TFrame')
        nav_frame.pack(fill=tk.X, pady=2)
        
        self.prev_button = ttk.Button(
            nav_frame,
            text="⏮",
            command=self.previous_song,
            style='Custom.TButton'
        )
        self.prev_button.pack(side=tk.LEFT, expand=True, padx=2)
        
        self.next_button = ttk.Button(
            nav_frame,
            text="⏭",
            command=self.next_song,
            style='Custom.TButton'
        )
        self.next_button.pack(side=tk.LEFT, expand=True, padx=2)
    
    def add_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            new_songs = []
            for file in Path(folder).rglob("*.mp3"):
                new_songs.append(str(file))
            self.songs.extend(new_songs)
            self.update_playlist()
            self.save_playlist()
    
    def update_playlist(self):
        self.playlist.delete(1.0, tk.END)
        for i, song in enumerate(self.songs, 1):
            song_name = Path(song).name
            self.playlist.insert(tk.END, f"{i}. {song_name}\n")
        self.playlist.tag_add("center", "1.0", tk.END)
    
    def play_pause(self):
        if not self.current_song and self.songs:
            self.current_song = self.songs[0]
            self.play_song(self.current_song)
        elif self.playing:
            pygame.mixer.music.pause()
            self.play_button.configure(text="▶ Play")
            self.playing = False
        else:
            pygame.mixer.music.unpause()
            self.play_button.configure(text="⏸ Pause")
            self.playing = True
    
    def stop(self):
        pygame.mixer.music.stop()
        self.play_button.configure(text="▶ Play")
        self.playing = False
        self.progress_bar['value'] = 0
        self.time_label.configure(text="0:00 / 0:00")
    
    def play_song(self, song_path):
        try:
            pygame.mixer.music.load(song_path)
            pygame.mixer.music.play()
            self.current_song = song_path
            self.current_song_label.configure(text=Path(song_path).name)
            self.play_button.configure(text="⏸ Pause")
            self.playing = True
        except Exception as e:
            print(f"Fehler beim Abspielen: {e}")
    
    def next_song(self):
        if not self.songs:
            return
        current_index = self.songs.index(self.current_song) if self.current_song else -1
        next_index = (current_index + 1) % len(self.songs)
        self.play_song(self.songs[next_index])
    
    def previous_song(self):
        if not self.songs:
            return
        current_index = self.songs.index(self.current_song) if self.current_song else 0
        prev_index = (current_index - 1) % len(self.songs)
        self.play_song(self.songs[prev_index])
    
    def set_volume(self, val):
        volume = float(val) / 100
        pygame.mixer.music.set_volume(volume)
    
    def update_progress(self):
        while True:
            if self.playing and pygame.mixer.music.get_busy():
                current_pos = pygame.mixer.music.get_pos() / 1000  # Sekunden
                self.progress_bar['value'] = (current_pos % 100)
                mins, secs = divmod(int(current_pos), 60)
                self.time_label.configure(text=f"{mins}:{secs:02d}")
            time.sleep(0.1)
    
    def save_playlist(self):
        playlist_file = Path.home() / ".spark_playlist.json"
        with open(playlist_file, 'w') as f:
            json.dump(self.songs, f)
    
    def load_playlist(self):
        playlist_file = Path.home() / ".spark_playlist.json"
        if playlist_file.exists():
            try:
                with open(playlist_file) as f:
                    self.songs = json.load(f)
                self.update_playlist()
            except:
                self.songs = []
    
    def on_closing(self):
        self.save_playlist()
        pygame.mixer.music.stop()
        pygame.mixer.quit()
        self.root.destroy()

def main():
    root = tk.Tk()
    app = ModernMusicPlayer(root)
    root.mainloop()

if __name__ == "__main__":
    main()

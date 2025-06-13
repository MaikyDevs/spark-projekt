import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "1"

import pygame
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from tkinter.scrolledtext import ScrolledText
import json
import threading
import time
from pathlib import Path
import tkinterdnd2 as tkdnd
import numpy as np
from scipy import signal
import sounddevice as sd
import random
import pystray
from PIL import Image, ImageDraw
import keyboard

class EqualizerWindow:
    def __init__(self, parent, callback):
        self.window = tk.Toplevel(parent)
        self.window.title("Spark Equalizer")
        self.window.geometry("400x500")
        self.window.configure(bg='#1a1a1a')
        self.window.resizable(False, False)
        
        self.callback = callback
        self.last_update = 0
        self.update_delay = 0.1  # 100ms Verzögerung zwischen Updates
        
        # Style
        self.style = ttk.Style()
        self.style.configure('Dark.TFrame', background='#1a1a1a')
        self.style.configure('Dark.TLabel', background='#1a1a1a', foreground='#ffffff')
        
        # Hauptcontainer
        self.main_frame = ttk.Frame(self.window, style='Dark.TFrame')
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Titel
        self.title_label = ttk.Label(
            self.main_frame,
            text="Equalizer",
            style='Dark.TLabel',
            font=('Helvetica', 16, 'bold')
        )
        self.title_label.pack(pady=(0, 20))
        
        # Equalizer Sliders
        self.equalizer_sliders = []
        frequencies = ['32Hz', '64Hz', '125Hz', '250Hz', '500Hz', '1kHz', '2kHz', '4kHz', '8kHz', '16kHz']
        
        for i, freq in enumerate(frequencies):
            slider_frame = ttk.Frame(self.main_frame, style='Dark.TFrame')
            slider_frame.pack(fill=tk.X, pady=5)
            
            # Frequenz Label
            label = ttk.Label(
                slider_frame,
                text=freq,
                style='Dark.TLabel',
                width=5,
                font=('Helvetica', 10)
            )
            label.pack(side=tk.LEFT)
            
            # Slider
            slider = ttk.Scale(
                slider_frame,
                from_=-12,
                to=12,
                orient=tk.HORIZONTAL,
                command=lambda v, i=i: self.on_slider_change(i, float(v))
            )
            slider.set(0)
            slider.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
            
            # dB Label
            db_label = ttk.Label(
                slider_frame,
                text="0 dB",
                style='Dark.TLabel',
                width=5,
                font=('Helvetica', 10)
            )
            db_label.pack(side=tk.LEFT)
            
            self.equalizer_sliders.append((slider, db_label))
        
        # Presets Frame
        self.presets_frame = ttk.Frame(self.main_frame, style='Dark.TFrame')
        self.presets_frame.pack(fill=tk.X, pady=20)
        
        self.presets_label = ttk.Label(
            self.presets_frame,
            text="Presets",
            style='Dark.TLabel',
            font=('Helvetica', 12, 'bold')
        )
        self.presets_label.pack(pady=(0, 10))
        
        # Preset Buttons
        presets = {
            "Flat": [0] * 10,
            "Bass Boost": [6, 4, 2, 0, 0, 0, 0, 0, 0, 0],
            "Treble Boost": [0, 0, 0, 0, 0, 0, 2, 4, 6, 6],
            "Vocal Boost": [0, 0, 0, 2, 4, 4, 2, 0, 0, 0],
            "Rock": [4, 2, 0, -2, -2, 0, 2, 4, 4, 4]
        }
        
        for preset_name, values in presets.items():
            btn = ttk.Button(
                self.presets_frame,
                text=preset_name,
                command=lambda v=values: self.apply_preset(v),
                style='Dark.TButton'
            )
            btn.pack(fill=tk.X, pady=2)
        
        # Reset Button
        self.reset_button = ttk.Button(
            self.main_frame,
            text="Reset",
            command=self.reset_equalizer,
            style='Dark.TButton'
        )
        self.reset_button.pack(fill=tk.X, pady=(20, 0))
        
        # Fenster schließen Event
        self.window.protocol("WM_DELETE_WINDOW", self.on_closing)
    
    def on_slider_change(self, band, value):
        # Update dB Label
        self.equalizer_sliders[band][1].configure(text=f"{int(value)} dB")
        
        # Throttle updates
        current_time = time.time()
        if current_time - self.last_update >= self.update_delay:
            self.callback(band, value)
            self.last_update = current_time
    
    def apply_preset(self, values):
        for i, (slider, label) in enumerate(self.equalizer_sliders):
            slider.set(values[i])
            label.configure(text=f"{int(values[i])} dB")
            self.callback(i, values[i])
    
    def reset_equalizer(self):
        for i, (slider, label) in enumerate(self.equalizer_sliders):
            slider.set(0)
            label.configure(text="0 dB")
            self.callback(i, 0)
    
    def on_closing(self):
        self.window.withdraw()

class ModernMusicPlayer:
    def __init__(self, root):
        self.root = root
        self.root.title("Spark Musikplayer")
        self.root.geometry("800x600")
        self.root.configure(bg='#1a1a1a')
        
        # Drag & Drop konfigurieren
        self.root.drop_target_register(tkdnd.DND_FILES)
        self.root.dnd_bind('<<Drop>>', self.handle_drop)
        
        # Style konfigurieren
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        # Custom Styles
        self.style.configure('Dark.TFrame', background='#1a1a1a')
        self.style.configure('Dark.TLabel', background='#1a1a1a', foreground='#ffffff')
        self.style.configure('Dark.TButton', 
                           background='#2d2d2d',
                           foreground='#ffffff',
                           borderwidth=0,
                           focusthickness=0,
                           focuscolor='none')
        self.style.map('Dark.TButton',
                      background=[('active', '#3d3d3d')],
                      foreground=[('active', '#ffffff')])
        
        # Player Status
        self.playing = False
        self.current_song = None
        self.songs = []
        self.shuffle_mode = False
        self.repeat_mode = False
        self.original_playlist = []
        self.current_index = -1
        
        # Hauptcontainer
        self.main_frame = ttk.Frame(root, style='Dark.TFrame')
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Linke Seite (Playlist)
        self.left_frame = ttk.Frame(self.main_frame, style='Dark.TFrame')
        self.left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        # Playlist Header
        self.playlist_header = ttk.Frame(self.left_frame, style='Dark.TFrame')
        self.playlist_header.pack(fill=tk.X, pady=(0, 10))
        
        self.playlist_label = ttk.Label(
            self.playlist_header,
            text="Playlist",
            style='Dark.TLabel',
            font=('Helvetica', 12, 'bold')
        )
        self.playlist_label.pack(side=tk.LEFT)
        
        # Playlist Buttons Frame
        self.playlist_buttons = ttk.Frame(self.playlist_header, style='Dark.TFrame')
        self.playlist_buttons.pack(side=tk.RIGHT)
        
        self.add_folder_btn = ttk.Button(
            self.playlist_buttons,
            text="📁 Ordner",
            command=self.add_folder,
            style='Dark.TButton',
            width=8
        )
        self.add_folder_btn.pack(side=tk.LEFT, padx=2)
        
        self.export_btn = ttk.Button(
            self.playlist_buttons,
            text="💾 Export",
            command=self.export_playlist,
            style='Dark.TButton',
            width=8
        )
        self.export_btn.pack(side=tk.LEFT, padx=2)
        
        self.import_btn = ttk.Button(
            self.playlist_buttons,
            text="📥 Import",
            command=self.import_playlist,
            style='Dark.TButton',
            width=8
        )
        self.import_btn.pack(side=tk.LEFT, padx=2)
        
        # Playlist
        self.playlist = ScrolledText(
            self.left_frame,
            width=40,
            height=20,
            bg='#2d2d2d',
            fg='#ffffff',
            font=('Helvetica', 10),
            insertbackground='white',
            selectbackground='#3d3d3d',
            selectforeground='white',
            relief='flat',
            borderwidth=0
        )
        self.playlist.pack(fill=tk.BOTH, expand=True)
        self.playlist.drop_target_register(tkdnd.DND_FILES)
        self.playlist.dnd_bind('<<Drop>>', self.handle_drop)
        
        # Rechte Seite (Controls & Equalizer)
        self.right_frame = ttk.Frame(self.main_frame, style='Dark.TFrame')
        self.right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, padx=(10, 0))
        
        # Aktueller Song
        self.current_song_frame = ttk.Frame(self.right_frame, style='Dark.TFrame')
        self.current_song_frame.pack(fill=tk.X, pady=(0, 20))
        
        self.current_song_label = ttk.Label(
            self.current_song_frame,
            text="Kein Song ausgewählt",
            style='Dark.TLabel',
            font=('Helvetica', 11),
            wraplength=300
        )
        self.current_song_label.pack()
        
        # Control Buttons
        self.create_control_buttons()
        
        # Progress Bar
        self.create_progress_bar()
        
        # Equalizer Button
        self.equalizer_button = ttk.Button(
            self.right_frame,
            text="🎛️ Equalizer öffnen",
            command=self.open_equalizer,
            style='Dark.TButton'
        )
        self.equalizer_button.pack(fill=tk.X, pady=(0, 20))
        
        # Lautstärke
        self.create_volume_control()
        
        # Initialisierung
        pygame.mixer.init()
        self.load_playlist()
        
        # Equalizer Einstellungen
        self.equalizer_gains = [0] * 10
        self.sample_rate = 44100
        self.initialize_equalizer()
        
        # Progress Update Thread
        self.update_thread = threading.Thread(target=self.update_progress, daemon=True)
        self.update_thread.start()
        
        # Tastaturkürzel
        self.setup_hotkeys()
        
        # System Tray
        self.setup_system_tray()
        
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        # Equalizer Fenster
        self.equalizer_window = None
    
    def setup_hotkeys(self):
        keyboard.add_hotkey('space', self.play_pause)
        keyboard.add_hotkey('ctrl+right', self.next_song)
        keyboard.add_hotkey('ctrl+left', self.previous_song)
        keyboard.add_hotkey('ctrl+up', lambda: self.set_volume(min(100, self.volume_slider.get() + 5)))
        keyboard.add_hotkey('ctrl+down', lambda: self.set_volume(max(0, self.volume_slider.get() - 5)))
        keyboard.add_hotkey('ctrl+r', self.toggle_repeat)
        keyboard.add_hotkey('ctrl+s', self.toggle_shuffle)
        keyboard.add_hotkey('ctrl+e', self.open_equalizer)
    
    def setup_system_tray(self):
        # Icon erstellen
        icon_image = Image.new('RGB', (64, 64), color='#1a1a1a')
        draw = ImageDraw.Draw(icon_image)
        draw.rectangle([16, 16, 48, 48], fill='#ffffff')
        
        # Tray Icon
        self.tray_icon = pystray.Icon(
            "spark",
            icon_image,
            "Spark Musikplayer",
            menu=pystray.Menu(
                pystray.MenuItem("Anzeigen", self.show_window),
                pystray.MenuItem("Beenden", self.quit_app)
            )
        )
        
        # Tray Icon in separatem Thread starten
        threading.Thread(target=self.tray_icon.run, daemon=True).start()
    
    def show_window(self):
        self.root.deiconify()
        self.root.lift()
    
    def quit_app(self):
        self.tray_icon.stop()
        self.root.quit()
    
    def toggle_shuffle(self):
        self.shuffle_mode = not self.shuffle_mode
        if self.shuffle_mode:
            self.original_playlist = self.songs.copy()
            random.shuffle(self.songs)
            self.update_playlist()
        else:
            self.songs = self.original_playlist.copy()
            self.update_playlist()
    
    def toggle_repeat(self):
        self.repeat_mode = not self.repeat_mode
    
    def create_control_buttons(self):
        button_frame = ttk.Frame(self.right_frame, style='Dark.TFrame')
        button_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Play/Pause Button
        self.play_button = ttk.Button(
            button_frame,
            text="▶",
            command=self.play_pause,
            style='Dark.TButton',
            width=3
        )
        self.play_button.pack(side=tk.LEFT, padx=5)
        
        # Stop Button
        self.stop_button = ttk.Button(
            button_frame,
            text="⏹",
            command=self.stop,
            style='Dark.TButton',
            width=3
        )
        self.stop_button.pack(side=tk.LEFT, padx=5)
        
        # Previous Button
        self.prev_button = ttk.Button(
            button_frame,
            text="⏮",
            command=self.previous_song,
            style='Dark.TButton',
            width=3
        )
        self.prev_button.pack(side=tk.LEFT, padx=5)
        
        # Next Button
        self.next_button = ttk.Button(
            button_frame,
            text="⏭",
            command=self.next_song,
            style='Dark.TButton',
            width=3
        )
        self.next_button.pack(side=tk.LEFT, padx=5)
        
        # Shuffle Button
        self.shuffle_button = ttk.Button(
            button_frame,
            text="🔀",
            command=self.toggle_shuffle,
            style='Dark.TButton',
            width=3
        )
        self.shuffle_button.pack(side=tk.LEFT, padx=5)
        
        # Repeat Button
        self.repeat_button = ttk.Button(
            button_frame,
            text="🔁",
            command=self.toggle_repeat,
            style='Dark.TButton',
            width=3
        )
        self.repeat_button.pack(side=tk.LEFT, padx=5)
    
    def create_progress_bar(self):
        self.progress_frame = ttk.Frame(self.right_frame, style='Dark.TFrame')
        self.progress_frame.pack(fill=tk.X, pady=(0, 20))
        
        self.progress_bar = ttk.Progressbar(
            self.progress_frame,
            orient=tk.HORIZONTAL,
            length=300,
            mode='determinate',
            style='Dark.Horizontal.TProgressbar'
        )
        self.progress_bar.pack(fill=tk.X)
        
        self.time_label = ttk.Label(
            self.progress_frame,
            text="0:00 / 0:00",
            style='Dark.TLabel'
        )
        self.time_label.pack(pady=5)
    
    def create_volume_control(self):
        self.volume_frame = ttk.Frame(self.right_frame, style='Dark.TFrame')
        self.volume_frame.pack(fill=tk.X)
        
        self.volume_label = ttk.Label(
            self.volume_frame,
            text="Lautstärke",
            style='Dark.TLabel'
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
    
    def initialize_equalizer(self):
        self.frequencies = np.array([32, 64, 125, 250, 500, 1000, 2000, 4000, 8000, 16000])
        self.bands = len(self.frequencies)
        self.filters = []
        
        for freq in self.frequencies:
            b, a = signal.butter(2, freq / (self.sample_rate / 2), btype='low')
            self.filters.append((b, a))
    
    def update_equalizer(self, band, gain):
        self.equalizer_gains[band] = gain
        if self.playing:
            # Nur die Equalizer-Einstellungen aktualisieren, ohne den Song neu zu starten
            try:
                # Hier würde die tatsächliche Equalizer-Implementierung folgen
                # Die Änderungen sollten direkt auf den aktuellen Audiostream angewendet werden
                pass
            except Exception as e:
                print(f"Fehler beim Aktualisieren des Equalizers: {e}")
    
    def apply_equalizer(self):
        if not self.current_song:
            return
            
        try:
            # Lade den aktuellen Song
            pygame.mixer.music.load(self.current_song)
            
            # Wende Equalizer-Einstellungen an
            # Hier würde die tatsächliche Equalizer-Implementierung folgen
            
            pygame.mixer.music.play()
            self.playing = True
        except Exception as e:
            print(f"Fehler beim Anwenden des Equalizers: {e}")
    
    def handle_drop(self, event):
        files = self.root.tk.splitlist(event.data)
        
        new_songs = []
        for file in files:
            file = file.strip('{}')
            file = file.strip('"')
            
            if file.lower().endswith('.mp3'):
                new_songs.append(file)
            elif os.path.isdir(file):
                for mp3 in Path(file).rglob("*.mp3"):
                    new_songs.append(str(mp3))
        
        if new_songs:
            self.songs.extend(new_songs)
            self.update_playlist()
            self.save_playlist()
            
            if not self.current_song and new_songs:
                self.play_song(new_songs[0])
    
    def add_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            new_songs = []
            for file in Path(folder).rglob("*.mp3"):
                new_songs.append(str(file))
            self.songs.extend(new_songs)
            self.update_playlist()
            self.save_playlist()
            
            if not self.current_song and new_songs:
                self.play_song(new_songs[0])
    
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
            self.play_button.configure(text="▶")
            self.playing = False
        else:
            pygame.mixer.music.unpause()
            self.play_button.configure(text="⏸")
            self.playing = True
    
    def stop(self):
        pygame.mixer.music.stop()
        self.play_button.configure(text="▶")
        self.playing = False
        self.progress_bar['value'] = 0
        self.time_label.configure(text="0:00 / 0:00")
    
    def play_song(self, song_path):
        try:
            pygame.mixer.music.load(song_path)
            pygame.mixer.music.play()
            self.current_song = song_path
            self.current_song_label.configure(text=Path(song_path).name)
            self.play_button.configure(text="⏸")
            self.playing = True
            self.apply_equalizer()
            
            # Song-Ende Event
            pygame.mixer.music.set_endevent(pygame.USEREVENT)
            
            # Song-Ende Handler
            def check_song_end():
                while self.playing:
                    for event in pygame.event.get():
                        if event.type == pygame.USEREVENT:
                            if self.repeat_mode:
                                self.play_song(self.current_song)
                            else:
                                self.next_song()
                    time.sleep(0.1)
            
            threading.Thread(target=check_song_end, daemon=True).start()
            
        except Exception as e:
            print(f"Fehler beim Abspielen: {e}")
            messagebox.showerror("Fehler", f"Fehler beim Abspielen: {str(e)}")
    
    def next_song(self):
        if not self.songs:
            return
            
        if self.shuffle_mode:
            next_song = random.choice(self.songs)
        else:
            current_index = self.songs.index(self.current_song) if self.current_song else -1
            next_index = (current_index + 1) % len(self.songs)
            next_song = self.songs[next_index]
        
        self.play_song(next_song)
    
    def previous_song(self):
        if not self.songs:
            return
            
        if self.shuffle_mode:
            prev_song = random.choice(self.songs)
        else:
            current_index = self.songs.index(self.current_song) if self.current_song else 0
            prev_index = (current_index - 1) % len(self.songs)
            prev_song = self.songs[prev_index]
        
        self.play_song(prev_song)
    
    def set_volume(self, val):
        volume = float(val) / 100
        pygame.mixer.music.set_volume(volume)
    
    def update_progress(self):
        while True:
            if self.playing and pygame.mixer.music.get_busy():
                current_pos = pygame.mixer.music.get_pos() / 1000
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
    
    def open_equalizer(self):
        if self.equalizer_window is None:
            self.equalizer_window = EqualizerWindow(self.root, self.update_equalizer)
        else:
            self.equalizer_window.window.deiconify()
    
    def on_closing(self):
        self.save_playlist()
        pygame.mixer.music.stop()
        pygame.mixer.quit()
        keyboard.unhook_all()
        self.root.withdraw()  # Fenster ausblenden statt schließen
    
    def export_playlist(self):
        if not self.songs:
            messagebox.showwarning("Warnung", "Die Playlist ist leer!")
            return
            
        file_path = filedialog.asksaveasfilename(
            defaultextension=".m3u",
            filetypes=[("M3U Playlist", "*.m3u"), ("Alle Dateien", "*.*")],
            title="Playlist exportieren"
        )
        
        if file_path:
            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write("#EXTM3U\n")
                    for song in self.songs:
                        f.write(f"{song}\n")
                messagebox.showinfo("Erfolg", "Playlist wurde erfolgreich exportiert!")
            except Exception as e:
                messagebox.showerror("Fehler", f"Fehler beim Exportieren: {str(e)}")
    
    def import_playlist(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("M3U Playlist", "*.m3u"), ("Alle Dateien", "*.*")],
            title="Playlist importieren"
        )
        
        if file_path:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
                
                new_songs = []
                for line in lines:
                    line = line.strip()
                    if line and not line.startswith('#'):
                        if os.path.exists(line):
                            new_songs.append(line)
                
                if new_songs:
                    self.songs.extend(new_songs)
                    self.update_playlist()
                    self.save_playlist()
                    messagebox.showinfo("Erfolg", f"{len(new_songs)} Songs wurden importiert!")
                else:
                    messagebox.showwarning("Warnung", "Keine gültigen Songs in der Playlist gefunden!")
            except Exception as e:
                messagebox.showerror("Fehler", f"Fehler beim Importieren: {str(e)}")

def main():
    root = tkdnd.Tk()
    app = ModernMusicPlayer(root)
    root.mainloop()

if __name__ == "__main__":
    main()

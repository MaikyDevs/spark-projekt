# 🎵 Spark Musikplayer

Ein moderner, benutzerfreundlicher Musikplayer mit einer schönen GUI, geschrieben in Python.

## ✨ Features

- 🎨 Modernes, dunkles Design
- 📂 Einfaches Hinzufügen von Musikordnern
- 📝 Automatisches Speichern der Playlist
- ⏯️ Grundlegende Wiedergabesteuerung (Play, Pause, Stop)
- ⏮️⏭️ Navigation zwischen Songs
- 🔊 Lautstärkeregelung
- 📊 Fortschrittsanzeige mit Timer
- 💾 Playlist-Persistenz zwischen Sitzungen

## 🚀 Installation

1. Stellen Sie sicher, dass Python 3.6 oder höher installiert ist
2.Starten sie Musicplayer
3. Installieren Sie die erforderlichen Pakete:tkinter,pygame
4. 
### Bedienung:

1. Klicken Sie auf "📁 Ordner hinzufügen" um Ihre Musikordner auszuwählen
2. Ihre MP3-Dateien erscheinen in der Playlist auf der linken Seite
3. Nutzen Sie die Steuerungselemente:
   - ▶️/⏸️ - Play/Pause
   - ⏹️ - Stop
   - ⏮️/⏭️ - Vorheriger/Nächster Song
   - 🔊 Lautstärkeregler unten

## 🛠️ Technische Details

- Python 3.6+
- Tkinter für die GUI
- Pygame für die Audiowiedergabe
- Unterstützt MP3-Dateien
- Playlist wird in `~/.spark_playlist.json` gespeichert

## 📝 Lizenz

MIT Lizenz - siehe [LICENSE](LICENSE) für Details.

## 🤝 Beitragen

Beiträge sind willkommen! Bitte erstellen Sie einen Pull Request oder öffnen Sie ein Issue für Vorschläge und Fehlermeldungen.

## ⚠️ Bekannte Probleme

- Fortschrittsanzeige zeigt nur die ersten 100 Sekunden eines Songs an
- Keine Unterstützung für Drag & Drop von Dateien
- Keine Anzeige der Gesamtlänge des Songs

## 🔜 Geplante Features

- [ ] Drag & Drop Unterstützung
- [ ] Playlist-Export/Import
- [ ] Equalizer
- [ ] Shuffle und Repeat Modi
- [ ] Tastaturkürzel
- [ ] Miniaturansicht im System-Tray

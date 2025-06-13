# Spark Musikplayer

Ein moderner, funktionsreicher Musikplayer mit professionellem Equalizer und benutzerfreundlicher Oberfläche.

## 🌟 Features

### 🎵 Musikwiedergabe
- Unterstützung für MP3-Dateien
- Drag & Drop für Dateien und Ordner
- Automatisches Speichern der Playlist
- Fortschrittsanzeige mit Zeitstempel
- Lautstärkeregelung

### 🎛️ Equalizer
- 10-Band Equalizer (32Hz - 16kHz)
- Separate Equalizer-Fenster
- Live-Updates ohne Neustart
- Vordefinierte Presets:
  - Flat (Neutral)
  - Bass Boost (Für elektronische Musik)
  - Treble Boost (Für klassische Musik)
  - Vocal Boost (Für Gesang)
  - Rock (Für Rock-Musik)

### 🔄 Wiedergabe-Modi
- Shuffle-Modus für zufällige Wiedergabe
- Repeat-Modus für Wiederholung
- Automatisches Weiterschalten
- Speicherung der Playlist-Reihenfolge

### ⌨️ Tastaturkürzel
- `Space`: Play/Pause
- `Ctrl + Pfeil Rechts`: Nächster Song
- `Ctrl + Pfeil Links`: Vorheriger Song
- `Ctrl + Pfeil Hoch`: Lautstärke erhöhen
- `Ctrl + Pfeil Runter`: Lautstärke verringern
- `Ctrl + R`: Repeat-Modus umschalten
- `Ctrl + S`: Shuffle-Modus umschalten
- `Ctrl + E`: Equalizer öffnen

### 💾 Playlist-Management
- Export als M3U-Datei
- Import von M3U-Playlists
- Drag & Drop Unterstützung
- Automatische Validierung

### 🖥️ System-Integration
- Minimierung in System-Tray
- Rechtsklick-Menü
- Schnellzugriff auf Funktionen
- Sauberes Beenden

## 🚀 Installation

1. Stelle sicher, dass Python 3.8 oder höher installiert ist
2. Klone das Repository:
   ```bash
   git clone https://github.com/MaikyDevs/spark-projekt.git
   ```
3. Installiere die Abhängigkeiten:
   ```bash
   pip install -r requirements.txt
   ```

## 💻 Verwendung

1. Starte den Player:
   ```bash
   python musicplayer.py
   ```
2. Füge Musik hinzu durch:
   - Drag & Drop von Dateien/Ordnern
   - "Ordner" Button für Verzeichnisauswahl
   - Import einer M3U-Playlist
3. Nutze die Steuerelemente oder Tastaturkürzel
4. Passe den Equalizer nach Bedarf an
5. Minimiere in die System-Tray-Leiste für Hintergrundbetrieb

## 🛠️ Technische Details

### Abhängigkeiten
- `pygame==2.5.2`: Audio-Wiedergabe
- `tkinterdnd2==0.3.0`: Drag & Drop
- `numpy==1.24.3`: Audio-Verarbeitung
- `scipy==1.10.1`: Equalizer-Filter
- `sounddevice==0.4.6`: Audio-Streaming
- `pystray==0.19.4`: System-Tray
- `Pillow==10.0.0`: Icon-Erstellung
- `keyboard==0.13.5`: Tastaturkürzel

### Systemanforderungen
- Windows 10/11
- Python 3.8+
- 4GB RAM empfohlen
- Soundkarte mit Treiber

## 📝 Lizenz

Dieses Projekt ist unter der MIT-Lizenz lizenziert. Siehe die [LICENSE](LICENSE) Datei für Details.

## 🤝 Beitragen

Beiträge sind willkommen! Bitte folge diesen Schritten:

1. Fork das Repository
2. Erstelle einen Feature-Branch
3. Committe deine Änderungen
4. Push zum Branch
5. Erstelle einen Pull Request

## 🐛 Bekannte Probleme

- Equalizer-Updates können bei sehr schnellen Änderungen verzögert sein
- Einige MP3-Dateien mit speziellen Tags werden möglicherweise nicht korrekt erkannt
- System-Tray-Icon erscheint manchmal verzögert

## 🔜 Geplante Features

- Unterstützung für weitere Audioformate (WAV, FLAC, etc.)
- Erweiterte Tag-Unterstützung
- Visualisierungen während der Wiedergabe
- Online-Radio-Integration
- Cloud-Speicher-Unterstützung
- Erweiterte Equalizer-Presets
- Playlist-Organisation mit Tags
- Automatische Metadaten-Aktualisierung 

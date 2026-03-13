# Portable Embedded Radio System

A portable Wi-Fi connected radio built around a Raspberry Pi Zero 2W with custom hardware, embedded Linux firmware, and a mobile web interface for remote media management.

This project combines embedded hardware design, Linux-based firmware, and a lightweight web server to create a standalone audio device that can be controlled from a smartphone.

---

## Features

* Single-button hardware control for playback states
* Mobile-friendly web interface
* Upload MP3 files directly to the device
* Add songs from YouTube using yt-dlp
* Real-time volume control
* Skip track remotely
* NFC tap-to-open control page
* Persistent shuffled playback engine
* Automatic startup using systemd
* Custom PCB and 3D printed enclosure

---

## Hardware

**Core Components**

* Raspberry Pi Zero 2W
* MAX98357A I2S Digital Audio Amplifier
* 4Ω speaker
* GPIO push button
* Custom PCB (designed in Altium Designer)

**Audio Path**

Raspberry Pi I2S → MAX98357A DAC → Speaker

**Power**

5V regulated supply integrated on the custom PCB.

---

## Software Architecture

The system is divided into two main components.

### Firmware Layer

`radio.py`

Responsible for:

* Hardware button handling via GPIO
* Finite state machine for playback modes
* Playlist shuffling
* Persistent mpg123 playback engine
* Real-time volume monitoring

Playback modes:

| State | Mode                  |
| ----- | --------------------- |
| 0     | Off                   |
| 1     | Vocal playlist        |
| 2     | Instrumental playlist |

---

### Web Server

`server.py`

A lightweight Flask server provides a mobile control interface.

Features include:

* Current song display
* MP3 file upload
* YouTube audio download
* Playlist selection
* Skip track
* Volume control

The web interface is optimized for mobile devices.

---

## Media Pipeline

Audio from YouTube is processed automatically.

YouTube URL
↓
`yt-dlp` downloads audio
↓
`ffmpeg` converts to MP3
↓
Saved into selected playlist
↓
Radio playback system loads during shuffle cycle

---

## File Structure

```
portable-embedded-radio/

firmware/
radio.py

server/
server.py

systemd/
radio.service
radio-server.service

hardware/
pcb/
schematic.pdf
board.png

enclosure/
case.stl

images/
radio_front.jpg
pcb.jpg
web_interface.png

docs/
architecture.md
setup.md
```

---

## Installation

Install dependencies:

```
sudo apt update
sudo apt install mpg123 yt-dlp ffmpeg python3-flask
```

Clone the repository:

```
git clone https://github.com/YOURUSERNAME/portable-embedded-radio.git
cd portable-embedded-radio
```

Enable services:

```
sudo cp systemd/*.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable radio.service
sudo systemctl enable radio-server.service
```

Start services:

```
sudo systemctl start radio
sudo systemctl start radio-server
```

---

## Accessing the Interface

Once running on the network, open:

```
http://radipi.local
```

The page allows users to:

* Upload songs
* Add songs from YouTube
* Skip tracks
* Adjust volume
* View the current song

---

## Mechanical Design

The radio enclosure was designed in SolidWorks and 3D printed to house:

* Custom PCB
* Raspberry Pi Zero 2W
* Speaker
* Power system

The enclosure ensures proper component spacing and structural integrity while maintaining a compact portable form factor.

---

## Photos

(Add project photos here)

Examples:

* PCB assembly
* Internal electronics
* Completed radio enclosure
* Web interface

---

## Future Improvements

* Multi-room streaming support
* Bluetooth audio mode
* OLED display for track information
* Battery-powered operation
* Playlist management UI

---

## Author

Ryan Blake Bussey
Computer Engineering
Embedded Systems | Hardware Design | Linux Systems

---

## License

MIT License

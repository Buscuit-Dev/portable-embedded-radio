#!/usr/bin/env python3
import os
import random
import subprocess
from gpiozero import Button
from threading import Thread, Event
import time

# -------------------------------
# CONFIG
# -------------------------------

BUTTON_PIN = 17  # GPIO17, physical pin 11

STATIONS = {
    "w-vocals": "/home/radio/music/w-vocals",
    "no-vocals": "/home/radio/music/no-vocals"
}

VOLUME_FILE = "/home/radio/volume.txt"
DEFAULT_VOLUME = 16384  # Default mpg123 volume if file missing

# -------------------------------
# GLOBALS
# -------------------------------

state = 0  # 0=off, 1=w-vocals, 2=no-vocals
play_thread = None
stop_event = Event()

# -------------------------------
# FUNCTIONS
# -------------------------------

def get_volume():
    """Read current volume from volume file."""
    try:
        with open(VOLUME_FILE) as f:
            vol = int(f.read().strip())
            return max(0, min(32768, vol))
    except:
        return DEFAULT_VOLUME

def play_station(station_path):
    """
    Play all songs in a folder, shuffled.
    Stops immediately if stop_event is set.
    """
    time.sleep(0.5)  # small delay to reduce first-track pop

    while not stop_event.is_set():
        files = [os.path.join(station_path, f) for f in os.listdir(station_path) if f.endswith(".mp3")]
        random.shuffle(files)

        for f in files:
            if stop_event.is_set():
                return

            # Read volume each song in case it changed
            volume = str(get_volume())

            # Update CURRENT file so Flask page shows now playing
            try:
                with open("/home/radio/current_song.txt", "w") as cf:
                    cf.write(os.path.basename(f))
            except:
                pass

            p = subprocess.Popen(["mpg123", "-f", volume, f])
            while p.poll() is None:
                if stop_event.is_set():
                    p.terminate()
                    return
                time.sleep(0.1)

def start_station(station_name):
    global play_thread, stop_event
    stop_event.clear()
    play_thread = Thread(target=play_station, args=(STATIONS[station_name],))
    play_thread.start()
    print(f"Playing station: {station_name}")

def stop_station():
    global stop_event, play_thread
    stop_event.set()
    if play_thread:
        play_thread.join()
    print("Playback stopped.")

def button_pressed():
    """
    Cycle through states:
    0=off -> 1=w-vocals -> 2=no-vocals -> 0=off
    """
    global state
    stop_station()
    state = (state + 1) % 3
    if state == 1:
        start_station("w-vocals")
    elif state == 2:
        start_station("no-vocals")
    # state 0 = off

# -------------------------------
# SETUP
# -------------------------------

station_button = Button(BUTTON_PIN, pull_up=True, bounce_time=0.1)
station_button.when_pressed = button_pressed

print("Radio ready. Press the button to start playback.")

# Keep script running
while True:
    time.sleep(0.1)

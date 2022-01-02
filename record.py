import os
from datetime import datetime
import pyaudio
import wave
import argparse

from pynput import keyboard
import pickle
import base64
import sys


root_folder = "recordings"
current_folder = None


p = pyaudio.PyAudio()
stream = None
frames = []


FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
CHUNK = 512
RECORD_SECONDS = 2
WAVE_OUTPUT_FILENAME = None


START_TIME = None
is_recording = True
episode = 30 # how long to record for each session



def on_release(key):
    global is_recording
    if key == keyboard.Key.esc:
        # Stop listener
        is_recording = False
        

listener = keyboard.Listener(
    on_release=on_release)
listener.start()        


def select_recording_device():
    global p, stream
    info = p.get_host_api_info_by_index(0)
    numdevices = info.get('deviceCount')
    for i in range(0, numdevices):
            if (p.get_device_info_by_host_api_device_index(0, i).get('maxInputChannels')) > 0:
                if p.get_device_info_by_host_api_device_index(0, i).get('name') == "pulse":
                    default_input = i
                    # break
                print ("Input Device id ", i, " - ", p.get_device_info_by_host_api_device_index(0, i).get('name'))
    stream = p.open(format=FORMAT, channels=CHANNELS,
                rate=RATE, input=True, input_device_index = default_input,
                frames_per_buffer=CHUNK)


def record_audio():
    global RECORD_SECONDS, RATE, CHUNK, FORMAT, CHANNELS, START_TIME, WAVE_OUTPUT_FILENAME
    global stream, frames, listener

    while is_recording:
        for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
            try:
                data = stream.read(CHUNK)
                frames.append(data)
            except OSError:
                pass
        if (datetime.now() - START_TIME).seconds >= episode*60:
            write_to_wav()
            START_TIME = datetime.now()
            WAVE_OUTPUT_FILENAME = generate_filename(START_TIME)
    if not is_recording:
        stream.stop_stream()
        stream.close()
        p.terminate()
        listener.stop()
        write_to_wav()


def write_to_wav():
    global p, frames
    waveFile = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    waveFile.setnchannels(CHANNELS)
    waveFile.setsampwidth(p.get_sample_size(FORMAT))
    waveFile.setframerate(RATE)
    waveFile.writeframes(b''.join(frames))
    frames = []
    waveFile.close()


def generate_filename(time_value):
    filename = datetime.now().strftime("%Y-%m-%dT%H-%M-%SZ") + ".wav"
    return os.path.join(root_folder, current_folder, filename)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Record data from websites')
    parser.add_argument('--episode', metavar='episode', default=30, type=int,
            help='How long should individual recordings last for (in minutes)?')
    args = parser.parse_args()
    episode = args.episode

    current_folder = datetime.now().strftime("%Y-%m-%dT%H-%M-%SZ")

    try:
        os.makedirs(os.path.join(root_folder, current_folder))
    except OSError:
        print("Folder already exists.")


    START_TIME = datetime.now()
    WAVE_OUTPUT_FILENAME = generate_filename(START_TIME)

    select_recording_device()
    record_audio()
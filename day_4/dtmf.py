import time
import math

import numpy as np
import pynput.keyboard
import pyaudio

bitrate = 44100

rows_usa_frequencies_in_hz = [697, 770, 852, 941]
columns_usa_frequencies_in_hz = [1209, 1336, 1477, 1633]

key_pad = {
    "1": [0, 0], "2": [0, 1], "3": [0, 2], "A": [0, 3],
    "4": [1, 0], "5": [1, 1], "6": [1, 2], "B": [1, 3],
    "7": [2, 0], "8": [2, 1], "9": [2, 2], "C": [2, 3],
    "*": [3, 0], "0": [3, 1], "#": [3, 2], "D": [3, 3],
}

keep_looping = True
buttons_pressed = []
last_buttons_pressed = None
last_wave = None

PyAudio = pyaudio.PyAudio


def on_press(key):

    global key_pad
    global buttons_pressed

    if type(key) is pynput.keyboard.Key:
        return
    else:
        key_character = str(key.char).upper()

        if key_character in key_pad.keys():
            if key_character not in buttons_pressed:
                buttons_pressed.append(key_character)


def on_release(key):

    global keep_looping
    global buttons_pressed

    if key == pynput.keyboard.Key.esc:
        keep_looping = False
        return False

    if type(key) is pynput.keyboard.KeyCode and str(key.char).upper() in buttons_pressed:
        buttons_pressed.remove(str(key.char).upper())


def get_current_tone(in_data, frame_count, time_info, status):

    global buttons_pressed

    global last_buttons_pressed
    global last_wave

    if np.array_equal(last_buttons_pressed, buttons_pressed):
        return np.array(last_wave, dtype='float32').astype(np.float32).tobytes(), pyaudio.paContinue

    waves = []
    length = 0.5
    rate = bitrate
    wave_length = int(length * rate)

    for key_character in buttons_pressed:
        wave_1 = np.sin(np.arange(wave_length) * (
                    float(rows_usa_frequencies_in_hz[key_pad[key_character][0]]) * ((math.pi * 2) / rate)))
        wave_2 = np.sin(np.arange(wave_length) * (
                    float(columns_usa_frequencies_in_hz[key_pad[key_character][1]]) * ((math.pi * 2) / rate)))

        waves.append(np.divide(wave_1 + wave_2, 2.0))

    if len(waves) > 0:
        final_wave = waves[0]
        for wave in waves[1:]:
            final_wave = np.divide(final_wave + wave, 2.0)
    else:
        # empty wave
        final_wave = np.sin(np.arange(wave_length) * float(0) * ((math.pi * 2) / rate))

    last_buttons_pressed = buttons_pressed.copy()
    last_wave = final_wave

    return np.array(final_wave, dtype='float32').astype(np.float32).tobytes(), pyaudio.paContinue


keyboard_listener = pynput.keyboard.Listener(on_press=on_press, on_release=on_release)
keyboard_listener.start()

p = PyAudio()
stream = p.open(format=pyaudio.paFloat32,
                channels=1,
                rate=bitrate,
                output=True,
                stream_callback=get_current_tone)

stream.start_stream()

while keep_looping:
    time.sleep(.1)

stream.stop_stream()
stream.close()
p.terminate()

import json
import random
import sys
import math

import pyaudio
import prompt_toolkit
import jsonschema
import numpy as np

dit_duration_default = .25
audio_bitrate_default = 44100
do_visual = True

DIT = "dit"
DAH = "dah"
PAUSE = "letter_pause"
SPACE = "word_space"


def tone_dictionary(dit_duration, morse_tone_frequency_in_hertz=641, bitrate=44100):

    dah_duration = 3 * dit_duration
    letter_space_duration = 3 * dit_duration
    word_space_duration = 7 * dit_duration

    dit_tone_wave = np.sin(
        np.arange(int(dit_duration * bitrate)) * ((float(morse_tone_frequency_in_hertz) * math.pi * 2) / bitrate))
    dah_tone_wave = np.sin(
        np.arange(int(dah_duration * bitrate)) * ((float(morse_tone_frequency_in_hertz) * math.pi * 2) / bitrate))
    letter_tone_wave = np.sin(
        np.arange(int(letter_space_duration * bitrate)) * ((float(0) * math.pi * 2) / bitrate))
    word_tone_wave = np.sin(
        np.arange(int(word_space_duration * bitrate)) * ((float(0) * math.pi * 2) / bitrate))

    dit_tone_samples = np.array(dit_tone_wave, dtype='float32').astype(np.float32).tobytes()
    dah_tone_samples = np.array(dah_tone_wave, dtype='float32').astype(np.float32).tobytes()
    letter_tone_samples = np.array(letter_tone_wave, dtype='float32').astype(np.float32).tobytes()
    word_tone_samples = np.array(word_tone_wave, dtype='float32').astype(np.float32).tobytes()

    tones_for_duration = {
        DIT: dit_tone_samples,
        DAH: dah_tone_samples,
        PAUSE: letter_tone_samples,
        SPACE: word_tone_samples
    }

    return tones_for_duration


with open("morse_code.json") as morse_code_file:
    morse_code = json.load(morse_code_file)

with open("phrase_books/lingo.json") as phrase_book_file:
    phrase_book = json.load(phrase_book_file)

with open("phrase_book_schema.json") as phrase_book_schema_file:
    phrase_book_schema = json.load(phrase_book_schema_file)

jsonschema.validate(phrase_book, phrase_book_schema)

bitrate = audio_bitrate_default

p_audio = pyaudio.PyAudio()
audio_out_stream = p_audio.open(format=pyaudio.paFloat32,
                                channels=1,
                                rate=bitrate,
                                output=True)

print("Morse code quizzer!")


tones = tone_dictionary(dit_duration_default)

phrase_index = random.randrange(0, len(phrase_book["phrases"]))
current_phrase = phrase_book["phrases"][phrase_index]["phrase"]

keep_quizzing = True

while keep_quizzing:

    print("")
    for letter in map(lambda l: l.upper(), [l for l in current_phrase]):

        if letter == " ":
            audio_out_stream.write(tones[SPACE])
        else:
            for pip in morse_code[letter]:
                if do_visual:
                    print(pip, end="", flush=True)
                if pip == ".":
                    audio_out_stream.write(tones[DIT])
                elif pip == "-":
                    audio_out_stream.write(tones[DAH])
                else:
                    print("UNKNOWN PIP '{}'".format(pip))
                    sys.exit()

            audio_out_stream.write(tones[PAUSE])

    print("")
    while True:
        again_reveal_quit = prompt_toolkit.prompt("(R)eveal, (A)gain, (N)ext or (Q)uit: ")
        if again_reveal_quit.lower() == "q":
            keep_quizzing = False
            break
        elif again_reveal_quit.lower() == "r":
            phrase_in_morse = "".join(
                map(lambda l: morse_code[l.upper()], [l for l in current_phrase.replace(" ", "")]))
            phrase_in_spaced = "".join(map(lambda l: l.upper().ljust(len(morse_code[l.upper()])),
                                           [l for l in current_phrase.replace(" ", "")]))

            print(f"[{phrase_in_morse}]")
            print(f"[{phrase_in_spaced}]")

        elif again_reveal_quit.lower() == "n":
            current_phrase = phrase_book["phrases"][random.randrange(0, len(phrase_book["phrases"]))]["phrase"]
            break
        elif again_reveal_quit.lower() == "a":
            break
        else:
            print("unkown option '{}'. Please input R, A or Q")

audio_out_stream.stop_stream()
audio_out_stream.close()
p_audio.terminate()

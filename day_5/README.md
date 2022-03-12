# Morse code quizer
---
```
Language: Python
Brief: Script for testing Morse code transcription and decoding
Scope: expirement
Tags: audio, HAM
State: basic funcionality 
Result: success
```
---

Present a word, phrase or sentence as Morse code visually or as audible tones or both. User can then see if they transcribed and decoded the sequence correctly.

I've been meaning to take the HAM Technician Test for a while. I don't think you need to be able to do Morse any more. Still kind of interested in it.

Also, still have audio on my mind from day_4 so I am going to write this in Python.

### Results

Basics work. Tones don't have the clipping problem as day_4 so day_4 is a bug in my code not the audio module. That's not surprising but this shows all the parts work as expected

Only wanted to spend about an hour coding today. There is some low-hanging fruit in "If I was to do more" that would make this a lot more useful. 

Probably will spin off into it's own project at a later date.

```
(py3_venv) (base) [pickard@eris.local:] projects/100_days_of_code_2022/day_5 [main] M?? % python morse_code_quizzer.py
Morse code quizzer!

.--..--.--..-.-.-.-.--.--..--.--..-.-.-.-.--
(R)eveal, (A)gain, (N)ext or (Q)uit: r
[.--..--.--..-.-.-.-.--.--..--.--..-.-.-.-.--]
[EM ER   G  EN C   Y   EM ER   G  EN C   Y   ]
(R)eveal, (A)gain, (N)ext or (Q)uit: n

.--.-----...--....---..-..-.--.
(R)eveal, (A)gain, (N)ext or (Q)uit: q

```

### Notes

### If I was to do more
- Add keyboard input to speed up or slow down the dit interval
- Be a bit more sophisticated on how phrase books are used
- Support showing 'hints'
- Record session for later, including self reported success / failure
import requests
import pyfiglet
import urllib.parse
import urllib.request

window_height = 8
window_width = 16
size=window_height * window_width

message_txt = "H e l l o  W o r k"
message = pyfiglet.figlet_format(message_txt, font="colossal", width=1000).replace(" ", ".")

message_as_rows = message.split("\n")
max_row_len = max(map(lambda r: len(r), message_as_rows))
number_of_frames = max_row_len+2

print(message)

for frame_index in range(0, number_of_frames):
    frame_line = ""

    for window_row_index in range(0, window_height):
        if window_row_index >= len(message_as_rows):

            frame_line += ''.join(["." for _ in range(window_width)])
            continue

        window_row = message_as_rows[window_row_index]

        frame_line += ''.join([window_row[k+frame_index] if k+frame_index < len(window_row) else "." for k in range(0, window_width)])

    payload_str = urllib.parse.urlencode({"m": frame_line}, safe='":+|\\/><\'()')

    print(payload_str)

    url="http://127.0.0.1:5000/?"
    urllib.request.urlopen(url+payload_str)

    print(frame_line)

#for frame_cell in range(0, size):
    #message_cell = ''.join([message[k-frame_cell] if k >= frame_cell and k-frame_cell < len(message) else "." for k in range(0, size)])
    #requests.get(" http://127.0.0.1:5000/?m={}".format(message_cell))

    #print(f"{frame_cell} {message_cell}")
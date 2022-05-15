import os


from flask import Flask, render_template
from termcolor import colored

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'


@app.route("/")
def route_index():
    text = colored('Hello, World!\n', 'red', attrs=['reverse', 'blink'])
    return text


if __name__ == '__main__':
    app.run()


from flask import Flask, Blueprint, render_template

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')

from flask import Flask, render_template, request, flash, url_for, redirect

from map import CreateMap

app = Flask(__name__)
app.config['SECRET_KEY'] = 'key'

SHOWN_POI = []

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/map')
def test():
    CreateMap()
    return render_template('map.html')
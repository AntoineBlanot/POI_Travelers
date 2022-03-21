from flask import Flask, render_template, request, flash, url_for, redirect

from map import CreateMap

app = Flask(__name__)
app.config['SECRET_KEY'] = 'key'

# To launch the hello world api, do in cmd: 
## export FLASK_APP=app/api
## export FLASK_ENV=development
## flask run
## CTRL+C to stop 
# Go to http://127.0.0.1:5000/

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/map')
def test():
    CreateMap()
    return render_template('map.html')
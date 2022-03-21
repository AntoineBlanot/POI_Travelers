from flask import Flask, render_template, request, flash, url_for, redirect

from map import CreateMap

app = Flask(__name__)
app.config['SECRET_KEY'] = 'key'

SHOWN_POI = []

@app.route('/')
def index():
    return render_template('index.html', content=["tom","marie","antoine","hugo"])

@app.route('/map')
def map():
    CreateMap()
    return render_template('map.html')

@app.route('/test')
def test():
    return render_template('info.html')

@app.route('/info', methods=('GET', 'POST'))
def info():
    if request.method ==  'POST':
        # do stuff here
        # language = request.form.get('language')
        CreateMap()
        return render_template('info.html')
    
if __name__=="__main__":
    app.run(debug=True)
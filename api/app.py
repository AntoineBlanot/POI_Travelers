from flask import Flask, render_template, request, flash, url_for, redirect, session 
from datetime import timedelta 
from map import CreateMap

app = Flask(__name__)
app.config['SECRET_KEY'] = 'key'
app.permanent_session_lifetime =timedelta(seconds=0)

SHOWN_POI = []

@app.route('/')
def index():
    return render_template('base.html', content=["tom","marie","antoine","hugo"])

@app.route('/map')
def map():
    CreateMap()
    return render_template('map.html')

@app.route('/test')
def test():
    return render_template('info.html')

@app.route('/login',methods=["POST","GET"])
def login():
    if request.method =='POST':
        session.permanent = True 
        user = request.form['nm']
        session["user"]=user
        flash("Login Succesfull !")
        return redirect(url_for("user"))
    else:
        if "user" in session:
            flash("Already Login")
            return redirect(url_for("user"))
        return render_template("login.html")
        

@app.route('/user')
def user():
    if "user" in session :
        user = session["user"]
        return render_template('user.html',user=user)
    else : 
        flash('Your are not logged in !')
        return redirect(url_for("login"))


@app.route('/logout')
def logout():
    session.pop("user",None)
    flash("You have been logged out!","info")
    return redirect(url_for("login"))


@app.route('/info', methods=('GET', 'POST'))
def info():
    if request.method ==  'POST':
        # do stuff here
        # language = request.form.get('language')
        CreateMap()
        return render_template('info.html')
    
# if __name__=="__main__":
#     app.run(debug=True)
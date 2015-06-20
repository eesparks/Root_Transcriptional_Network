import os
from flask import Flask, render_template, request, redirect, url_for, Response
from functools import wraps

app = Flask(__name__, static_folder='static', static_url_path='')
app.debug = True

def check_auth(username, password):
    """This function is called to check if a username /
    password combination is valid.
    """
    return username == 'admin' and password == 'secret'

def authenticate():
    """Sends a 401 response that enables basic auth"""
    return Response(
    'Could not verify your access level for that URL.\n'
    'You have to login with proper credentials', 401,
    {'WWW-Authenticate': 'Basic realm="Login Required"'})

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)
    return decorated


@app.route('/')
@requires_auth
def home():
    return redirect("/index.html", code=302)

@app.route('/index.html')
@requires_auth
def index():
    return app.send_static_file('index.html')


@app.route('/2_TF_Clusters.html')
@requires_auth
def tf_clusters():
    return app.send_static_file('2_TF_Clusters.html')

@app.route('/3_Motifs_Network_Supp.html')
@requires_auth
def motifs():
    return app.send_static_file('3_Motifs_Network_Supp.html')

@app.route('/4_SHR_All.html')
@requires_auth
def shr():
    return app.send_static_file('4_SHR_All.html')


@app.route('/5_SCR_All.html')
@requires_auth
def scr():
    return app.send_static_file('5_SCR_All.html')

@app.route('/6_SHR_Validated.html')
@requires_auth
def shr_v():
    return app.send_static_file('6_SHR_Validated.html')

@app.route('/7_SCR_Validated.html')
@requires_auth
def scr_v():
    return app.send_static_file('7_SCR_Validated.html')

@app.route('/8_Light.html')
@requires_auth
def light():
    return app.send_static_file('8_Light.html')


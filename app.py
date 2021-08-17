from flask import Flask, request, render_template
from random import choice, sample
from surveys import *

from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)
app.config['SECRET_KEY'] = "oh-so-secret"

debug = DebugToolbarExtension(app)


@app.route('/')
def survey():
    satis = surveys['satisfaction']

    return render_template("home.html", satis=satis)


@app.route('/questions/0', methods=["POST"])
def questions():
    return render_template("base.html", satis=satis)


# this will keep track of user responses
responses = []
x = 'hello'

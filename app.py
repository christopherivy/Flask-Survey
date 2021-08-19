from flask import Flask, request, render_template
from random import choice, sample
from surveys import *

from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)
app.config['SECRET_KEY'] = "oh-so-secret"

debug = DebugToolbarExtension(app)
satis = surveys['satisfaction']
all_questions = satis.questions
choices = satis.questions[0].choices

# this will keep track of user responses
responses = []


@app.route('/')
def survey():
    return render_template("home.html", satis=satis, choice=choices)


@app.route('/questions/0', methods=["GET", "POST"])
def questions():
    return render_template("base.html", satis=satis, choice=choices)

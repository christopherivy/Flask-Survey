
from flask import Flask, request, render_template, redirect, session
from random import choice, sample
from surveys import satisfaction_survey as satis

from flask_debugtoolbar import DebugToolbarExtension


app = Flask(__name__)
app.config['SECRET_KEY'] = "oh-so-secret"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)


# satis = surveys['satisfaction']
all_questions = satis.questions
choices = satis.questions[0].choices


# this will keep track of user responses via key
ANSWER_KEY = 'responses'


# this is the start of the survey. like the home page. start button takes you to question/0
# app.route is the url that will show
@app.route('/')
def start_survey():
    return render_template("start.html", satis=satis, choice=choices)


# need to replace 0 with dynamic variable
# app.route is the url that will show
# the render_template is the
@app.route('/questions/0', methods=["GET", "POST"])
def questions():
    return render_template("questions.html", satis=satis, choice=choices)


# when the survey is done show this
@app.route('/complete', methods=["GET", "POST"])
def survey_complete():
    return render_template('complete.html')


@app.route('/begin', methods=["GET", "POST"])
def start_questions():
    session[ANSWER_KEY] = []

    return redirect('/questions/0')

    # save the questions when user responds


@app.route('/answer', methods=["GET", "POST"])
def saved_responses():
    """ Save the responses from the user """

    # return 'thank you'

    if('answer' not in request.form):
        return redirect("/question/0")

    # this is the chioces var for
    choice = request.form['answer']

    responses = session[ANSWER_KEY]
    responses.append(choice)
    session[ANSWER_KEY] = responses

    if (len(responses) == len(satis.questions)):
        return redirect('/complete')

    else:
        return redirect(f'/questions/{len(responses)}')


@app.route('/questions/<int:ques_id>')
# this is to show the html for the question were on.
def show_question():
    """ This shows the current question """

    responses = session.get(ANSWER_KEY)

    if (responses is None):
        return redirect('/')

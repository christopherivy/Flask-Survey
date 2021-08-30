from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey

# key names will use to store some things in the session;
# put here as constants so we're guaranteed to be consistent in
# our spelling of these
RESPONSES_KEY = "responses"

app = Flask(__name__)
app.config['SECRET_KEY'] = "never-tell!"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)


@app.route("/")
def show_survey_start():
    """Select a survey."""

    # Customer Satisfaction Survey
    return render_template("survey_start.html", survey=survey)


@app.route("/begin", methods=["POST"])
def start_survey():
    """Clear the session of responses."""
    session[RESPONSES_KEY] = []

    return redirect("/questions/0")


@app.route("/answer", methods=["POST"])
def handle_question():
    """Save response and redirect to next question."""

    # I added this part (line 38-39)
    if ('answer' not in request.form):
        return redirect("/questions/0")

    # get the response choice
    choice = request.form['answer']

    # add this response to the session
    responses = session[RESPONSES_KEY]
    responses.append(choice)
    session[RESPONSES_KEY] = responses

    # if we are on the last question
    if (len(responses) == len(survey.questions)):
        # They've answered all the questions! Thank them.
        return redirect("/complete")

    else:
        return redirect(f"/questions/{len(responses)}")


@app.route("/questions/<int:qid>")
def show_question(qid):
    """Display current question."""

    responses = session.get(RESPONSES_KEY)

    # if session has no responses, send to start of survey
    if (responses is None):
        # trying to access question page too soon
        return redirect("/")

    # if questions origin list same length as responses. survey done
    if (len(responses) == len(survey.questions)):
        # They've answered all the questions! Thank them.
        return redirect("/complete")

    # trying to get to more questions than available
    if (len(responses) != qid):
        # Trying to access questions out of order.

        # flash(f"Invalid question id: {qid}.")
        flash('Please select an answer before going to the next question.')
        return redirect(f"/questions/{len(responses)}")

    question = survey.questions[qid]
    return render_template(
        "question.html", question_num=qid, question=question, remaining_ques=len(survey.questions), current_ques=qid+1)


@app.route("/complete")
def complete():
    """Survey complete. Show completion page."""
    responses = session.get(RESPONSES_KEY)

    responses = ', '.join(responses)

    return render_template("completion.html", responses=responses)

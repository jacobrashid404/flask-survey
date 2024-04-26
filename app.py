from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey

app = Flask(__name__)
app.config['SECRET_KEY'] = "never-tell!"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

responses = []  # store user answers in this list


@app.get('/')
def show_survey_info():
    # get title and instructions for survey
    # pass to survey_start.jinja
    title = survey.title
    instructions = survey.instructions

    return render_template(
        "survey_start.jinja",
        title=title,
        instructions=instructions
    )


@app.post("/begin")
def redirect_to_survey():
    return redirect("/questions/0")


@app.get("/questions/<int:question_num>")
def get_question(question_num):
    question = survey.questions[question_num]

    return render_template(
        "question.jinja",
        question=question
    )


@app.post("/answer")
def store_and_redirect():
    """ Store user's response in responses list.
    Redirect user to next survey question. """  # ask re: docstring indentation

    responses.append(request.form['answer'])

    if len(responses) == len(survey.questions):
        return redirect("/thank-you")
    else:
        return redirect(f"/questions/{len(responses)}")


@app.get("/thank-you")
def end_survey():
    """ Display message thanking user for filling out survey.
    Display list of survey questions and user's answers. """

    # # Make dict of {code:story, code:story, ...}
    # stories = {s.code: s for s in [story1, story2]}

    # syntax for dictionary comprehension from two lists comes from:
    # https://www.geeksforgeeks.org/python-convert-two-lists-into-a-dictionary/
    question_answer = {
        survey.questions[i]: responses[i] for i in range(len(survey.questions))}

    return render_template(
        "completion.jinja",
        question_answer
    )

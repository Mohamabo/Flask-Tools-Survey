from flask import Flask, render_template, request, redirect, session, flash
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey

RESPONSES_KEY = "responses"

app = Flask(__name__)
app.config['SECRET_KEY'] = "secret"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

@app.route('/')
def begin_survey():
    """Display the survey start page."""
    return render_template('survey_start.html', survey=survey)

@app.route('/begin', methods=['POST'])
def start_survey():
    """Start the survey by clearing the session."""
    session[RESPONSES_KEY] = []
    return redirect('/questions/0')

@app.route('/questions/<int:qid>')
def show_question(qid):
    """Display a question."""
    responses = session.get(RESPONSES_KEY)

    if responses is None:
        # If there are no responses, redirect to the start page
        return redirect('/')

    if qid != len(responses):
        # If the question ID doesn't match the number of responses,
        # redirect to the current question
        flash("Invalid question ID.")
        return redirect(f'/questions/{len(responses)}')
    
    if len(responses) == len(survey.questions):
        # If all questions have been answered, redirect to the completion page
        return redirect('/complete')

    question = survey.questions[qid]
    return render_template('questions.html', question=question, question_num=qid)

@app.route('/answer', methods=['POST'])
def handle_answer():
    """Handle the answer to a question."""
    choice = request.form['answer']
    responses = session[RESPONSES_KEY]
    responses.append(choice)
    session[RESPONSES_KEY] = responses

    if len(responses) == len(survey.questions):
        # If all questions have been answered, redirect to the completion page
        return redirect('/complete')
    else:
        # Redirect to the next question
        return redirect(f'/questions/{len(responses)}')
    
@app.route('/complete')
def complete_survey():
    """Display the completion page."""
    return render_template('complete.html')
    
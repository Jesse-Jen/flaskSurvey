from flask import Flask, request, redirect, render_template, session, flash
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey


app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False


debug = DebugToolbarExtension(app)

RESPONSES_KEY = 'responses'


@app.route('/',methods = ['GET'])
def start_survey():
    return render_template('start_survey.html', survey = survey)


@app.route('/begin', methods = ['POST'])
def intialize():
    """Empties responses"""
    session[RESPONSES_KEY] = []
    return redirect('/questions/0')


@app.route('/answer', methods = ['POST'])
def ask_questions():
    choice = request.form['answer']
    responses = session[RESPONSES_KEY]
    responses.append(choice)
    session[RESPONSES_KEY] = responses


    if (len(responses) == len(survey.questions)):
        return redirect('/complete')
    else:
        return redirect(f'/questions/{len(responses)}')
    
@app.route('/complete', methods = ['GET'])
def completed_survey():
    '''rendering compeleted survey page'''
    return render_template('complete.html')

@app.route("/questions/<int:qid>")
def show_question(qid):
    """Display current question."""
    responses = session.get(RESPONSES_KEY)

    if (responses is None):
        return redirect("/")

    if (len(responses) == len(survey.questions)):
        return redirect("/complete")

    if (len(responses) != qid):
        flash(f"Invalid question id: {qid}.")
        return redirect(f"/questions/{len(responses)}")

    question = survey.questions[qid]
    return render_template(
        "question.html", question_num=qid, question=question)


if __name__ == '__main__':
    app.run(debug=True)

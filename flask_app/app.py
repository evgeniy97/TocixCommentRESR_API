from flask import Flask, request, render_template, redirect
from joblib import load
import sqlite3
from wtforms import Form, TextAreaField, validators

DB_PATH = 'commentDB.sqlite'

app = Flask(__name__)

def loadMOdel(path):
    model = load(path)
    return model

vector = loadMOdel('model/vec.joblib')
model = loadMOdel('model/model.joblib')

LABEL = {0: 'not toxic', 1: 'toxic'}

def classify(text):
    # Get text from request
    #text = request.text
    #prediction = model.predict(text)
    
    y = 1
    probability = 1.0

    return LABEL[y], probability

def sqlite_entry(path, text, y):
    conn = sqlite3.connect(path)
    c = conn.cursor()
    c.execute("INSERT INTO comment_db (comment, toxic, date)"\
    " VALUES (?, ?, DATETIME('now'))", (text, y))
    conn.commit()
    conn.close()

## Flask

class CommentForm(Form):
    comment = TextAreaField('',
                                [validators.DataRequired(),
                                validators.length(min=15)])

@app.route('/')
def index():
    form = CommentForm(request.form)
    return render_template('main.html', form=form)

@app.route('/results', methods=['POST'])
def results():
    form = CommentForm(request.form)
    if request.method == 'POST' and form.validate():
        comment = request.form['comment']
        y, proba = classify(comment)
        return render_template('results.html',
                                content=comment,
                                prediction=y,
                                probability=round(proba*100, 2))
    return render_template('main.html', form=form)

@app.route('/thanks', methods=['POST'])
def feedback():
    feedback = request.form['feedback_button']
    comment = request.form['comment']
    prediction = request.form['prediction']

    y = LABEL[prediction]
    if feedback == 'Incorrect':
        y = int(not(y))
    sqlite_entry(DB_PATH, comment, y)
    return render_template('thanks.html')

if __name__ == '__main__':
    app.run()
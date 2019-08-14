from flask import Flask, request, render_template, redirect
import pickle
import sqlite3
import os
import numpy as np
from wtforms import Form, TextAreaField, validators

DB_PATH = 'commentDB.sqlite'

app = Flask(__name__)


from vectorizer import vect

LABEL = {0: 'toxic', 1: 'not toxic'}

LABEL_INV = {'not toxic': 1,'toxic': 0}

cur_dir = os.path.dirname(__file__)
clf = pickle.load(open(os.path.join(cur_dir,
                 'model',
                 'classifier.pkl'), 'rb'))

def classify(text):
    
    X = vect.transform([text])
    y = clf.predict(X)[0]
    proba = np.max(clf.predict_proba(X))

    return LABEL[y], proba

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

    print()
    y = LABEL_INV[prediction]
    if feedback == 'Incorrect':
        y = int(not(y))
    sqlite_entry(DB_PATH, comment, y)
    return render_template('thanks.html')

if __name__ == '__main__':
    app.run()
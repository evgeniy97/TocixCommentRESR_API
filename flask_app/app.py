from flask import Flask, request, render_template, redirect
from joblib import load
app = Flask(__name__)

def loadMOdel(path='model/model.joblib'):
    model = load(path)
    return model

model = loadMOdel()

@app.route('/', methods=["GET"])
def hi():
    return render_template('main.html')

@app.route('/predict', methods=["POST"])
def predict():
    text = request.text
    predictionn = model.predict(text)
    return predictionn


@app.route('/add', methods=["POST"])
def addExample():
    pass

@app.route('/take', methods=["GET"])
def getDB():
    pass

if __name__ == '__main__':
    app.run()
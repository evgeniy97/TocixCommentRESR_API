from flask import Flask, request, render_template, redirect
from joblib import load
app = Flask(__name__)

def loadMOdel(path):
    model = load(path)
    return model

vector = loadMOdel('model/vec.joblib')
model = loadMOdel('model/model.joblib')

@app.route('/', methods=["GET"])
def hi():
    return render_template('main.html')

@app.route('/predict', methods=["POST"])
def predict():
    # Get text from request
    #text = request.text
    #prediction = model.predict(text)
    
    prediction = 1

    return prediction


@app.route('/add', methods=["POST"])
def addExample():
    pass

@app.route('/take', methods=["GET"])
def getDB():
    pass

if __name__ == '__main__':
    app.run()
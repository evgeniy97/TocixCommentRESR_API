from flask import Flask, request, render_template, redirect

app = Flask(__name__)

def loadMOdel():
    pass

@app.route('/', methods=["GET"])
def hi():
    pass

@app.route('/predict', methods=["POST"])
def predict():
    pass


@app.route('/add', methods=["POST"])
def addExample():
    pass

@app.route('/take', methods=["GET"])
def getDB():
    pass

if __name__ == '__main__':
    app.run()
from flask import Flask, jsonify
from flask_cors import CORS
from random import randrange
from os.path import join

app = Flask(__name__)
CORS(app)

@app.route('/')
def random_text():
    with open(join('data', 'oblique.txt'), 'r') as ost:
        strats = ost.readlines()
        length = len(strats)
    idx = randrange(569)
    strat = strats[idx] 
    # this is going to give us 3 things.
    stratout = strat.split(',')[2]
    return jsonify({"text": stratout.strip()})

if __name__ == "__main__":
    app.run(debug=True)
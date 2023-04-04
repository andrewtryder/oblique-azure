from flask import Flask, jsonify
from random import randrange
from os import join

app = Flask(__name__)

@app.route('/')
def random_text():
    with open(join('data', 'oblique.txt'), 'r') as ost:
        strats = ost.readlines()
        length = len(strats)
    idx = randrange(190)
    strat = strats[idx]
    return jsonify({"text": strat.strip()})

if __name__ == "__main__":
    app.run(debug=True)
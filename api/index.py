from flask import Flask, jsonify
import random
import sqlite3

app = Flask(__name__)

@app.route('/')
def random_text():
    conn = sqlite3.connect("db/texts.db")
    cursor = conn.cursor()
    cursor.execute("SELECT text FROM texts ORDER BY RANDOM() LIMIT 1")
    random_text = cursor.fetchone()[0]
    conn.close()
    return jsonify({"text": random_text})

if __name__ == "__main__":
    app.run(debug=True)
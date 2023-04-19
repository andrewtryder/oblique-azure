from flask import Flask, jsonify, render_template
from flask_cors import CORS
import random
from os.path import join
import os
from googleapiclient.discovery import build
from utils import get_file_ids, get_file_content, resize_and_compress_image, get_contrasting_color
from dotenv import load_dotenv

env_path = os.path.join(os.path.dirname(__file__), '..', '.env')
if os.path.exists(env_path):
    load_dotenv(dotenv_path=env_path)

# setup templates directory for Flask.
template_dir = os.path.abspath('templates')
# setup Flask app and CORS.
app = Flask(__name__, template_folder=template_dir)
CORS(app)


@app.route('/')
def index():
    folder_id = os.environ.get("GOOGLE_DRIVE_FOLDER_ID")
    api_key = os.environ.get("GOOGLE_DRIVE_API_KEY")
    drive_service = build('drive', 'v3', developerKey=api_key)
    file_ids = get_file_ids(drive_service, folder_id)
    if len(file_ids) > 0:
        random_file_id = random.choice(file_ids)
        file_content = get_file_content(drive_service, random_file_id)
        image_data, hex_color = resize_and_compress_image(file_content)
        text_color = get_contrasting_color(hex_color)

        return render_template('index.html', image_data=image_data, text_color=text_color)
    else:
        return 'No images found in the specified folder.'


@app.route('/api')
def random_text():
    with open(join('data', 'oblique.txt'), 'r') as ost:
        strats = ost.readlines()
        length = len(strats)
    idx = random.randrange(length)
    strat = strats[idx]
    # this is going to give us 3 things: The overall number, the deck and the actual strategty quote.
    stratout = strat.split(',')[2]
    return jsonify({"text": stratout.strip()})


if __name__ == "__main__":
    app.run(debug=True)

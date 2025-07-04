from flask import Flask, render_template, request, redirect, url_for
import json
import time
import os

app = Flask(__name__)

DATA_FILE = 'data.json'
WEEK_SECONDS = 7 * 24 * 3600


def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE) as f:
            return json.load(f)
    return {
        "characters": [
            {"id": 1, "name": "Leader", "level": 1},
            {"id": 2, "name": "Captain A", "level": 2},
            {"id": 3, "name": "Captain B", "level": 2},
            {"id": 4, "name": "Soldier A", "level": 3},
            {"id": 5, "name": "Soldier B", "level": 3},
            {"id": 6, "name": "Soldier C", "level": 3},
        ],
        "votes": []
    }


def save_data(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f)


def count_votes(data):
    cutoff = time.time() - WEEK_SECONDS
    counts = {c["id"]: 0 for c in data["characters"]}
    data["votes"] = [v for v in data["votes"] if v["timestamp"] >= cutoff]
    for vote in data["votes"]:
        counts[vote["character_id"]] += 1
    return counts


@app.route('/')
def index():
    data = load_data()
    votes = count_votes(data)
    save_data(data)
    chars_by_level = {}
    for c in data["characters"]:
        chars_by_level.setdefault(c["level"], []).append(c)
    return render_template('index.html', levels=sorted(chars_by_level.items()), votes=votes)


@app.route('/vote/<int:char_id>', methods=['POST'])
def vote(char_id):
    data = load_data()
    data["votes"].append({"character_id": char_id, "timestamp": time.time()})
    save_data(data)
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)

from flask import Flask, jsonify
from database.db import init_db, seed_db

app = Flask(__name__)


@app.route('/')
def health():
    return jsonify({'status': 'ok'})


if __name__ == '__main__':
    with app.app_context():
        init_db()
        seed_db()
    app.run(debug=True)

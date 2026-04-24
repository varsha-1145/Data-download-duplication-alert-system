from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime
import hashlib

from models import db, Download

app = Flask(__name__)
CORS(app, origins=["chrome-extension://dekggdincebnggmjaipefhpadggjagaa"])

# Database setup
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

def compute_fake_hash(filename, url):
    data = f"{filename}:{url}"
    return hashlib.sha256(data.encode('utf-8')).hexdigest()

@app.before_first_request
def create_tables():
    db.create_all()

@app.route('/check_duplicate', methods=['POST'])
def check_duplicate():
    data = request.json
    filename = data.get('filename')
    file_url = data.get('url')
    file_hash = compute_fake_hash(filename, file_url)

    existing = Download.query.filter_by(filehash=file_hash).first()

    if existing:
        return jsonify({
            'is_duplicate': True,
            'uploader': existing.uploader,
            'timestamp': existing.timestamp
        })

    new_download = Download(
        filename=filename,
        filehash=file_hash,
        url=file_url,
        uploader="Batch No:12",
        timestamp=datetime.now().isoformat()
    )

    db.session.add(new_download)
    db.session.commit()

    return jsonify({'is_duplicate': False})

if __name__ == '__main__':
    app.run(debug=True)

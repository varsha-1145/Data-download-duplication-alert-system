from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Download(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(255))
    filehash = db.Column(db.String(64))
    url = db.Column(db.String(500))
    uploader = db.Column(db.String(100))
    timestamp = db.Column(db.String(100))

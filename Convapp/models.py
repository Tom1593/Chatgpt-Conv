from datetime import datetime
from Convapp import db

class Entry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    conv_id = db.Column(db.Integer, db.ForeignKey('conv.id'), nullable=False)
    owner = db.Column(db.String(20), nullable=False)
    content = db.Column(db.Text, nullable=False)
    audio_file = db.Column(db.BLOB, nullable=False)
    
    def __repr__(self):
        return f"Entry('{self.owner}','{self.content}','{self.audio_file}')"

class Conv(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_started = db.Column(db.DateTime, nullable=False, default=datetime.today)
    entries = db.relationship('Entry', backref='conv_id', lazy=True)
    
    def __repr__(self):
        return f"Conv('{self.id}','{self.date_started}', '{self.entries}')"
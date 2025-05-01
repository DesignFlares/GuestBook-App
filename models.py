from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db= SQLAlchemy()
    
class Review(db.Model):
    __tablename__ = 'reviews'
    sno = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), nullable=True)
    user = db.Column(db.String(150), nullable=True)
    review_text = db.Column(db.String(500), nullable=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
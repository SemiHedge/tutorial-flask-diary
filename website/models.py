from . import db  # from website import db
from flask_login import UserMixin
from sqlalchemy.sql import func


# define User Model
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    nickname = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200))
    notes = db.relationship('Note')


# define Note Model
class Note(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    content = db.Column(db.String(2000))
    datetime = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
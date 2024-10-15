from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class DialogueRecord(db.Model):
    __tablename__ = 'dialogue_record'
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String, nullable=False)
    answer = db.Column(db.String,  nullable=False)

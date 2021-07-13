from models.settings import db


class Questions(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question_name = db.Column(db.String, unique=False)
    question_text = db.Column(db.String, unique=False)


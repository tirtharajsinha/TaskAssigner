from flask_sqlalchemy import SQLAlchemy

# create your db model here

db = SQLAlchemy()


class Log(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    person = db.Column(db.String(100), nullable=False)
    task = db.Column(db.String(100), nullable=False)
    date = db.Column(db.String(100), nullable=False)
    submit = db.Column(db.String(100), nullable=False)

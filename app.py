import views
from flask import Flask
from flask_wtf.csrf import CSRFProtect
from models import db
import config
import urls

app = Flask(__name__)


# csrf
csrf = CSRFProtect(app)

# config
app.config.from_object('config.Config')

# database connection

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
# app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///registration.db'
app.config["SQLALCHEMY_DATABASE_URI"] = 'postgresql://zycvbnvwvumfpo:ec9a7853e5f5b94eaf0d413d5a38288d16ba770cd1532f98818daa091219e73b@ec2-54-195-76-73.eu-west-1.compute.amazonaws.com:5432/dc77499m8jiavo'
db.init_app(app)


#######################


# urls
app = urls.add_url(app)


if __name__ == "__main__":
    #  run this db.create first timels

    try:
        with app.app_context():
            db.create_all()
    except Exception as e:
        print(e)
    app.run(debug=True)


# this is a custom template from Tirtharaj Sinha (https://github.com/tirtharajsinha/Flask-starter.git)

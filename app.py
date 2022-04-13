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
app.config["SQLALCHEMY_DATABASE_URI"]="postgresql://tyosmlsokpjgdh:eb9a24de65cba23c3bcd37908e6b9d9be6d03571b47450c005badf2278bbc220@ec2-54-247-137-184.eu-west-1.compute.amazonaws.com:5432/db9d3kel7dg6c8"
db.init_app(app)


#######################


# urls
app = urls.add_url(app)


if __name__ == "__main__":
    #  run this db.create first timels

    # try:
    #     with app.app_context():
    #         db.create_all()
    # except Exception as e:
    #     print(e)
    app.run(debug=True)


# this is a custom template from Tirtharaj Sinha (https://github.com/tirtharajsinha/Flask-starter.git)

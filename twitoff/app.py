from flask import Flask, render_template
from .models import DB


def create_app():
    """Create and configure an instance of the Flask Application"""
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
    DB.init_app(app)

    @app.route('/')
    def root():
        return render_template('home.html')
    
    @app.route("/about")
    def preds():
        return render_template('about.html')

    return app



# #import flask package. flask makes app objects.
# from flask import Flask, render_template

# #create Flask web server, makes the application
# app = Flask(__name__)

# #routes determine location
# @app.route("/")

# # #Define simple function
# # def home():
# #     return render_template('home.html')

# @app.route("/about")
# def preds():
#     return render_template('about.html')

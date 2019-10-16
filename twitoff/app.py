from decouple import config
from flask import Flask, render_template, request
from .models import DB, User, Tweet
from .twitter import add_or_update_user

def create_app():
    """Create and configure an instance of the Flask Application"""
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = config('DATABASE_URL')
    app.config['ENV'] = config('ENV')
    app.config['DEBUG'] = config('FLASK_DEBUG')
    DB.init_app(app)
    
    @app.route('/')
    def root():
        users = User.query.all()
        return render_template('home.html', title='Welcome to Twitoff!', users=users)
    
    @app.route("/about")
    def preds():
        return render_template('about.html')

    @app.route("/reset")
    def reset():
        DB.drop_all()
        DB.create_all()
        return render_template('reset.html', title='DB Reset!', users=[])
    
    @app.route('/user', methods=['POST'])
    @app.route('/user/<name>/', methods=['GET'])
    def user(name=None, message=''):
        name = (name or request.values['user_name'])
        try:
            if request.method =='POST':
                add_or_update_user(name)
                message = 'User {} successfully added!'.format(name)
            tweets = User.query.filter(User.name == name).one().tweets
        except Exception as e:
            message = 'Error adding {}: {}'.format(name,e)
            tweets=[]
            pass
        return render_template('user.html', name=name, tweets=tweets, message=message)
    return app
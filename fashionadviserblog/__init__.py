import os
from dotenv import load_dotenv
from flask import Flask, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_dance.contrib.google import make_google_blueprint, google

#flask db init
#flask db migrate  -m "message"
#flask db upgrade
# os.environ["OAUTHLIB_RELAX_TOKEN_SCOPE"] = '1'
# pip freeze > requirements.txt
#heroku run printenv
# export OAUTHLIB_INSECURE_TRANSPORT=1
# export FLASK_ENV=development
#python app.py

load_dotenv()
app = Flask(__name__)


app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
app.config['ELASTICSEARCH_URL'] = os.environ.get('ELASTICSEARCH_URL')


################################################
#################Database setup#################
################################################
basedir = os.path.abspath(os.path.dirname(__file__ ))
#app.config['SQLALCHEMY_DATABASE_URI'] = or 'sqlite:///' + os.path.join(basedir, 'blog_posts.db')

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'blog_posts.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
Migrate(app, db)
################################################################################################

################################################
###############Login configurations#############
################################################

blueprint_google = make_google_blueprint(
    client_id="930782827177-m6l1onmtdkau9ua2acoggl87cof130fs.apps.googleusercontent.com",
    client_secret=os.environ.get('CLIENT_SECRET'),
    reprompt_consent=True,
    redirect_to = 'blog_posts.admin',
    offline=True,
    scope=["https://www.googleapis.com/auth/userinfo.email",
        "https://www.googleapis.com/auth/userinfo.profile",
        "openid"])



################################################################################################

from fashionadviserblog.core.views import core
from fashionadviserblog.blog_posts.views import blog_posts
from fashionadviserblog.error_pages.handlers import error_pages

app.register_blueprint(core)
app.register_blueprint(error_pages)
app.register_blueprint(blog_posts)
app.register_blueprint(blueprint_google, url_prefix="/login")

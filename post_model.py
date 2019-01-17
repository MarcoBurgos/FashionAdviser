import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

basedir = os.path.abspath(os.path.dirname(__file__ ))

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'blog_posts.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy()

class Blog_posts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(70), nullable=False)
    subtitle = db.Column(db.String(200), nullable=False)
    photo_url = db.Column(db.String(150), nullable=False)
    timestap = db.Column(db.DateTime, nullable=False)
    post_content = db.Column(db.Text, nullable=False)
    section_type = db.Column(db.String(30), nullable=False)

    def __init__(self,title, subtitle, photo_url, timestap, post_content, section_type):
        self.title = title
        self.subtitle = subtitle
        self.photo_url = photo_url
        self.timestap = timestap
        self.post_content = post_content
        self.section_type = section_type

    def __repr__(self):
        return f"Title {self.title} was uploaded on {self.timestap}"

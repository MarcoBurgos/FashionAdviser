from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://///Users/marcoburgos/Desktop/website/Blog/blog-env/blog_posts.db'


db = SQLAlchemy(app)

class blog_posts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(70), nullable=False)
    subtitle = db.Column(db.String(200), nullable=False)
    photo_url = db.Column(db.String(150), nullable=False)
    timestap = db.Column(db.DateTime, nullable=False)
    post_content = db.Column(db.Text)

@app.route('/')
def index():
    main_posts = blog_posts.query.filter(blog_posts.id>0).limit(2).all()
    feature_post = blog_posts.query.filter(blog_posts.id>2).limit(2).all()
    side_posts = blog_posts.query.filter(blog_posts.id>4).limit(3).all()
    return render_template('testindex.html', main_posts=main_posts, feature_post=feature_post, side_posts=side_posts)

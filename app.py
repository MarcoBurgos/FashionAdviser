from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
from datetime import datetime
from post_model import Blog_posts, db
from postForm import PostForm
import os
import re

basedir = os.path.abspath(os.path.dirname(__file__ ))



app = Flask(__name__)
app.config['SECRET_KEY'] = 'TFA20191601'


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'blog_posts.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
db.init_app(app)


@app.route('/')
def index():
    main_posts = Blog_posts.query.order_by(Blog_posts.timestap.desc()).limit(2).all()
    #main_posts = Blog_posts.query.filter(Blog_posts.id>0).limit(2).all()
    feature_post = Blog_posts.query.filter(Blog_posts.id>2).limit(2).all()
    side_posts = Blog_posts.query.filter(Blog_posts.id>4).limit(2).all()

    return render_template('index.html', main_posts=main_posts, feature_post=feature_post, side_posts=side_posts)


@app.route('/section/<string:section_name>'+'.html')
def section(section_name):
    count = db.session.query(Blog_posts).filter(Blog_posts.id>0).count()
    count = round(count/5)
    main_posts = Blog_posts.query.order_by(Blog_posts.timestap.desc()).filter(Blog_posts.section_type==section_name).limit(3).all()
    print(f"main posts are {main_posts}")
    side_posts = Blog_posts.query.filter(Blog_posts.id>4).limit(3).all()
    print(f"titule urle is {section_name}")

    return render_template('section.html', main_posts=main_posts, side_posts=side_posts, section_name=section_name, count=count)


@app.route('/post/<int:post_id>')
def post(post_id):
     post = Blog_posts.query.filter_by(id=post_id).one()

     return render_template('post.html', post=post)


@app.route('/dashboard/addpost', methods=['GET', 'POST'])
def addpost():
    form = PostForm()

    if form.validate_on_submit():
        session['title'] = form.title.data
        session['subtitle'] = form.subtitle.data
        session['photo_url'] = form.photo_url.data
        session['section_type'] = form.section_type.data
        session['post_content'] = form.post_content.data
        post = Blog_posts(form.title.data, form.subtitle.data, form.photo_url.data, datetime.now(), form.post_content.data, form.section_type.data)
        db.session.add(post)
        db.session.commit()

        return redirect(url_for("index"))

    return render_template('addpost.html', form=form)



if __name__ == '__main__':
    app.run(debug=True)

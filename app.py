from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
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
    main_posts = Blog_posts.query.filter(Blog_posts.id>0).limit(2).all()
    feature_post = Blog_posts.query.filter(Blog_posts.id>2).limit(2).all()
    side_posts = Blog_posts.query.filter(Blog_posts.id>4).limit(3).all()
    return render_template('index.html', main_posts=main_posts, feature_post=feature_post, side_posts=side_posts)


@app.route('/<string:section_type>')
def section(section_type):
    section_name = re.sub(".html", "", section_type )
    main_posts = Blog_posts.query.filter(Blog_posts.section_type==section_name).all()
    side_posts = Blog_posts.query.filter(Blog_posts.id>4).limit(9).all()
    print(f"titule urle is {section_name}")
    print(f"main_posts is {main_posts}")
    return render_template('section.html', main_posts=main_posts, side_posts=side_posts, section_type=section_name)


@app.route('/post/<int:post_id>')
def post(post_id):
     post = Blog_posts.query.filter_by(id=post_id).one()

     return render_template('post.html', post=post)


@app.route('/addpost.html', methods=['GET', 'POST'])
def addpost():

    form = PostForm()
    print(form.validate_on_submit())
    if form.validate_on_submit():

        session['title'] = form.title.data
        session['subtitle'] = form.subtitle.data
        session['photo_url'] = form.photo_url.data
        session['section_type'] = form.section_type.data
        session['post_content'] = form.post_content.data
        print("is valid!")
        post = Blog_posts(form.title.data, form.subtitle.data, form.photo_url.data, datetime.now(), form.post_content.data, form.section_type.data)
        #post = Blog_posts(title=form.title.data, subtitle=form.subtitle.data, photo_url=form.photo_url.data, timestap=datetime.now(),post_content=form.post_content.data, section_type=form.section_type.data)
        print(post)
        db.session.add(post)
        db.session.commit()
        print(post)
        return redirect(url_for("index"))
    else:
        print("Not valid")


    return render_template('addpost.html', form=form)

@app.route('/preview', methods=['GET','POST'])
def preview():
    print("we got here")
    return render_template('preview.html')

# @app.route('/addpost', methods=['POST'])
# def addpost():
#     title = request.form['title']
#     subtitle = request.form['subtitle']
#     author = request.form['author']
#     content = request.form['content']
#
#     post = Blogpost(title=title, subtitle=subtitle, author=author, content=content, date_posted=datetime.now())
#
#     db.session.add(post)
#     db.session.commit()
#
#     return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)

from flask import Flask, render_template, request, redirect, url_for, session, flash, Blueprint
from fashionadviserblog.models import Blog_posts
from fashionadviserblog import db

core = Blueprint("section", __name__)

@core.route('/')
def index():
    main_posts = Blog_posts.query.order_by(Blog_posts.post_timestamp.desc()).limit(2).all()
    feature_post = Blog_posts.query.order_by(Blog_posts.post_timestamp.desc()).limit(5).all()
    feature_post = feature_post[2:]
    side_posts = Blog_posts.query.order_by(Blog_posts.post_timestamp.desc()).limit(10).all()
    side_posts =  side_posts[5:]

    return render_template('index.html', main_posts=main_posts, feature_post=feature_post, side_posts=side_posts)

@core.route('/section/<string:sec_name>')
def blog_section(sec_name):
    count = db.session.query(Blog_posts).filter(Blog_posts.id>0).count()
    count = round(count/5)
    main_posts = Blog_posts.query.order_by(Blog_posts.post_timestamp.desc()).filter(Blog_posts.section_name==sec_name).limit(3).all()
    side_posts = Blog_posts.query.order_by(Blog_posts.post_timestamp.desc()).filter(Blog_posts.section_name!=sec_name).limit(7).all()
    side_posts =  side_posts[3:]
    print(f"Section name {sec_name}")

    return render_template('section.html', main_posts=main_posts, side_posts=side_posts, section_name=sec_name, count=count)


@core.route('/google082e320c4857255c.html')
def google_validator():

    return render_template('google082e320c4857255c.html')


@core.route('/post_circulator')
def post_circulator():

    post = Blog_posts.query.get_or_404(12)
    p = Blog_posts.query.get_or_404(11)
    po = Blog_posts.query.get_or_404(6)
    lines = (post.post_content).splitlines()

    return render_template('post_circulator.html', post=post, p=p, po=po, lines=lines)

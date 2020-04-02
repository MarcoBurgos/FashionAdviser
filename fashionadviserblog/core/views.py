from flask import Flask, render_template, request, redirect, url_for, session, flash, Blueprint
from fashionadviserblog.models import Blog_posts
from fashionadviserblog import db

core = Blueprint("section", __name__)

@core.route('/')
def index():
    main_posts = Blog_posts.query.order_by(Blog_posts.post_timestamp.desc()).limit(4).all()
    feature_post = Blog_posts.query.order_by(Blog_posts.post_timestamp.desc()).limit(7).all()
    feature_post = feature_post[4:]


    fashion_count = db.session.query(Blog_posts).filter(Blog_posts.section_name=='Fashion').count()
    lifestyle_count = db.session.query(Blog_posts).filter(Blog_posts.section_name=='Lifestyle').count()
    news_count = db.session.query(Blog_posts).filter(Blog_posts.section_name=='News').count()

    return render_template('index.html', main_posts=main_posts, feature_post=feature_post, fashion_count=fashion_count, lifestyle_count=lifestyle_count, news_count=news_count )



@core.route('/section/<string:sec_name>')
def blog_section(sec_name):
    count = db.session.query(Blog_posts).filter(Blog_posts.id>0).count()
    count = round(count/5)

    fashion_count = db.session.query(Blog_posts).filter(Blog_posts.section_name=='Fashion').count()
    lifestyle_count = db.session.query(Blog_posts).filter(Blog_posts.section_name=='Lifestyle').count()
    news_count = db.session.query(Blog_posts).filter(Blog_posts.section_name=='News').count()

    main_posts = Blog_posts.query.order_by(Blog_posts.post_timestamp.desc()).filter(Blog_posts.section_name==sec_name).limit(8).all()


    return render_template('section.html', main_posts=main_posts, section_name=sec_name, count=count, fashion_count=fashion_count, lifestyle_count=lifestyle_count, news_count=news_count )


@core.route('/google082e320c4857255c.html')
def google_validator():

    return render_template('google082e320c4857255c.html')

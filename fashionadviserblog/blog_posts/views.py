from flask import Flask, render_template, request, redirect, url_for, session, flash, Blueprint, abort
from flask_sqlalchemy import SQLAlchemy
from flask_dance.contrib.google import make_google_blueprint, google
from fashionadviserblog import db
from fashionadviserblog.models import Blog_posts
from fashionadviserblog.check_auth import is_user_auth
from fashionadviserblog.blog_posts.forms import PostForm
from datetime import datetime

blog_posts = Blueprint('blog_posts', __name__)


@blog_posts.route('/create', methods=['GET', 'POST'])
def create_post():

    if is_user_auth():
        form = PostForm()

        if form.validate_on_submit():

            post = Blog_posts(title = form.title.data,
                           subtitle = form.subtitle.data,
                           photo_url = form.photo_url.data,
                           post_timestamp = datetime.now(),
                           post_content = form.post_content.data,
                           section_name =  form.section_name.data)

            db.session.add(post)
            db.session.commit()
            flash(f"Creaste un post, id: {post.id}, título: {post.title}")
            return redirect(url_for('blog_posts.preview_post', post_id=post.id))

        return render_template('create_post.html', form=form)
    else:
        abort(403)


@blog_posts.route('/post/<int:post_id>', methods=['GET', 'POST'])
def post(post_id):
    post = Blog_posts.query.get_or_404(post_id)
    fashion_count = db.session.query(Blog_posts).filter(Blog_posts.section_name=='Fashion').count()
    lifestyle_count = db.session.query(Blog_posts).filter(Blog_posts.section_name=='Lifestyle').count()
    news_count = db.session.query(Blog_posts).filter(Blog_posts.section_name=='News').count()


    return render_template('post.html', post=post, fashion_count=fashion_count, lifestyle_count=lifestyle_count, news_count=news_count )



@blog_posts.route('/<int:post_id>/update', methods=['GET', 'POST'])
def update_post(post_id):

    post = Blog_posts.query.get_or_404(post_id)

    if is_user_auth():
        form = PostForm()

        if form.validate_on_submit():

            post.title = form.title.data
            post.subtitle = form.subtitle.data
            post.photo_url = form.photo_url.data
            post.post_content = form.post_content.data
            post.section_name =  form.section_name.data

            db.session.commit()
            flash(f"Editaste post id: {post.id}, título: {post.title}")

            return redirect(url_for('blog_posts.admin'))

        elif request.method == 'GET':
            form.title.data = post.title
            form.subtitle.data = post.subtitle
            form.photo_url.data = post.photo_url
            form.post_timestamp = post.post_timestamp
            form.post_content.data = post.post_content
            form.section_name.data = post.section_name

        return render_template('create_post.html', post=post, form=form)

    else:
        abort(403)


@blog_posts.route('/<int:post_id>/delete', methods=['GET', 'POST'])
def delete_post(post_id):
    post = Blog_posts.query.get_or_404(post_id)

    if is_user_auth():
        flash(f"Eliminaste post: {post.id}, con título {post.title}")
        db.session.delete(post)
        db.session.commit()
    return redirect(url_for("blog_posts.admin"))


@blog_posts.route('/preview/<int:post_id>', methods=['GET', 'POST'])
def preview_post(post_id):

    if is_user_auth():
        post = Blog_posts.query.get_or_404(post_id)


        return render_template('preview.html', post=post)

    else:
        abort(403)



@blog_posts.route('/admin', methods = ['GET', 'POST'])
def admin():
    if not google.authorized:
        return redirect(url_for("google.login"))

    resp = google.get("/oauth2/v2/userinfo")
    assert resp.ok, resp.text
    email= resp.json()["email"]
    name = resp.json()["name"]

    if email in ['marko.burgos@gmail.com', 'angie.zcoln@gmail.com']:
        bposts = Blog_posts.query.order_by(Blog_posts.post_timestamp.desc()).all()

        return render_template('dashboard.html', bposts=bposts, name=name)
    else:
        abort(403)

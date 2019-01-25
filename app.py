from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from flask_dance.contrib.google import make_google_blueprint, google
from sqlalchemy import func
from datetime import datetime
from post_model import Blog_posts, db
from postForm import PostForm
from check_auth import is_user_auth
import os
import re


os.environ["OAUTHLIB_RELAX_TOKEN_SCOPE"] = '1'

basedir = os.path.abspath(os.path.dirname(__file__ ))



app = Flask(__name__)
app.config['SECRET_KEY'] = 'TFA20191601'


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'blog_posts.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
db.init_app(app)


blueprint = make_google_blueprint(
    client_id="930782827177-m6l1onmtdkau9ua2acoggl87cof130fs.apps.googleusercontent.com",
    client_secret="p_PiTxEJQv8sjUk2o2RrYvbB",
    # reprompt_consent=True,
    offline=True,
    scope=["profile", "email"]
)

app.register_blueprint(blueprint, url_prefix="/login")

@app.route('/')
def index():
    main_posts = Blog_posts.query.order_by(Blog_posts.timestap.desc()).limit(2).all()
    feature_post = Blog_posts.query.order_by(Blog_posts.timestap.desc()).limit(5).all()
    feature_post = feature_post[2:]
    side_posts = Blog_posts.query.order_by(Blog_posts.timestap.desc()).limit(10).all()
    side_posts =  side_posts[5:]

    return render_template('index.html', main_posts=main_posts, feature_post=feature_post, side_posts=side_posts)


@app.route('/section/<string:section_name>'+'.html')
def section(section_name):
    count = db.session.query(Blog_posts).filter(Blog_posts.id>0).count()
    count = round(count/5)
    main_posts = Blog_posts.query.order_by(Blog_posts.timestap.desc()).filter(Blog_posts.section_type==section_name).limit(3).all()
    side_posts = Blog_posts.query.order_by(Blog_posts.timestap.desc()).filter(Blog_posts.section_type!=section_name).limit(7).all()
    side_posts =  side_posts[3:]


    return render_template('section.html', main_posts=main_posts, side_posts=side_posts, section_name=section_name, count=count)


@app.route('/post/<int:post_id>')
def post(post_id):
     post = Blog_posts.query.filter_by(id=post_id).one()

     return render_template('post.html', post=post)


@app.route('/dashboard/addpost', methods=['GET', 'POST'])
def addpost():
    if not google.authorized:
        return redirect(url_for("login"))

    resp = google.get("/oauth2/v2/userinfo")
    assert resp.ok, resp.text
    email=resp.json()["email"]

    if is_user_auth(email):

        form = PostForm()

        if form.validate_on_submit():

            post = Blog_posts(form.title.data, form.subtitle.data, form.photo_url.data, datetime.now(), form.post_content.data, form.section_type.data)

            db.session.add(post)
            db.session.commit()

            return redirect(url_for("preview"))

        return render_template('addpost.html', form=form)
    else:
        return render_template('not_authorized.html', email=email)

@app.route("/dashboard/preview/")
def preview():
    if not google.authorized:
        return redirect(url_for("login"))

    resp = google.get("/oauth2/v2/userinfo")
    assert resp.ok, resp.text
    name = resp.json()["given_name"]
    email = resp.json()['email']

    if is_user_auth(email):
        post_id = Blog_posts.query.order_by(Blog_posts.timestap.desc()).limit(1).one()
        print(post_id.id)
        post = Blog_posts.query.filter_by(id=post_id.id).one()
        print(post.title)

        return render_template('preview.html', post=post)



@app.route("/editpost/<int:post_id>", methods=['GET', 'POST'])
def editpost(post_id):
    if not google.authorized:
        return redirect(url_for("login"))

    resp = google.get("/oauth2/v2/userinfo")
    assert resp.ok, resp.text
    name = resp.json()["given_name"]
    email = resp.json()['email']

    if is_user_auth(email):
        post = Blog_posts.query.get(post_id)

        form = PostForm(obj=post)


        if form.validate_on_submit():

            updated_post = Blog_posts.query.get(post_id)
            updated_post.title = form.title.data
            updated_post.subtitle = form.subtitle.data
            updated_post.photo_url = form.photo_url.data
            updated_post.section_type = form.section_type.data
            updated_post.post_content = form.post_content.data

            updated_post = db.session.merge(updated_post)

            db.session.add(updated_post)
            db.session.commit()

            return redirect(url_for("dashboard"))

        return render_template('addpost.html', post=post, form=form)
    else:
        return render_template('not_authorized.html', email=email)


@app.route("/delete/<int:post_id>", methods=["GET", "POST"])
def delete(post_id):
    post = Blog_posts.query.get(post_id)
    flash(f"Eliminaste post: {post_id}, con título {post.title}")
    post = db.session.merge(post)
    db.session.delete(post)
    db.session.commit()

    return redirect("/dashboard")




@app.route("/dashboard")
def dashboard():
    if not google.authorized:
        return redirect(url_for("login"))

    resp = google.get("/oauth2/v2/userinfo")
    assert resp.ok, resp.text
    name = resp.json()["given_name"]
    email = resp.json()['email']

    if is_user_auth(email):
        posts = Blog_posts.query.order_by(Blog_posts.timestap.desc()).all()

        return render_template('dashboard.html', posts=posts, name=name)
    else:
        return render_template('not_authorized.html', email=email)



@app.route("/login/google")
def login():
    if not google.authorized:
        return render_template(url_for("google.login"))

    resp = google.get("/oauth2/v2/userinfo")
    assert resp.ok, resp.text

    return render_template('dashboard.html')



if __name__ == '__main__':
    app.run(debug=True)

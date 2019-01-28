from flask import redirect, url_for
from flask_dance.contrib.google import make_google_blueprint, google

def is_user_auth():
    if not google.authorized:
        return redirect(url_for("google.login"))

    resp = google.get("/oauth2/v2/userinfo")
    assert resp.ok, resp.text
    email=resp.json()["email"]


    if email in ['marko.burgos@gmail.com', 'angie.zcoln@gmail.com']:
        return True
    else:
        return False

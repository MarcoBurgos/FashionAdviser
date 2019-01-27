from fashionadviserblog import db

class Blog_posts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(70), unique=True, nullable=False)
    subtitle = db.Column(db.String(200), nullable=False)
    photo_url = db.Column(db.String(150), nullable=False)
    post_timestamp = db.Column(db.DateTime, nullable=False)
    post_content = db.Column(db.Text, nullable=False)
    section_name = db.Column(db.String(30), nullable=False)

    def __init__(self,title, subtitle, photo_url, post_timestamp, post_content, section_name):
        self.title = title
        self.subtitle = subtitle
        self.photo_url = photo_url
        self.post_timestamp = post_timestamp
        self.post_content = post_content
        self.section_name = section_name

    def __repr__(self):
        return f"Title {self.title} was uploaded on {self.post_timestamp}"

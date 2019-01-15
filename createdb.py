import sqlite3
from datetime import datetime

conn = sqlite3.connect("blog_posts.db")

c = conn.cursor()


def create_table():
    c.execute('CREATE TABLE IF NOT EXISTS blog_posts(id INT PRIMARY KEY, title varchar(70) NOT NULL, subtitle text NOT NULL, photo_url varchar(255) NOT NULL, timestap date NOT NULL, post_content text)')

def insert_into_table():
    c.execute("""insert into blog_posts
          values (1 'test','test','test',datetime.now(),'test')""")
    #c.execute("INSERT INTO blog_posts (id, title, subtitle, photo_url, timestap, post_content) values (1, 'Title', 'Subtitle', 'https://unsplash.com/photos/R2aodqJn3b8', datetime.now(), 'Content')")
    # conn.commit()
    # c.close()
    # conn.close()

def select():
    c.execute("SELECT blog_posts.id AS blog_posts_id, blog_posts.title AS blog_posts_title, blog_posts.subtitle AS blog_posts_subtitle, blog_posts.photo_url AS blog_posts_photo_url, blog_posts.timestap AS blog_posts_timestap, blog_posts.post_content AS blog_posts_post_content FROM blog_posts")
    print(c.fetchall())

#create_table()
#insert_into_table()
select()

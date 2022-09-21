"""Models for Blogly."""

from flask_sqlalchemy import SQLAlchemy 
import datetime

db = SQLAlchemy()

DEFAULT_IMAGE_URL = "https://www.freeiconspng.com/uploads/icon-user-blue-symbol-people-person-generic--public-domain--21.png" 

def connect_db(app): 
    db.app = app 
    db.init_app(app) 

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.Text, nullable=False)
    last_name = db.Column(db.Text, nullable=False) 
    image_url = db.Column(db.Text, nullable=False, default=DEFAULT_IMAGE_URL)

    posts = db.relationship('Post', backref='users', cascade="all, delete-orphan")

    @property
    def full_name(self): 
        """Combine first and last name to create full name"""

        return f"{self.first_name} {self.last_name}" 

    def __repr__(self): 
        u = self
        return f"<User id={self.id} first_name={u.first_name} last_name={u.last_name} image_url={u.image_url} >" 

class Post(db.Model): 
    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.Text, nullable=False)
    content = db.Column(db.Text, nullable=False) 
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now) # Have no clue how this works

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False) 

    @property
    def friendly_date_time(self): 
        """Returns the date""" 
        # datetime object containing current date and time
        # now = datetime.now()
        # # dd/mm/YY H:M:S
        # dt_string = now.strftime("%m/%d/%Y %H:%M:%S") 
        # return dt_string
        return self.created_at.strftime("%a %b %-d  %Y, %-I:%M %p")


    def __repr__(self): 
        p = self 
        return f"<Post id={self.id} title={p.title} content={p.content} created_at={p.created_at} >"

class Tag(db.Model): 

    __tablename__ = 'tags' 

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(20), nullable=False, unique=True)

    posts = db.relationship('Post', secondary="posts_tags", backref="tags", cascade="all,delete") 

class PostTag(db.Model): 

    __tablename__ = 'posts_tags' 

    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), primary_key=True)

    tag_id = db.Column(db.Integer, db.ForeignKey('tags.id'), primary_key=True)










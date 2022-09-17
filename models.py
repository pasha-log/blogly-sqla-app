"""Models for Blogly."""

from flask_sqlalchemy import SQLAlchemy 

db = SQLAlchemy()

DEFAULT_IMAGE_URL = "https://www.freeiconspng.com/uploads/icon-user-blue-symbol-people-person-generic--public-domain--21.png" 

def connect_db(app): 
    db.app = app 
    db.init_app(app) 

class User(db.Model):
    __tablename__ = 'users'

    def __repr__(self): 
        u = self
        return f"<User id={self.id} first_name={u.first_name} last_name={u.last_name} image_url={u.image_url}>" 

    id = db.Column(db.Integer, 
                    primary_key=True,
                    autoincrement=True)
    first_name = db.Column(db.Text,
                    nullable=False)
    last_name = db.Column(db.Text,
                    nullable=False) 
    image_url = db.Column(db.Text, nullable=False, default=DEFAULT_IMAGE_URL) 

    @property
    def full_name(self): 
        """Combine first and last name to create full name"""

        return f"{self.first_name} {self.last_name}"







from unittest import TestCase 

from app import app 
from models import db, User, Post
import datetime

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_user_test' 
app.config['SQLALCHEMY_ECHO'] = False 

db.drop_all()
db.create_all()

class UserModelTestCase(TestCase):
    """Tests for model for User.""" 

    def setUp(self): 
        """Clean up any existing users.""" 

        User.query.delete()
    
    def tearDown(self): 
        """Clean up any fouled transaction.""" 

        db.session.rollback()

    def test_full_name(self): 
        user = User(first_name='Test', last_name="User")
        self.assertEquals(user.full_name, "Test User")
    
    def test_default_image(self):
        """Test whether a default image shows up if no image is added"""
        DEFAULT_IMAGE_URL = "https://www.freeiconspng.com/uploads/icon-user-blue-symbol-people-person-generic--public-domain--21.png" 
        user = User(first_name='Test', last_name="User", image_url=DEFAULT_IMAGE_URL)
        self.assertEquals(user.image_url, DEFAULT_IMAGE_URL) 

    def test_friendly_date_time(self): 
        user = User(first_name='Test', last_name="User")
        self.user_id = user.id
        post = Post(title="It's a Title", content='Here is some content', user_id=self.user_id, created_at=datetime.datetime.now) 
        self.post = post
        self.assertEquals(self.post.created_at, datetime.datetime.now)


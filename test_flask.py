from unittest import TestCase
from app import app 
from models import db, User 

app.config["SQLALCHEMY_DATABASE_URI"] = 'postgresql:///blogly_user_test'
app.config['SQLALCHEMY_ECHO'] = False 
app.config['TESTING'] = True 
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar'] 

db.drop_all() 
db.create_all()  

class UserViewsTestCase(TestCase): 
    """Tests for views for Users.""" 

    def setUp(self): 
        """Add new user.""" 

        User.query.delete() 

        user = User(first_name="Test", last_name='User') 
        db.session.add(user) 
        db.session.commit()

        self.user_id = user.id
        self.user = user
    
    def tearDown(self): 
        """Clean up any fouled transaction.""" 

        db.session.rollback() 

    def test_list_users(self): 
        with app.test_client() as client: 
            resp = client.get('/users') 
            html = resp.get_data(as_text=True) 

            self.assertEqual(resp.status_code, 200) 
            self.assertIn('Test', html) 

    def test_detail_user(self): 
        with app.test_client() as client: 
            resp = client.get(f"/users/{self.user_id}") 
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Test User', html)
            self.assertIn(self.user.image_url, html)

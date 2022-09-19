from unittest import TestCase
from app import app 
from models import db, User, Post

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

        user = User(first_name="Test", last_name='User') 
        db.session.add(user) 
        db.session.commit()

        self.user_id = user.id
        self.user = user
    
        """Add new post."""  

        Post.query.delete() 
        
        post = Post(title="It's a Title", content='Here is some content', user_id=self.user_id) 
        db.session.add(post) 
        db.session.commit()

        self.post_id = post.id
        self.post = post

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

    def test_post_list_shows_on_user_page(self): 
        """Make sure user page shows personal list of posts"""
        with app.test_client() as client: 
            resp = client.get(f"/users/{self.user_id}") 
            html = resp.get_data(as_text=True) 

            self.assertEqual(resp.status_code, 200) 
            self.assertIn("<h1>Posts</h1>", html) 

    def test_user_post_page(self):
        """Make sure clicking on a post takes user to the post.html""" 
        with app.test_client() as client: 
            resp = client.get(f'/posts/{ self.post_id }') 
            html = resp.get_data(as_text=True) 

            self.assertEqual(resp.status_code, 200) 
            self.assertIn(f"<p>{ self.post.content }</p>" , html) 

    def test_edit_page(self): 
        """Make sure edit post page shows up"""
        with app.test_client() as client: 
            resp = client.get(f'posts/{ self.post_id }/edit') 
            html = resp.get_data(as_text=True) 

            self.assertEqual(resp.status_code, 200) 
            self.assertIn("<h1>Edit Post</h1>", html) 
            


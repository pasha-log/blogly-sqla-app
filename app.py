"""Blogly application."""
from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension 
from flask_sqlalchemy import SQLAlchemy 
from models import db, connect_db, User, Post
import os
from sqlalchemy import desc
from functions import if_made_new_post
# , if_no_title_or_content

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = os.environ.get("SECRET_KEY", 'bjsjsdjaj')
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False 
debug = DebugToolbarExtension(app)

connect_db(app)
db.create_all()

@app.route('/')
def redirect_to_users():
    """Redirects to /users"""
    return redirect('/users')

@app.route('/users')
def list_pets(): 
    """Shows list of all users in db""" 
    users = User.query.all()
    return render_template('base.html', users=users) 

@app.route('/users/<int:user_id>')
def create_user_page(user_id):
    """Show users of single user""" 
    user = User.query.get_or_404(user_id)
    return render_template("user.html", user=user)

@app.route('/users/new', methods=["GET"]) 
def add_user_form(): 
    """Create a new user form"""
    return render_template('create/user.html') 

@app.route('/users/new', methods=["POST"])
def process_new_user():
    """Takes new user info, adds it to db, and redirects to /users"""
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    image_url = request.form['image_url']

    new_user = User(first_name=first_name, last_name=last_name, image_url=image_url)
    db.session.add(new_user)
    db.session.commit()
    
    return redirect('/users') 

@app.route('/users/<int:user_id>/edit')
def edit_user(user_id): 
    """Take user to edit page""" 
    user = User.query.get_or_404(user_id)
    return render_template("edit/user.html", user=user)

@app.route('/users/<int:user_id>/edit', methods=["POST"])
def process_edited_user(user_id):
    """Takes newly edited user info, updates the db, and redirects to /users page"""
    updated_user = User.query.get_or_404(user_id)
    updated_user.first_name = request.form['first_name']
    updated_user.last_name = request.form['last_name']
    updated_user.image_url = request.form['image_url']
    
    db.session.add(updated_user)
    db.session.commit() 

    return redirect('/users')

@app.route('/users/<int:user_id>/delete', methods=["POST"])
def delete_user_forever(user_id):
    """Reacts to delete button by deleting user from db completely"""
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()

    return redirect('/users')

############################################################
# POSTS ROUTES

@app.route('/hompage')
def show_top_five():
    """Show top five most recent posts on homepage.html"""
    # SELECT * FROM posts ORDER BY created_at DESC LIMIT 5;
    users = User.query.all()
    q = Post.query
    posts = q.order_by(desc('created_at')).limit(5).all()
    return render_template('homepage.html', posts=posts, users=users)

@app.route('/users/<int:user_id>/posts/new') 
def show_post_form(user_id): 
    """Reacts to add post button by showing page with post form""" 
    user = User.query.get_or_404(user_id)

    return render_template('create/post.html', user=user) 

@app.route('/users/<int:user_id>/posts/new', methods=["POST"])
def process_new_post(user_id):
    """Takes new post info, adds it to db, and redirects to user's user page"""
    title = request.form['title']
    content = request.form['content']

    new_post = Post(title=title, content=content, user_id=user_id)
    db.session.add(new_post)
    db.session.commit()
    if_made_new_post(title, content, user_id)

    return redirect(f'/users/{user_id}')

@app.route('/posts/<int:post_id>')
def show_post(post_id): 
    """Shows user's post through the link in their user page""" 
    post = Post.query.get_or_404(post_id) 
    user = User.query.get_or_404(post.user_id)

    return render_template('post.html', post=post, user=user) 

@app.route('/posts/<int:post_id>/edit')
def edit_post(post_id): 
    """Shows post edit page""" 
    post = Post.query.get_or_404(post_id) 
    user = User.query.get_or_404(post.user_id)

    return render_template('edit/post.html', post=post, user=user)

@app.route('/posts/<int:post_id>/edit', methods=["POST"])
def process_edited_post(post_id):
    """Update post with edits and redirect to post page""" 
    updated_post = Post.query.get_or_404(post_id)
    updated_post.title = request.form['title']
    updated_post.content = request.form['content']
    
    db.session.add(updated_post)
    db.session.commit() 

    return redirect(f"/posts/{post_id}")
    
@app.route("/posts/<int:post_id>/delete", methods=["POST"])
def delete_post(post_id): 
    """Delete a specific post with a click""" 
    post = Post.query.get_or_404(post_id) 

    db.session.delete(post)
    db.session.commit()

    return redirect(f'/users/{post.user_id}')


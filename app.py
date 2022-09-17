"""Blogly application."""
from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension 
from flask_sqlalchemy import SQLAlchemy 
from models import db, connect_db, User
import os

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
def create_detail_page(user_id):
    """Show details of single user""" 
    user = User.query.get_or_404(user_id)
    return render_template("detail.html", user=user)

@app.route('/users/new', methods=["GET"]) 
def add_user_form(): 
    """Creates a new user form"""
    return render_template('create.html') 

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
    return render_template("edit.html", user=user)

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



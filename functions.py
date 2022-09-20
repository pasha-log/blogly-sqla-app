from models import db, connect_db, User, Post
from flask import Flask, request, render_template, redirect, flash, session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_db'
connect_db(app)
db.create_all()

def if_made_new_post(title, content, user_id): 
    if (title != "") or (content != ""):
        flash('You have added a new post!', 'success')
    if (title == "") or (content == ""):
        # Post.query.filter_by(post).delete()
        # db.session.commit()
        flash('Missing title or content!', 'error')
        # return redirect(f'/users/{ user_id }/posts/new')


        
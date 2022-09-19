from models import db, connect_db, User, Post
from flask import flash

def if_made_new_post(): 
    flash(f'You have added a new post!', 'success')

# def if_no_title_or_content(title, content):
#     if (title == Null) or (content == Null):
#         flash(f'You are missing a title, content, or both!', 'error')
        
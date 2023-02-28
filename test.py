from flask import render_template, redirect, url_for
from flask_login import current_user

from Pack import db, app
from Pack.forms import AddPost
from Pack.models import User , Post
import sys
def create_db():
    with app.app_context():
        db.create_all()


def create_users():
    with app.app_context():
        user = User(username='Omar', email='sssssss@gmail.com', password='123567')
        db.session.add(user)
        db.session.commit()

def create_use():
    with app.app_context():
        post = Post(title='Physics', user_id=2)
        db.session.add(post)
        db.session.commit()


def read_users():
    with app.app_context():
        students = User.query.all()
        student_ids = [
                       student.id
                       for student in students
                       ]
        print(student_ids)
def home():
    #posts = current_user.posts
    # userID = current_user.id
    with app.app_context():

        posts = Post.query.filter_by(user_id=1).first()
    print(posts)

def test():
    with app.app_context():
        posts = Post.query.filter_by(user_id=3).all()
        print(posts)
        for post in posts:
            db.session.delete(post)
            db.session.commit()




if __name__ == '__main__':
    globals()[sys.argv[1]]()
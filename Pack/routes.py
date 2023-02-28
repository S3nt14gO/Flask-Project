from flask_bcrypt import Bcrypt
from flask import Flask, render_template, url_for, redirect, flash, request, Blueprint, session
from flask_login import current_user, login_user, login_required, logout_user

from Pack import app, db, photos
from Pack.forms import RegisterUser, LoginUser, AddPost
from Pack.models import User, Post

bcrypt = Bcrypt()


@app.route('/')
def homepage():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterUser()
    if form.validate_on_submit():
        # filename= photos.save(form.profile_picture.data)
        flash(f" Regestertion Completed {form.username.data}", "success")
        with app.app_context():
            hashed_password= bcrypt.generate_password_hash(form.password.data).decode('utf8')
            user = User(username=form.username.data, email=form.email.data, password=hashed_password)
                        # ,profile_picture=form.profile_picture.data)
            db.session.add(user)
            db.session.commit()
        return redirect(url_for('login'))

    return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('profile'))
    form = LoginUser()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            flash(f" Login Successfully {form.username.data} ", "success")

            return redirect(url_for('login'))
        else:
            flash("wrong credentials", "warning")
            return render_template('login.html', form=form)
    return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('homepage'))

@app.route('/post', methods=['GET','POST'])
@login_required
def addPost():
    form = AddPost()
    with app.app_context():
        userID = current_user.id
        if form.validate_on_submit():
            with app.app_context():
                post = Post(title=form.title.data, description=form.description.data, user_id=userID)
                db.session.add(post)
                db.session.commit()
            return redirect(url_for('home'))
    return render_template('posts.html', form=form, userID=userID)

@app.route("/home",  methods=['GET', 'POST'])
@login_required
def home():
    userID = current_user.id
    with app.app_context():
        posts = Post.query.filter_by(user_id=userID).all()

    return render_template('home.html', posts = posts)

@app.route("/profile",  methods=['GET', 'POST'])
@login_required
def profile():
    return render_template('profile.html')


@app.route("/updateUsername/",  methods=['GET', 'POST'])
@login_required
def updateUsername():
    form = RegisterUser(request.form, obj=current_user)
    with app.app_context():
        current_user.username = form.username.data
        db.session.commit()
    return render_template('updateUsername.html', **locals())


@app.route("/updateEmail/",  methods=['GET', 'POST'])
@login_required
def updateEmail():
    form = RegisterUser(request.form, obj=current_user)
    with app.app_context():
        current_user.email = form.email.data
        print(current_user.email)
        db.session.commit()
    return render_template('updateEmail.html', **locals())

@app.route("/delete",  methods=['GET', 'POST'])
@login_required
def delete():
    with app.app_context():
        posts = Post.query.filter_by(user_id=current_user.id).all()
        print(posts)
        for post in posts:
            db.session.delete(post)
            db.session.commit()
        user = User.query.filter_by(id=current_user.id).first()
        db.session.delete(user)
        db.session.commit()
    return redirect(url_for('register'))


@app.route("/updatePost/<int:key>", methods=['GET', 'POST'])
@login_required
def updatePost(key):
    form = AddPost()
    post = Post.query.filter_by(id=key).first()
    ptitle = post.title
    pdescripe = post.description
    if form.validate_on_submit():
        # with app.app_context():
            post.title=form.title.data
            db.session.commit()
            post.description = form.description.data
            db.session.commit()
            print(post.title)
            return redirect(url_for('home'))
    return render_template('updatePost.html', form=form , ptitle = ptitle, pdescripe=pdescripe)

@app.route("/deletePost/<int:key>",  methods=['GET', 'POST'])
@login_required
def deletePost(key):
    with app.app_context():
        post = Post.query.filter_by(id=key).first()
        db.session.delete(post)
        db.session.commit()
    return redirect(url_for('home'))



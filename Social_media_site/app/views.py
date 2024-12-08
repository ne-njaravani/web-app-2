from flask import Flask, render_template, redirect, url_for, flash, request, make_response, session
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user, login_required, login_user, logout_user
from app import app, db, models, admin
from .forms import AccountForm, PostForm, LoginForm, SignupForm
from .models import User, Post, Like
import json

admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(Post, db.session))
admin.add_view(ModelView(Like, db.session))

@app.route('/')
def home():
    form = PostForm()
    posts = models.Post.query.all()
    return render_template('home.html', posts=posts, form=form)

@app.route('/set_cookie')
def set_cookie():
    response = make_response(render_template('index.html'))
    response.set_cookie('username', 'john_doe')
    return response

@app.route('/get_cookie')
def get_cookie():
    username = request.cookies.get('username')
    return f'Welcome {username}'

@app.route('/set_session')
def set_session():
    session['username'] = 'john_doe'
    return 'Session variable set'

@app.route('/get_session')
def get_session():
    username = session.get('username')
    return f'Welcome {username}'

@app.route('/delete_session')
def delete_session():
    session.pop('username', None)
    return 'Session variable deleted'

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm()
    if form.validate_on_submit():
        user = User(username=form.username.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        login_user(user)  # Log the user in after sign up
        flash('Your account has been created! You are now logged in', 'success')
        return redirect(url_for('home'))
    return render_template('signup.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            flash('Logged in successfully.', 'success')
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
            if not user:
                flash('Username does not exist. Please create an account.', 'warning')
    return render_template('login.html', form=form)

@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'success')
    return redirect(url_for('home'))

@app.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    form = AccountForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.set_password(form.password.data)
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
    return render_template('account.html', form=form)

@app.route('/account/edit', methods=['GET', 'POST'])
@login_required
def account_edit():
    form = AccountForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.set_password(form.password.data)
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
    return render_template('accountEdit.html', form=form)

@app.route('/like', methods=['POST'])
@login_required
def vote():
    data = json.loads(request.data)
    post_id = int(data.get('post_id'))
    post = models.Post.query.get(post_id)
    reaction_type = data.get('reaction_type')

    if reaction_type == "like":
        like = Like.query.filter_by(post_id=post_id, user_id=current_user.id).first()
        if not like:
            new_like = Like(post_id=post_id, user_id=current_user.id)
            db.session.add(new_like)
            db.session.commit()
        likes_count = Like.query.filter_by(post_id=post_id).count()
    else:
        like = Like.query.filter_by(post_id=post_id, user_id=current_user.id).first()
        if like:
            db.session.delete(like)
            db.session.commit()
        likes_count = Like.query.filter_by(post_id=post_id).count()

    return jsonify({'status': 'OK', 'likes': likes_count})

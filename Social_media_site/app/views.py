from flask import Flask, render_template, redirect, url_for, flash, request, make_response, session
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user, login_required, login_user, logout_user
from app import app, db, models, admin
from .forms import AccountForm, PostForm, LoginForm, CommentForm, SignupForm
from .models import User, Post, Comment
import json

admin.add_view(ModelView(User, db.session)) 
admin.add_view(ModelView(Post, db.session)) 
admin.add_view(ModelView(Comment, db.session))


# Display all the posts grouping them by whether they are complete or incomplete
@app.route('/')
def home(): 

    form = PostForm()
    if form.validate_on_submit():
        new_post = models.Post(content=form.post.data)
        db.session.add(new_post)
        db.session.commit()
        flash('Your post has been created!', 'success')    


    posts = models.Post.query.all() 
    form = CommentForm()
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

# Set session
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
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
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
    return render_template('login.html', form=form)

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect("/home")

# Manage the user's profile. Change email and password
@app.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    form = AccountForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
    return render_template('account.html', form=form)


@app.route('/add_comment/<int:post_id>', methods=['POST']) 
@login_required 
def add_comment(post_id):
    form = CommentForm() 
    if form.validate_on_submit(): 
        comment = db.Comment(content=form.content.data, user_id=current_user.id, post_id=post_id) 
        db.session.add(comment) 
        db.session.commit() 
        flash('Your comment has been added!', 'success') 
        return redirect(url_for('home'))
    
    # Likes
@app.route('/like', methods=['POST'])
@login_required
def vote():
    data = json.loads(request.data)
    post_id = int(data.get('post_id'))
    post = models.Idea.query.get(post_id)

        # Increment the correct vote
    if data.get('reaction_type') == "like":
        post.upvotes += 1
    else:
        post.downvotes += 1

        # Save the updated vote count in the DB
    db.session.commit()
        # Tell the JS .ajax() call that the data was processed OK
    return json.dumps({'status':'OK','likes': post.upvotes, 'dislikes': post.downvotes })
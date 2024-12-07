from flask import Flask, render_template, redirect, url_for, flash, request
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user, login_required, login_user, logout_user
from app import app, db, models, admin
from .forms import AccountForm, PostForm, LoginForm, CommentForm
from .models import User, Post, Comment
import json

admin.add_view(ModelView(User, db.session)) 
admin.add_view(ModelView(Post, db.session)) 
admin.add_view(ModelView(Comment, db.session))


# Display all the posts grouping them by whether they are complete or incomplete
@app.route('/')
def home(): 
    posts = models.Post.query.all() 
    form = CommentForm()
    return render_template('home.html', posts=posts, form=form)
    

@app.route('/login', methods=['GET', 'POST'])
def login():
    # Here we use a class of some kind to represent and validate our
    # client-side form data. For example, WTForms is a library that will
    # handle this for us, and we use a custom LoginForm to validate.
    form = LoginForm()
    if form.validate_on_submit():
        # Login and validate the user.
        # user should be an instance of your `User` class
        login_user(user)

        flash('Logged in successfully.')

        next = request.args.get('next')
        if not url_has_allowed_host_and_scheme(next, request.host):
            return flask.abort(400)

        return flask.redirect(next or flask.url_for('index'))
    return flask.render_template('login.html', form=form)

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(somewhere)

# Manage the user's profile. Change email and password
@app.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    pass
    form = AccountForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
    return render_template('account.html', form=form)

# Likes
@app.route('/likes', methods=['POST'])
def vote():
        # Load the JSON data and use the ID of the idea that was clicked to get the object
    data = json.loads(request.data)
    idea_id = int(data.get('idea_id'))
    idea = models.Idea.query.get(idea_id)

        # Increment the correct vote
    if data.get('reaction_type') == "like":
        idea.upvotes += 1
    else:
        idea.downvotes += 1

        # Save the updated vote count in the DB
    db.session.commit()
        # Tell the JS .ajax() call that the data was processed OK
    return json.dumps({'status':'OK','likes': idea.upvotes, 'dislikes': idea.downvotes })


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
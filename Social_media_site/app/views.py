from flask import Flask, render_template, redirect, url_for, flash, request, make_response, session, jsonify
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user, login_required, login_user, logout_user
from app import app, db, models, admin
from .forms import AccountForm, PostForm, LoginForm, SignupForm, CommentForm
from .models import User, Post, Reaction, Comment
import json

admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(Post, db.session))
admin.add_view(ModelView(Reaction, db.session))
admin.add_view(ModelView(Comment, db.session))

@app.route('/')
def home():
    form = PostForm()
    if form.validate_on_submit():
        new_post = models.Post(content=form.post.data, user_id=current_user.id)
        db.session.add(new_post)
        db.session.commit()
        flash('Your post has been created!', 'success')
        return redirect(url_for('home'))

    # Get posts sorted by timestamp (newest first)
    posts = models.Post.query.order_by(models.Post.timestamp.desc()).all()
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
        user = User(username=form.username.data, email=form.email.data)
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
        if user:
            if user.check_password(form.password.data):
                login_user(user)
                flash('Logged in successfully.', 'success')
                next_page = request.args.get('next')
                return redirect(next_page) if next_page else redirect(url_for('home'))
            else:
                flash('Login Unsuccessful. Please check username and password', 'danger')
        else:
            flash('Username does not exist. Please create an account.', 'warning')
            return redirect(url_for('signup'))
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
        current_user.email = form.email.data
        current_user.set_password(form.password.data)
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    posts = Post.query.filter_by(user_id=current_user.id).all()
    return render_template('account.html', form=form, posts=posts)

@app.route('/account/edit', methods=['GET', 'POST'])
@login_required
def account_edit():
    form = AccountForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        current_user.set_password(form.password.data)
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    return render_template('accountEdit.html', form=form)

@app.route('/create', methods=['GET', 'POST'])
@login_required
def create_post():
    form = PostForm()
    if form.validate_on_submit():
        new_post = Post(content=form.post.data, user_id=current_user.id)
        db.session.add(new_post)
        db.session.commit()
        flash('Your post has been created!', 'success')
        return redirect(url_for('home'))
    return render_template('create.html', form=form)

@app.route('/edit_post/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_post(id):
    post = Post.query.get_or_404(id)
    if post.user_id != current_user.id:
        flash('You do not have permission to edit this post.', 'danger')
        return redirect(url_for('account'))
    
    form = PostForm()
    if form.validate_on_submit():
        post.content = form.post.data
        db.session.commit()
        flash('Your post has been updated!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.post.data = post.content
    return render_template('editPost.html', form=form, post=post)

@app.route('/delete_post/<int:id>', methods=['POST'])
@login_required
def delete_post(id):
    post = Post.query.get_or_404(id)
    if post.user_id != current_user.id:
        flash('You do not have permission to delete this post.', 'danger')
        return redirect(url_for('account'))
    
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('account'))

@app.route('/reaction', methods=['POST'])
@login_required
def reaction():
    data = json.loads(request.data)
    post_id = int(data.get('post_id'))
    reaction_type = data.get('reaction_type')
    post = Post.query.get_or_404(post_id)

    reaction = Reaction.query.filter_by(post_id=post_id, user_id=current_user.id).first()
    if reaction:
        if reaction.reaction_type == reaction_type:
            db.session.delete(reaction)
        else:
            reaction.reaction_type = reaction_type
    else:
        new_reaction = Reaction(post_id=post_id, user_id=current_user.id, reaction_type=reaction_type)
        db.session.add(new_reaction)

    db.session.commit()

    likes_count = Reaction.query.filter_by(post_id=post_id, reaction_type='like').count()
    dislikes_count = Reaction.query.filter_by(post_id=post_id, reaction_type='dislike').count()

    return jsonify({
        'status': 'OK',
        'likes': likes_count,
        'dislikes': dislikes_count
    })

@app.route('/comment/<int:post_id>', methods=['POST'])
@login_required
def add_comment(post_id):
    form = CommentForm()
    if form.validate_on_submit():
        comment = Comment(content=form.comment.data, post_id=post_id, user_id=current_user.id)
        db.session.add(comment)
        db.session.commit()
        flash('Comment added!', 'success')
    return redirect(request.referrer or url_for('home'))

@app.route('/delete_comment/<int:comment_id>', methods=['POST'])
@login_required
def delete_comment(comment_id):
    comment = Comment.query.get_or_404(comment_id)
    if comment.user_id != current_user.id:
        flash('You do not have permission to delete this comment.', 'danger')
        return redirect(request.referrer or url_for('home'))
    
    db.session.delete(comment)
    db.session.commit()
    flash('Comment deleted!', 'success')
    return redirect(request.referrer or url_for('home'))

@app.route('/user/<username>')
def user_profile(username):
    user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query.filter_by(user_id=user.id).order_by(Post.timestamp.desc()).all()
    return render_template('user_profile.html', user=user, posts=posts)

@app.route('/follow/<username>', methods=['POST'])
@login_required
def follow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('User not found.', 'warning')
        return redirect(url_for('home'))
    if user == current_user:
        flash('You cannot follow yourself!', 'warning')
        return redirect(url_for('user_profile', username=username))
    current_user.follow(user)
    db.session.commit()
    flash(f'You are now following {username}!', 'success')
    return redirect(url_for('user_profile', username=username))

@app.route('/unfollow/<username>', methods=['POST'])
@login_required
def unfollow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('User not found.', 'warning')
        return redirect(url_for('home'))
    if user == current_user:
        flash('You cannot unfollow yourself!', 'warning')
        return redirect(url_for('user_profile', username=username))
    current_user.unfollow(user)
    db.session.commit()
    flash(f'You have unfollowed {username}.', 'info')
    return redirect(url_for('user_profile', username=username))

@app.route('/search')
def search():
    query = request.args.get('q', '')
    if query:
        # Search in posts and usernames
        posts = Post.query.filter(Post.content.contains(query)).order_by(Post.timestamp.desc()).all()
        users = User.query.filter(User.username.contains(query)).all()
    else:
        posts = []
        users = []
    return render_template('search.html', posts=posts, users=users, query=query)
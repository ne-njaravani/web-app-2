from flask import Flask, render_template, redirect, url_for, flash, request
from flask_admin.contrib.sqla import ModelView
from app import app, db, models
from .forms import AssessmentForm
from flask_login import LoginManager

admin.add_view(ModelView(Property, db.session))
admin.add_view(ModelView(Landlord, db.session))

login_manager = LoginManager()
@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)

# Display all the assessments grouping them by whether they are complete or incomplete
@app.route('/')
def home():
    

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

        flask.flash('Logged in successfully.')

        next = flask.request.args.get('next')
        # url_has_allowed_host_and_scheme should check if the url is safe
        # for redirects, meaning it matches the request host.
        # See Django's url_has_allowed_host_and_scheme for an example.
        if not url_has_allowed_host_and_scheme(next, request.host):
            return flask.abort(400)

        return flask.redirect(next or flask.url_for('index'))
    return flask.render_template('login.html', form=form)

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(somewhere)


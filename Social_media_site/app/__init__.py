from flask import Flask, request, session
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_admin import Admin
from flask_babel import Babel
from flask_wtf.csrf import CSRFProtect
from flask_login import LoginManager

def get_locale():
    if request.args.get('lang'):
        session['lang'] = request.args.get('lang')
    return session.get('lang', 'en')

app = Flask(__name__)
app.config.from_object('config')
app.secret_key = 'your_secret_key'

db = SQLAlchemy(app)
migrate = Migrate(app, db)

login_manager = LoginManager()
login_manager.init_app(app)

login_manager.login_view = 'login'
login_manager.login_message = 'Please log in to access.'

@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)

Bootstrap(app)
csrf = CSRFProtect(app)

babel = Babel(app, locale_selector=get_locale)
admin = Admin(app,template_mode='bootstrap4')

# Register models with Flask-Admin 
from flask_admin.contrib.sqla import ModelView
from .models import User, Post

admin.add_view(ModelView(User, db.session, name='Admin Users', endpoint='admin_users'))
admin.add_view(ModelView(Post, db.session, name='Admin Posts', endpoint='admin_posts'))

from app import views, models
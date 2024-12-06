from flask import Flask, request, session
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_admin import Admin
from flask_babel import Babel
from flask_wtf.csrf import CSRFProtect
from flask_login import LoginManager
from models import User

def get_locale():
    if request.args.get('lang'):
        session['lang'] = request.args.get('lang')
    return session.get('lang', 'en')

app = Flask(__name__)
app.config.from_object('config')


login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)

Bootstrap(app)
csrf = CSRFProtect(app)

db = SQLAlchemy(app)
migrate = Migrate(app, db)

babel = Babel(app, locale_selector=get_locale)
admin = Admin(app,template_mode='bootstrap4')

from app import views, models

# Register models with Flask-Admin 
from flask_admin.contrib.sqla import ModelView

# Assuming models Property and Landlord 
admin.add_view(ModelView(Property, db.session)) 
admin.add_view(ModelView(Landlord, db.session))
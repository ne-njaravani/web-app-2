from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship
from flask_login import UserMixin
from app import db
from datetime import datetime

# Many-to-many relationship for posts and users
posts_users = db.Table(
    'posts_users',
    db.Model.metadata,
    Column('post_id', db.Integer, ForeignKey('post.id')),
    Column('user_id', db.Integer, ForeignKey('user.id'))
)

class User(UserMixin, db.Model):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    password = Column(String(128))
    posts = relationship('Post', back_populates='user')
    reactions = relationship('Reaction', back_populates='user')

    def set_password(self, password):
        self.password = password

    def check_password(self, password):
        return self.password == password
    
    def __repr__(self):
        return f'<User {self.username}>'

class Post(db.Model):
    __tablename__ = 'post'
    id = Column(Integer, primary_key=True)
    content = Column(String(500), nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    timestamp = Column(db.DateTime, default=datetime.utcnow, nullable=False)  # Add this line
    user = relationship('User', back_populates='posts')
    reactions = relationship('Reaction', back_populates='post')

    def __repr__(self):
        return f'<Post {self.id}>'

class Reaction(db.Model):
    __tablename__ = 'reaction'
    id = Column(Integer, primary_key=True)
    post_id = Column(Integer, ForeignKey('post.id'), nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    reaction_type = Column(String(10), nullable=False)  # 'like' or 'dislike'
    post = relationship('Post', back_populates='reactions')
    user = relationship('User', back_populates='reactions')

    def __repr__(self):
        return f'<Reaction {self.reaction_type} by User {self.user_id} on Post {self.post_id}>'
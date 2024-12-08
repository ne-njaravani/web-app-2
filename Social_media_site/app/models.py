from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship
from flask_login import UserMixin
from app import db

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
    password = Column(String(128))
    posts = relationship('Post', secondary=posts_users, back_populates='users')
    likes = relationship('Like', back_populates='user')

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
    users = relationship('User', secondary=posts_users, back_populates='posts')
    likes = relationship('Like', back_populates='post')

    def __repr__(self):
        return f'<Post {self.id}>'

class Like(db.Model):
    __tablename__ = 'like'
    id = Column(Integer, primary_key=True)
    post_id = Column(Integer, ForeignKey('post.id'))
    user_id = Column(Integer, ForeignKey('user.id'))
    post = relationship('Post', back_populates='likes')
    user = relationship('User', back_populates='likes')

    def __repr__(self):
        return f'<Like {self.id}>'

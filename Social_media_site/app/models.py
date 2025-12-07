from sqlalchemy import Column, Integer, String, ForeignKey, Table, Text
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

# Follower relationship table
followers = db.Table(
    'followers',
    db.Model.metadata,
    Column('follower_id', db.Integer, ForeignKey('user.id')),
    Column('followed_id', db.Integer, ForeignKey('user.id'))
)

class User(UserMixin, db.Model):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    password = Column(String(128))
    bio = Column(Text, nullable=True)
    avatar = Column(String(200), default='default-avatar.png')
    posts = relationship('Post', back_populates='user')
    reactions = relationship('Reaction', back_populates='user')
    comments = relationship('Comment', back_populates='user')
    followed = relationship(
        'User', secondary=followers,
        primaryjoin=(followers.c.follower_id == id),
        secondaryjoin=(followers.c.followed_id == id),
        backref=db.backref('followers', lazy='dynamic'),
        lazy='dynamic'
    )

    def set_password(self, password):
        self.password = password

    def check_password(self, password):
        return self.password == password
    
    def follow(self, user):
        if not self.is_following(user):
            self.followed.append(user)

    def unfollow(self, user):
        if self.is_following(user):
            self.followed.remove(user)

    def is_following(self, user):
        return self.followed.filter(followers.c.followed_id == user.id).count() > 0
    
    def __repr__(self):
        return f'<User {self.username}>'

class Post(db.Model):
    __tablename__ = 'post'
    id = Column(Integer, primary_key=True)
    content = Column(String(500), nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    timestamp = Column(db.DateTime, default=datetime.utcnow, nullable=False)
    user = relationship('User', back_populates='posts')
    reactions = relationship('Reaction', back_populates='post', cascade='all, delete-orphan')
    comments = relationship('Comment', back_populates='post', cascade='all, delete-orphan')

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

class Comment(db.Model):
    __tablename__ = 'comment'
    id = Column(Integer, primary_key=True)
    content = Column(String(300), nullable=False)
    timestamp = Column(db.DateTime, default=datetime.utcnow, nullable=False)
    post_id = Column(Integer, ForeignKey('post.id'), nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    post = relationship('Post', back_populates='comments')
    user = relationship('User', back_populates='comments')

    def __repr__(self):
        return f'<Comment {self.id} on Post {self.post_id}>'
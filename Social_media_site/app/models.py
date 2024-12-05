from app import db
from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship

# Many-to-many relationship table for followers
followers = Table(
    'followers',
    Base.metadata,
    db.Column('follower_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('followed_id', db.Integer, db.ForeignKey('user.id'))
)

# Many-to-many relationship table for posts and users
posts_users = Table(
    'posts_users',
    Base.metadata,
    db.Column('post_id', db.Integer, db.ForeignKey('post.id')),
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'))
)

# Many-to-many relationship table for likes
likes = Table(
    'likes',
    Base.metadata,
    db.Column('post_id', db.Integer, db.ForeignKey('post.id'))
)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    posts = db.relationship('Post', secondary=posts_users, back_populates='users')
    liked_posts = db.relationship('Post', secondary=likes, back_populates='liked_by')
    comments = db.relationship('Comment', back_populates='user')
    followed = db.relationship(
        'User', secondary=followers,
        primaryjoin=id==followers.c.follower_id,
        secondaryjoin=id==followers.c.followed_id,
        back_populates='followers'
    )
    post = relationship('Post', back_populates='comments')
        'User', secondary=followers,
        primaryjoin=id==followers.c.followed_id,
        secondaryjoin=id==followers.c.follower_id,
        back_populates='followed'
       

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(500), nullable=False)
    users = db.relationship('User', secondary=posts_users, back_populates='posts')
    liked_by = db.relationship('User', secondary=likes, back_populates='liked_posts')
    comments = db.relationship('Comment', back_populates='post')

class Comment(db.Model): 
    id = Column(Integer, primary_key=True) 
    content = Column(String(500), nullable=False) 
    user_id = Column(Integer, ForeignKey('users.id')) 
    post_id = Column(Integer, ForeignKey('posts.id')) 
    user = relationship('User', back_populates='comments') 
    post = relationship('Post', back_populates='comments'

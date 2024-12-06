from app import db
from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship

# Many-to-many relationship tables
followers = Table(
    'followers',
    db.Model.metadata,
    Column('follower_id', Integer, ForeignKey('user.id')),
    Column('following_id', Integer, ForeignKey('user.id'))
)

posts_users = Table(
    'posts_users',
    db.Model.metadata,
    Column('post_id', Integer, ForeignKey('post.id')),
    Column('user_id', Integer, ForeignKey('user.id'))
)

likes = Table(
    'likes',
    db.Model.metadata,
    Column('post_id', Integer, ForeignKey('post.id'))
)

class User(db.Model):
    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    password = Column(String(128))
    posts = relationship('Post', secondary=posts_users, back_populates='users')
    liked_posts = relationship('Post', secondary=likes, back_populates='liked_by')
    comments = relationship('Comment', back_populates='user')
    followers = relationship(
        'User', secondary=followers,
        primaryjoin=id==followers.c.follower_id,
        secondaryjoin=id==followers.c.following_id,
        back_populates='following'
    )
    following = relationship(
        'User', secondary=followers,
        primaryjoin=id==followers.c.following_id,
        secondaryjoin=id==followers.c.follower_id,
        back_populates='followers'
    )

    def set_password(self, password): 
        self.password = password 
    
    def check_password(self, password): 
        return self.password == password

class Post(db.Model):
    id = Column(Integer, primary_key=True)
    content = Column(String(500), nullable=False)
    users = relationship('User', secondary=posts_users, back_populates='posts')
    liked_by = relationship('User', secondary=likes, back_populates='liked_posts')
    comments = relationship('Comment', back_populates='post')

class Comment(db.Model): 
    id = Column(Integer, primary_key=True) 
    content = Column(String(500), nullable=False) 
    user_id = Column(Integer, ForeignKey('user.id')) 
    post_id = Column(Integer, ForeignKey('post.id')) 
    user = relationship('User', back_populates='comments') 
    post = relationship('Post', back_populates='comments')

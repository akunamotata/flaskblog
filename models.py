#coding=utf-8
from flask.ext.sqlalchemy import SQLAlchemy
from datetime import datetime
from main import app

db = SQLAlchemy(app)

class Setting(db.Model):
	'''
		博客配置
	'''

	id            = db.Column(db.Integer, primary_key=True)
	blog_title    = db.Column(db.String(120), nullable=False)	
	blog_subtitle = db.Column(db.String(120))
	about_author  = db.Column(db.String(300))
	about_detail  = db.Column(db.Text)

class Message(db.Model):
	'''
		用户留言
	'''

	id         = db.Column(db.Integer, primary_key=True)
	nickname   = db.Column(db.String(25), nullable=False)
	email      = db.Column(db.String(50), nullable=False)
	address    = db.Column(db.String(100))
	content    = db.Column(db.Text, nullable=False)
	datetime   = db.Column(db.DateTime, default=datetime.now)
	article_id = db.Column(db.Integer, db.ForeignKey('article.id'))
	reply_to   = db.Column(db.String(25))

	def __unicode__(self):
		return self.id

class Tag(db.Model):
	id   = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(30), nullable=False)

	def __unicode__(self):
		return self.name

#Many To Many table
article_tags_table = db.Table('article_tags', db.metadata,
	db.Column('article_id', db.Integer, db.ForeignKey('article.id')),
	db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'))
)

class Article(db.Model):
	id          = db.Column(db.Integer, primary_key=True)
	title       = db.Column(db.String(50), nullable=False)
	content     = db.Column(db.Text)
	create_time = db.Column(db.DateTime, default=datetime.now)
	modify_time = db.Column(db.DateTime, default=datetime.now, \
		onupdate=datetime.now)
	category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
	category    = db.relationship('Category', backref='articles')
	messages    = db.relationship('Message', backref='article')
	tags        = db.relationship('Tag', secondary=article_tags_table)
	user_id     = db.Column(db.Integer, db.ForeignKey('user.id'))
	author      = db.relationship('User')

	def __unicode__(self):
		return self.title

class Category(db.Model):
	id   = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(50), nullable=False)

	def __unicode__(self):
		return self.name

class User(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(50), nullable=False)
	
	def __unicode__(self):
		return self.name

if __name__ == '__main__':
	db.drop_all()
	db.create_all()

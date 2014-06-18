#coding=utf-8
from flask import request, redirect
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.admin.contrib.sqla import ModelView
from flask.ext.admin.base import AdminIndexView, expose
from datetime import datetime
from main import app
from wtforms import validators, Form, StringField, TextAreaField, TextField, \
	HiddenField
from wtforms.widgets import TextArea

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

	'''
	def __init__(self, blog_title, blog_subtitle,  
		about_author, about_detail):
		self.blog_title    = blog_title
		self.blog_subtitle = blog_subtitle
		self.about_author  = about_author
		self.about_detail  = about_detail
	'''

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

class SettingAdminView(ModelView):
	column_list = ('id', 'blog_title', 'blog_subtitle')
	column_exclude_list = ('about_author', 'about_detail')
	column_searchable_list = ('blog_title', 'blog_subtitle' \
		, 'about_author')

	form_args = dict(
		blog_title=dict(validators=[validators.required()])
	)
	'''
	column_labels = dict(id=u'ID', blog_title=u'博客标题', blog_subtitle=u'子标题' \
		, about_author=u'关于作者', about_detail=u'其他描述')
	'''

class MessageAdminView(ModelView):
	# can_create = False
	# can_edit = False
	column_list = ('id', 'nickname', 'email')
	column_searchable_list = ('nickname', 'email')
	form_excluded_columns = ('article','reply_to')

'''
class ArticleAdminForm(Form):
	title = StringField('Title')
	tags = TextField('Tags')
'''

class ArticleAdminView(ModelView):

	create_template = '/admin/article_edit.html'
	edit_template = '/admin/article_edit.html'

	column_list = ('id', 'title', 'modify_time')
	column_searchable_list = ('title',)
	form_columns = ('title', 'category', 'author', 'tags', 'content')
	form_excluded_columns = ('create_time',)

	form_args = dict(
		modify_time=dict(default=datetime.now)
	)

	form_widget_args = {
        'content': {
            'class': 'ckeditor'
        }
    }

class CategoryAdminView(ModelView):
	form_columns = ('name',)

class HomeView(AdminIndexView):
    @expose('/')
    def index(self):
    	setting = Setting.query.get(1)
        return self.render('admin/index.html', setting=setting)

    @expose('/setting/', methods=('GET', 'POST'))
    def setting(self):
    	form = SettingForm(request.form)
    	if request.method == 'POST' and form.validate():
    		setting = Setting()
    		form.populate_obj(setting)
    		if len(setting.id) != 0 and int(setting.id) == 1:
    			db.session.merge(setting)
    		else:
    			setting.id = 1
	    		db.session.add(setting)
    		db.session.commit()
    		return redirect('/admin')

    	if request.method == 'GET':
	    	setting = Setting.query.get(1)
	    	form = SettingForm(obj=setting)

        return self.render('admin/setting.html', form=form)

class SettingForm(Form):
	id = HiddenField()
	blog_title = StringField('BlogTitle', validators=[validators.input_required()])
	blog_subtitle = StringField('BlogSubtitle', validators=[validators.input_required()])
	about_author = StringField('AboutAuthor', widget=TextArea(), \
		validators=[validators.input_required()])
	about_detail = StringField('AboutDetail', widget=TextArea(), \
		validators=[validators.input_required()])

if __name__ == '__main__':
	db.drop_all()
	db.create_all()

#coding=utf-8
from flask import request, redirect
from flask.ext.admin.contrib.sqla import ModelView
from flask.ext.admin.base import AdminIndexView, expose
from datetime import datetime
from wtforms import validators, Form, StringField, TextAreaField, TextField, \
	HiddenField
from wtforms.widgets import TextArea
from models import Setting, db

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

class SettingForm(Form):
	id = HiddenField()
	blog_title = StringField('BlogTitle', validators=[validators.input_required()])
	blog_subtitle = StringField('BlogSubtitle', validators=[validators.input_required()])
	about_author = StringField('AboutAuthor', widget=TextArea(), \
		validators=[validators.input_required()])
	about_detail = StringField('AboutDetail', widget=TextArea(), \
		validators=[validators.input_required()])


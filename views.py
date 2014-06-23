#coding=utf-8
from flask import request, render_template, url_for, redirect
from wtforms import Form, TextField, TextAreaField, HiddenField, validators
from datetime import datetime
from main import app
from models import *

Mons = {
    '1':u'一',
    '2':u'二',
    '3':u'三',
    '4':u'四',
    '5':u'五',
    '6':u'六',
    '7':u'七',
    '8':u'八',
    '9':u'九',
    '10':u'十',
    '11':u'十一',
    '12':u'十二'
}

def _dateformat(dt):
    mon = Mons[str(dt.month)]
    return u'%s月<span>%d</span>' % (mon, dt.day)
app.jinja_env.filters['dateformat'] = _dateformat

def _timeformat(dt):
    return u'%d:%d' % (dt.hour, dt.minute)
app.jinja_env.filters['timeformat'] = _timeformat

def _global_dicts():
	'''
	全局变量
	'''
	setting = Setting.query.get(1)
	dicts = {
		'blog':setting
	}

	return dicts

class MessageForm(Form):
	blog_id  = HiddenField('blog_id', [validators.required()])
	nickname = TextField('nickname', [validators.required()])
	email    = TextField('email', [validators.required()])
	address  = TextField('address')
	content  = TextAreaField('content', [validators.required()])

@app.route('/')
def index():
	articles = Article.query.order_by(Article.create_time.desc())
	return render_template('index.html', current='home',\
	 articles = articles, **_global_dicts())

@app.route('/blog/<int:id>')
def show(id):
	article = Article.query.get(id)
	return render_template('show.html', article=article, \
		**_global_dicts())

@app.route('/tag/<int:id>')
def tag(id):
	return render_template('tag.html', article=article, \
		**_global_dicts())

@app.route('/message', methods=['POST'])
def message():
	form = MessageForm(request.form)
	if request.method == 'POST' and form.validate():
		message = Message(nickname=form.nickname.data, email=form.email.data, \
			address=form.address.data, content=form.content.data, \
			article_id=form.blog_id.data)
		db.session.add(message)
		db.session.commit()
	return redirect(url_for('.show', id=form.blog_id.data))

@app.route('/about')
def about():
	return render_template('about.html', current='about',\
		**_global_dicts())

if __name__ == '__main__':
	str1 = _timestr0(datetime.now());
	print str1
	print '%s'%datetime.now()
	print '%s'%datetime.today()

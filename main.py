from flask import Flask, render_template
from flask.ext.admin import Admin
from flask.ext.admin.contrib.sqla import ModelView

app = Flask(__name__)
app.config['DEBUG']                   = True
app.config['SECRET_KEY']              = '123456'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///flaskblog.sqlite'
app.config['SQLALCHEMY_ECHO']         = True

from views import *

if __name__ == '__main__':

	from admin.views import *
	from models import *

	admin = Admin(app, name='flaskblog', url='/admin', index_view=HomeView())
	admin.add_view(MessageAdminView(Message, db.session))
	admin.add_view(ModelView(Tag, db.session))
	admin.add_view(ModelView(User, db.session))
	admin.add_view(ArticleAdminView(Article, db.session))
	admin.add_view(CategoryAdminView(Category, db.session))

	app.run()